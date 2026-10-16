import tempfile
import unittest
from datetime import timedelta
from pathlib import Path

from diedigital import deadman
from diedigital.actions import DONE, FAILED, GAVE_UP, INCOMPLETE, ActionError, ActionSpec
from diedigital.util import fmt_time, parse_time

T0 = parse_time("2026-01-01T00:00:00Z")


class FakeActions:
    """Gerçek ağ çağrısı yapmayan sahte eylemler."""

    def __init__(self):
        self.calls = []
        self.behaviour = {}

    def spec(self, name):
        def run(params, ctx):
            self.calls.append((params.get("id"), ctx.dry_run))
            outcome = self.behaviour.get(params.get("id"), DONE)
            if outcome == FAILED:
                raise ActionError("olmadı")
            return {"status": outcome, "summary": name}

        return ActionSpec(run=run, check=lambda p, c: "tamam", describe=lambda p: name)

    def registry(self):
        return {t: self.spec(t) for t in ("noop", "self_destruct")}


def make(actions=None, **overrides):
    fake = FakeActions()
    data = {"checkin_interval_days": 30, "grace_days": 7, "notify": {}, "actions": actions or []}
    data.update(overrides)
    tmp = Path(tempfile.mkdtemp())
    cfg = deadman.Config.from_dict(data, tmp / "deadman.json", known=fake.registry())
    return cfg, deadman.new_state(T0), fake


def quiet(_msg):
    pass


class EvaluateTests(unittest.TestCase):
    def test_phases_follow_checkin_interval(self):
        cfg, state, _ = make()
        self.assertEqual(deadman.evaluate(cfg, state, T0 + timedelta(days=29)).phase, "ok")
        self.assertEqual(deadman.evaluate(cfg, state, T0 + timedelta(days=30)).phase, "warning")
        self.assertEqual(deadman.evaluate(cfg, state, T0 + timedelta(days=36, hours=23)).phase, "warning")
        self.assertEqual(deadman.evaluate(cfg, state, T0 + timedelta(days=37)).phase, "trigger")

    def test_fixed_date_wins_when_earlier(self):
        cfg, state, _ = make(trigger_at="2026-01-15T00:00:00Z")
        ev = deadman.evaluate(cfg, state, T0)
        self.assertEqual(ev.trigger_time, parse_time("2026-01-15T00:00:00Z"))
        self.assertEqual(ev.warn_from, parse_time("2026-01-08T00:00:00Z"))

    def test_date_only_mode(self):
        cfg, state, _ = make(checkin_interval_days=None, trigger_at="2027-01-01")
        self.assertEqual(deadman.evaluate(cfg, state, parse_time("2027-01-01")).phase, "trigger")
        deadman.checkin(cfg, state, parse_time("2026-12-31"))
        self.assertEqual(deadman.evaluate(cfg, state, parse_time("2027-01-01")).phase, "trigger")

    def test_checkin_resets_timer_and_aborts_trigger(self):
        cfg, state, _ = make()
        state["triggered_at"] = fmt_time(T0 + timedelta(days=40))
        state["last_warning"] = fmt_time(T0 + timedelta(days=39))
        later = T0 + timedelta(days=41)
        deadman.checkin(cfg, state, later)
        self.assertIsNone(state["triggered_at"])
        self.assertIsNone(state["last_warning"])
        self.assertEqual(deadman.evaluate(cfg, state, later + timedelta(days=1)).phase, "ok")

    def test_missing_state_never_triggers_immediately(self):
        cfg, _, _ = make()
        state = deadman.load_state(cfg, T0)
        self.assertEqual(deadman.evaluate(cfg, state, T0).phase, "ok")


class ConfigTests(unittest.TestCase):
    def test_needs_a_trigger(self):
        with self.assertRaises(deadman.ConfigError):
            make(checkin_interval_days=None)

    def test_unknown_action_type(self):
        with self.assertRaises(deadman.ConfigError):
            make(actions=[{"type": "nope"}])

    def test_self_destruct_must_be_last(self):
        with self.assertRaises(deadman.ConfigError):
            make(actions=[{"id": "s", "type": "self_destruct"}, {"id": "a", "type": "noop"}])

    def test_disabled_actions_are_dropped(self):
        cfg, _, _ = make(actions=[{"id": "a", "type": "noop", "enabled": False}, {"id": "b", "type": "noop"}])
        self.assertEqual([a["id"] for a in cfg.actions], ["b"])


