"""Bilinen hizmetlerin silme bağlantıları ve notları."""

from __future__ import annotations

from pathlib import Path

from .util import DATA_DIR, domain_of, fold, load_json, registrable_domain

DIFFICULTY = {"easy": "kolay", "medium": "orta", "hard": "zor", "impossible": "imkânsız"}


class Catalog:
    def __init__(self, entries: list[dict]):
        self.entries = entries
        self._by_id = {e["id"]: e for e in entries}
        self._by_domain = {}
        for e in entries:
            for d in e.get("domains", []):
                self._by_domain[d.lower()] = e

    @classmethod
    def load(cls, path: str | Path | None = None) -> "Catalog":
        data = load_json(path or DATA_DIR / "services.json", {"services": []})
        return cls(data["services"])

    def get(self, service_id: str | None) -> dict | None:
        return self._by_id.get(service_id or "")

    def by_domain(self, host: str | None) -> dict | None:
        if not host:
            return None
        host = host.lower().strip(".")
        labels = host.split(".")
        for i in range(len(labels) - 1):
            entry = self._by_domain.get(".".join(labels[i:]))
            if entry:
                return entry
        return self._by_domain.get(registrable_domain(host) or "")

    def by_name(self, name: str | None) -> dict | None:
        key = fold(name)
        if not key:
            return None
        for e in self.entries:
            if key in (fold(e["id"]), fold(e["name"])):
                return e
        return None

    def match(self, name: str | None = None, url: str | None = None) -> dict | None:
        return self.by_domain(domain_of(url)) or self.by_name(name) or self.by_domain(domain_of(name))

    def search(self, query: str) -> list[dict]:
        key = fold(query)
        return [
            e for e in self.entries
            if key in fold(e["id"]) or key in fold(e["name"]) or key in fold(e.get("category"))
            or any(key in d for d in e.get("domains", []))
        ]


def describe(entry: dict) -> str:
    lines = [f"{entry['name']}  [{entry['id']}]"]
    if entry.get("delete_url"):
        lines.append(f"  Silme   : {entry['delete_url']}")
    if entry.get("export_url"):
        lines.append(f"  Yedek   : {entry['export_url']}")
    if entry.get("privacy_email"):
        lines.append(f"  Gizlilik: {entry['privacy_email']}")
    if entry.get("grace_days") is not None:
        lines.append(f"  Bekleme : {entry['grace_days']} gün")
    if entry.get("difficulty"):
        lines.append(f"  Zorluk  : {DIFFICULTY.get(entry['difficulty'], entry['difficulty'])}")
    if entry.get("wipe_tool"):
        lines.append(f"  Araç    : diedigital wipe {entry['wipe_tool']}")
    if entry.get("notes"):
        lines.append(f"  Not     : {entry['notes']}")
    return "\n".join(lines)
