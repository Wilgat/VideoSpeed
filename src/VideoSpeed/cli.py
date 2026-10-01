#!/usr/bin/env python
# =============================================================================
# VideoSpeed CLI — specialized from bootstrap interactive editor (cli.bootstrap-old)
# Domain: cut → speed/length → optional boomerang (MP4)
# Law keys: requirement-domain-videospeed, requirement-video-ffmpeg-pipeline,
#           requirement-python-cli-interface,
#           requirement-python-interactive-vs-noninteractive,
#           requirement-python-json-output,
#           requirement-python-tui,
#           requirement-python-about,
#           requirement-python-version, requirement-python-error-handling,
#           requirement-python-cli-logging,
#           requirement-runtime-prerequisites
# CIAO-Lite: Caution • Intentional • Anti-fragile • Over-protect
# =============================================================================
from __future__ import print_function, unicode_literals

import argparse
import datetime
import json
import os
import platform
import shutil
import subprocess
import sys
import sysconfig
import tempfile
from pathlib import Path

# Version SSOT: requirement-python-version. No second triple and no fallback literal.
# The formatted triple equals __version__. That equality is a suite check
# (requirement-python-coding-style). Do not raise it when this module is imported.
from . import MAJOR_VERSION, MINOR_VERSION, PATCH_VERSION, __version__
from .menu import MENU_ROWS

_PKG_VERSION = "{0}.{1}.{2}".format(MAJOR_VERSION, MINOR_VERSION, PATCH_VERSION)

APP_NAME = "VideoSpeed"
CONSOLE_NAME = "video-speed"
# Positional product verbs. Exit and ./build.sh tokens are not in this list.
PRODUCT_VERBS = ("help", "about", "hello", "edit", "list-mp4")
AUTHOR_NAME = "Wilgat Wong"
HOMEPAGE = "https://github.com/Wilgat/VideoSpeed"
LAST_UPDATE = "2026-10-01"
# requirement-domain-videospeed: about must not advertise a curl|sh channel.
DOWNLOAD_URL = ""
BASIC_USAGE = "video-speed --file clip.mp4 --start 0 --end 5"

# When set, out_info / out_err report here instead of the terminal.
# The edit step uses this so those lines stay on the open text screen.
_MESSAGE_SINK = None

# Length percent bounds (domain / pipeline guidance made fail-closed)
RATIO_MIN = 20.0
RATIO_MAX = 200.0


def out_info(msg):
    """User-facing informational line (stdout, or the open text screen)."""
    if _JSON_MODE:
        return
    if _MESSAGE_SINK is not None:
        _MESSAGE_SINK(msg, False)
        return
    print(msg)


def out_err(msg):
    """User-facing error line (stderr, or the open text screen)."""
    if _MESSAGE_SINK is not None:
        _MESSAGE_SINK(msg, True)
        return
    print(msg, file=sys.stderr)


# requirement-python-json-output: --json quiets stdout and emits one object.
_JSON_MODE = False
_JSON_WALK = False
_JSON_ERROR = None
_JSON_NEXT = None
_JSON_JOBS = []


def _json_reset():
    """General Purpose: Clear the JSON result before a new main()."""
    global _JSON_MODE, _JSON_WALK, _JSON_ERROR, _JSON_NEXT, _JSON_JOBS
    _JSON_MODE = False
    _JSON_WALK = False
    _JSON_ERROR = None
    _JSON_NEXT = None
    _JSON_JOBS = []


def _remember(message, next_step=None):
    """General Purpose: Keep the first terminal failure for the JSON object."""
    global _JSON_ERROR, _JSON_NEXT
    if not _JSON_MODE:
        return
    if _JSON_ERROR is None and message:
        _JSON_ERROR = message
    if next_step and _JSON_NEXT is None:
        _JSON_NEXT = next_step


def _remember_job(video_path, start, end, percent, boomerang, output):
    """General Purpose: Append one finished job to the JSON result."""
    if not _JSON_MODE:
        return
    _JSON_JOBS.append({
        "file": str(video_path),
        "start": float(start),
        "end": float(end),
        "percent": float(percent),
        "boomerang": bool(boomerang),
        "output": str(output),
    })


