import unittest
from update_helper import safe_member

class SafeZipMemberTests(unittest.TestCase):
    def test_allows_application_files(self):
        self.assertTrue(safe_member("LOICatFarmPro.exe"))
        self.assertTrue(safe_member("_internal/app.pyc"))
        self.assertTrue(safe_member("_internal/subdir/data.bin"))
        self.assertTrue(safe_member("spotify_webview_host.exe"))

    def test_allows_normal_directory_entries(self):
        self.assertTrue(safe_member("_internal/"))
        self.assertTrue(safe_member("_internal/subdir/"))

    def test_rejects_escape_paths_and_unapproved_files(self):
        for path in ("../evil.exe", "_internal/../../evil", "/absolute", "C:/evil", "other.txt", "LOICatFarmPro.exe/", "spotify_webview_host.exe/"):
            with self.subTest(path=path):
                self.assertFalse(safe_member(path))

if __name__ == "__main__":
    unittest.main()