class RunTests(unittest.TestCase):
    def run_at(self, cfg, state, fake, days, armed=True):
        saved = []
        phase = deadman.run(cfg, state, T0 + timedelta(days=days), armed=armed, environ={},
                            save=lambda s: saved.append(True), log=quiet, known=fake.registry())
        return phase

    def test_unarmed_trigger_only_dry_runs(self):
        cfg, state, fake = make(actions=[{"id": "a", "type": "noop"}])
        self.run_at(cfg, state, fake, 40, armed=False)
        self.assertEqual(fake.calls, [("a", True)])
        self.assertIsNone(state["triggered_at"])
        self.assertEqual(state["actions"], {})

    def test_armed_trigger_runs_actions_once(self):
        cfg, state, fake = make(actions=[{"id": "a", "type": "noop"}, {"id": "b", "type": "noop"}])
        self.run_at(cfg, state, fake, 40)
        self.run_at(cfg, state, fake, 41)
        self.assertEqual(fake.calls, [("a", False), ("b", False)])
        self.assertEqual(state["actions"]["a"]["status"], DONE)
        self.assertIsNotNone(state["triggered_at"])

    def test_no_actions_before_trigger(self):
        cfg, state, fake = make(actions=[{"id": "a", "type": "noop"}])
        self.assertEqual(self.run_at(cfg, state, fake, 10), "ok")
        self.assertEqual(self.run_at(cfg, state, fake, 32), "warning")
        self.assertEqual(fake.calls, [])

    def test_warnings_are_rate_limited(self):
        cfg, state, fake = make(warn_every_hours=24)
        self.run_at(cfg, state, fake, 31)
        self.run_at(cfg, state, fake, 31.5)
        self.run_at(cfg, state, fake, 32.1)
        self.assertEqual(state["warnings_sent"], 2)

    def test_incomplete_action_resumes(self):
        cfg, state, fake = make(actions=[{"id": "a", "type": "noop"}])
        fake.behaviour["a"] = INCOMPLETE
        self.run_at(cfg, state, fake, 40)
        self.assertEqual(state["actions"]["a"]["status"], INCOMPLETE)
        fake.behaviour["a"] = DONE
        self.run_at(cfg, state, fake, 41)
        self.assertEqual(state["actions"]["a"]["status"], DONE)
        self.assertEqual(len(fake.calls), 2)

    def test_self_destruct_waits_for_others(self):
        cfg, state, fake = make(actions=[{"id": "a", "type": "noop"}, {"id": "s", "type": "self_destruct"}])
        fake.behaviour["a"] = FAILED
        self.run_at(cfg, state, fake, 40)
        self.assertNotIn(("s", False), fake.calls)
        fake.behaviour["a"] = DONE
        self.run_at(cfg, state, fake, 41)
        self.assertIn(("s", False), fake.calls)

    def test_failed_action_gives_up_and_unblocks(self):
        cfg, state, fake = make(actions=[{"id": "a", "type": "noop", "max_attempts": 2},
                                         {"id": "s", "type": "self_destruct"}])
        fake.behaviour["a"] = FAILED
        self.run_at(cfg, state, fake, 40)
        self.run_at(cfg, state, fake, 41)
        self.assertEqual(state["actions"]["a"]["status"], GAVE_UP)
        self.assertIn(("s", False), fake.calls)

    def test_delay_days(self):
        cfg, state, fake = make(actions=[{"id": "a", "type": "noop", "delay_days": 3}])
        self.run_at(cfg, state, fake, 40)
        self.assertEqual(fake.calls, [])
        self.run_at(cfg, state, fake, 43)
        self.assertEqual(fake.calls, [("a", False)])


if __name__ == "__main__":
    unittest.main()
