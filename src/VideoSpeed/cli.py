#!/usr/bin/env python
# =============================================================================
# VideoSpeed CLI — specialized from bootstrap interactive editor (cli.bootstrap-old)
# Domain: cut → speed/length → optional boomerang (MP4)
# Law keys: requirement-domain-videospeed, requirement-video-ffmpeg-pipeline,
#           requirement-python-cli-interface, requirement-python-error-handling,
#           requirement-runtime-prerequisites
# CIAO-Lite: Caution • Intentional • Anti-fragile • Over-protect
# =============================================================================
from __future__ import print_function, unicode_literals

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# -----------------------------------------------------------------------------
# Version (package SSOT lives in __init__.__version__; fallback for direct run)
# -----------------------------------------------------------------------------
try:
    from . import __version__ as _PKG_VERSION
except Exception:
    _PKG_VERSION = "1.0.5"

APP_NAME = "VideoSpeed"
CONSOLE_NAME = "video-speed"

# Length percent bounds (domain / pipeline guidance made fail-closed)
RATIO_MIN = 20.0
RATIO_MAX = 200.0


def out_info(msg):
    """User-facing informational line (stdout)."""
    print(msg)


def out_err(msg):
    """User-facing error line (stderr)."""
    print(msg, file=sys.stderr)


# =============================================================================
# CIAO-Lite Protection Zone — temp staging + publish (USB / multi-mount)
# System TMPDIR and removable media are often different filesystems.
# Bare os.rename / os.replace / Path.rename / Path.replace do NOT cross mounts
# (Linux EXDEV). Publish completed intermediates with shutil.move (rename same
# FS; copy+delete on EXDEV). Prefer temps next to final output when writable.
# Do NOT "simplify" back to bare os.replace from default /tmp onto USB paths.
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
    General Purpose: Publish src → dest using shutil.move (stdlib cross-FS safe).

    Same mount: rename. Different mount (USB, etc.): copy then remove source.
    Never use bare os.replace alone when src may live under system TMPDIR.
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
        out_err("ERROR: ffmpeg not found on PATH.")
        out_err("   Install FFmpeg and ensure `ffmpeg` is available.")
        out_err("   → https://ffmpeg.org/download.html")
        return False
    return True


def run_ffmpeg(cmd):
    """
    General Purpose: Run one FFmpeg command; fail closed on non-zero exit.
    Does not modify the user's source media path.
    """
    out_info("   Running → {}".format(" ".join(str(c) for c in cmd)))
    try:
        subprocess.run(cmd, check=True)
    except FileNotFoundError:
        out_err("ERROR: ffmpeg not found while running a encode step.")
        raise
    except subprocess.CalledProcessError as exc:
        out_err("ERROR: ffmpeg failed (exit {}).".format(exc.returncode))
        raise


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
        out_err("   Install with: pip install opencv-python")
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
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
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
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
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
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
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
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
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


def choose_index(prompt, count):
    """General Purpose: Prompt for 1-based index in [1, count]; re-prompt on error."""
    while True:
        raw = input(prompt).strip()
        try:
            idx = int(raw)
        except ValueError:
            out_info("   → Please type a number")
            continue
        if 1 <= idx <= count:
            return idx - 1
        out_info("   → Enter 1–{}".format(count))


def prompt_float(prompt, default=None):
    """General Purpose: Prompt for float; empty uses default if provided."""
    while True:
        raw = input(prompt).strip()
        if raw == "" and default is not None:
            return float(default)
        try:
            return float(raw.replace("%", ""))
        except ValueError:
            out_info("   → Please enter a number")


