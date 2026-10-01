# TP-BUILD — maintainer verbs (requirement-python-build-script)
from __future__ import print_function, unicode_literals

import os
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

OPERATIONAL = (
    "help",
    "version",
    "setup",
    "clean",
    "build",
    "upload",
    "git",
    "tag",
    "release",
    "all",
    "test-install",
)


def _run(args, stdin=subprocess.DEVNULL, env=None):
    return subprocess.run(
        [str(ROOT / "build.sh")] + args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=stdin,
        cwd=str(ROOT),
        check=False,
        env=env,
    )


def _project_identity():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        data = tomllib.load(handle)
    project = data["project"]
    scripts = tuple(project.get("scripts", {}).keys())
    return project["name"], scripts


def _between(script, start_token, end_token):
    start = script.index(start_token)
    end = script.index(end_token, start)
    return script[start:end]


def _write_fake_python(directory):
    path = Path(directory) / "python3"
    path.write_text(
        "#!" + sys.executable + "\n"
        "import os, sys\n"
        "log = os.environ.get('VS_FAKE_PY_LOG', '')\n"
        "data = ''\n"
        "try:\n"
        "    if not sys.stdin.isatty():\n"
        "        data = sys.stdin.read()\n"
        "except Exception:\n"
        "    data = ''\n"
        "argv = sys.argv[1:]\n"
        "if log:\n"
        "    with open(log, 'a', encoding='utf-8') as handle:\n"
        "        handle.write('ARGV ' + ' '.join(argv) + '\\n')\n"
        "if 'tomllib' in data or 'pyproject.toml' in data:\n"
        "    if os.environ.get('VS_FAKE_NAME_MODE') == 'fail':\n"
        "        sys.exit(1)\n"
        "    sys.stdout.write('FromPyproject\\n')\n"
        "    sys.exit(0)\n"
        "if '-m' in argv and 'pip' in argv:\n"
        "    if 'show' in argv and os.environ.get('VS_FAKE_SHOW') == 'no':\n"
        "        sys.exit(1)\n"
        "    if 'uninstall' in argv and os.environ.get('VS_FAKE_UNINSTALL') == 'fail':\n"
        "        sys.exit(1)\n"
        "    if (\n"
        "        'install' in argv\n"
        "        and 'uninstall' not in argv\n"
        "        and os.environ.get('VS_FAKE_INSTALL') == 'fail'\n"
        "    ):\n"
        "        sys.exit(1)\n"
        "    sys.exit(0)\n"
        "sys.exit(1)\n"
    )
    path.chmod(0o755)
    return path


def _fake_env(log_path, directory, **extra):
    env = os.environ.copy()
    env["PATH"] = str(directory) + os.pathsep + env.get("PATH", "")
    env["VS_FAKE_PY_LOG"] = str(log_path)
    env.update(extra)
    return env


def _pip_lines(log_path):
    text = Path(log_path).read_text(encoding="utf-8") if Path(log_path).is_file() else ""
    return [line for line in text.splitlines() if " -m pip " in line]


