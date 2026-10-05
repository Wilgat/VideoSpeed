# =============================================================================
# Cut, speed, and optional boomerang.
# requirement-python-oop — class Encoder.
# requirement-video-ffmpeg-pipeline — order stays cut, then speed, then boomerang.
# requirement-python-time-consuming-process — run_ffmpeg waits and flashes one line.
# =============================================================================
from __future__ import print_function, unicode_literals

import os
import shutil
import subprocess
import sys
from pathlib import Path

from .file_stage import FileStage



class Encoder:
    """FFmpeg steps and one job. One class, one module.

    At 100% length, process_job publishes the cut and skips the speed encode.
    Every command uses -nostdin. run_ffmpeg passes stdin DEVNULL.
    While the child runs, one line flashes please wait for time consuming process.
    """

    FLASH_SECONDS = 0.5
    WAIT_PHRASE = "please wait for time consuming process"
    WAIT_MARK_ON = "\u25cf"
    WAIT_MARK_OFF = "\u25cb"

    def __init__(self, output, media, stage, ratio_min, ratio_max, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="Encoder")
        self.output = output
        self.media = media
        self.stage = stage if stage is not None else FileStage(logger=logger)
        self.ratio_min = ratio_min
        self.ratio_max = ratio_max
        self._plain_wait_open = False

    def _wait_line(self, mark):
        """General Purpose: One flashing wait line. Three spaces, bullet, phrase."""
        return "   {} {}".format(mark, self.WAIT_PHRASE)

    def _show_wait(self, mark):
        """General Purpose: Paint or rewrite the one wait line. --json stays silent."""
        if self.output.json_mode:
            return
        line = self._wait_line(mark)
        if self.output.message_sink is not None:
            self.output.out_info(line)
            return
        sys.stdout.write("\r" + line)
        sys.stdout.flush()
        self._plain_wait_open = True

    def _close_plain_wait(self):
        """General Purpose: End the rewritten terminal line so the next line is new."""
        if self._plain_wait_open:
            sys.stdout.write("\n")
            sys.stdout.flush()
            self._plain_wait_open = False

    def _stop_child(self, proc):
        """General Purpose: Stop a child that is still running, then wait for it.

        This is the child stop subprocess.run already performed. It is not Exit?.
        """
        if proc is None or proc.poll() is not None:
            return
        proc.kill()
        proc.wait()

    def ensure_ffmpeg(self):
        """
        General Purpose: Fail closed if the system ffmpeg binary is not on PATH.
        requirement-runtime-prerequisites / requirement-video-ffmpeg-pipeline
        """
        if shutil.which("ffmpeg") is None:
            self.output._remember(
                "ffmpeg not found on PATH.",
                "Install FFmpeg and ensure ffmpeg is available.",
            )
            self.output.out_err("ERROR: ffmpeg not found on PATH.")
            self.output.out_err("   Install FFmpeg and ensure `ffmpeg` is available.")
            self.output.out_err("   → https://ffmpeg.org/download.html")
            return False
        return True

    def _restore_text_screen(self):
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

    def run_ffmpeg(self, cmd):
        """
        General Purpose: Run one FFmpeg command; fail closed on non-zero exit.
        requirement-python-time-consuming-process — this call waits in the foreground.
        The half-second flash does not stop the child.
        Does not modify the user's source media path.
        Captured pipes keep the flashing line and a JSON object free of FFmpeg text.
        -nostdin stops FFmpeg from waiting on the terminal at the end of a step.
        """
        mark = self.WAIT_MARK_ON
        self._show_wait(mark)
        proc = None
        try:
            proc = subprocess.Popen(
                cmd,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            stderr = b""
            while True:
                try:
                    _stdout, stderr = proc.communicate(timeout=self.FLASH_SECONDS)
                    break
                except subprocess.TimeoutExpired:
                    mark = (
                        self.WAIT_MARK_OFF
                        if mark == self.WAIT_MARK_ON
                        else self.WAIT_MARK_ON
                    )
                    self._show_wait(mark)
            if proc.returncode != 0:
                err = (stderr or b"").decode("utf-8", "replace").strip()
                if err:
                    self.output.out_err(err)
                raise subprocess.CalledProcessError(proc.returncode, cmd)
        except FileNotFoundError:
            self.output.out_err("ERROR: ffmpeg not found while running a encode step.")
            raise
        except subprocess.CalledProcessError as exc:
            self.output.out_err("ERROR: ffmpeg failed (exit {}).".format(exc.returncode))
            raise
        except BaseException:
            self._stop_child(proc)
            raise
        finally:
            self._close_plain_wait()
            self._restore_text_screen()

    def cut_clip(self, src, start, end, output_path):
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
        self.run_ffmpeg(cmd)

    def _atempo_filters(self, speed):
        """
        General Purpose: Build atempo chain. FFmpeg single atempo accepts 0.5–100.
        speed = playback rate ( >1 faster, shorter wall time for same content).
        """
        filters = []
        remaining = float(speed)
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

    def speed_change(self, input_path, ratio_percent, output_path):
        """
        General Purpose: Change clip length to ratio_percent of original cut length.
        100 = unchanged duration intent; 50 ≈ half length (faster); 200 ≈ double length.
        """
        speed = 100.0 / float(ratio_percent)
        atempo = self._atempo_filters(speed)
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
        self.run_ffmpeg(cmd)

    def add_boomerang(self, forward_clip, final_output):
        """
        General Purpose: Concat forward + reverse of forward_clip into final_output.
        Intermediate reverse/list files are staged near final_output (USB-safe).
        Cleans reverse and concat-list temps on all paths.
        """
        reverse_clip = None
        concat_list = None
        try:
            reverse_clip = self.stage.make_temp_path(".mp4", final_output)
            self.run_ffmpeg([
                "ffmpeg", "-nostdin", "-y", "-hide_banner", "-loglevel", "error",
                "-i", str(forward_clip),
                "-vf", "reverse", "-af", "areverse",
                str(reverse_clip),
            ])
            concat_list = self.stage.make_temp_path(".txt", final_output)
            with open(str(concat_list), "w", encoding="utf-8") as handle:
                handle.write("file '{}'\n".format(Path(forward_clip).resolve().as_posix()))
                handle.write("file '{}'\n".format(Path(reverse_clip).resolve().as_posix()))
            self.run_ffmpeg([
                "ffmpeg", "-nostdin", "-y", "-hide_banner", "-loglevel", "error",
                "-f", "concat", "-safe", "0",
                "-i", str(concat_list),
                "-c", "copy",
                str(final_output),
            ])
        finally:
            for path in (reverse_clip, concat_list):
                if path is not None and Path(path).exists():
                    try:
                        os.unlink(path)
                    except OSError:
                        pass

    def valid_cut_range(self, start, end, duration):
        """General Purpose: True iff 0 <= start < end <= duration (no encode)."""
        try:
            start = float(start)
            end = float(end)
            duration = float(duration)
        except (TypeError, ValueError):
            return False
        return 0.0 <= start < end <= duration

    def valid_percent(self, ratio):
        """General Purpose: True iff length percent is inside 20–200."""
        try:
            ratio = float(ratio)
        except (TypeError, ValueError):
            return False
        return self.ratio_min <= ratio <= self.ratio_max

    def _length_unchanged(self, ratio):
        """General Purpose: True when the asked length is 100% of the cut."""
        try:
            return abs(float(ratio) - 100.0) <= 1e-6
        except (TypeError, ValueError):
            return False

    def build_output_name(self, video_path, start, end, ratio, boomerang):
        """General Purpose: Domain output naming pattern beside source."""
        name = "{}_cut{:.1f}-{:.1f}s_{:d}pct".format(
            video_path.stem, start, end, int(ratio)
        )
        if boomerang:
            name += "_BOOMERANG"
        name += ".mp4"
        return video_path.parent / name

    def process_job(self, video_path, start, end, ratio, boomerang):
        """
        General Purpose: Run cut → speed → optional boomerang pipeline.
        Never overwrites source; cleans intermediate temps.
        Temps are staged on the destination filesystem when possible.
        Publish uses shutil.move so removable media does not depend on os.rename
        or os.replace.
        Returns final Path or None on failure.
        """
        final_out = self.build_output_name(video_path, start, end, ratio, boomerang)
        self.output.out_info("\nProcessing → {}\n".format(final_out))
        self.output.out_info("   Staging dir → {}".format(self.stage.staging_dir_for(final_out)))

        cut_temp = None
        speed_temp = None
        try:
            cut_temp = self.stage.make_temp_path(".mp4", final_out)
            self.output.out_info("1. Cutting segment...")
            self.cut_clip(video_path, start, end, cut_temp)
            if self._length_unchanged(ratio):
                # 100% keeps the cut. A second encode (preset medium, +faststart)
                # holds the text screen and leaves the clip on its temporary name
                # until that pass returns.
                self.output.out_info("2. Length stays 100%...")
                forward = cut_temp
            else:
                speed_temp = self.stage.make_temp_path(".mp4", final_out)
                shown = int(ratio) if ratio == int(ratio) else ratio
                self.output.out_info("2. Changing length to {}%...".format(shown))
                self.speed_change(cut_temp, ratio, speed_temp)
                forward = speed_temp
            if boomerang:
                self.output.out_info("3. Creating boomerang...")
                self.add_boomerang(forward, final_out)
            else:
                self.stage.promote_file(forward, final_out)
                if forward is cut_temp:
                    cut_temp = None
                else:
                    speed_temp = None
            self.output.out_info("\nSUCCESS → {}\n".format(final_out.name))
            return final_out
        except (subprocess.CalledProcessError, FileNotFoundError, OSError, ValueError) as exc:
            err = getattr(exc, "errno", None)
            self.output._remember("Job failed: {}".format(exc))
            self.output.out_err("Job failed: {}".format(exc))
            if err in (getattr(os, "EXDEV", 18), 18):
                self.output.out_err(
                    "   Hint: cross-filesystem rename failed (USB vs system temp). "
                    "Temps should stage next to the output; publish uses shutil.move. "
                    "Check USB write permission and free space."
                )
            return None
        finally:
            for path in (cut_temp, speed_temp):
                if path is not None and Path(path).exists():
                    try:
                        os.unlink(path)
                    except OSError:
                        pass

    def batch_session(self, file_path, start, end, percent, boomerang):
        """
        General Purpose: One non-interactive job. Fail closed on bad range/percent
        before encode. requirement-python-interactive-vs-noninteractive.
        """
        video_path = Path(file_path)
        if not video_path.is_file():
            self.output._remember(
                "File not found: {}".format(file_path),
                "pass an existing MP4 with --file.",
            )
            self.output.out_err("ERROR: File not found: {}".format(file_path))
            self.output.out_err("   Next: pass an existing MP4 with --file.")
            return 1
        if not self.ensure_ffmpeg():
            return 1
        duration = self.media.get_duration_cv2(video_path)
        if duration <= 0:
            self.output._remember("Could not read duration for {}".format(video_path.name))
            self.output.out_err("ERROR: Could not read duration for {}".format(video_path.name))
            return 1
        if not self.valid_cut_range(start, end, duration):
            message = (
                "Invalid range. Need 0 <= start < end <= duration ({:.3f}s)."
                .format(duration)
            )
            self.output._remember(message)
            self.output.out_err("ERROR: {}".format(message))
            return 1
        if not self.valid_percent(percent):
            message = "Invalid percent. Use {}–{} (got {}).".format(
                int(self.ratio_min), int(self.ratio_max), percent
            )
            self.output._remember(message)
            self.output.out_err("ERROR: {}".format(message))
            return 1
        result = self.process_job(video_path, start, end, percent, boomerang)
        if result is None:
            return 1
        self.output._remember_job(video_path, start, end, percent, boomerang, result)
        return 0
