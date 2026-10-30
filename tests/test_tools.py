import tempfile
import unittest
from datetime import date
from pathlib import Path

from diedigital import discover, footprint, letters, net
from diedigital.catalog import Catalog
from diedigital.inventory import Inventory, import_csv
from diedigital.util import domain_of, registrable_domain


class DomainTests(unittest.TestCase):
    def test_registrable_domain(self):
        self.assertEqual(registrable_domain("mail.google.com"), "google.com")
        self.assertEqual(registrable_domain("www.trendyol.com.tr"), "trendyol.com.tr")
        self.assertEqual(registrable_domain("example.co.uk"), "example.co.uk")
        self.assertEqual(domain_of("https://accounts.reddit.com/login"), "reddit.com")
        self.assertIsNone(domain_of("androidapp://com.instagram.android"))

    def test_catalog_lookup(self):
        cat = Catalog.load()
        self.assertEqual(cat.by_domain("old.reddit.com")["id"], "reddit")
        self.assertEqual(cat.match("Instagram")["id"], "instagram")
        self.assertEqual(cat.match(url="https://www.amazon.com.tr/")["id"], "amazon")
        self.assertIsNone(cat.match("bilinmeyen hizmet"))
        apollo = cat.match(url="https://app.apollo.io/")
        self.assertEqual(apollo["template"], "data-broker-suppression")
        self.assertIn("zoominfo", [e["id"] for e in cat.search("b2b")])


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp())
        self.inv = Inventory(self.dir / "accounts.json")

    def write(self, name, text):
        path = self.dir / name
        path.write_text(text, encoding="utf-8")
        return path

    def test_import_bitwarden_drops_passwords(self):
        csv_path = self.write("bw.csv", (
            "folder,favorite,type,name,notes,fields,reprompt,login_uri,login_username,login_password,login_totp\n"
            ",,login,Reddit,,,0,https://www.reddit.com/login,ben123,GIZLI-PAROLA,\n"
            ",,login,Benim Forum,,,0,https://forum.example.org,ben@example.com,GIZLI-2,\n"
            ",,login,Reddit,,,0,https://reddit.com,ben123,GIZLI-PAROLA,\n"
        ))
        added, skipped = import_csv(self.inv, csv_path)
        self.inv.save()
        self.assertEqual((added, skipped), (2, 1))
        saved = (self.dir / "accounts.json").read_text(encoding="utf-8")
        self.assertNotIn("GIZLI", saved)
        reddit = self.inv.find("reddit")
        self.assertEqual(reddit["username"], "ben123")
        self.assertEqual(self.inv.find("example.org")["email"], "ben@example.com")

    def test_import_chrome(self):
        csv_path = self.write("chrome.csv", "name,url,username,password,note\n"
                                            "github.com,https://github.com/session,ben,x,\n")
        self.assertEqual(import_csv(self.inv, csv_path), (1, 0))
        self.assertEqual(self.inv.accounts[0]["catalog_id"], "github")

    def test_status_and_overdue(self):
        acc = self.inv.add("Trendyol", email="ben@example.com")
        self.assertEqual(acc["jurisdiction"], "tr")
        self.inv.set_status(acc, "requested")
        acc["requested_at"] = "2020-01-01T00:00:00Z"
        self.assertEqual(self.inv.overdue(30), [acc])
        with self.assertRaises(ValueError):
            self.inv.set_status(acc, "uydurma")