def _emit_json(mode, code):
    """General Purpose: Write the only stdout bytes for a --json run."""
    ok = code == 0 and _JSON_ERROR is None
    doc = {
        "ok": ok,
        "mode": mode,
        "app": APP_NAME,
        "version": _PKG_VERSION,
        "error": _JSON_ERROR,
        "next": _JSON_NEXT,
        "jobs": list(_JSON_JOBS),
    }
    sys.stdout.write(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    return 0 if ok else (code or 1)


def _call_sunk(sink, fn):
    """General Purpose: Run fn while user-facing lines go to sink."""
    global _MESSAGE_SINK
    previous = _MESSAGE_SINK
    _MESSAGE_SINK = sink
    try:
        return fn()
    finally:
        _MESSAGE_SINK = previous


def _collect_lines(bucket):
    """General Purpose: Sink that keeps non-empty user-facing lines."""
    def sink(msg, _is_err):
        for part in str(msg).splitlines():
            if part.strip():
                bucket.append(part)
    return sink


# =============================================================================
# CIAO-Lite Protection Zone — temp staging + publish (USB / multi-mount)
# System TMPDIR and removable media are often different filesystems.
# Move and publish files with shutil.move only.
# Do NOT call os.rename, os.replace, Path.rename, or Path.replace.
# Removable media (USB, SD, external disks) is often a different device from
# the system disk and from TMPDIR. Those calls raise EXDEV and do not copy.
# shutil.move renames on the same device and copies then removes the source
# on EXDEV. Prefer temps next to the final output when that parent is writable.
# Law: requirement-video-ffmpeg-pipeline, requirement-python-coding-style
# =============================================================================


def staging_dir_for(dest_path):
    """
    General Purpose: Choose a directory for intermediate files on the same
    filesystem as dest when possible (USB-safe). Falls back to system temp.
    """
    dest_path = Path(dest_path)
    parent = dest_path.parent if dest_path.suffix else dest_path
    if not parent.is_dir():
        parent = dest_path.parent
    try:
        if parent.is_dir() and os.access(str(parent), os.W_OK):
            return parent
    except OSError:
        pass
    return Path(tempfile.gettempdir())


def make_temp_path(suffix, near_path):
    """
    General Purpose: Create a unique temp file path near near_path's directory
    (same FS when writable). File is created empty and closed; caller overwrites.
    """
    d = staging_dir_for(near_path)
    fd, name = tempfile.mkstemp(suffix=suffix, prefix="videospeed_", dir=str(d))
    os.close(fd)
    return Path(name)


def promote_file(src, dest):
    """
    General Purpose: Publish src → dest using shutil.move (cross-device safe).

    Same device: shutil.move renames. Removable media or any other device:
    shutil.move copies then removes the source.
    Do not call os.rename or os.replace.
    """
    src = Path(src)
    dest = Path(dest)
    if not src.is_file():
        raise FileNotFoundError("promote source missing: {}".format(src))
    dest.parent.mkdir(parents=True, exist_ok=True)
    # shutil.move: try rename; on EXDEV copy + unlink source
    shutil.move(str(src), str(dest))


def ensure_ffmpeg():
    """
    General Purpose: Fail closed if the system ffmpeg binary is not on PATH.
    requirement-runtime-prerequisites / requirement-video-ffmpeg-pipeline
    """
    if shutil.which("ffmpeg") is None:
        _remember(
            "ffmpeg not found on PATH.",
            "Install FFmpeg and ensure ffmpeg is available.",
        )
        out_err("ERROR: ffmpeg not found on PATH.")
        out_err("   Install FFmpeg and ensure `ffmpeg` is available.")
        out_err("   → https://ffmpeg.org/download.html")
        return False
    return True


def _restore_text_screen():
    """General Purpose: Put the text screen back after a child process.

    FFmpeg can change terminal modes. Without a restore, the next paint stays
    off the glass and the next key read looks like a frozen menu.
    """
    try:
        import curses
        if curses.isendwin():
            return
        curses.reset_prog_mode()
    except Exception:
        return


def run_ffmpeg(cmd):
    """
    General Purpose: Run one FFmpeg command; fail closed on non-zero exit.
    Does not modify the user's source media path.
    On the open text screen, capture the child's pipes so the frame stays up.
    -nostdin stops FFmpeg from waiting on the terminal at the end of a step.
    """
    if _MESSAGE_SINK is not None:
        out_info("   Running ffmpeg…")
    else:
        out_info("   Running → {}".format(" ".join(str(c) for c in cmd)))
    try:
        if _MESSAGE_SINK is not None or _JSON_MODE:
            proc = subprocess.run(
                cmd,
                check=False,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            if proc.returncode != 0:
                err = (proc.stderr or b"").decode("utf-8", "replace").strip()
                if err:
                    out_err(err)
                raise subprocess.CalledProcessError(proc.returncode, cmd)
            return
        subprocess.run(cmd, check=True, stdin=subprocess.DEVNULL)
    except FileNotFoundError:
        out_err("ERROR: ffmpeg not found while running a encode step.")
        raise
    except subprocess.CalledProcessError as exc:
        out_err("ERROR: ffmpeg failed (exit {}).".format(exc.returncode))
        raise
    finally:
        _restore_text_screen()


def get_mp4_files(folder="."):
    """General Purpose: Recursively list MP4 files under folder (case variants)."""
    folder = Path(folder)
    if not folder.is_dir():
        return []
    files = list(folder.rglob("*.mp4")) + list(folder.rglob("*.MP4"))
    files = [f for f in files if f.is_file()]
    # de-dupe same path if filesystem is case-insensitive
    seen = set()
    unique = []
    for f in files:
        key = str(f.resolve()) if f.exists() else str(f)
        if key not in seen:
            seen.add(key)
            unique.append(f)
    unique.sort(key=lambda x: x.name.lower())
    return unique


def get_duration_cv2(video_path):
    """
    General Purpose: Probe duration via OpenCV (lazy import).
    Returns seconds; 0.0 if unreadable.
    """
    try:
        import cv2
    except ImportError:
        out_err("ERROR: OpenCV (cv2) is not installed.")
        out_err("   Install with: pip install 'opencv-python-headless>=5.0.0.93'")
        return 0.0

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        cap.release()
        return 0.0
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    if fps is None or fps <= 0 or frame_count <= 0:
        return 0.0
    return float(frame_count) / float(fps)


def format_time(seconds):
    """General Purpose: Format seconds as H:MM:SS.mmm or M:SS.mmm."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    if h == 0:
        return "{:02d}:{:06.3f}".format(m, s)
    return "{:02d}:{:02d}:{:06.3f}".format(h, m, s)


def cut_clip(src, start, end, output_path):
    """
    General Purpose: Extract [start, end] segment to output_path via FFmpeg.
    Source file is read-only input.
    """
    cmd = [
        "ffmpeg", "-nostdin", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(src),
        "-vf", "trim=start={}:end={},setpts=PTS-STARTPTS".format(start, end),
        "-af", "atrim=start={}:end={},asetpts=PTS-STARTPTS".format(start, end),
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "17",
        "-c:a", "aac", "-avoid_negative_ts", "make_zero",
        str(output_path),
    ]
    run_ffmpeg(cmd)


def _atempo_filters(speed):
    """
    General Purpose: Build atempo chain. FFmpeg single atempo accepts 0.5–100.
    speed = playback rate ( >1 faster, shorter wall time for same content).
    """
    filters = []
    remaining = float(speed)
    # Speed up: atempo max 100; slow down: min 0.5 — chain when needed
    if remaining <= 0:
        raise ValueError("speed must be positive")
    while remaining > 100.0:
        filters.append("atempo=100.0")
        remaining /= 100.0
    while remaining < 0.5:
        filters.append("atempo=0.5")
        remaining /= 0.5
    filters.append("atempo={:.6f}".format(remaining))
    return ",".join(filters)


def speed_change(input_path, ratio_percent, output_path):
    """
    General Purpose: Change clip length to ratio_percent of original cut length.
    100 = unchanged duration intent; 50 ≈ half length (faster); 200 ≈ double length.
    """
    speed = 100.0 / float(ratio_percent)
    atempo = _atempo_filters(speed)
    cmd = [
        "ffmpeg", "-nostdin", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(input_path),
        "-filter_complex",
        "[0:v]setpts={:.6f}*PTS[v];[0:a]{}[a]".format(1.0 / speed, atempo),
        "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart",
        str(output_path),
    ]
    run_ffmpeg(cmd)


def add_boomerang(forward_clip, final_output):
    """
    General Purpose: Concat forward + reverse of forward_clip into final_output.
    Intermediate reverse/list files are staged near final_output (USB-safe).
    Cleans reverse and concat-list temps on all paths.
    """
    reverse_clip = None
    concat_list = None
    try:
        # Stage reverse next to final output so reverse+concat stay on one mount.
        reverse_clip = make_temp_path(".mp4", final_output)

        run_ffmpeg([
            "ffmpeg", "-nostdin", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(forward_clip),
            "-vf", "reverse", "-af", "areverse",
            str(reverse_clip),
        ])

        # Concat list file also near dest FS; paths absolute for demuxer.
        concat_list = make_temp_path(".txt", final_output)
        with open(str(concat_list), "w", encoding="utf-8") as f:
            f.write("file '{}'\n".format(Path(forward_clip).resolve().as_posix()))
            f.write("file '{}'\n".format(Path(reverse_clip).resolve().as_posix()))

        run_ffmpeg([
            "ffmpeg", "-nostdin", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "concat", "-safe", "0",
            "-i", str(concat_list),
            "-c", "copy",
            str(final_output),
        ])
    finally:
        for p in (reverse_clip, concat_list):
            if p is not None and Path(p).exists():
                try:
                    os.unlink(p)
                except OSError:
                    pass


def _visible_lines(lines, room, pin_last):
    """General Purpose: Lines that fit above the input box.

    A question pins its last line so the prompt stays on screen. A job log
    keeps the newest lines.
    """
    if room < 1:
        return []
    if len(lines) <= room:
        return list(lines)
    if not pin_last:
        return list(lines[-room:])
    if room == 1:
        return [lines[-1]]
    return list(lines[: room - 2]) + ["…", lines[-1]]


def _paint_prompt(screen, model, title, lines, pin_last):
    """
    General Purpose: Draw one domain question on the open text screen.

    The rounded box is VideoSpeed.menu's painter. This function does not draw
    that frame itself. The question sits in the menu region; the answer is
    typed in the box.
    """
    import curses
    from .menu import CHROME_ROWS, _paint_box, _put

    screen.erase()
    italic = curses.A_ITALIC if hasattr(curses, "A_ITALIC") else curses.A_DIM
    _put(screen, 0, 0, APP_NAME, curses.A_BOLD)
    cursor = len(APP_NAME)
    _put(screen, 0, cursor, " (")
    cursor += 2
    _put(screen, 0, cursor, _PKG_VERSION, italic)
    cursor += len(_PKG_VERSION)
    _put(screen, 0, cursor, ") — {}".format(title))
    height, _width = screen.getmaxyx()
    box_top = height - CHROME_ROWS
    stop = box_top
    if model.error and box_top >= 4:
        stop = box_top - 1
    shown = _visible_lines(lines, stop - 2, pin_last)
    y = 2
    for line in shown:
        if y >= stop:
            break
        _put(screen, y, 0, line)
        y += 1
    if model.error and box_top >= 4:
        _put(screen, box_top - 1, 0, model.error, curses.A_BOLD)
    _paint_box(screen, model, box_top, APP_NAME, _PKG_VERSION, title)
    if hasattr(screen, "curs_set"):
        try:
            screen.curs_set(0)
        except curses.error:
            pass
    screen.refresh()


def _tui_read(screen, model, lines):
    """
    General Purpose: Read one line from the bottom input box.

    Returns the text, or None when the person presses Esc or the screen
    reports no key (back to the front board).
    """
    import curses
    from .menu import _edge_keys

    model.buffer = ""
    model.cursor = 0
    model.focus = "input"
    while True:
        _paint_prompt(screen, model, "edit", lines, pin_last=True)
        key = screen.getch()
        if key in (-1, 27):
            model.error = ""
            model.buffer = ""
            model.cursor = 0
            model.focus = "list"
            return None
        if key in (10, 13, curses.KEY_ENTER):
            text = model.buffer
            model.buffer = ""
            model.cursor = 0
            model.error = ""
            return text
        if key in (curses.KEY_BACKSPACE, 127, 8):
            model._backspace()
            model.error = ""
            continue
        if key in (curses.KEY_LEFT, curses.KEY_RIGHT) or key in _edge_keys():
            model._slide(key)
            continue
        if key in (curses.KEY_UP, curses.KEY_DOWN):
            continue
        if 32 <= key < 127:
            model._insert(chr(key))
            model.error = ""
            continue


def _tui_notice(screen, model, lines):
    """General Purpose: Show lines on the edit screen until the next key."""
    model.buffer = ""
    model.cursor = 0
    model.focus = "list"
    model.error = ""
    body = list(lines) + ["", "Press a key to return to the main menu."]
    _paint_prompt(screen, model, "edit", body, pin_last=True)
    try:
        screen.getch()
    except Exception:
        return


def _tui_float(screen, model, lines, default=None):
    """General Purpose: Read a float from the box; empty uses default."""
    while True:
        raw = _tui_read(screen, model, lines)
        if raw is None:
            return None
        raw = raw.strip()
        if raw == "" and default is not None:
            return float(default)
        try:
            return float(raw.replace("%", ""))
        except ValueError:
            model.error = "Please enter a number"


def _tui_yes_no(screen, model, lines, default_no=True):
    """General Purpose: y/n from the box; empty uses the default."""
    while True:
        raw = _tui_read(screen, model, lines)
        if raw is None:
            return None
        raw = raw.strip().lower()
        if raw == "":
            return not default_no
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        model.error = "Please enter y or n"


def _tui_index(screen, model, lines, count):
    """General Purpose: Read a 1-based index from the box; re-ask on error."""
    while True:
        raw = _tui_read(screen, model, lines)
        if raw is None:
            return None
        raw = raw.strip()
        try:
            idx = int(raw)
        except ValueError:
            model.error = "Please type a number"
            continue
        if 1 <= idx <= count:
            return idx - 1
        model.error = "Enter 1–{}".format(count)


def stdin_is_tty():
    """General Purpose: Whether stdin can take interactive prompts."""
    try:
        return sys.stdin.isatty()
    except Exception:
        return False


def stdout_is_tty():
    """General Purpose: Whether the text screen can be drawn on this stdout."""
    try:
        return sys.stdout.isatty()
    except Exception:
        return False


def menu_lines():
    """
    General Purpose: Title and aligned menu rows for the text screen.
    The column widths come from VideoSpeed.menu, so a shorter verb is padded
    before the colon.
    """
    from .menu import format_rows

    title = "{} ({}) — main menu".format(APP_NAME, _PKG_VERSION)
    return [title] + format_rows(MENU_ROWS)


def parse_sys_version(version_text, python_version):
    """
    General Purpose: Python display and C library string from sys.version.
    The C library line is the compiler token, such as GCC 13.3.0.
    """
    gcc = version_text
    if "\n" in gcc:
        gcc = gcc.split("\n", 1)[1]
    elif "[" in gcc and "]" in gcc:
        gcc = gcc.split("[", 1)[1].split("]", 1)[0]
    if gcc == "GCC":
        gcc = "[GCC]"
    if " (Red Hat" in gcc:
        gcc = gcc.split(" (Red Hat", 1)[0] + "]"
    probe = gcc if "[PyPy " in gcc else version_text
    if "[PyPy " in probe and "with" in probe:
        extra = probe.split("with", 1)[0].split("[", 1)[1].strip()
        python_version = "{} ({})".format(python_version, extra)
        gcc = "[" + probe.split("with ", 1)[1]
    shown = gcc.strip()
    if shown.startswith("[") and shown.endswith("]"):
        shown = shown[1:-1].strip()
    return python_version, shown


def arch_label(version_text, machine=None):
    """General Purpose: amd64 / arm64 / x86 style name for this host."""
    if "AMD64" in version_text:
        return "amd64"
    if "AMD32" in version_text:
        return "x86"
    if machine is None:
        machine = platform.machine()
    mapped = {
        "x86_64": "amd64",
        "amd64": "amd64",
        "aarch64": "arm64",
        "arm64": "arm64",
        "i386": "x86",
        "i686": "x86",
        "x86": "x86",
    }
    return mapped.get(machine.lower(), machine)


def libc_label(version_text, shell, detected=None):
    """General Purpose: libc token used in the binary type, such as glibc."""
    if detected is None:
        try:
            detected = platform.libc_ver()[0] or ""
        except Exception:
            detected = "unknown"
    name = detected
    if ("AMD64" in version_text or "AMD32" in version_text) and "MSC" in version_text:
        name = "msc"
    if "clang" in version_text.lower():
        name = "clang"
    if name == "" and shell == "/bin/ash":
        name = "muslc"
    return name


def binary_type(arch, libc):
    """General Purpose: arch-libc token, such as amd64-glibc."""
    if arch == "":
        return ""
    if libc == "":
        return "{}-".format(arch)
    return "{}-{}".format(arch, libc)


def current_user():
    """General Purpose: Login name for the about system check."""
    user = os.environ.get("USER") or os.environ.get("USERNAME") or ""
    if user:
        return user
    try:
        import getpass
        return getpass.getuser()
    except Exception:
        return ""


def shell_text():
    """General Purpose: The shell path from the environment."""
    return os.environ.get("SHELL") or ""


def python_executable_name():
    """General Purpose: Basename of the running Python executable."""
    exe = sys.executable or ""
    if "/" in exe:
        return exe.rsplit("/", 1)[-1]
    if "\\" in exe:
        return exe.rsplit("\\", 1)[-1]
    return exe


def command_location(name):
    """General Purpose: PATH location of a tool, or an empty string."""
    found = shutil.which(name)
    return found or ""


def os_text():
    """General Purpose: Pretty operating-system name, such as Ubuntu 24.04 LTS."""
    try:
        info = platform.freedesktop_os_release()
    except Exception:
        info = {}
    pretty = info.get("PRETTY_NAME") or ""
    if pretty:
        return pretty
    return platform.platform()


def inside_docker(marker="/.dockerenv"):
    """General Purpose: True when the docker marker file is present."""
    return os.path.exists(marker)


def cpython_soabi():
    """General Purpose: CPython ABI string shown as the Cython string."""
    value = sysconfig.get_config_var("SOABI") or ""
    return value


def self_location():
    """
    General Purpose: Path of the running program.
    A console-script argv wins. Otherwise this module file.
    """
    here = os.path.realpath(__file__)
    argv0 = sys.argv[0] if sys.argv else ""
    if argv0 and os.path.isfile(argv0):
        argv_real = os.path.realpath(argv0)
        base = os.path.basename(argv_real)
        if base in (CONSOLE_NAME, APP_NAME):
            return argv_real
        same_dir = os.path.dirname(argv_real) == os.path.dirname(here)
        if same_dir and base in ("cli.py", "__main__.py"):
            return argv_real
    return here


def _is_source_checkout(path):
    """True when path is this package inside a source tree that has pyproject.toml."""
    marker = "{}src{}VideoSpeed{}".format(os.sep, os.sep, os.sep)
    if marker not in path:
        return False
    cursor = os.path.dirname(path)
    for _ in range(8):
        if os.path.isfile(os.path.join(cursor, "pyproject.toml")):
            return True
        parent = os.path.dirname(cursor)
        if parent == cursor:
            return False
        cursor = parent
    return False


def install_kind(path):
    """
    General Purpose: global, local, or uninstalled for an about location.
    A source checkout is uninstalled. A copy under the home directory is local.
    """
    path = os.path.realpath(path)
    parts = path.split(os.sep)
    packaged = "site-packages" in parts or "dist-packages" in parts
    if not packaged and _is_source_checkout(path):
        return "uninstalled"
    home = os.path.realpath(os.path.expanduser("~"))
    in_home = path == home or path.startswith(home + os.sep)
    base = os.path.basename(path)
    if in_home and (packaged or base in (CONSOLE_NAME, APP_NAME)):
        return "local"
    if path.startswith("/usr/") or path.startswith("/opt/") or path.startswith("/bin/"):
        return "global"
    if packaged and not in_home:
        return "global"
    return "uninstalled"


def install_sentence(kind):
    """General Purpose: The location sentence inside the about box."""
    if kind == "global":
        return "You are using the GLOBAL INSTALLED version, location:"
    if kind == "local":
        return "You are using the LOCAL INSTALLED version, location:"
    return "You are using an UNINSTALLED version, location:"


def about_box_lines(
    usage=None,
    location=None,
    kind=None,
    homepage=None,
    download_url=None,
    author=None,
    updated=None,
):
    """
    General Purpose: Star-bordered about box.
    An empty download URL omits the install line.
    """
    if usage is None:
        usage = BASIC_USAGE
    if location is None:
        location = self_location()
    if kind is None:
        kind = install_kind(location)
    if homepage is None:
        homepage = HOMEPAGE
    if download_url is None:
        download_url = DOWNLOAD_URL
    if author is None:
        author = AUTHOR_NAME
    if updated is None:
        updated = LAST_UPDATE
    app = install_sentence(kind)
    python_exe = python_executable_name() or "python3"
    msg1 = "{} ({}.{}.{}) by {} on {}".format(
        APP_NAME, MAJOR_VERSION, MINOR_VERSION, PATCH_VERSION, author, updated
    )
    if download_url == "":
        msg = [
            msg1,
            "",
            app,
            "    {}".format(location),
            "",
            "Basic Usage:",
            "    {}".format(usage),
            "",
            "Please visit our homepage: ",
            '    "{}"'.format(homepage),
            "",
            "",
            "",
            "",
        ]
    else:
        msg = [
            msg1,
            "",
            app,
            "    {}".format(location),
            "",
            "Basic Usage:",
            "    {}".format(usage),
            "",
            "Please visit our homepage: ",
            '    "{}"'.format(homepage),
            "",
            "Installation command:",
            "    curl -fsSL {} | {}".format(download_url, python_exe),
            "",
        ]
    if download_url == "":
        if homepage == "":
            max_line = len(msg) - 3
        else:
            max_line = len(msg) - 2
    else:
        max_line = len(msg) - 1
    if max_line < 1:
        max_line = len(msg)
    max_len = 0
    for n in range(0, max_line):
        if len(msg[n]) > max_len:
            max_len = len(msg[n])
    boxed = []
    for n in range(0, max_line):
        boxed.append(msg[n] + (" " * (max_len - len(msg[n]))))
    star = "*" * (max_len + 4)
    blank = " " * max_len
    lines = [star, "* {} *".format(blank)]
    for row in boxed:
        lines.append("* {} *".format(row))
    lines.append("* {} *".format(blank))
    lines.append(star)
    return lines


def check_system_lines(now=None):
    """
    General Purpose: Host check block for the about page.
    The stamp is local time with microseconds.
    """
    when = now if now is not None else datetime.datetime.now()
    stamp = when.strftime("%Y-%m-%d %H:%M:%S.%f")
    version_text = sys.version
    py_text, c_library = parse_sys_version(version_text, platform.python_version())
    arch = arch_label(version_text)
    shell = shell_text()
    libc = libc_label(version_text, shell)
    rows = [
        "{} {}(v{})  [CHECK SYSTEM]:".format(stamp, APP_NAME, _PKG_VERSION),
        "  Now checking your operation system!",
        "    Python: {}".format(py_text),
        "    C Library: {}".format(c_library),
        "    Operation System: {}".format(os_text()),
        "    Architecture: {}".format(arch),
        "    Current User: {}".format(current_user()),
        "    Shell: {}".format(shell),
        "    Python Executable: {}".format(python_executable_name()),
        "    python2 location: {}".format(command_location("python2")),
        "    python3 location: {}".format(command_location("python3")),
        "    conda location: {}".format(command_location("conda")),
        "    pyenv location: {}".format(command_location("pyenv")),
        "    Inside docker container: {}".format(inside_docker()),
        "    Cython String: {}".format(cpython_soabi()),
        "    Binary Type: {}".format(binary_type(arch, libc)),
        "    Location: {}".format(self_location()),
    ]
    return rows


def framework_hello():
    """
    General Purpose: Hello text for menu item 7.
    requirement-python-tui: the result page shows this message.
    """
    return "Hello."


def framework_about():
    """
    General Purpose: About text for the menu result page.
    requirement-python-about: identity, host check, and the install box.
    """
    lines = [
        "{} {}".format(APP_NAME, _PKG_VERSION),
        "Domain: Cut → speed/length → optional boomerang for MP4",
        "Runtime tools: FFmpeg (encode), OpenCV (duration probe)",
        "Entry points: video-speed, python -m VideoSpeed",
        "",
    ]
    lines.extend(check_system_lines())
    lines.append("")
    lines.extend(about_box_lines())
    return "\n".join(lines)


def open_text_menu():
    """
    General Purpose: Draw the text menu and keep edit's questions on it.

    The session is VideoSpeed.menu.MenuSession with this product's name,
    package version, and MENU_ROWS. edit asks for the folder and the later
    steps in the same bottom box. Returns "missing" when the screen cannot
    open, and None when the person leaves.
    """
    if not stdout_is_tty():
        out_err(
            "ERROR: No terminal for the text menu. "
            "Next: pass --file, --start, and --end, or run in a terminal."
        )
        return "missing"
    try:
        import curses
        from .menu import MenuScreenError, MenuSession
    except ImportError:
        out_err("ERROR: The text menu could not be loaded.")
        out_err("   Next: video-speed --help")
        return "missing"

    screen_box = {}

    def on_kind(kind):
        if kind == "hello":
            return framework_hello()
        if kind != "edit":
            return None
        screen = screen_box.get("screen")
        if screen is None:
            return None
        try:
            _edit_in_tui(screen, session.model)
        except Exception as exc:
            _tui_notice(screen, session.model, ["ERROR: {}".format(exc)])
        finally:
            session.model._show_front()
        return None

    session = MenuSession(
        APP_NAME,
        _PKG_VERSION,
        on_version=lambda: "{} {}".format(APP_NAME, _PKG_VERSION),
        on_about=framework_about,
        boards={"front": MENU_ROWS},
        on_kind=on_kind,
    )

    def _wrapped(screen):
        screen_box["screen"] = screen
        session.run(screen)

    try:
        curses.wrapper(_wrapped)
    except MenuScreenError:
        out_err(
            "ERROR: The text screen is too small for the menu and the input box."
        )
        out_err("   Next: video-speed --help")
        return "missing"
    except Exception:
        out_err("ERROR: The text menu could not open on this terminal.")
        out_err("   Next: video-speed --help")
        return "missing"
    return None


def valid_cut_range(start, end, duration):
    """General Purpose: True iff 0 <= start < end <= duration (no encode)."""
    try:
        start = float(start)
        end = float(end)
        duration = float(duration)
    except (TypeError, ValueError):
        return False
    return 0.0 <= start < end <= duration


def valid_percent(ratio):
    """General Purpose: True iff length percent is inside 20–200."""
    try:
        ratio = float(ratio)
    except (TypeError, ValueError):
        return False
    return RATIO_MIN <= ratio <= RATIO_MAX


def _length_unchanged(ratio):
    """General Purpose: True when the asked length is 100% of the cut."""
    try:
        return abs(float(ratio) - 100.0) <= 1e-6
    except (TypeError, ValueError):
        return False


def build_output_name(video_path, start, end, ratio, boomerang):
    """General Purpose: Domain output naming pattern beside source."""
    name = "{}_cut{:.1f}-{:.1f}s_{:d}pct".format(
        video_path.stem, start, end, int(ratio)
    )
    if boomerang:
        name += "_BOOMERANG"
    name += ".mp4"
    return video_path.parent / name


def process_job(video_path, start, end, ratio, boomerang):
    """
    General Purpose: Run cut → speed → optional boomerang pipeline.
    Never overwrites source; cleans intermediate temps.
    Temps are staged on the destination filesystem when possible.
    Publish uses shutil.move so removable media does not depend on os.rename
    or os.replace.
    Returns final Path or None on failure.
    """
    final_out = build_output_name(video_path, start, end, ratio, boomerang)
    out_info("\nProcessing → {}\n".format(final_out))
    out_info("   Staging dir → {}".format(staging_dir_for(final_out)))

    cut_temp = None
    speed_temp = None
    try:
        # Same-FS temps next to final_out (e.g. on the USB volume).
        cut_temp = make_temp_path(".mp4", final_out)

        out_info("1. Cutting segment...")
        cut_clip(video_path, start, end, cut_temp)
        if _length_unchanged(ratio):
            # 100% keeps the cut. A second encode (preset medium, +faststart)
            # holds the text screen and leaves the clip on its temporary name
            # until that pass returns.
            out_info("2. Length stays 100%...")
            forward = cut_temp
        else:
            speed_temp = make_temp_path(".mp4", final_out)
            shown = int(ratio) if ratio == int(ratio) else ratio
            out_info("2. Changing length to {}%...".format(shown))
            speed_change(cut_temp, ratio, speed_temp)
            forward = speed_temp
        if boomerang:
            out_info("3. Creating boomerang...")
            add_boomerang(forward, final_out)
        else:
            # Publish with shutil.move (same-FS rename or cross-FS copy+delete).
            promote_file(forward, final_out)
            if forward is cut_temp:
                cut_temp = None
            else:
                speed_temp = None
        out_info("\nSUCCESS → {}\n".format(final_out.name))
        return final_out
    except (subprocess.CalledProcessError, FileNotFoundError, OSError, ValueError) as exc:
        err = getattr(exc, "errno", None)
        _remember("Job failed: {}".format(exc))
        out_err("Job failed: {}".format(exc))
        if err in (getattr(os, "EXDEV", 18), 18):
            out_err(
                "   Hint: cross-filesystem rename failed (USB vs system temp). "
                "Temps should stage next to the output; publish uses shutil.move. "
                "Check USB write permission and free space."
            )
        return None
    finally:
        for p in (cut_temp, speed_temp):
            if p is not None and Path(p).exists():
                try:
                    os.unlink(p)
                except OSError:
                    pass


def _edit_in_tui(
    screen,
    model,
    folder=None,
    video=None,
    start_preset=None,
    end_preset=None,
    percent_preset=None,
    boomerang_preset=None,
):
    """
    General Purpose: Domain steps D-01..D-08 on the open text screen.

    The front board stays up. Each question is typed in the bottom box.
    Esc returns to that board. A direct verb may already know the folder
    or the file, and may pre-fill percent or boomerang.
    requirement-domain-videospeed, requirement-python-tui,
    requirement-python-interactive-vs-noninteractive.
    Last updated: 2026-10-01
    """
    notes = []
    ok = _call_sunk(_collect_lines(notes), ensure_ffmpeg)
    if not ok:
        _tui_notice(
            screen,
            model,
            notes or ["ERROR: ffmpeg not found on PATH."],
        )
        return

    video_path = None
    duration = None
    if video:
        video_path = Path(video)
        if not video_path.is_file():
            _tui_notice(
                screen,
                model,
                ["ERROR: File not found: {}".format(video)],
            )
            return
        probe_notes = []
        duration = _call_sunk(
            _collect_lines(probe_notes),
            lambda: get_duration_cv2(video_path),
        )
        if duration <= 0:
            detail = probe_notes[-1] if probe_notes else (
                "Could not read duration for {}".format(video_path.name)
            )
            _tui_notice(screen, model, [detail])
            return
    else:
        folder_lines = [
            "Cut → Speed → Optional Boomerang",
            "Esc returns to the menu.",
            "",
            "Folder (Enter = current):",
        ]
        folder_path = Path(folder) if folder else None
        files = []
        while True:
            if folder_path is None:
                raw = _tui_read(screen, model, folder_lines)
                if raw is None:
                    return
                folder = raw.strip() or "."
                folder_path = Path(folder)
            if not folder_path.is_dir():
                model.error = "ERROR: Not a directory: {}".format(folder_path)
                folder_path = None
                continue
            files = get_mp4_files(folder_path)
            if not files:
                _tui_notice(screen, model, ["No MP4 files found!"])
                return
            break

        listing = ["{:2d}. {}".format(i, f.name) for i, f in enumerate(files, 1)]
        choose_lines = listing + ["", "Choose video (1–{}):".format(len(files))]
        while True:
            sel = _tui_index(screen, model, choose_lines, len(files))
            if sel is None:
                return
            video_path = files[sel]
            probe_notes = []
            duration = _call_sunk(
                _collect_lines(probe_notes),
                lambda: get_duration_cv2(video_path),
            )
            if duration <= 0:
                detail = probe_notes[-1] if probe_notes else (
                    "Could not read duration for {}".format(video_path.name)
                )
                model.error = detail
                continue
            break

    header = [
        "Selected: {}".format(video_path.name),
        "Duration: {} ({:.3f}s)".format(format_time(duration), duration),
    ]
    ratio_default = 100.0 if percent_preset is None else float(percent_preset)
    if percent_preset is None:
        ratio_label = "New length % [100%]:"
    else:
        shown = (
            int(ratio_default) if ratio_default == int(ratio_default) else ratio_default
        )
        ratio_label = "New length % [{}%]:".format(shown)
    boom_default_no = not bool(boomerang_preset)
    boom_mark = "n" if boom_default_no else "y"
    boom_label = "Make it go forward + backward (y/n) [{}]:".format(boom_mark)
    start_default = 0.0 if start_preset is None else float(start_preset)
    if start_preset is None:
        start_label = "Start seconds (default 0.0):"
    else:
        start_label = "Start seconds (default {:.1f}):".format(start_default)
    preset_cut = (
        start_preset is not None
        and end_preset is not None
        and valid_cut_range(start_preset, end_preset, duration)
    )
    while True:
        if preset_cut:
            start = float(start_preset)
            end = float(end_preset)
            preset_cut = False
        else:
            start = _tui_float(
                screen,
                model,
                header + ["", "Step 1/4 – Cut segment", start_label],
                default=start_default,
            )
            if start is None:
                return
            end_default = duration if end_preset is None else float(end_preset)
            end = _tui_float(
                screen,
                model,
                header + [
                    "Start: {:.3f}s".format(start),
                    "End seconds [{:.3f}]:".format(end_default),
                ],
                default=end_default,
            )
            if end is None:
                return
            if not valid_cut_range(start, end, duration):
                model.error = "Invalid range! Need 0 ≤ start < end ≤ duration."
                continue

        ratio = _tui_float(
            screen,
            model,
            [
                "Step 2/4 – Resize length ({}–{}%)".format(
                    int(RATIO_MIN), int(RATIO_MAX)
                ),
                ratio_label,
            ],
            default=ratio_default,
        )
        if ratio is None:
            return
        if not valid_percent(ratio):
            model.error = "Invalid percent! Use {}–{} (got {}).".format(
                int(RATIO_MIN), int(RATIO_MAX), ratio
            )
            continue

        boomerang = _tui_yes_no(
            screen,
            model,
            [
                "Step 3/4 – Add boomerang effect?",
                boom_label,
            ],
            default_no=boom_default_no,
        )
        if boomerang is None:
            return

        body = ["Working…"]
        model.focus = "list"
        model.buffer = ""
        model.error = ""
        _paint_prompt(screen, model, "edit", body, pin_last=False)

        def paint_job(msg, _is_err, _body=body):
            for part in str(msg).splitlines():
                if part.strip():
                    _body.append(part)
            model.buffer = ""
            model.cursor = 0
            model.focus = "list"
            model.error = ""
            _paint_prompt(screen, model, "edit", _body, pin_last=False)

        result = _call_sunk(paint_job, lambda: process_job(
            video_path, start, end, ratio, boomerang
        ))
        _restore_text_screen()
        if result is None:
            closing = "Not saved. Again? (y/n):"
        else:
            closing = "Saved {} — Again? (y/n):".format(Path(result).name)
        again = _tui_yes_no(
            screen,
            model,
            [closing],
            default_no=True,
        )
        if again is None:
            return
        if not again:
            _tui_notice(screen, model, ["Done."])
            return


def _err_line(text):
    """General Purpose: Prompt or re-ask line on stderr. Not the JSON object."""
    print(text, file=sys.stderr)


def _prompt_line(label):
    """General Purpose: One answer from stdin. None means EOF."""
    _err_line(label)
    try:
        return input("")
    except EOFError:
        return None


def _prompt_float(label, default):
    """General Purpose: Float from stderr prompt. Empty uses default. None is EOF."""
    while True:
        raw = _prompt_line(label)
        if raw is None:
            return None
        raw = raw.strip()
        if raw == "":
            return float(default)
        try:
            return float(raw.replace("%", ""))
        except ValueError:
            _err_line("Please enter a number")


def _prompt_yes_no(label, default_no=True):
    """General Purpose: y/n from stderr. Empty uses the default. None is EOF."""
    while True:
        raw = _prompt_line(label)
        if raw is None:
            return None
        raw = raw.strip().lower()
        if raw == "":
            return not default_no
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        _err_line("Please enter y or n")


def _edit_json(args=None):
    """
    General Purpose: Same edit fields as the menu walk, without the text menu.

    Prompts go to stderr. stdout stays unused until main emits one JSON object.
    EOF ends the walk and does not encode the open question.
    A direct edit verb may already name the folder or the file.
    requirement-python-json-output.
    Last updated: 2026-10-01
    """
    global _JSON_WALK
    _JSON_WALK = True
    if not ensure_ffmpeg():
        return 1
    file_preset = None if args is None else args.file
    folder_preset = None if args is None else args.folder
    start_preset = None if args is None else args.start
    end_preset = None if args is None else args.end
    percent_preset = None if args is None else args.percent
    boomerang_preset = False if args is None else bool(args.boomerang)

    if file_preset:
        video_path = Path(file_preset)
        if not video_path.is_file():
            _remember(
                "File not found: {}".format(file_preset),
                "pass an existing MP4 with --file.",
            )
            _err_line("ERROR: File not found: {}".format(file_preset))
            _err_line("   Next: pass an existing MP4 with --file.")
            return 1
        duration = get_duration_cv2(video_path)
        if duration <= 0:
            _err_line("Could not read duration for {}".format(video_path.name))
            return 1
    else:
        folder_path = Path(folder_preset) if folder_preset else None
        while True:
            if folder_path is None:
                raw = _prompt_line("Folder (Enter = current):")
                if raw is None:
                    return 0
                folder = raw.strip() or "."
                folder_path = Path(folder)
            if not folder_path.is_dir():
                _err_line("ERROR: Not a directory: {}".format(folder_path))
                folder_path = None
                continue
            files = get_mp4_files(folder_path)
            if not files:
                _err_line("No MP4 files found!")
                folder_path = None
                continue
            break

        while True:
            for i, item in enumerate(files, 1):
                _err_line("{:2d}. {}".format(i, item.name))
            raw = _prompt_line("Choose video (1–{}):".format(len(files)))
            if raw is None:
                return 0
            try:
                idx = int(raw.strip())
            except ValueError:
                _err_line("Please type a number")
                continue
            if not 1 <= idx <= len(files):
                _err_line("Enter 1–{}".format(len(files)))
                continue
            video_path = files[idx - 1]
            duration = get_duration_cv2(video_path)
            if duration <= 0:
                _err_line("Could not read duration for {}".format(video_path.name))
                continue
            break

    ratio_default = 100.0 if percent_preset is None else float(percent_preset)
    if percent_preset is None:
        ratio_label = "New length % [100%]:"
    else:
        shown = (
            int(ratio_default) if ratio_default == int(ratio_default) else ratio_default
        )
        ratio_label = "New length % [{}%]:".format(shown)
    boom_default_no = not boomerang_preset
    boom_mark = "n" if boom_default_no else "y"
    boom_label = "Make it go forward + backward (y/n) [{}]:".format(boom_mark)
    start_default = 0.0 if start_preset is None else float(start_preset)
    if start_preset is None:
        start_label = "Start seconds (default 0.0):"
    else:
        start_label = "Start seconds (default {:.1f}):".format(start_default)
    preset_cut = (
        start_preset is not None
        and end_preset is not None
        and valid_cut_range(start_preset, end_preset, duration)
    )

    while True:
        if preset_cut:
            start = float(start_preset)
            end = float(end_preset)
            preset_cut = False
        else:
            start = _prompt_float(start_label, start_default)
            if start is None:
                return 0
            end_default = duration if end_preset is None else float(end_preset)
            end = _prompt_float(
                "End seconds [{:.3f}]:".format(end_default),
                end_default,
            )
            if end is None:
                return 0
            if not valid_cut_range(start, end, duration):
                _err_line("Invalid range! Need 0 ≤ start < end ≤ duration.")
                continue
        ratio = _prompt_float(ratio_label, ratio_default)
        if ratio is None:
            return 0
        if not valid_percent(ratio):
            _err_line(
                "Invalid percent! Use {}–{} (got {}).".format(
                    int(RATIO_MIN), int(RATIO_MAX), ratio
                )
            )
            continue
        boomerang = _prompt_yes_no(boom_label, default_no=boom_default_no)
        if boomerang is None:
            return 0
        result = process_job(video_path, start, end, ratio, boomerang)
        if result is None:
            return 1
        _remember_job(video_path, start, end, ratio, boomerang, result)
        again = _prompt_yes_no("Again? (y/n):", default_no=True)
        if again is None or not again:
            return 0


def batch_session(file_path, start, end, percent, boomerang):
    """
    General Purpose: One non-interactive job. Fail closed on bad range/percent
    before encode. requirement-python-interactive-vs-noninteractive.
    """
    video_path = Path(file_path)
    if not video_path.is_file():
        _remember(
            "File not found: {}".format(file_path),
            "pass an existing MP4 with --file.",
        )
        out_err("ERROR: File not found: {}".format(file_path))
        out_err("   Next: pass an existing MP4 with --file.")
        return 1
    if not ensure_ffmpeg():
        return 1
    duration = get_duration_cv2(video_path)
    if duration <= 0:
        _remember("Could not read duration for {}".format(video_path.name))
        out_err("ERROR: Could not read duration for {}".format(video_path.name))
        return 1
    if not valid_cut_range(start, end, duration):
        message = (
            "Invalid range. Need 0 <= start < end <= duration ({:.3f}s)."
            .format(duration)
        )
        _remember(message)
        out_err("ERROR: {}".format(message))
        return 1
    if not valid_percent(percent):
        message = "Invalid percent. Use {}–{} (got {}).".format(
            int(RATIO_MIN), int(RATIO_MAX), percent
        )
        _remember(message)
        out_err("ERROR: {}".format(message))
        return 1
    result = process_job(video_path, start, end, percent, boomerang)
    if result is None:
        return 1
    _remember_job(video_path, start, end, percent, boomerang, result)
    return 0


def _verb_help(parser):
    """
    General Purpose: Same usage text as --help. Does not open the menu.
    Last updated: 2026-10-01
    """
    parser.print_help()
    return 0


def _verb_page(text):
    """
    General Purpose: Print one page and do not ask for a folder or a file.
    Last updated: 2026-10-01
    """
    if _JSON_MODE:
        print(text, file=sys.stderr)
    else:
        print(text)
    return 0


def _verb_about():
    """
    General Purpose: Show the about page. Job flags are ignored.
    Last updated: 2026-10-01
    """
    return _verb_page(framework_about())


def _verb_hello():
    """
    General Purpose: Show Hello. Job flags are ignored.
    Last updated: 2026-10-01
    """
    return _verb_page(framework_hello())


def _unknown_verb(token):
    """
    General Purpose: Reject a positional token that is not a product verb.
    Last updated: 2026-10-01
    """
    names = ", ".join(PRODUCT_VERBS)
    message = "Unknown verb '{}'.".format(token)
    nxt = "video-speed help — verbs: {}".format(names)
    _remember(message, nxt)
    out_err("ERROR: {}".format(message))
    out_err("   Next: {}".format(nxt))
    return 1


def _print_mp4_list(folder):
    """
    General Purpose: Print the numbered MP4 list. Do not encode.
    Last updated: 2026-10-01
    """
    folder_path = Path(folder)
    if not folder_path.is_dir():
        _remember("Not a directory: {}".format(folder))
        out_err("ERROR: Not a directory: {}".format(folder))
        return 1
    files = get_mp4_files(folder_path)
    if not files:
        _remember("No MP4 files found!")
        out_err("No MP4 files found!")
        return 1
    lines = ["{:2d}. {}".format(i, item.name) for i, item in enumerate(files, 1)]
    stream = sys.stderr if _JSON_MODE else sys.stdout
    for line in lines:
        print(line, file=stream)
    return 0


def _list_in_tui(screen, model, folder=None):
    """
    General Purpose: Folder question, then the numbered MP4 list. No encode.
    Last updated: 2026-10-01
    Esc during the folder question returns 0. No MP4 returns 1.
    """
    folder_path = Path(folder) if folder else None
    while True:
        if folder_path is None:
            raw = _tui_read(
                screen,
                model,
                [
                    "List MP4 files",
                    "Esc returns to the menu.",
                    "",
                    "Folder (Enter = current):",
                ],
            )
            if raw is None:
                return 0
            folder = raw.strip() or "."
            folder_path = Path(folder)
        if not folder_path.is_dir():
            model.error = "ERROR: Not a directory: {}".format(folder_path)
            folder_path = None
            continue
        files = get_mp4_files(folder_path)
        if not files:
            _tui_notice(screen, model, ["No MP4 files found!"])
            return 1
        listing = ["{:2d}. {}".format(i, item.name) for i, item in enumerate(files, 1)]
        _tui_notice(screen, model, listing)
        return 0


def _open_direct_screen(kind, args):
    """
    General Purpose: Open the text screen on one verb, not on the front board.
    Last updated: 2026-10-01
    A test driver exposes keys. A finished script must not spin on an empty
    key list. A real screen has no keys attribute, so the front board waits.
    """
    if not stdout_is_tty():
        out_err(
            "ERROR: No terminal for the text menu. "
            "Next: pass --file, --start, and --end, or run in a terminal."
        )
        return 1
    try:
        import curses
        from .menu import MenuScreenError, MenuSession, paint
    except ImportError:
        out_err("ERROR: The text menu could not be loaded.")
        out_err("   Next: video-speed --help")
        return 1

    code_box = {"code": 0}
    session = MenuSession(
        APP_NAME,
        _PKG_VERSION,
        on_version=lambda: "{} {}".format(APP_NAME, _PKG_VERSION),
        on_about=framework_about,
        boards={"front": MENU_ROWS},
        on_kind=lambda _kind: None,
    )

    def _wrapped(screen):
        try:
            if kind == "edit":
                _edit_in_tui(
                    screen,
                    session.model,
                    folder=args.folder,
                    video=args.file,
                    start_preset=args.start,
                    end_preset=args.end,
                    percent_preset=args.percent,
                    boomerang_preset=True if args.boomerang else None,
                )
            else:
                code_box["code"] = _list_in_tui(
                    screen, session.model, args.folder
                )
        except Exception as exc:
            _tui_notice(screen, session.model, ["ERROR: {}".format(exc)])
            code_box["code"] = 1
        finally:
            session.model._show_front()
        # Test drivers expose keys. A finished script must not spin.
        # A real screen has no keys list, so the front board waits.
        if getattr(screen, "keys", None) == []:
            paint(screen, session.model, APP_NAME, _PKG_VERSION)
            return
        session.run(screen)

    try:
        curses.wrapper(_wrapped)
    except MenuScreenError:
        out_err(
            "ERROR: The text screen is too small for the menu and the input box."
        )
        out_err("   Next: video-speed --help")
        return 1
    except Exception:
        out_err("ERROR: The text menu could not open on this terminal.")
        out_err("   Next: video-speed --help")
        return 1
    return code_box["code"]


def _verb_list_mp4(args, logger):
    """
    General Purpose: List MP4 files and stop. Do not encode or pick a file.
    Last updated: 2026-10-01
    """
    if args.folder is None and args.file is not None:
        args.folder = str(Path(args.file).parent)
    if not stdin_is_tty():
        return _print_mp4_list("." if args.folder is None else args.folder)
    if _JSON_MODE:
        global _JSON_WALK
        if args.folder is None:
            _JSON_WALK = True
            raw = _prompt_line("Folder (Enter = current):")
            if raw is None:
                return 0
            args.folder = raw.strip() or "."
        return _print_mp4_list(args.folder)
    logger.quiet(True)
    return _open_direct_screen("list-mp4", args)


def _verb_edit(args, logger):
    """
    General Purpose: One edit job, or the edit questions when a target is missing.
    Last updated: 2026-10-01
    """
    if args.file is not None and args.start is not None and args.end is not None:
        percent = 100.0 if args.percent is None else args.percent
        return batch_session(
            args.file, args.start, args.end, percent, args.boomerang
        )
    if not stdin_is_tty():
        _remember(
            "Non-interactive job needs --file, --start, and --end.",
            "video-speed edit --file clip.mp4 --start 0 --end 5",
        )
        out_err(
            "ERROR: Non-interactive job needs --file, --start, and --end."
        )
        out_err("   Next: video-speed edit --file clip.mp4 --start 0 --end 5")
        return 1
    if _JSON_MODE:
        return _edit_json(args)
    logger.quiet(True)
    return _open_direct_screen("edit", args)


def build_parser():
    """
    General Purpose: One optional product verb, plus the job flags.
    No verb in a terminal still starts the editor.
    Last updated: 2026-10-01
    """
    p = argparse.ArgumentParser(
        prog=CONSOLE_NAME,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=(
            "{} — cut an MP4, change length/speed, optional boomerang.\n"
            "With no arguments in a terminal, starts the interactive editor.\n"
            "Product verbs: help, about, hello, edit, list-mp4.\n"
            "help prints this usage. about and hello print a page and do not\n"
            "ask for a folder or a file. edit asks for a folder, then a file,\n"
            "when those are not already named. list-mp4 lists MP4 files and\n"
            "does not encode.\n"
            "For scripts, pass --file, --start, and --end."
            .format(APP_NAME)
        ),
    )
    p.add_argument(
        "verb",
        nargs="?",
        default=None,
        metavar="verb",
        help="Product verb: help, about, hello, edit, or list-mp4",
    )
    p.add_argument(
        "--version",
        action="version",
        version="{} {}".format(APP_NAME, _PKG_VERSION),
    )
    p.add_argument(
        "--file",
        help="MP4 path for a non-interactive job",
    )
    p.add_argument(
        "--folder",
        help="Folder of MP4s (non-interactive list / empty check)",
    )
    p.add_argument(
        "--start",
        type=float,
        help="Cut start seconds (non-interactive; with --file and --end)",
    )
    p.add_argument(
        "--end",
        type=float,
        help="Cut end seconds (non-interactive; with --file and --start)",
    )
    p.add_argument(
        "--percent",
        type=float,
        default=None,
        help="New length percent of the cut (default 100; allowed 20–200)",
    )
    p.add_argument(
        "--boomerang",
        action="store_true",
        help="Append reverse after the forward clip (non-interactive)",
    )
    p.add_argument(
        "--json",
        action="store_true",
        help=(
            "Quiet stdout and print one JSON object. "
            "Does not open the text menu."
        ),
    )
    return p


def _start_logger(argv, log_basedir="", log_logdir=""):
    """
    General Purpose: One ChronicleLogger for this process, then the debug identity.

    requirement-python-cli-logging: construct with logname, read logName, baseDir,
    and logDir, and display the identity lines only when isDebug() is already true.
    Empty basedir and logdir leave the folder choice to ChronicleLogger.
    A missing library returns None. That line cannot go through log_message.
    """
    try:
        from ChronicleLogger import ChronicleLogger
    except ImportError:
        out_err("ERROR: ChronicleLogger is not installed.")
        out_err("   Next: pip install 'ChronicleLogger>=1.3.1'")
        return None

    logger = ChronicleLogger(
        logname="VideoSpeed",
        basedir=log_basedir or "",
        logdir=log_logdir or "",
        is_quiet=("--json" in argv),
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
    return logger


def main(argv=None, log_basedir="", log_logdir=""):
    """
    General Purpose: Package entry for video-speed / python -m VideoSpeed.
    No arguments in a terminal → interactive editor.
    No arguments without a terminal → fail closed (ask for --file/--start/--end).

    requirement-python-cli-interface: version, ChronicleLogger, debug identity,
    then the argument parser. log_basedir and log_logdir stay empty in normal
    use so ChronicleLogger chooses the folder. Tests pass a temporary folder.
    """
    _json_reset()
    if argv is None:
        argv = sys.argv[1:]
    argv = list(argv)

    logger = _start_logger(argv, log_basedir, log_logdir)
    if logger is None:
        return 1

    parser = build_parser()
    args = parser.parse_args(argv)
    # help stays human usage text, including when --json is also set.
    if args.verb == "help":
        return _verb_help(parser)
    global _JSON_MODE
    if args.json:
        _JSON_MODE = True

    code = _dispatch(args, logger)
    if not args.json:
        return code
    mode = "interactive" if _JSON_WALK else "noninteractive"
    code = _emit_json(mode, code)
    _JSON_MODE = False
    return code


def _dispatch(args, logger):
    """
    General Purpose: One product verb, one job, the menu, or a fail-closed stop.
    Last updated: 2026-10-01
    A product verb is decided before selectors and modifiers, so about and
    edit are not rejected for a lone --percent. No verb keeps the job path.
    """
    verb = args.verb
    if verb == "about":
        return _verb_about()
    if verb == "hello":
        return _verb_hello()
    if verb == "edit":
        return _verb_edit(args, logger)
    if verb == "list-mp4":
        return _verb_list_mp4(args, logger)
    if verb is not None:
        return _unknown_verb(verb)

    selectors = (
        args.file is not None
        or args.start is not None
        or args.end is not None
        or args.folder is not None
    )
    # requirement-python-interactive-vs-noninteractive: a modifier alone
    # must not fall through into the text menu.
    if (args.percent is not None or args.boomerang) and not selectors:
        _remember(
            "--percent and --boomerang need --file, --start, and --end.",
            "video-speed --file clip.mp4 --start 0 --end 5",
        )
        out_err(
            "ERROR: --percent and --boomerang need --file, --start, and --end."
        )
        out_err("   Next: video-speed --file clip.mp4 --start 0 --end 5")
        return 1

    if selectors:
        if args.folder is not None:
            folder_path = Path(args.folder)
            if not folder_path.is_dir():
                _remember("Not a directory: {}".format(args.folder))
                out_err("ERROR: Not a directory: {}".format(args.folder))
                return 1
            files = get_mp4_files(folder_path)
            if not files:
                _remember("No MP4 files found!")
                out_err("No MP4 files found!")
                return 1
            if args.file is None:
                message = (
                    "--folder listed {} MP4 file(s); also pass --file, "
                    "--start, and --end for a non-interactive job."
                    .format(len(files))
                )
                _remember(message)
                out_err("ERROR: {}".format(message))
                return 1
        if args.file is None or args.start is None or args.end is None:
            _remember(
                "Non-interactive job needs --file, --start, and --end.",
                "video-speed --file clip.mp4 --start 0 --end 5",
            )
            out_err(
                "ERROR: Non-interactive job needs --file, --start, and --end."
            )
            out_err("   Next: video-speed --file clip.mp4 --start 0 --end 5")
            return 1
        percent = 100.0 if args.percent is None else args.percent
        return batch_session(
            args.file, args.start, args.end, percent, args.boomerang
        )

    if not stdin_is_tty():
        _remember(
            "No terminal for prompts.",
            "pass --file, --start, and --end, or run in a terminal.",
        )
        out_err(
            "ERROR: No terminal for prompts. "
            "Next: pass --file, --start, and --end, or run in a terminal."
        )
        return 1

    if _JSON_MODE:
        return _edit_json()

    # requirement-python-cli-logging: keep the console mirror off the frame.
    logger.quiet(True)
    action = open_text_menu()
    if action == "missing":
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
