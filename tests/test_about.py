# TP-ABOUT-01..07 — about page (requirement-python-about).
# TP-ABOUT-09..10 — pyenv paths (requirement-python-pyenv).
# TP-OOP-02 — class CheckSystem owns the host check (requirement-python-oop).
from __future__ import print_function, unicode_literals

import datetime
import os
import shutil
import subprocess
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

    def _with_env(self, updates):
        """Restore the named environment keys after the test body."""
        saved = {}
        for key in updates:
            if key in os.environ:
                saved[key] = os.environ[key]
        class _Guard:
            def __enter__(_self):
                for key, value in updates.items():
                    if value is None:
                        os.environ.pop(key, None)
                    else:
                        os.environ[key] = value
                return _self

            def __exit__(_self, exc_type, exc, tb):
                for key in updates:
                    os.environ.pop(key, None)
                os.environ.update(saved)
                return False

        return _Guard()

    def _write_exe(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write("#!/bin/sh\n")
        os.chmod(path, 0o755)

    def _pyenv_tree(self, root, version_text, versions, shims):
        """A fake pyenv root. bin/pyenv is a symlink to libexec/pyenv."""
        libexec = os.path.join(root, "libexec", "pyenv")
        self._write_exe(libexec)
        bindir = os.path.join(root, "bin")
        os.makedirs(bindir, exist_ok=True)
        os.symlink(os.path.join("..", "libexec", "pyenv"), os.path.join(bindir, "pyenv"))
        with open(os.path.join(root, "version"), "w", encoding="utf-8") as handle:
            handle.write(version_text)
        for name in shims:
            self._write_exe(os.path.join(root, "shims", name))
        for version, binary in versions:
            self._write_exe(os.path.join(root, "versions", version, "bin", binary))
        return libexec

    def _location_line(self, text, label):
        prefix = "    {}:".format(label)
        for row in text.splitlines():
            if row.startswith(prefix):
                return row.split(":", 1)[1].strip()
        self.fail("missing {}".format(label))

    def test_pyenv_paths_stay_inside_the_root(self):
        """TP-ABOUT-09: under pyenv, bin/pyenv and interpreters inside the root."""
        from VideoSpeed.check_system import CheckSystem

        host = CheckSystem()
        with tempfile.TemporaryDirectory() as tmp:
            root = os.path.join(tmp, "pyenv")
            libexec = self._pyenv_tree(
                root,
                "system\n",
                [("3.12.11", "python3"), ("2.7.18", "python2")],
                ["python2", "python3"],
            )
            path = libexec.rsplit(os.sep, 1)[0] + os.pathsep + os.environ.get("PATH", "")
            updates = {
                "PYENV_ROOT": root,
                "PYENV_VERSION": "3.12.11:2.7.18",
                "PATH": path,
            }
            with self._with_env(updates):
                self.assertTrue(host.under_pyenv())
                self.assertEqual(host.pyenv_root(), os.path.abspath(root))
                self.assertEqual(host.pyenv_location(), os.path.join(root, "bin", "pyenv"))
                self.assertNotEqual(host.pyenv_location(), libexec)
                self.assertEqual(shutil.which("pyenv"), libexec)
                python3 = os.path.join(root, "versions", "3.12.11", "bin", "python3")
                python2 = os.path.join(root, "versions", "2.7.18", "bin", "python2")
                self.assertEqual(host.about_tool_location("python3"), python3)
                self.assertEqual(host.about_tool_location("python2"), python2)
                self.assertEqual(host.about_tool_location("pyenv"), os.path.join(root, "bin", "pyenv"))
                spawned = []

                def _refuse(*_args, **_kwargs):
                    spawned.append(True)
                    raise AssertionError("spawned")

                original_run = subprocess.run
                original_popen = subprocess.Popen
                subprocess.run = _refuse
                subprocess.Popen = _refuse
                try:
                    text = self._page().framework_about()
                finally:
                    subprocess.run = original_run
                    subprocess.Popen = original_popen
                self.assertEqual(spawned, [])
                self.assertEqual(self._location_line(text, "python3 location"), python3)
                self.assertEqual(self._location_line(text, "python2 location"), python2)
                self.assertEqual(
                    self._location_line(text, "pyenv location"),
                    os.path.join(root, "bin", "pyenv"),
                )

            shim_root = os.path.join(tmp, "shims-only")
            self._pyenv_tree(shim_root, "system\n", [], ["python2", "python3"])
            with self._with_env({"PYENV_ROOT": shim_root, "PYENV_VERSION": None}):
                self.assertTrue(host.under_pyenv())
                self.assertEqual(
                    host.about_tool_location("python3"),
                    os.path.join(shim_root, "shims", "python3"),
                )
                self.assertEqual(
                    host.about_tool_location("python2"),
                    os.path.join(shim_root, "shims", "python2"),
                )
                self.assertEqual(
                    host.pyenv_location(),
                    os.path.join(shim_root, "bin", "pyenv"),
                )

    def test_named_root_without_launcher_is_not_under_pyenv(self):
        """TP-ABOUT-10: a PYENV_ROOT with no bin/pyenv stays on shutil.which."""
        import VideoSpeed.check_system as check_mod
        from VideoSpeed.check_system import CheckSystem

        host = CheckSystem()
        found = {
            "python2": "",
            "python3": "/usr/bin/python3",
            "pyenv": "/usr/bin/pyenv",
        }
        original = check_mod.shutil.which
        check_mod.shutil.which = lambda name: found.get(name) or None
        try:
            with tempfile.TemporaryDirectory() as tmp:
                with self._with_env({"PYENV_ROOT": tmp, "PYENV_VERSION": None}):
                    self.assertFalse(host.under_pyenv())
                    self.assertEqual(host.pyenv_root(), "")
                    self.assertEqual(host.pyenv_location(), "")
                    self.assertEqual(host.pyenv_interpreter("python3"), "")
                    rows = host.check_system_lines(
                        now=datetime.datetime(2026, 10, 2, 1, 2, 3, 4)
                    )
                    text = "\n".join(rows)
                    self.assertEqual(self._location_line(text, "python2 location"), "")
                    self.assertEqual(
                        self._location_line(text, "python3 location"),
                        "/usr/bin/python3",
                    )
                    self.assertEqual(
                        self._location_line(text, "pyenv location"),
                        "/usr/bin/pyenv",
                    )
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
            "under_pyenv",
            "pyenv_root",
            "pyenv_location",
            "pyenv_version_names",
            "pyenv_interpreter",
            "about_tool_location",
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