class LetterTests(unittest.TestCase):
    profile = {"name": "Ada Yılmaz", "email": "ada@example.com", "address": "İstanbul"}

    def test_empty_placeholder_lines_are_dropped(self):
        subject, body = letters.render("kvkk-silme", self.profile, {"service": "Örnek A.Ş."},
                                       today=date(2026, 3, 1))
        self.assertIn("Örnek A.Ş.", subject)
        self.assertIn("Ad Soyad: Ada Yılmaz", body)
        self.assertNotIn("T.C. Kimlik No", body)
        self.assertNotIn("$", body)
        self.assertIn("01.03.2026", body)

    def test_identifiers_are_deduplicated(self):
        account = {"service": "X", "email": "ADA@example.com", "username": "ada"}
        ids = letters.identifiers(self.profile, account)
        self.assertEqual(ids, ["ADA@example.com", "ada"])

    def test_auto_template(self):
        self.assertEqual(letters.auto_template({"jurisdiction": "tr"}), "kvkk-silme")
        b2b = {"jurisdiction": "eu", "template": "data-broker-suppression"}
        self.assertEqual(letters.auto_template(b2b), "data-broker-suppression")
        self.assertEqual(letters.auto_template(b2b, reminder=True), "gdpr-reminder")
        self.assertEqual(letters.auto_template({"jurisdiction": "eu"}, reminder=True), "gdpr-reminder")

    def test_all_templates_render(self):
        account = {"service": "S", "email": "a@b.c", "requested_at": "2026-01-01T00:00:00Z"}
        for name in letters.list_templates():
            subject, body = letters.render(name, self.profile, account, urls=["https://example.com/x"])
            self.assertTrue(subject)
            self.assertNotRegex(body, r"\$\w")

    def test_profile_required(self):
        with self.assertRaises(letters.LetterError):
            letters.render("kvkk-silme", {}, None)


class FootprintTests(unittest.TestCase):
    def test_phone_variants(self):
        variants = footprint.phone_variants("+90 (532) 123 45 67")
        self.assertIn("0532 123 45 67", variants)
        self.assertIn("05321234567", variants)
        self.assertIn("+90 532 123 45 67", variants)

    def test_dorks(self):
        queries = footprint.dork_queries(name="Ada Yılmaz", emails=["ada@example.com"])
        texts = [q for _, q in queries]
        self.assertIn('"Ada Yılmaz"', texts)
        self.assertIn('"ada@example.com"', texts)
        self.assertIn("google.com/search", footprint.dork_markdown(queries))


class DiscoverTests(unittest.TestCase):
    def test_signup_headers_are_counted_by_domain(self):
        senders = {}
        discover.add_header(senders, b"From: Trendyol <noreply@mail.trendyol.com>\r\n"
                                     b"Subject: =?utf-8?q?Trendyol=27a_ho=C5=9F_geldin!?=\r\n"
                                     b"Date: Mon, 01 Jan 2024 10:00:00 +0300\r\n")
        discover.add_header(senders, b"From: Ali <ali@gmail.com>\r\nSubject: Welcome back\r\n")
        self.assertEqual(list(senders), ["trendyol.com"])
        self.assertEqual(senders["trendyol.com"].signup_hits, 1)

    def test_all_mail_folder_detection(self):
        class Conn:
            def list(self):
                return "OK", [b'(\\HasNoChildren) "/" "INBOX"',
                              b'(\\All \\HasNoChildren) "/" "[Gmail]/T&APw-m Postalar"']
        self.assertEqual(discover.find_all_mail(Conn()), '"[Gmail]/T&APw-m Postalar"')

    def test_imap_date_is_locale_independent(self):
        self.assertEqual(discover.imap_since(date(2015, 3, 7)), "07-Mar-2015")


class RetryDelayTests(unittest.TestCase):
    def test_retry_after_seconds(self):
        self.assertEqual(net.retry_delay({"Retry-After": "12"}, 1, now=0), 12)

    def test_github_epoch_reset(self):
        self.assertEqual(net.retry_delay({"x-ratelimit-reset": "2000000100"}, 1, now=2000000000), 100)

    def test_reddit_relative_reset(self):
        self.assertEqual(net.retry_delay({"x-ratelimit-reset": "42"}, 1, now=2000000000), 42)

    def test_mastodon_iso_reset(self):
        now = 1767225600  # 2026-01-01T00:00:00Z
        self.assertEqual(net.retry_delay({"x-ratelimit-reset": "2026-01-01T00:10:00.000Z"}, 1, now=now), 600)

    def test_backoff_without_headers(self):
        self.assertEqual(net.retry_delay({}, 3, now=0), 8)


if __name__ == "__main__":
    unittest.main()