def prompt_yes_no(prompt, default_no=True):
    """General Purpose: y/n prompt; empty → default."""
    raw = input(prompt).strip().lower()
    if raw == "":
        return not default_no
    return raw in ("y", "yes")


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
    Temps are staged on the destination filesystem when possible so USB /
    removable media does not hit cross-device os.replace failures.
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
        speed_temp = make_temp_path(".mp4", final_out)

        out_info("1. Cutting segment...")
        cut_clip(video_path, start, end, cut_temp)
        out_info("2. Changing length to {}%...".format(int(ratio) if ratio == int(ratio) else ratio))
        speed_change(cut_temp, ratio, speed_temp)
        if boomerang:
            out_info("3. Creating boomerang...")
            add_boomerang(speed_temp, final_out)
        else:
            # Publish with shutil.move (same-FS rename or cross-FS copy+delete).
            promote_file(speed_temp, final_out)
            speed_temp = None  # moved away
        out_info("\nSUCCESS → {}\n".format(final_out))
        return final_out
    except (subprocess.CalledProcessError, FileNotFoundError, OSError, ValueError) as exc:
        err = getattr(exc, "errno", None)
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


def interactive_session():
    """
    General Purpose: Type N interactive domain session (empty argv default).
    requirement-domain-videospeed steps D-01..D-08
    """
    out_info("{} v{} — Cut → Speed → Optional Boomerang".format(APP_NAME, _PKG_VERSION))
    out_info("=" * 62)

    if not ensure_ffmpeg():
        return 1

    folder = input("Folder (Enter = current): ").strip() or "."
    folder_path = Path(folder)
    if not folder_path.is_dir():
        out_err("ERROR: Not a directory: {}".format(folder))
        return 1

    files = get_mp4_files(folder_path)
    if not files:
        out_err("No MP4 files found!")
        return 1

    for i, f in enumerate(files, 1):
        out_info("{:2d}. {}".format(i, f.name))

    sel = choose_index("\nChoose video (1–{}): ".format(len(files)), len(files))
    video_path = files[sel]

    duration = get_duration_cv2(video_path)
    if duration <= 0:
        out_err("ERROR: Could not read duration for {}".format(video_path.name))
        return 1

    out_info("\nSelected: {}".format(video_path.name))
    out_info("Duration: {} ({:.3f}s)\n".format(format_time(duration), duration))

    while True:
        out_info("Step 1/4 – Cut segment")
        start = prompt_float("   Start seconds (default 0.0): ", default=0.0)
        out_info("   → Using start: {:.3f}s".format(start))
        end = prompt_float(
            "   End seconds [{:.3f}]: ".format(duration),
            default=duration,
        )

        if not (0 <= start < end <= duration):
            out_info("Invalid range! Need 0 ≤ start < end ≤ duration.\n")
            continue

        out_info("\nStep 2/4 – Resize length ({}–{}%)".format(int(RATIO_MIN), int(RATIO_MAX)))
        ratio = prompt_float("   New length % [100%]: ", default=100.0)
        if not (RATIO_MIN <= ratio <= RATIO_MAX):
            out_info(
                "Invalid percent! Use {}–{} (got {}).\n".format(
                    int(RATIO_MIN), int(RATIO_MAX), ratio
                )
            )
            continue

        out_info("\nStep 3/4 – Add boomerang effect?")
        boomerang = prompt_yes_no(
            "   Make it go forward + backward (y/n) [n]: ",
            default_no=True,
        )

        process_job(video_path, start, end, ratio, boomerang)

        if not prompt_yes_no("Again? (y/n): ", default_no=True):
            break

    out_info("Done.")
    return 0


def build_parser():
    """General Purpose: Optional flags; bare invoke remains interactive (Type N)."""
    p = argparse.ArgumentParser(
        prog=CONSOLE_NAME,
        description=(
            "{} — interactive MP4 cut, length/speed change, optional boomerang."
            .format(APP_NAME)
        ),
    )
    p.add_argument(
        "--version",
        action="version",
        version="{} {}".format(APP_NAME, _PKG_VERSION),
    )
    return p


def main(argv=None):
    """
    General Purpose: Package entry for video-speed / python -m VideoSpeed.
    Empty argv → interactive domain session (Type N).
    """
    if argv is None:
        argv = sys.argv[1:]

    # Allow --help / --version without starting prompts
    if argv:
        parser = build_parser()
        parser.parse_args(argv)
        # No non-interactive job flags yet → if user passed only unknown, argparse exits
        # If parse succeeds with no action flags, fall through to interactive
        # (version/help already exited via argparse)

    return interactive_session()


if __name__ == "__main__":
    sys.exit(main() or 0)
