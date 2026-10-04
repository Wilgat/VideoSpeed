#!/usr/bin/env python
# =============================================================================
# VideoSpeed CLI — specialized from bootstrap interactive editor (cli.bootstrap-old)
# Domain: cut → speed/length → optional boomerang (MP4)
# Law keys: requirement-domain-videospeed, requirement-video-ffmpeg-pipeline,
#           requirement-python-cli-interface,
#           requirement-python-interactive-vs-noninteractive,
#           requirement-python-json-output,
#           requirement-python-tui,
#           requirement-python-oop,
#           requirement-python-about,
#           requirement-python-version, requirement-python-error-handling,
#           requirement-python-cli-logging,
#           requirement-runtime-prerequisites
# CIAO-Lite: Caution • Intentional • Anti-fragile • Over-protect
# This module defines class Cli and def main. Other jobs live in their own modules.
# =============================================================================
from __future__ import print_function, unicode_literals

import argparse
import sys
from pathlib import Path

# Version SSOT: requirement-python-version. No second triple and no fallback literal.
# The formatted triple equals __version__. That equality is a suite check
# (requirement-python-coding-style). Do not raise it when this module is imported.
from . import MAJOR_VERSION, MINOR_VERSION, PATCH_VERSION, __version__
from .about_page import AboutPage
from .check_system import CheckSystem
from .edit_walk import EditWalk
from .encoder import Encoder
from .file_stage import FileStage
from .media_info import MediaInfo
from .run_output import RunOutput
from .self_management import SelfManage
from .tui import Tui


