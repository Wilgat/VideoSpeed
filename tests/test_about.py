# TP-ABOUT-01..07 — about page (requirement-python-about).
# TP-OOP-02 — class CheckSystem owns the host check (requirement-python-oop).
from __future__ import print_function, unicode_literals

import datetime
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


class TestAbout(unittest.TestCase):
    def _cli(self):
        from VideoSpeed import cli

        return cli

    def _page(self):
        from VideoSpeed.cli import Cli

        return Cli().about

    def test_about_names_the_host_check_and_the_box(self):
        """TP-ABOUT-01: identity, host-check labels, star-box title; no curl line."""
        cli = self._cli()
        text = self._page().framework_about()
        for label in (
            "Domain:",
            "[CHECK SYSTEM]:",
            "Now checking your operation system!",
            "Python:",
            "C Library:",
            "Operation System:",
            "Architecture:",
            "Current User:",
            "Shell:",
            "Python Executable:",
            "python2 location:",
            "python3 location:",
            "conda location:",
            "pyenv location:",
            "Inside docker container:",
            "Cython String:",
            "Binary Type:",
            "Location:",
            "Basic Usage:",
            "Please visit our homepage:",
            "VideoSpeed ({}.{}.{}) by {} on {}".format(
                cli.MAJOR_VERSION,
                cli.MINOR_VERSION,
                cli.PATCH_VERSION,
                cli.AUTHOR_NAME,
                cli.LAST_UPDATE,
            ),
        ):
            self.assertIn(label, text)
        self.assertNotIn("curl -fsSL", text)
        self.assertNotIn("py-tui", text)
        self.assertNotIn("py_tui", text)
        self.assertTrue(
            "GLOBAL INSTALLED" in text
            or "LOCAL INSTALLED" in text
            or "UNINSTALLED" in text
        )

    def test_check_system_stamp_and_field_order(self):
        """TP-ABOUT-02: stamp, CHECK SYSTEM header, and field order."""
        from VideoSpeed.check_system import CheckSystem

        when = datetime.datetime(2026, 10, 1, 11, 16, 23, 700590)
        rows = CheckSystem().check_system_lines(now=when)
        self.assertTrue(rows[0].startswith("2026-10-01 11:16:23.700590 VideoSpeed(v"))
        self.assertTrue(rows[0].endswith("  [CHECK SYSTEM]:"))
        self.assertEqual(rows[1], "  Now checking your operation system!")
        labels = [row.strip().split(":", 1)[0] for row in rows[2:]]
        self.assertEqual(
            labels,
            [
                "Python",
                "C Library",
                "Operation System",
                "Architecture",
                "Current User",
                "Shell",
                "Python Executable",
                "python2 location",
                "python3 location",
                "conda location",
                "pyenv location",
                "Inside docker container",
                "Cython String",
                "Binary Type",
                "Location",
            ],
        )

    def test_about_box_is_a_rectangle(self):
        """TP-ABOUT-03: the star box is one rectangle."""
        box = self._page().about_box_lines(
            usage="video-speed --file clip.mp4 --start 0 --end 5",
            location="/tmp/video-speed",
            kind="global",
            homepage="https://example.test/VideoSpeed",
            download_url="",
        )
        width = len(box[0])
        self.assertGreater(width, 4)
        for line in box:
            self.assertEqual(len(line), width, line)
            self.assertTrue(line.startswith("*"), line)
            self.assertTrue(line.endswith("*"), line)
        flat = "\n".join(box)
        self.assertIn("GLOBAL INSTALLED", flat)
        self.assertIn("/tmp/video-speed", flat)
        self.assertIn('    "https://example.test/VideoSpeed"', flat)
        self.assertNotIn("curl", flat)

    def test_about_box_can_show_an_install_line_when_a_url_is_given(self):
        """TP-ABOUT-04: install line only when a URL is passed; product URL stays empty."""
        cli = self._cli()
        box = "\n".join(
            self._page().about_box_lines(
                location="/tmp/video-speed",
                kind="local",
                download_url="https://example.test/install",
            )
        )
        self.assertIn("LOCAL INSTALLED", box)
        self.assertIn("Installation command:", box)
        self.assertIn("curl -fsSL https://example.test/install |", box)
        self.assertEqual(cli.DOWNLOAD_URL, "")

    def test_compiler_arch_and_libc_labels(self):
        """TP-ABOUT-05: compiler token, arch map, and libc token."""
        from VideoSpeed.check_system import CheckSystem

        host = CheckSystem()
        py, lib = host.parse_sys_version(
            "3.12.3 (main, Jan 1 2024, 00:00:00) [GCC 13.3.0]",
            "3.12.3",
        )
        self.assertEqual(py, "3.12.3")
        self.assertEqual(lib, "GCC 13.3.0")
        py2, lib2 = host.parse_sys_version(
            "3.10.14 (build)\n[PyPy 7.3.16 with GCC 13.2.0]",
            "3.10.14",
        )
        self.assertEqual(py2, "3.10.14 (PyPy 7.3.16)")
        self.assertEqual(lib2, "GCC 13.2.0")
        self.assertEqual(host.arch_label("MSC v.1929 64 bit (AMD64)", "AMD64"), "amd64")
        self.assertEqual(host.arch_label("GCC 13.3.0", "x86_64"), "amd64")
        self.assertEqual(host.arch_label("GCC 13.3.0", "aarch64"), "arm64")
        self.assertEqual(
            host.libc_label("MSC v.1929 64 bit (AMD64)", "/bin/bash", detected="glibc"),
            "msc",
        )
        self.assertEqual(
            host.libc_label("[Clang 15.0.0]", "/bin/bash", detected="glibc"),
            "clang",
        )
        self.assertEqual(host.libc_label("GCC 13.3.0", "/bin/ash", detected=""), "muslc")
        self.assertEqual(host.binary_type("amd64", "glibc"), "amd64-glibc")
        self.assertEqual(host.binary_type("amd64", ""), "amd64-")

    def test_install_kind(self):
        """TP-ABOUT-06: checkout, home copy, and /usr copy."""
        cli = self._cli()
        page = self._page()
        self.assertEqual(page.install_kind(cli.__file__), "uninstalled")
        self.assertTrue(page._is_source_checkout(os.path.realpath(cli.__file__)))
        home = os.path.realpath(os.path.expanduser("~"))
        local_script = os.path.join(home, ".local", "bin", "video-speed")
        self.assertEqual(page.install_kind(local_script), "local")
        local_pkg = os.path.join(
            home, ".pyenv", "versions", "3.14.7", "lib", "python3.14",
            "site-packages", "VideoSpeed", "cli.py",
        )
        self.assertEqual(page.install_kind(local_pkg), "local")
        self.assertEqual(page.install_kind("/usr/local/bin/video-speed"), "global")
        self.assertEqual(
            page.install_kind("/usr/lib/python3/dist-packages/VideoSpeed/cli.py"),
            "global",
        )
        self.assertIn("GLOBAL INSTALLED", page.install_sentence("global"))
        self.assertIn("UNINSTALLED", page.install_sentence("uninstalled"))

    def test_docker_marker_and_missing_command(self):
        """TP-ABOUT-07: docker marker file; missing tool location stays blank."""
        import VideoSpeed.check_system as check_mod
        from VideoSpeed.check_system import CheckSystem

        host = CheckSystem()
        self.assertFalse(host.inside_docker(marker="/tmp/videospeed-no-such-dockerenv"))
        with tempfile.TemporaryDirectory() as tmp:
            marker = os.path.join(tmp, ".dockerenv")
            with open(marker, "w", encoding="utf-8"):
                pass
            self.assertTrue(host.inside_docker(marker=marker))
        original = check_mod.shutil.which
        check_mod.shutil.which = lambda _name: None
        try:
            self.assertEqual(host.command_location("conda"), "")
        finally:
            check_mod.shutil.which = original

    def test_tp_oop_02_check_system_owns_the_host_check(self):
        """TP-OOP-02: CheckSystem in check_system.py; rule 11 functions are not in cli.py."""
        import inspect

        from VideoSpeed import cli
        from VideoSpeed.about_page import AboutPage
        from VideoSpeed.check_system import CheckSystem

        names = (
            "check_system_lines",
            "parse_sys_version",
            "arch_label",
            "libc_label",
            "binary_type",
            "current_user",
            "shell_text",
            "python_executable_name",
            "command_location",
            "os_text",
            "inside_docker",
            "cpython_soabi",
            "self_location",
        )
        self.assertTrue(inspect.isclass(CheckSystem))
        self.assertEqual(
            Path(inspect.getfile(CheckSystem)).resolve(),
            (ROOT / "src" / "VideoSpeed" / "check_system.py").resolve(),
        )
        ship = (ROOT / "src" / "VideoSpeed" / "cli.py").read_text(encoding="utf-8")
        for name in names:
            self.assertTrue(inspect.isfunction(CheckSystem.__dict__[name]), name)
            self.assertFalse(inspect.isfunction(getattr(cli, name, None)), name)
            self.assertNotIn("\ndef {}(".format(name), "\n" + ship)
        about = inspect.getsource(AboutPage.framework_about)
        box = inspect.getsource(AboutPage.about_box_lines)
        self.assertIn("check_system_lines", about)
        self.assertIn("self.check", about)
        self.assertIn("self_location", box)
        self.assertIn("self.check", box)
        page = (ROOT / "src" / "VideoSpeed" / "about_page.py").read_text(encoding="utf-8")
        self.assertIn("CheckSystem", page)
        self.assertIn("def framework_about(", page)
        self.assertIn("def about_box_lines(", page)
        self.assertNotIn("\ndef framework_about(", "\n" + ship)
        self.assertNotIn("\ndef about_box_lines(", "\n" + ship)


if __name__ == "__main__":
    unittest.main()
