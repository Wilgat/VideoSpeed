# TP-CLI — CLI surface (requirement-python-cli-interface)
# TP-MODE — menu walk vs one job (requirement-python-interactive-vs-noninteractive)
from __future__ import print_function, unicode_literals

import io
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
ENV = os.environ.copy()
env_pp = ENV.get("PYTHONPATH", "")
ENV["PYTHONPATH"] = str(ROOT / "src") + ((":" + env_pp) if env_pp else "")


def _run(args, stdin_devnull=True):
    kw = dict(
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=ENV,
        cwd=str(ROOT),
    )
    if stdin_devnull:
        kw["stdin"] = subprocess.DEVNULL
    return subprocess.run(
        [sys.executable, "-m", "VideoSpeed"] + args,
        **kw
    )


class TestCli(unittest.TestCase):
    def test_tp_cli_01_version_exit_0(self):
        """TP-CLI-01: python -m VideoSpeed --version exits 0, prints version."""
        import VideoSpeed

        proc = _run(["--version"])
        self.assertEqual(proc.returncode, 0, proc.stderr.decode("utf-8", "replace"))
        out = (proc.stdout + proc.stderr).decode("utf-8", "replace")
        self.assertIn(VideoSpeed.__version__, out)
        self.assertIn("VideoSpeed", out)

    def test_tp_cli_02_help_lists_usage(self):
        """TP-CLI-02: --help lists usage and batch flags."""
        proc = _run(["--help"])
        self.assertEqual(proc.returncode, 0, proc.stderr.decode("utf-8", "replace"))
        out = proc.stdout.decode("utf-8", "replace")
        self.assertIn("--file", out)
        self.assertIn("--start", out)
        self.assertIn("--end", out)
        self.assertIn("--percent", out)
        self.assertIn("--boomerang", out)
        self.assertIn("--json", out)

    def test_tp_cli_04_empty_folder_no_mp4(self):
        """TP-CLI-04: No MP4 in folder → clear message, non-success."""
        tmp = tempfile.mkdtemp(prefix="videospeed_empty_")
        try:
            proc = _run(["--folder", tmp])
            self.assertNotEqual(proc.returncode, 0)
            err = proc.stderr.decode("utf-8", "replace")
            self.assertIn("No MP4 files found", err)
        finally:
            os.rmdir(tmp)

    def test_tp_cli_06_batch_requires_file_start_end(self):
        """TP-CLI-06: --file without start/end fails closed (no hang)."""
        proc = _run(["--file", "/tmp/does-not-exist-videospeed.mp4"])
        self.assertNotEqual(proc.returncode, 0)
        err = proc.stderr.decode("utf-8", "replace")
        self.assertIn("--file", err)
        self.assertIn("--start", err)

    def test_tp_cli_06_missing_file(self):
        """TP-CLI-06: --file missing path fails closed with next-step text."""
        proc = _run([
            "--file", str(ROOT / "no-such-clip.mp4"),
            "--start", "0",
            "--end", "1",
        ])
        self.assertNotEqual(proc.returncode, 0)
        err = proc.stderr.decode("utf-8", "replace")
        self.assertIn("File not found", err)
        self.assertIn("Next:", err)

    def test_tp_mode_03_no_tty_empty_argv_fail_closed(self):
        """TP-MODE-03: empty argv with no terminal exits 1 and names a next step."""
        proc = _run([])
        self.assertEqual(proc.returncode, 1)
        err = proc.stderr.decode("utf-8", "replace")
        self.assertIn("No terminal for prompts", err)
        self.assertIn("--file", err)
        self.assertIn("--start", err)
        self.assertIn("--end", err)
        self.assertIn("Next:", err)

    def test_tp_mode_01_selector_does_not_open_menu(self):
        """TP-MODE-01: any selector stays off the menu, even when stdin is a terminal."""
        from VideoSpeed import cli

        self.assertTrue(Path(cli.__file__).resolve().is_relative_to(ROOT))
        opened = []
        from VideoSpeed.tui import Tui
        saved_open = Tui.open_text_menu
        saved_in = cli.Cli.stdin_is_tty
        Tui.open_text_menu = lambda self: opened.append("open") or None
        cli.Cli.stdin_is_tty = lambda self: True
        try:
            cases = (
                ["--file", "clip.mp4"],
                ["--start", "0"],
                ["--end", "1"],
                ["--folder", "/tmp/does-not-exist-videospeed-mode"],
            )
            for argv in cases:
                err = io.StringIO()
                with redirect_stderr(err):
                    code = cli.main(argv)
                self.assertNotEqual(code, 0, argv)
                self.assertEqual(opened, [], argv)
                self.assertIn("ERROR:", err.getvalue(), argv)
        finally:
            Tui.open_text_menu = saved_open
            cli.Cli.stdin_is_tty = saved_in

    def test_tp_mode_02_modifier_alone_fail_closed(self):
        """TP-MODE-02: lone --percent or --boomerang exits 1 and does not open the menu."""
        from VideoSpeed import cli

        opened = []
        from VideoSpeed.tui import Tui
        saved_open = Tui.open_text_menu
        saved_in = cli.Cli.stdin_is_tty
        Tui.open_text_menu = lambda self: opened.append("open") or None
        cli.Cli.stdin_is_tty = lambda self: True
        try:
            for argv in (["--percent", "80"], ["--boomerang"]):
                err = io.StringIO()
                with redirect_stderr(err):
                    code = cli.main(argv)
                text = err.getvalue()
                self.assertEqual(code, 1, argv)
                self.assertEqual(opened, [], argv)
                self.assertIn("--file", text, argv)
                self.assertIn("--start", text, argv)
                self.assertIn("--end", text, argv)
                self.assertIn("Next:", text, argv)
        finally:
            Tui.open_text_menu = saved_open
            cli.Cli.stdin_is_tty = saved_in

    def test_tp_cli_07_help_and_unknown_verb(self):
        """TP-CLI-07: help lists the five verbs; an unknown verb exits 1."""
        proc = _run(["help"])
        self.assertEqual(proc.returncode, 0, proc.stderr.decode("utf-8", "replace"))
        out = proc.stdout.decode("utf-8", "replace")
        for name in ("help", "about", "hello", "edit", "list-mp4"):
            self.assertIn(name, out)
        self.assertIn("--file", out)
        self.assertIn("--start", out)
        self.assertIn("--end", out)
        self.assertNotIn("Folder (Enter", out)

        flagged = _run(["--help"])
        help_out = flagged.stdout.decode("utf-8", "replace")
        self.assertEqual(flagged.returncode, 0, flagged.stderr.decode())
        for name in ("help", "about", "hello", "edit", "list-mp4"):
            self.assertIn(name, help_out)

        # help stays human text even with --json.
        coated = _run(["help", "--json"])
        coated_out = coated.stdout.decode("utf-8", "replace")
        self.assertEqual(coated.returncode, 0, coated.stderr.decode())
        self.assertIn("list-mp4", coated_out)
        self.assertNotIn('"ok"', coated_out)

        from VideoSpeed import cli

        opened = []
        from VideoSpeed.tui import Tui
        saved_open = Tui.open_text_menu
        saved_in = cli.Cli.stdin_is_tty
        Tui.open_text_menu = lambda self: opened.append("open") or None
        cli.Cli.stdin_is_tty = lambda self: True
        try:
            for token in ("setup", "Exit", "exit", "version", "test", "clean"):
                proc = _run([token])
                err = proc.stderr.decode("utf-8", "replace")
                self.assertEqual(proc.returncode, 1, err)
                self.assertIn("Unknown verb", err)
                self.assertIn("Next:", err)
                for name in ("help", "about", "hello", "edit", "list-mp4"):
                    self.assertIn(name, err, token)
                self.assertNotIn("main menu", proc.stdout.decode("utf-8", "replace"))
                err_buf = io.StringIO()
                with redirect_stderr(err_buf):
                    code = cli.main([token])
                self.assertEqual(code, 1, token)
                self.assertEqual(opened, [], token)
        finally:
            Tui.open_text_menu = saved_open
            cli.Cli.stdin_is_tty = saved_in

        proc = _run(["--json", "setup"])
        raw = proc.stdout.decode("utf-8")
        doc = json_loads(raw)
        self.assertEqual(proc.returncode, 1)
        self.assertFalse(doc["ok"])
        self.assertEqual(doc["mode"], "noninteractive")
        self.assertEqual(doc["jobs"], [])
        self.assertIn("setup", doc["error"])
        self.assertIn("list-mp4", doc["next"])
        self.assertIn("Unknown verb", proc.stderr.decode("utf-8", "replace"))

    def test_tp_mode_06_edit_without_terminal_does_not_prompt(self):
        """TP-MODE-06: edit with no terminal and no full job exits 1 and does not prompt."""
        proc = _run(["edit"])
        err = proc.stderr.decode("utf-8", "replace")
        out = proc.stdout.decode("utf-8", "replace")
        self.assertEqual(proc.returncode, 1, err)
        self.assertIn("--file", err)
        self.assertIn("--start", err)
        self.assertIn("--end", err)
        self.assertIn("Next:", err)
        self.assertNotIn("Folder (Enter", err)
        self.assertNotIn("Folder (Enter", out)
        self.assertNotIn("Choose video", err + out)

        partial = _run(["edit", "--percent", "50"])
        text = (partial.stdout + partial.stderr).decode("utf-8", "replace")
        self.assertEqual(partial.returncode, 1, text)
        self.assertNotIn("Folder (Enter", text)
        self.assertIn("--file", text)

    def test_tp_mode_07_list_mp4_without_terminal(self):
        """TP-MODE-07: list-mp4 with no terminal lists a folder and does not prompt or encode."""
        empty = tempfile.mkdtemp(prefix="videospeed_list_")
        filled = tempfile.mkdtemp(prefix="videospeed_list_")
        clip = Path(filled) / "clip.mp4"
        try:
            clip.write_bytes(b"")
            missing = _run(["list-mp4", "--folder", empty])
            err = missing.stderr.decode("utf-8", "replace")
            self.assertEqual(missing.returncode, 1, err)
            self.assertIn("No MP4 files found", err)
            self.assertNotIn("Folder (Enter", err)
            self.assertNotIn("Processing", err)

            listed = _run(["list-mp4", "--folder", filled])
            out = listed.stdout.decode("utf-8", "replace")
            err = listed.stderr.decode("utf-8", "replace")
            self.assertEqual(listed.returncode, 0, err)
            self.assertIn("clip.mp4", out)
            self.assertNotIn("Folder (Enter", out + err)
            self.assertNotIn("Choose video", out + err)
            self.assertNotIn("Processing", out + err)

            parent = _run([
                "list-mp4",
                "--file", str(clip),
                "--start", "0",
                "--end", "1",
            ])
            body = (parent.stdout + parent.stderr).decode("utf-8", "replace")
            self.assertEqual(parent.returncode, 0, body)
            self.assertIn("clip.mp4", parent.stdout.decode("utf-8", "replace"))
            self.assertNotIn("Processing", body)
            self.assertNotIn("File not found", body)
            self.assertNotIn("Folder (Enter", body)
        finally:
            if clip.exists():
                clip.unlink()
            os.rmdir(filled)
            os.rmdir(empty)

    def test_tp_mode_08_pages_do_not_ask(self):
        """TP-MODE-08: about, help, and hello do not ask for a folder or a file."""
        hello = _run(["hello"])
        self.assertEqual(hello.returncode, 0, hello.stderr.decode())
        self.assertIn("Hello.", hello.stdout.decode("utf-8", "replace"))
        self.assertNotIn("Folder (Enter", (hello.stdout + hello.stderr).decode())

        about = _run(["about", "--percent", "50", "--file", "clip.mp4"])
        about_text = (about.stdout + about.stderr).decode("utf-8", "replace")
        self.assertEqual(about.returncode, 0, about_text)
        self.assertIn("Domain:", about.stdout.decode("utf-8", "replace"))
        self.assertNotIn("Folder (Enter", about_text)
        self.assertNotIn("Choose video", about_text)
        self.assertNotIn("Processing", about_text)

        coated = _run(["--json", "hello"])
        raw = coated.stdout.decode("utf-8")
        doc = json_loads(raw)
        self.assertEqual(coated.returncode, 0, coated.stderr.decode())
        self.assertTrue(doc["ok"])
        self.assertEqual(doc["mode"], "noninteractive")
        self.assertEqual(doc["jobs"], [])
        self.assertIn("Hello.", coated.stderr.decode("utf-8", "replace"))
        self.assertNotIn("Folder (Enter", coated.stderr.decode())

        from VideoSpeed import cli

        opened = []
        from VideoSpeed.tui import Tui
        saved_open = Tui.open_text_menu
        saved_in = cli.Cli.stdin_is_tty
        saved_out = cli.Cli.stdout_is_tty
        Tui.open_text_menu = lambda self: opened.append("open") or None
        cli.Cli.stdin_is_tty = lambda self: True
        cli.Cli.stdout_is_tty = lambda self: True
        try:
            for argv in (["about"], ["hello"], ["help"], ["about", "--boomerang"]):
                buf = io.StringIO()
                err = io.StringIO()
                with redirect_stdout(buf), redirect_stderr(err):
                    code = cli.main(argv)
                self.assertEqual(code, 0, argv)
                self.assertNotIn("Folder (Enter", err.getvalue() + buf.getvalue(), argv)
            self.assertEqual(opened, [])
        finally:
            Tui.open_text_menu = saved_open
            cli.Cli.stdin_is_tty = saved_in
            cli.Cli.stdout_is_tty = saved_out

    def test_tp_mode_05_edit_json_and_complete_job(self):
        """TP-MODE-05 coat: edit --json asks on stderr; a full job does not open the menu."""
        from VideoSpeed import cli

        opened = []
        from VideoSpeed.tui import Tui
        saved_open = Tui.open_text_menu
        saved_in = cli.Cli.stdin_is_tty
        saved_out = cli.Cli.stdout_is_tty
        from VideoSpeed.encoder import Encoder
        saved_ff = Encoder.ensure_ffmpeg
        saved_stdin = sys.stdin
        Tui.open_text_menu = lambda self: opened.append("open") or None
        cli.Cli.stdin_is_tty = lambda self: True
        cli.Cli.stdout_is_tty = lambda self: True
        Encoder.ensure_ffmpeg = lambda self: True
        sys.stdin = io.StringIO("")
        out = io.StringIO()
        err = io.StringIO()
        try:
            with redirect_stdout(out), redirect_stderr(err):
                code = cli.main(["--json", "edit"])
        finally:
            Tui.open_text_menu = saved_open
            cli.Cli.stdin_is_tty = saved_in
            cli.Cli.stdout_is_tty = saved_out
            Encoder.ensure_ffmpeg = saved_ff
            sys.stdin = saved_stdin
        raw = out.getvalue()
        doc = json_loads(raw)
        self.assertEqual(code, 0, err.getvalue())
        self.assertEqual(doc["mode"], "interactive")
        self.assertEqual(doc["jobs"], [])
        self.assertEqual(opened, [])
        self.assertIn("Folder (Enter = current):", err.getvalue())
        self.assertNotIn("Folder (Enter", raw)

        opened.clear()
        Tui.open_text_menu = lambda self: opened.append("open") or None
        cli.Cli.stdin_is_tty = lambda self: True
        try:
            err = io.StringIO()
            with redirect_stderr(err):
                code = cli.main([
                    "edit",
                    "--file", "no-such-videospeed-clip.mp4",
                    "--start", "0",
                    "--end", "1",
                ])
            self.assertEqual(code, 1)
            self.assertEqual(opened, [])
            self.assertIn("File not found", err.getvalue())
            self.assertNotIn("Folder (Enter", err.getvalue())
        finally:
            Tui.open_text_menu = saved_open
            cli.Cli.stdin_is_tty = saved_in

    def test_tp_oop_04_cli_is_the_entry_class(self):
        """TP-OOP-04: cli.py is class Cli plus def main. Other jobs are not functions there."""
        import inspect

        from VideoSpeed.about_page import AboutPage
        from VideoSpeed.cli import Cli, main
        from VideoSpeed.edit_walk import EditWalk
        from VideoSpeed.encoder import Encoder
        from VideoSpeed.file_stage import FileStage
        from VideoSpeed.media_info import MediaInfo
        from VideoSpeed.run_output import RunOutput

        self.assertTrue(inspect.isclass(Cli))
        self.assertTrue(inspect.isfunction(main))
        self.assertEqual(str(inspect.signature(main)), "(argv=None, log_basedir='', log_logdir='')")
        ship = (ROOT / "src" / "VideoSpeed" / "cli.py").read_text(encoding="utf-8")
        self.assertIn("class Cli", ship)
        self.assertIn("def main(", ship)
        self.assertEqual(ship.count("\nclass "), 1)
        homes = (
            (Encoder, "encoder.py", (
                "ensure_ffmpeg", "run_ffmpeg", "_restore_text_screen", "cut_clip",
                "_atempo_filters", "speed_change", "add_boomerang", "process_job",
                "batch_session", "build_output_name", "valid_cut_range",
                "valid_percent", "_length_unchanged",
            )),
            (FileStage, "file_stage.py", (
                "staging_dir_for", "make_temp_path", "promote_file",
            )),
            (MediaInfo, "media_info.py", (
                "get_mp4_files", "get_duration_cv2", "format_time",
            )),
            (AboutPage, "about_page.py", (
                "framework_about", "about_box_lines", "install_kind",
                "install_sentence", "_is_source_checkout",
            )),
            (EditWalk, "edit_walk.py", (
                "_edit_json", "_prompt_line", "_prompt_float", "_prompt_yes_no",
                "_err_line", "run_screen",
            )),
            (RunOutput, "run_output.py", (
                "out_info", "out_err", "_json_reset", "_remember", "_remember_job",
                "_emit_json", "_call_sunk", "_collect_lines",
            )),
        )
        for cls, filename, names in homes:
            self.assertEqual(Path(inspect.getfile(cls)).name, filename)
            for name in names:
                self.assertTrue(inspect.isfunction(cls.__dict__[name]), name)
                self.assertNotIn("\ndef {}(".format(name), "\n" + ship)
        for name in (
            "build_parser", "_dispatch", "_start_logger", "_verb_help",
            "_verb_about", "_verb_hello", "_verb_edit", "_verb_list_mp4",
            "_unknown_verb", "stdin_is_tty", "stdout_is_tty",
        ):
            self.assertTrue(inspect.isfunction(Cli.__dict__[name]), name)


def json_loads(raw):
    import json
    return json.loads(raw)


if __name__ == "__main__":
    unittest.main()