class Cli:
    """Parser, dispatch, the product verbs, and the tty gates. One class in this file.

    Identity, verb lists, and length bounds are attributes of this class.
    Collaborators arrive through the constructor. def main stays beside this class.
    """

    # Formatted triple. Equality with __version__ is a suite check
    # (requirement-python-coding-style). Do not raise it here.
    _PKG_VERSION = "{0}.{1}.{2}".format(MAJOR_VERSION, MINOR_VERSION, PATCH_VERSION)
    APP_NAME = "VideoSpeed"
    CONSOLE_NAME = "video-speed"
    # Positional product verbs. Exit and ./build.sh tokens are not in this list.
    PRODUCT_VERBS = (
        "help",
        "version",
        "about",
        "hello",
        "edit",
        "list-mp4",
        "self-install",
        "version-check",
        "self-update",
        "self-uninstall",
    )
    LIFECYCLE_VERBS = (
        "version",
        "self-install",
        "version-check",
        "self-update",
        "self-uninstall",
    )
    AUTHOR_NAME = "Wilgat Wong"
    HOMEPAGE = "https://github.com/Wilgat/VideoSpeed"
    LAST_UPDATE = "2026-10-01"
    # requirement-domain-videospeed: about must not advertise a curl|sh channel.
    DOWNLOAD_URL = ""
    BASIC_USAGE = "video-speed --file clip.mp4 --start 0 --end 5"
    # Length percent bounds (domain / pipeline guidance made fail-closed)
    RATIO_MIN = 20.0
    RATIO_MAX = 200.0

    def __init__(self, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="Cli")
        self.app_name = Cli.APP_NAME
        self.version = Cli._PKG_VERSION
        self.output = RunOutput(Cli.APP_NAME, Cli._PKG_VERSION, logger=logger)
        self.stage = FileStage(logger=logger)
        self.media = MediaInfo(self.output, logger=logger)
        self.encoder = Encoder(
            self.output,
            self.media,
            self.stage,
            Cli.RATIO_MIN,
            Cli.RATIO_MAX,
            logger=logger,
        )
        self.about = AboutPage(
            CheckSystem(
                logger=logger,
                app_name=Cli.APP_NAME,
                version=Cli._PKG_VERSION,
                console_name=Cli.CONSOLE_NAME,
            ),
            Cli.APP_NAME,
            Cli._PKG_VERSION,
            MAJOR_VERSION,
            MINOR_VERSION,
            PATCH_VERSION,
            Cli.AUTHOR_NAME,
            Cli.LAST_UPDATE,
            Cli.HOMEPAGE,
            Cli.DOWNLOAD_URL,
            Cli.BASIC_USAGE,
            Cli.CONSOLE_NAME,
            logger=logger,
        )
        self.edit = EditWalk(
            self.output,
            self.encoder,
            self.media,
            Cli.RATIO_MIN,
            Cli.RATIO_MAX,
            logger=logger,
        )
        self.self_manage = SelfManage(Cli.APP_NAME, Cli._PKG_VERSION, logger=logger)
        self.tui = Tui(self, logger=logger)

    @staticmethod
    def stdin_is_tty():
        """General Purpose: Whether stdin can take interactive prompts."""
        try:
            return sys.stdin.isatty()
        except Exception:
            return False

    @staticmethod
    def stdout_is_tty():
        """General Purpose: Whether the text screen can be drawn on this stdout."""
        try:
            return sys.stdout.isatty()
        except Exception:
            return False

    def _verb_help(self, parser):
        """
        General Purpose: Same usage text as --help. Does not open the menu.
        Last updated: 2026-10-01
        """
        parser.print_help()
        return 0

    def _verb_page(self, text):
        """
        General Purpose: Print one page and do not ask for a folder or a file.
        Last updated: 2026-10-01
        """
        if self.output.json_mode:
            print(text, file=sys.stderr)
        else:
            print(text)
        return 0

    def _verb_about(self):
        """
        General Purpose: Show the about page. Job flags are ignored.
        Last updated: 2026-10-01
        """
        return self._verb_page(self.about.framework_about())

    def _verb_hello(self):
        """
        General Purpose: Show Hello. Job flags are ignored.
        Last updated: 2026-10-01
        """
        return self._verb_page(self.tui.framework_hello())

    def _unknown_verb(self, token):
        """
        General Purpose: Reject a positional token that is not a product verb.
        Last updated: 2026-10-01
        """
        names = ", ".join(Cli.PRODUCT_VERBS)
        message = "Unknown verb '{}'.".format(token)
        nxt = "video-speed help — verbs: {}".format(names)
        self.output._remember(message, nxt)
        self.output.out_err("ERROR: {}".format(message))
        self.output.out_err("   Next: {}".format(nxt))
        return 1

    def _print_mp4_list(self, folder):
        """
        General Purpose: Print the numbered MP4 list. Do not encode.
        Last updated: 2026-10-01
        """
        folder_path = Path(folder)
        if not folder_path.is_dir():
            self.output._remember("Not a directory: {}".format(folder))
            self.output.out_err("ERROR: Not a directory: {}".format(folder))
            return 1
        files = self.media.get_mp4_files(folder_path)
        if not files:
            self.output._remember("No MP4 files found!")
            self.output.out_err("No MP4 files found!")
            return 1
        lines = ["{:2d}. {}".format(i, item.name) for i, item in enumerate(files, 1)]
        stream = sys.stderr if self.output.json_mode else sys.stdout
        for line in lines:
            print(line, file=stream)
        return 0

    def _verb_list_mp4(self, args, logger):
        """
        General Purpose: List MP4 files and stop. Do not encode or pick a file.
        Last updated: 2026-10-01
        """
        if args.folder is None and args.file is not None:
            args.folder = str(Path(args.file).parent)
        if not self.stdin_is_tty():
            return self._print_mp4_list("." if args.folder is None else args.folder)
        if self.output.json_mode:
            if args.folder is None:
                self.output.json_walk = True
                raw = self.edit._prompt_line("Folder (Enter = current):")
                if raw is None:
                    return 0
                args.folder = raw.strip() or "."
            return self._print_mp4_list(args.folder)
        logger.quiet(True)
        return self.tui._open_direct_screen("list-mp4", args)

    def _verb_edit(self, args, logger):
        """
        General Purpose: One edit job, or the edit questions when a target is missing.
        Last updated: 2026-10-01
        """
        if args.file is not None and args.start is not None and args.end is not None:
            percent = 100.0 if args.percent is None else args.percent
            return self.encoder.batch_session(
                args.file, args.start, args.end, percent, args.boomerang
            )
        if not self.stdin_is_tty():
            self.output._remember(
                "Non-interactive job needs --file, --start, and --end.",
                "video-speed edit --file clip.mp4 --start 0 --end 5",
            )
            self.output.out_err(
                "ERROR: Non-interactive job needs --file, --start, and --end."
            )
            self.output.out_err("   Next: video-speed edit --file clip.mp4 --start 0 --end 5")
            return 1
        if self.output.json_mode:
            return self.edit._edit_json(args)
        logger.quiet(True)
        return self.tui._open_direct_screen("edit", args)

    def build_parser(self):
        """
        General Purpose: One optional product verb, plus the job flags.
        No verb in a terminal still starts the editor.
        Last updated: 2026-10-01
        """
        parser = argparse.ArgumentParser(
            prog=Cli.CONSOLE_NAME,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=(
                "{} — cut an MP4, change length/speed, optional boomerang.\n"
                "With no arguments in a terminal, starts the interactive editor.\n"
                "Product verbs: help, version, about, hello, edit, list-mp4,\n"
                "self-install, version-check, self-update, self-uninstall.\n"
                "help prints this usage. version prints the installed version.\n"
                "about and hello print a page and do not ask for a folder or a file.\n"
                "edit asks for a folder, then a file, when those are not already named.\n"
                "list-mp4 lists MP4 files and does not encode.\n"
                "version-check runs: python -m pip index versions VideoSpeed\n"
                "self-update runs: python -m pip install --upgrade VideoSpeed\n"
                "self-install runs: python -m pip install VideoSpeed\n"
                "self-uninstall runs: python -m pip uninstall -y VideoSpeed\n"
                "and needs --force. Empty arguments do not install or update.\n"
                "For scripts, pass --file, --start, and --end."
                .format(Cli.APP_NAME)
            ),
        )
        parser.add_argument(
            "verb",
            nargs="?",
            default=None,
            metavar="verb",
            help=(
                "Product verb: help, version, about, hello, edit, list-mp4, "
                "self-install, version-check, self-update, or self-uninstall"
            ),
        )
        parser.add_argument(
            "--version",
            action="version",
            version="{} {}".format(Cli.APP_NAME, Cli._PKG_VERSION),
        )
        parser.add_argument(
            "--file",
            help="MP4 path for a non-interactive job",
        )
        parser.add_argument(
            "--folder",
            help="Folder of MP4s (non-interactive list / empty check)",
        )
        parser.add_argument(
            "--start",
            type=float,
            help="Cut start seconds (non-interactive; with --file and --end)",
        )
        parser.add_argument(
            "--end",
            type=float,
            help="Cut end seconds (non-interactive; with --file and --start)",
        )
        parser.add_argument(
            "--percent",
            type=float,
            default=None,
            help="New length percent of the cut (default 100; allowed 20–200)",
        )
        parser.add_argument(
            "--boomerang",
            action="store_true",
            help="Append reverse after the forward clip (non-interactive)",
        )
        parser.add_argument(
            "--json",
            action="store_true",
            help=(
                "Quiet stdout and print one JSON object. "
                "Does not open the text menu."
            ),
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Confirm self-uninstall. Required on the command line.",
        )
        return parser

    @staticmethod
    def _opens_text_screen(argv):
        """
        General Purpose: Whether this argv draws the text screen.
        Last updated: 2026-10-01
        The real parser has not run yet. This walk only decides the debug
        mirror. --json, --help, and --version never draw that screen.
        """
        if "--json" in argv or "--help" in argv or "-h" in argv or "--version" in argv:
            return False
        if not Cli.stdin_is_tty() or not Cli.stdout_is_tty():
            return False
        verb = None
        has_file = False
        has_start = False
        has_end = False
        has_folder = False
        has_percent = False
        has_boomerang = False
        index = 0
        while index < len(argv):
            token = argv[index]
            if token == "--file" or token.startswith("--file="):
                has_file = True
                if token == "--file":
                    index += 1
            elif token == "--start" or token.startswith("--start="):
                has_start = True
                if token == "--start":
                    index += 1
            elif token == "--end" or token.startswith("--end="):
                has_end = True
                if token == "--end":
                    index += 1
            elif token == "--folder" or token.startswith("--folder="):
                has_folder = True
                if token == "--folder":
                    index += 1
            elif token == "--percent" or token.startswith("--percent="):
                has_percent = True
                if token == "--percent":
                    index += 1
            elif token == "--boomerang":
                has_boomerang = True
            elif not token.startswith("-") and verb is None:
                verb = token
            index += 1
        if verb in ("help", "about", "hello") or verb in Cli.LIFECYCLE_VERBS:
            return False
        if verb == "edit":
            return not (has_file and has_start and has_end)
        if verb == "list-mp4":
            return True
        if verb is not None:
            return False
        if has_file or has_start or has_end or has_folder:
            return False
        if has_percent or has_boomerang:
            return False
        return True

    def _dispatch(self, args, logger):
        """
        General Purpose: One product verb, one job, the menu, or a fail-closed stop.
        Last updated: 2026-10-01
        A product verb is decided before selectors and modifiers, so about and
        edit are not rejected for a lone --percent. No verb keeps the job path.
        """
        verb = args.verb
        if args.force and verb != "self-uninstall":
            self.output._remember(
                "--force is only for self-uninstall.",
                "video-speed self-uninstall --force",
            )
            self.output.out_err("ERROR: --force is only for self-uninstall.")
            self.output.out_err("   Next: video-speed self-uninstall --force")
            return 1
        if verb == "about":
            return self._verb_about()
        if verb == "hello":
            return self._verb_hello()
        if verb == "version":
            return self._verb_page(self.self_manage.local_version())
        if verb == "self-uninstall":
            if not args.force:
                self.output._remember(
                    "self-uninstall removes this package with pip.",
                    "video-speed self-uninstall --force",
                )
                self.output.out_err(
                    "ERROR: self-uninstall removes this package with pip."
                )
                self.output.out_err("   Next: video-speed self-uninstall --force")
                return 1
            return self.self_manage.emit(verb, json_mode=self.output.json_mode)
        if verb in ("version-check", "self-update", "self-install"):
            return self.self_manage.emit(verb, json_mode=self.output.json_mode)
        if verb == "edit":
            return self._verb_edit(args, logger)
        if verb == "list-mp4":
            return self._verb_list_mp4(args, logger)
        if verb is not None:
            return self._unknown_verb(verb)

        selectors = (
            args.file is not None
            or args.start is not None
            or args.end is not None
            or args.folder is not None
        )
        # requirement-python-interactive-vs-noninteractive: a modifier alone
        # must not fall through into the text menu.
        if (args.percent is not None or args.boomerang) and not selectors:
            self.output._remember(
                "--percent and --boomerang need --file, --start, and --end.",
                "video-speed --file clip.mp4 --start 0 --end 5",
            )
            self.output.out_err(
                "ERROR: --percent and --boomerang need --file, --start, and --end."
            )
            self.output.out_err("   Next: video-speed --file clip.mp4 --start 0 --end 5")
            return 1

        if selectors:
            if args.folder is not None:
                folder_path = Path(args.folder)
                if not folder_path.is_dir():
                    self.output._remember("Not a directory: {}".format(args.folder))
                    self.output.out_err("ERROR: Not a directory: {}".format(args.folder))
                    return 1
                files = self.media.get_mp4_files(folder_path)
                if not files:
                    self.output._remember("No MP4 files found!")
                    self.output.out_err("No MP4 files found!")
                    return 1
                if args.file is None:
                    message = (
                        "--folder listed {} MP4 file(s); also pass --file, "
                        "--start, and --end for a non-interactive job."
                        .format(len(files))
                    )
                    self.output._remember(message)
                    self.output.out_err("ERROR: {}".format(message))
                    return 1
            if args.file is None or args.start is None or args.end is None:
                self.output._remember(
                    "Non-interactive job needs --file, --start, and --end.",
                    "video-speed --file clip.mp4 --start 0 --end 5",
                )
                self.output.out_err(
                    "ERROR: Non-interactive job needs --file, --start, and --end."
                )
                self.output.out_err("   Next: video-speed --file clip.mp4 --start 0 --end 5")
                return 1
            percent = 100.0 if args.percent is None else args.percent
            return self.encoder.batch_session(
                args.file, args.start, args.end, percent, args.boomerang
            )

        if not self.stdin_is_tty():
            self.output._remember(
                "No terminal for prompts.",
                "pass --file, --start, and --end, or run in a terminal.",
            )
            self.output.out_err(
                "ERROR: No terminal for prompts. "
                "Next: pass --file, --start, and --end, or run in a terminal."
            )
            return 1

        if self.output.json_mode:
            return self.edit._edit_json()

        # requirement-python-cli-logging: keep the console mirror off the frame.
        logger.quiet(True)
        action = self.tui.open_text_menu()
        if action == "missing":
            return 1
        return 0

    def run(self, argv=None, log_basedir="", log_logdir="", logger=None):
        """One job. def main already wrote ChronicleLogger(...) and passed it in."""
        self.output._json_reset()
        if argv is None:
            argv = sys.argv[1:]
        argv = list(argv)
        if logger is None:
            logger = self.logger

        parser = self.build_parser()
        args = parser.parse_args(argv)
        # help stays human usage text, including when --json is also set.
        if args.verb == "help":
            return self._verb_help(parser)
        if args.json:
            self.output.json_mode = True

        code = self._dispatch(args, logger)
        if not args.json:
            return code
        mode = "interactive" if self.output.json_walk else "noninteractive"
        code = self.output._emit_json(mode, code)
        self.output.json_mode = False
        return code


