# TP-ABOUT-01..07 — about page (requirement-python-about).
# TP-ABOUT-09..10 — pyenv paths (requirement-python-pyenv).
# TP-ABOUT-11..12 — conda paths (requirement-python-conda).
# TP-ABOUT-13..15 — PID, cache chain, persistence, TTY, about --json streams.
# TP-ABOUT-16 — in_venv, in_pyenv, and in_conda come from the process logger.
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

from VideoSpeed.cli import Cli  # noqa: E402


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
            "PID:",
            "Cache folder used:",
            "Cache folder (preferred):",
            "Cache folder (1st fallback):",
            "Cache folder (2nd fallback):",
            "Persistence storage:",
            "TTY / Interactive:",
            "Basic Usage:",
            "Please visit our homepage:",
            "VideoSpeed ({}.{}.{}) by {} on {}".format(
                cli.MAJOR_VERSION,
                cli.MINOR_VERSION,
                cli.PATCH_VERSION,
                cli.Cli.AUTHOR_NAME,
                cli.Cli.LAST_UPDATE,
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
        rows = CheckSystem(app_name=Cli.APP_NAME, version=Cli._PKG_VERSION, console_name=Cli.CONSOLE_NAME).check_system_lines(now=when)
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
                "PID",
                "Cache folder used",
                "Cache folder (preferred)",
                "Cache folder (1st fallback)",
                "Cache folder (2nd fallback)",
                "Persistence storage",
                "TTY / Interactive",
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
        self.assertEqual(cli.Cli.DOWNLOAD_URL, "")

    def test_compiler_arch_and_libc_labels(self):
        """TP-ABOUT-05: compiler token, arch map, and libc token."""
        from VideoSpeed.check_system import CheckSystem

        host = CheckSystem(app_name=Cli.APP_NAME, version=Cli._PKG_VERSION, console_name=Cli.CONSOLE_NAME)
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

        host = CheckSystem(app_name=Cli.APP_NAME, version=Cli._PKG_VERSION, console_name=Cli.CONSOLE_NAME)
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

    def _conda_tree(self, root, env_name, base_bins, env_bins):
        """A fake conda root. bin/conda is a symlink to condabin/conda."""
        condabin = os.path.join(root, "condabin", "conda")
        self._write_exe(condabin)
        bindir = os.path.join(root, "bin")
        os.makedirs(bindir, exist_ok=True)
        os.symlink(os.path.join("..", "condabin", "conda"), os.path.join(bindir, "conda"))
        for name in base_bins:
            self._write_exe(os.path.join(bindir, name))
        if env_name:
            for name in env_bins:
                self._write_exe(os.path.join(root, "envs", env_name, "bin", name))
        return condabin

    def _location_line(self, text, label):
        prefix = "    {}:".format(label)
        for row in text.splitlines():
            if row.startswith(prefix):
                return row.split(":", 1)[1].strip()
        self.fail("missing {}".format(label))

    def test_pyenv_paths_stay_inside_the_root(self):
        """TP-ABOUT-09: under pyenv, bin/pyenv and interpreters inside the root."""
        from VideoSpeed.check_system import CheckSystem

        host = CheckSystem(app_name=Cli.APP_NAME, version=Cli._PKG_VERSION, console_name=Cli.CONSOLE_NAME)
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
                "CONDA_EXE": os.path.join(tmp, "not-conda"),
                "CONDA_PREFIX": None,
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
            with self._with_env({
                "PYENV_ROOT": shim_root,
                "PYENV_VERSION": None,
                "CONDA_EXE": os.path.join(tmp, "not-conda"),
                "CONDA_PREFIX": None,
            }):
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

        host = CheckSystem(app_name=Cli.APP_NAME, version=Cli._PKG_VERSION, console_name=Cli.CONSOLE_NAME)
        found = {
            "python2": "",
            "python3": "/usr/bin/python3",
            "pyenv": "/usr/bin/pyenv",
        }
        original = check_mod.shutil.which
        check_mod.shutil.which = lambda name: found.get(name) or None
        try:
            with tempfile.TemporaryDirectory() as tmp:
                with self._with_env({
                    "PYENV_ROOT": tmp,
                    "PYENV_VERSION": None,
                    "CONDA_EXE": os.path.join(tmp, "not-conda"),
                    "CONDA_PREFIX": None,
                }):
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

    def _refuse_spawn(self):
        """Patch process start so a host check that spawns fails the proof."""
        spawned = []

        def _refuse(*_args, **_kwargs):
            spawned.append(True)
            raise AssertionError("spawned")

        class _Guard:
            def __enter__(_self):
                _self.original_run = subprocess.run
                _self.original_popen = subprocess.Popen
                subprocess.run = _refuse
                subprocess.Popen = _refuse
                return spawned

            def __exit__(_self, exc_type, exc, tb):
                subprocess.run = _self.original_run
                subprocess.Popen = _self.original_popen
                return False

        return _Guard()

    def _home_expand(self, home):
        """Treat ~ as a temporary login home for the conda install search."""
        real_expand = os.path.expanduser

        def _expand(path):
            if path == "~":
                return home
            if isinstance(path, str) and (path.startswith("~/") or path.startswith("~\\")):
                return os.path.join(home, path[2:])
            return real_expand(path)

        class _Guard:
            def __enter__(_self):
                os.path.expanduser = _expand
                return _self

            def __exit__(_self, exc_type, exc, tb):
                os.path.expanduser = real_expand
                return False

        return _Guard()

    def test_conda_paths_stay_inside_the_prefix(self):
        """TP-ABOUT-11: under conda, bin/conda and interpreters inside the prefix."""
        from VideoSpeed.check_system import CheckSystem

        host = CheckSystem(app_name=Cli.APP_NAME, version=Cli._PKG_VERSION, console_name=Cli.CONSOLE_NAME)
        with tempfile.TemporaryDirectory() as tmp:
            root = os.path.join(tmp, "conda")
            condabin = self._conda_tree(
                root,
                "demo",
                ("python2", "python3"),
                ("python3",),
            )
            pyenv_root = os.path.join(tmp, "pyenv")
            self._pyenv_tree(
                pyenv_root,
                "3.12.11\n",
                [("3.12.11", "python3"), ("2.7.18", "python2")],
                ["python2", "python3"],
            )
            path = os.path.dirname(condabin) + os.pathsep + os.environ.get("PATH", "")
            prefix = os.path.join(root, "envs", "demo")
            python3 = os.path.join(prefix, "bin", "python3")
            conda_bin = os.path.join(root, "bin", "conda")
            pyenv_bin = os.path.join(pyenv_root, "bin", "pyenv")
            updates = {
                "CONDA_EXE": condabin,
                "CONDA_PREFIX": prefix,
                "PYENV_ROOT": pyenv_root,
                "PYENV_VERSION": "3.12.11:2.7.18",
                "PATH": path,
            }
            with self._with_env(updates):
                self.assertTrue(host.under_conda())
                self.assertTrue(host.under_pyenv())
                self.assertEqual(host.conda_root(), os.path.abspath(root))
                self.assertEqual(host.conda_location(), conda_bin)
                self.assertNotEqual(host.conda_location(), condabin)
                self.assertEqual(shutil.which("conda"), condabin)
                self.assertEqual(host.about_tool_location("python3"), python3)
                self.assertEqual(host.about_tool_location("python2"), "")
                self.assertEqual(host.about_tool_location("conda"), conda_bin)
                self.assertEqual(host.about_tool_location("pyenv"), pyenv_bin)
                with self._refuse_spawn() as spawned:
                    text = self._page().framework_about()
                self.assertEqual(spawned, [])
                self.assertEqual(self._location_line(text, "python3 location"), python3)
                self.assertEqual(self._location_line(text, "python2 location"), "")
                self.assertEqual(self._location_line(text, "conda location"), conda_bin)
                self.assertEqual(self._location_line(text, "pyenv location"), pyenv_bin)

            home = os.path.join(tmp, "home")
            mini = os.path.join(home, "miniconda3")
            self._write_exe(os.path.join(mini, "bin", "conda"))
            self._write_exe(os.path.join(mini, "bin", "python3"))
            base_python3 = os.path.join(mini, "bin", "python3")
            base_conda = os.path.join(mini, "bin", "conda")
            with self._home_expand(home):
                with self._with_env({
                    "CONDA_EXE": None,
                    "CONDA_PREFIX": None,
                    "PYENV_ROOT": os.path.join(tmp, "not-pyenv"),
                    "PYENV_VERSION": None,
                }):
                    self.assertTrue(host.under_conda())
                    self.assertFalse(host.under_pyenv())
                    self.assertEqual(host.conda_location(), base_conda)
                    self.assertEqual(host.about_tool_location("python3"), base_python3)
                    self.assertEqual(host.about_tool_location("python2"), "")
                    with self._refuse_spawn() as spawned:
                        text = self._page().framework_about()
                    self.assertEqual(spawned, [])
                    self.assertEqual(self._location_line(text, "python3 location"), base_python3)
                    self.assertEqual(self._location_line(text, "python2 location"), "")
                    self.assertEqual(self._location_line(text, "conda location"), base_conda)

    def test_named_exe_without_launcher_is_not_under_conda(self):
        """TP-ABOUT-12: a CONDA_EXE outside bin or condabin stays on shutil.which."""
        import VideoSpeed.check_system as check_mod
        from VideoSpeed.check_system import CheckSystem

        host = CheckSystem(app_name=Cli.APP_NAME, version=Cli._PKG_VERSION, console_name=Cli.CONSOLE_NAME)
        found = {
            "python2": "",
            "python3": "/usr/bin/python3",
            "conda": "/usr/bin/conda",
            "pyenv": "",
        }
        original = check_mod.shutil.which
        check_mod.shutil.which = lambda name: found.get(name) or None
        try:
            with tempfile.TemporaryDirectory() as tmp:
                home = os.path.join(tmp, "home")
                mini = os.path.join(home, "miniconda3")
                self._write_exe(os.path.join(mini, "bin", "conda"))
                self._write_exe(os.path.join(mini, "bin", "python3"))
                bad = os.path.join(tmp, "somewhere", "conda")
                self._write_exe(bad)
                with self._home_expand(home):
                    with self._with_env({
                        "CONDA_EXE": bad,
                        "CONDA_PREFIX": os.path.join(mini, "envs", "demo"),
                        "PYENV_ROOT": os.path.join(tmp, "not-pyenv"),
                        "PYENV_VERSION": None,
                    }):
                        self.assertFalse(host.under_conda())
                        self.assertEqual(host.conda_root(), "")
                        self.assertEqual(host.conda_location(), "")
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
                            self._location_line(text, "conda location"),
                            "/usr/bin/conda",
                        )
                    junk = os.path.join(tmp, "not-a-prefix")
                    os.makedirs(junk, exist_ok=True)
                    with self._with_env({
                        "CONDA_EXE": None,
                        "CONDA_PREFIX": junk,
                        "PYENV_ROOT": os.path.join(tmp, "not-pyenv"),
                        "PYENV_VERSION": None,
                    }):
                        self.assertFalse(host.under_conda())
                        self.assertEqual(
                            host.about_tool_location("conda"),
                            "/usr/bin/conda",
                        )
                        self.assertEqual(
                            host.about_tool_location("python3"),
                            "/usr/bin/python3",
                        )
                        self.assertEqual(host.about_tool_location("python2"), "")
        finally:
            check_mod.shutil.which = original

    def test_environment_checks_come_from_the_logger(self):
        """TP-ABOUT-16: in_venv, in_pyenv, and in_conda are the logger methods."""
        import inspect

        from VideoSpeed.check_system import CheckSystem

        class _Env:
            """Stand-in logger. The check calls these three methods."""

            def __init__(self, venv, pyenv, conda):
                self.venv = venv
                self.pyenv = pyenv
                self.conda = conda
                self.calls = []

            def log_message(self, *_args, **_kwargs):
                return None

            def inVenv(self):
                self.calls.append("inVenv")
                return self.venv

            def inPyenv(self):
                self.calls.append("inPyenv")
                return self.pyenv

            def inConda(self):
                self.calls.append("inConda")
                return self.conda

        inside = _Env(True, False, True)
        host = CheckSystem(
            logger=inside,
            app_name=Cli.APP_NAME,
            version=Cli._PKG_VERSION,
            console_name=Cli.CONSOLE_NAME,
        )
        with self._refuse_spawn() as spawned:
            self.assertTrue(host.in_venv())
            self.assertFalse(host.in_pyenv())
            self.assertTrue(host.in_conda())
        self.assertEqual(spawned, [])
        self.assertEqual(inside.calls, ["inVenv", "inPyenv", "inConda"])

        bare = CheckSystem(
            app_name=Cli.APP_NAME,
            version=Cli._PKG_VERSION,
            console_name=Cli.CONSOLE_NAME,
        )
        self.assertFalse(bare.in_venv())
        self.assertFalse(bare.in_pyenv())
        self.assertFalse(bare.in_conda())

        for method, call_name, banned in (
            (CheckSystem.in_venv, "inVenv", "VIRTUAL_ENV"),
            (CheckSystem.in_pyenv, "inPyenv", "/.pyenv/"),
            (CheckSystem.in_conda, "inConda", "CONDA_DEFAULT_ENV"),
        ):
            body = inspect.getsource(method)
            self.assertIn(call_name, body)
            self.assertNotIn(banned, body)

        ship = (ROOT / "src" / "VideoSpeed" / "check_system.py").read_text(encoding="utf-8")
        for banned_call in ("pyenvVenv", "pyenv_versions", "condaPath", "conda_env_list"):
            self.assertNotIn(banned_call, ship)

        outside = _Env(False, True, True)
        outside_host = CheckSystem(
            logger=outside,
            app_name=Cli.APP_NAME,
            version=Cli._PKG_VERSION,
            console_name=Cli.CONSOLE_NAME,
        )
        with tempfile.TemporaryDirectory() as tmp:
            empty = os.path.join(tmp, "not-pyenv")
            os.makedirs(empty)
            with self._with_env({
                "PYENV_ROOT": empty,
                "CONDA_EXE": os.path.join(tmp, "not-conda"),
                "CONDA_PREFIX": None,
            }):
                self.assertTrue(outside_host.in_pyenv())
                self.assertTrue(outside_host.in_conda())
                self.assertFalse(outside_host.under_pyenv())
                self.assertFalse(outside_host.under_conda())
                self.assertEqual(
                    outside_host.about_tool_location("pyenv"),
                    outside_host.command_location("pyenv"),
                )
                self.assertEqual(
                    outside_host.about_tool_location("conda"),
                    outside_host.command_location("conda"),
                )

            root = os.path.join(tmp, "pyenv")
            self._pyenv_tree(root, "system\n", [], ["python3"])
            quiet = _Env(False, False, False)
            rooted = CheckSystem(
                logger=quiet,
                app_name=Cli.APP_NAME,
                version=Cli._PKG_VERSION,
                console_name=Cli.CONSOLE_NAME,
            )
            with self._with_env({
                "PYENV_ROOT": root,
                "PYENV_VERSION": None,
                "CONDA_EXE": os.path.join(tmp, "not-conda"),
                "CONDA_PREFIX": None,
            }):
                self.assertFalse(rooted.in_pyenv())
                self.assertTrue(rooted.under_pyenv())
                self.assertEqual(
                    rooted.about_tool_location("pyenv"),
                    os.path.join(root, "bin", "pyenv"),
                )

        from ChronicleLogger import ChronicleLogger

        with tempfile.TemporaryDirectory() as tmp:
            real = ChronicleLogger(
                logname="VideoSpeed",
                basedir=tmp,
                logdir=os.path.join(tmp, "log"),
                is_quiet=True,
            )
            live = CheckSystem(
                logger=real,
                app_name=Cli.APP_NAME,
                version=Cli._PKG_VERSION,
                console_name=Cli.CONSOLE_NAME,
            )
            self.assertEqual(live.in_venv(), real.inVenv())
            self.assertEqual(live.in_pyenv(), real.inPyenv())
            self.assertEqual(live.in_conda(), real.inConda())

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
            "process_id",
            "cache_folder_preferred",
            "cache_folder_first_fallback",
            "cache_folder_second_fallback",
            "cache_folder_used",
            "persistence_storage",
            "tty_interactive",
            "in_venv",
            "in_pyenv",
            "in_conda",
            "under_pyenv",
            "pyenv_root",
            "pyenv_location",
            "pyenv_version_names",
            "pyenv_interpreter",
            "under_conda",
            "conda_root",
            "conda_location",
            "conda_prefix",
            "conda_interpreter",
            "about_tool_location",
        )
        self.assertTrue(inspect.isclass(CheckSystem))
        self.assertEqual(
            Path(inspect.getfile(CheckSystem)).resolve(),
            (ROOT / "src" / "VideoSpeed" / "check_system.py").resolve(),
        )
        ship = (ROOT / "src" / "VideoSpeed" / "cli.py").read_text(encoding="utf-8")
        for name in names:
            self.assertTrue(inspect.isfunction(inspect.getattr_static(CheckSystem, name)), name)
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

    def test_run_lines_name_pid_cache_persistence_and_tty(self):
        """TP-ABOUT-13: run lines after Location; the check does not create them."""
        from VideoSpeed.check_system import CheckSystem

        host = CheckSystem(app_name=Cli.APP_NAME, version=Cli._PKG_VERSION, console_name=Cli.CONSOLE_NAME)
        created = []
        real_makedirs = os.makedirs
        real_mkdir = os.mkdir

        def _refuse_makedirs(*args, **kwargs):
            created.append(args[0] if args else "")
            return real_makedirs(*args, **kwargs)

        def _refuse_mkdir(*args, **kwargs):
            created.append(args[0] if args else "")
            return real_mkdir(*args, **kwargs)

        os.makedirs = _refuse_makedirs
        os.mkdir = _refuse_mkdir
        try:
            rows = host.check_system_lines(
                now=datetime.datetime(2026, 10, 2, 12, 0, 0, 1)
            )
            text = "\n".join(rows)
            page = self._page().framework_about()
        finally:
            os.makedirs = real_makedirs
            os.mkdir = real_mkdir

        self.assertEqual(created, [])
        pid = str(os.getpid())
        self.assertIn("    PID: {}".format(pid), text)
        self.assertIn("    PID: {}".format(pid), page)
        preferred = host.cache_folder_preferred()
        first = host.cache_folder_first_fallback()
        second = host.cache_folder_second_fallback()
        store = host.persistence_storage()
        self.assertIn("    Cache folder (preferred): {}".format(preferred), text)
        self.assertIn("    Cache folder (1st fallback): {}".format(first), text)
        self.assertIn("    Cache folder (2nd fallback): {}".format(second), text)
        self.assertIn("    Persistence storage: {}".format(store), text)
        self.assertIn("cache-VideoSpeed-", preferred)
        self.assertTrue(preferred.startswith("/dev/shm/cache/"))
        self.assertTrue(first.startswith("/tmp/cache/"))
        self.assertNotIn("\n    PID:", text.split("    Location:", 1)[0])
        tty = "yes" if sys.stdout.isatty() else "no"
        self.assertIn("    TTY / Interactive: {}".format(tty), text)
        self.assertEqual(host.tty_interactive(_FlagStream(True)), "yes")
        self.assertEqual(host.tty_interactive(_FlagStream(False)), "no")
        self.assertEqual(host.tty_interactive(_FlagStream(None)), "no")
        for label in (
            "PID:",
            "Cache folder used:",
            "Cache folder (preferred):",
            "Cache folder (1st fallback):",
            "Cache folder (2nd fallback):",
            "Persistence storage:",
            "TTY / Interactive:",
        ):
            self.assertIn(label, page)

    def test_cache_used_follows_shm_then_tmp_then_home(self):
        """TP-ABOUT-14: used follows /dev/shm, then /tmp, then the 2nd fallback."""
        from VideoSpeed.check_system import CheckSystem

        host = CheckSystem(app_name=Cli.APP_NAME, version=Cli._PKG_VERSION, console_name=Cli.CONSOLE_NAME)
        home = tempfile.mkdtemp(prefix="vs-about-home-")
        saved = {
            key: os.environ.get(key)
            for key in ("HOME", "USER", "USERNAME")
        }
        real_isdir = os.path.isdir
        real_getuser = None
        try:
            import getpass

            real_getuser = getpass.getuser
            os.environ["HOME"] = home
            os.environ["USER"] = "demo"
            os.environ["USERNAME"] = "demo"

            def _isdir_shm(path):
                if path == "/dev/shm":
                    return True
                if path == "/tmp":
                    return False
                return real_isdir(path)

            os.path.isdir = _isdir_shm
            self.assertEqual(host.cache_folder_used(), host.cache_folder_preferred())
            preferred = host.cache_folder_preferred()
            self.assertTrue(
                preferred.endswith(
                    "cache-VideoSpeed-demo-{}".format(host.process_id())
                )
            )

            def _isdir_tmp(path):
                if path == "/dev/shm":
                    return False
                if path == "/tmp":
                    return True
                return real_isdir(path)

            os.path.isdir = _isdir_tmp
            self.assertEqual(
                host.cache_folder_used(), host.cache_folder_first_fallback()
            )

            def _isdir_neither(path):
                if path in ("/dev/shm", "/tmp"):
                    return False
                return real_isdir(path)

            os.path.isdir = _isdir_neither
            second = host.cache_folder_second_fallback()
            self.assertEqual(host.cache_folder_used(), second)
            self.assertTrue(
                second.endswith(
                    "/.cache/cache-VideoSpeed-{}".format(host.process_id())
                )
            )
            self.assertNotIn("demo", os.path.basename(second))
            self.assertEqual(
                host.persistence_storage(),
                os.path.join(home, ".local", "VideoSpeed"),
            )
            self.assertFalse(os.path.exists(second))

            os.environ["USER"] = ""
            os.environ["USERNAME"] = ""
            getpass.getuser = lambda: ""
            bare = host.cache_folder_preferred()
            self.assertTrue(
                bare.endswith("cache-VideoSpeed-{}".format(host.process_id()))
            )
            self.assertNotIn("cache-VideoSpeed--", bare)

            os.environ["HOME"] = "   "
            getpass.getuser = real_getuser
            os.environ["USER"] = "demo"

            def _no_expand(path):
                return path

            real_expand = os.path.expanduser
            os.path.expanduser = _no_expand
            try:
                self.assertEqual(host.cache_folder_second_fallback(), "")
                self.assertEqual(host.persistence_storage(), "")
            finally:
                os.path.expanduser = real_expand
        finally:
            os.path.isdir = real_isdir
            if real_getuser is not None:
                import getpass

                getpass.getuser = real_getuser
            for key, value in saved.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value
            shutil.rmtree(home, ignore_errors=True)

    def test_tp_about_15_json_splits_the_page_and_the_object(self):
        """TP-ABOUT-15: about --json puts the page on stderr and one object on stdout."""
        import io
        import json
        from contextlib import redirect_stderr, redirect_stdout

        cli = self._cli()
        parent = tempfile.mkdtemp(prefix="videospeed_about_json_")
        self.addCleanup(shutil.rmtree, parent, ignore_errors=True)
        saved_debug = os.environ.get("DEBUG")
        os.environ["DEBUG"] = "1"

        class Tty(io.StringIO):
            def isatty(self):
                return True

        class Notty(io.StringIO):
            def isatty(self):
                return False

        try:
            out = Tty()
            err = io.StringIO()
            logd = os.path.join(parent, "logs-tty")
            with redirect_stdout(out), redirect_stderr(err):
                code = cli.main(
                    ["about", "--json"], log_basedir=parent, log_logdir=logd
                )
            self.assertEqual(code, 0)
            raw = out.getvalue()
            page = err.getvalue()
            obj = json.loads(raw)
            self.assertTrue(obj["ok"])
            self.assertEqual(obj["mode"], "noninteractive")
            self.assertEqual(obj["jobs"], [])
            self.assertNotIn("[CHECK SYSTEM]:", raw)
            self.assertNotIn("Domain:", raw)
            self.assertNotIn("Basic Usage:", raw)
            self.assertNotIn("Created directory:", raw)
            self.assertNotIn("instantiated", raw)
            self.assertIn("Domain:", page)
            self.assertIn("[CHECK SYSTEM]:", page)
            self.assertIn("Basic Usage:", page)
            self.assertIn("TTY / Interactive: yes", page)
            self.assertNotIn('"ok"', page)
            self.assertNotIn("Created directory:", page)
            self.assertNotIn("] pid:", page)

            out_file = Notty()
            err_file = io.StringIO()
            logd_file = os.path.join(parent, "logs-file")
            with redirect_stdout(out_file), redirect_stderr(err_file):
                code_file = cli.main(
                    ["about", "--json"],
                    log_basedir=parent,
                    log_logdir=logd_file,
                )
            self.assertEqual(code_file, 0)
            self.assertIn("TTY / Interactive: no", err_file.getvalue())
            filed = json.loads(out_file.getvalue())
            self.assertEqual(filed["mode"], "noninteractive")
            self.assertNotIn("[CHECK SYSTEM]:", out_file.getvalue())
        finally:
            if saved_debug is None:
                os.environ.pop("DEBUG", None)
            else:
                os.environ["DEBUG"] = saved_debug


class _FlagStream(object):
    """Stand-in stdout. isatty raises when flag is None."""

    def __init__(self, flag):
        self._flag = flag

    def isatty(self):
        if self._flag is None:
            raise OSError("no tty")
        return self._flag


if __name__ == "__main__":
    unittest.main()