class TestBuild(unittest.TestCase):
    def test_tp_build_01_help_lists_verbs(self):
        """TP-BUILD-01: help and empty argv exit 0 and separate the test verb."""
        for args in ([], ["help"], ["-h"], ["--help"]):
            proc = _run(args)
            text = (proc.stdout + proc.stderr).decode("utf-8", "replace")
            self.assertEqual(proc.returncode, 0, text)
            self.assertLess(text.index("Operational commands:"), text.index("Test command:"))
            for verb in OPERATIONAL:
                self.assertIn(verb, text.split("Test command:", 1)[0], args)
            test_part = text.split("Test command:", 1)[1].split("Examples:", 1)[0]
            self.assertIn("\n  test ", test_part)
            self.assertNotIn("test-install", test_part)
            self.assertIn("tests/run.sh", text)
            self.assertNotIn("pytest", text)
            self.assertNotIn("Unknown command", text)

    def test_tp_build_02_unknown_exits_1(self):
        """TP-BUILD-02: an unknown verb exits 1 and names the error."""
        proc = _run(["no-such-verb"])
        err = proc.stderr.decode("utf-8", "replace")
        self.assertEqual(proc.returncode, 1, err)
        self.assertIn("Unknown command", err)
        self.assertIn("no-such-verb", err)

    def test_tp_build_03_version_matches_package(self):
        """TP-BUILD-03: version prints the checkout package version."""
        import VideoSpeed

        proc = _run(["version"])
        text = (proc.stdout + proc.stderr).decode("utf-8", "replace")
        self.assertEqual(proc.returncode, 0, text)
        self.assertIn(VideoSpeed.__version__, text)
        self.assertNotIn("unknown", text.lower())

    def test_tp_build_04_test_rejects_extra_args(self):
        """TP-BUILD-04: extra test arguments exit 1 and do not start the suite."""
        script = (ROOT / "build.sh").read_text(encoding="utf-8")
        self.assertIn("./tests/run.sh", script)
        self.assertNotIn("python3 -m pytest", script)
        self.assertNotIn("command -v pytest", script)
        proc = _run(["test", "-k", "nope"])
        text = (proc.stdout + proc.stderr).decode("utf-8", "replace")
        self.assertEqual(proc.returncode, 1, text)
        self.assertIn("no extra arguments", text)
        self.assertIn("Next:", text)
        self.assertNotIn("Ran ", text)

    def test_tp_build_06_test_install_reads_project_name(self):
        """TP-BUILD-06: test-install uninstalls then installs the name from metadata."""
        script = (ROOT / "build.sh").read_text(encoding="utf-8")
        project_name, script_names = _project_identity()
        reader = _between(script, "read_project_name()", "do_test_install()")
        installer = _between(script, "do_test_install()", "cmd=${1:-}")
        for token in (project_name,) + script_names:
            self.assertNotIn(token, reader)
            self.assertNotIn(token, installer)
        self.assertIn("tomllib", reader)
        self.assertIn("pyproject.toml", reader)
        self.assertIn("pip uninstall", installer)
        self.assertIn("pip install", installer)
        self.assertIn('"$ROOT"', installer)
        self.assertNotIn("setup.sh", installer)

        marker = reader.index("<<'PY'")
        body = reader[reader.index("\n", marker) + 1:]
        body = body[: body.index("\nPY")]
        proc = subprocess.run(
            [sys.executable, "-", str(ROOT)],
            input=body.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr.decode("utf-8", "replace"))
        self.assertEqual(proc.stdout.decode("utf-8"), project_name)

        with tempfile.TemporaryDirectory() as tmp:
            _write_fake_python(tmp)
            log = Path(tmp) / "log"
            proc = _run(["test-install"], env=_fake_env(log, tmp))
            text = (proc.stdout + proc.stderr).decode("utf-8", "replace")
            self.assertEqual(proc.returncode, 0, text)
            pip = _pip_lines(log)
            self.assertEqual(len(pip), 3, pip)
            self.assertIn(" show ", pip[0])
            self.assertIn("FromPyproject", pip[0])
            self.assertIn(" uninstall ", pip[1])
            self.assertIn("-y", pip[1])
            self.assertIn("FromPyproject", pip[1])
            self.assertIn(" install ", pip[2])
            self.assertIn(str(ROOT), pip[2])
            self.assertNotIn(project_name, pip[0])
            self.assertNotIn(project_name, pip[1])
            self.assertIn("Removing previous install of FromPyproject", text)

            log.write_text("")
            proc = _run(
                ["test-install"],
                env=_fake_env(log, tmp, VS_FAKE_SHOW="no"),
            )
            text = (proc.stdout + proc.stderr).decode("utf-8", "replace")
            self.assertEqual(proc.returncode, 0, text)
            pip = _pip_lines(log)
            self.assertEqual(len(pip), 2, pip)
            self.assertIn(" show ", pip[0])
            self.assertNotIn(" uninstall ", pip[0])
            self.assertIn(" install ", pip[1])
            self.assertNotIn(" uninstall ", " ".join(pip[1:]))

            log.write_text("")
            proc = _run(
                ["test-install"],
                env=_fake_env(log, tmp, VS_FAKE_UNINSTALL="fail"),
            )
            text = (proc.stdout + proc.stderr).decode("utf-8", "replace")
            self.assertEqual(proc.returncode, 1, text)
            self.assertIn("Could not remove", text)
            pip = _pip_lines(log)
            self.assertTrue(any(" uninstall " in line for line in pip), pip)
            self.assertFalse(any(" install " in line for line in pip), pip)

            log.write_text("")
            proc = _run(
                ["test-install"],
                env=_fake_env(log, tmp, VS_FAKE_NAME_MODE="fail"),
            )
            text = (proc.stdout + proc.stderr).decode("utf-8", "replace")
            self.assertEqual(proc.returncode, 1, text)
            self.assertIn("pyproject.toml", text)
            self.assertIn("Next:", text)
            self.assertEqual(_pip_lines(log), [])

            log.write_text("")
            proc = _run(["test-install", "--user"], env=_fake_env(log, tmp))
            text = (proc.stdout + proc.stderr).decode("utf-8", "replace")
            self.assertEqual(proc.returncode, 1, text)
            self.assertIn("no extra arguments", text)
            self.assertEqual(_pip_lines(log), [])


if __name__ == "__main__":
    unittest.main()