def main(argv=None, log_basedir="", log_logdir=""):
    """
    General Purpose: Package entry for video-speed / python -m VideoSpeed.
    No arguments in a terminal → interactive editor.
    No arguments without a terminal → fail closed (ask for --file/--start/--end).

    requirement-python-cli-interface and requirement-python-cli-logging:
    def main writes ChronicleLogger(...). is_quiet=True when --json or the
    text screen is already known. The library stores that flag before it
    creates the log folder. Then logName, baseDir, and logDir, then the
    debug identity, then Cli(logger), then the argument parser. A non-TUI,
    non-JSON run leaves the console mirror on. The text screen and --json
    keep that mirror off. log_basedir and log_logdir stay empty in normal
    use so ChronicleLogger chooses the folder. Tests pass a temporary folder.
    """
    if argv is None:
        argv = sys.argv[1:]
    argv = list(argv)
    try:
        from ChronicleLogger import ChronicleLogger
    except ImportError:
        # This line cannot go through log_message. No product object exists yet.
        print("ERROR: ChronicleLogger is not installed.", file=sys.stderr)
        print("   Next: pip install 'ChronicleLogger>=1.3.1'", file=sys.stderr)
        return 1

    json_or_screen = "--json" in argv or Cli._opens_text_screen(argv)
    logger = ChronicleLogger(
        logname="VideoSpeed",
        basedir=log_basedir or "",
        logdir=log_logdir or "",
        is_quiet=json_or_screen,
    )
    appname = logger.logName()
    basedir = logger.baseDir()
    logger.logDir()
    if logger.isDebug():
        logger.log_message(
            "{0} v{1}.{2}.{3} ({4})".format(
                appname,
                MAJOR_VERSION,
                MINOR_VERSION,
                PATCH_VERSION,
                __file__,
            ),
            component="main",
        )
        logger.log_message(
            "Using {0}".format(ChronicleLogger.class_version()),
            component="main",
        )
        logger.log_message(
            "Base {0}".format(basedir),
            level="DEBUG",
            component="main",
        )
        logger.log_message(
            "debug mode",
            component="main",
        )
    app = Cli(logger)
    return app.run(argv, logger=logger)


if __name__ == "__main__":
    sys.exit(main() or 0)
