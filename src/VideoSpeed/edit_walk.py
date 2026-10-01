# =============================================================================
# Shared edit questions: folder, file, start, end, percent, boomerang, again.
# requirement-python-oop — class EditWalk.
# The screen path and the --json stderr path both call this class.
# Question text stays on requirement-python-interactive-vs-noninteractive
# and requirement-python-json-output.
# =============================================================================
from __future__ import print_function, unicode_literals

import sys
from pathlib import Path


class EditWalk:
    """The edit question order. One class, one module."""

    def __init__(self, output, encoder, media, ratio_min, ratio_max):
        self.output = output
        self.encoder = encoder
        self.media = media
        self.ratio_min = ratio_min
        self.ratio_max = ratio_max

    def _err_line(self, text):
        """General Purpose: Prompt or re-ask line on stderr. Not the JSON object."""
        print(text, file=sys.stderr)

    def _prompt_line(self, label):
        """General Purpose: One answer from stdin. None means EOF."""
        self._err_line(label)
        try:
            return input("")
        except EOFError:
            return None

    def _prompt_float(self, label, default):
        """General Purpose: Float from stderr prompt. Empty uses default. None is EOF."""
        while True:
            raw = self._prompt_line(label)
            if raw is None:
                return None
            raw = raw.strip()
            if raw == "":
                return float(default)
            try:
                return float(raw.replace("%", ""))
            except ValueError:
                self._err_line("Please enter a number")

    def _prompt_yes_no(self, label, default_no=True):
        """General Purpose: y/n from stderr. Empty uses the default. None is EOF."""
        while True:
            raw = self._prompt_line(label)
            if raw is None:
                return None
            raw = raw.strip().lower()
            if raw == "":
                return not default_no
            if raw in ("y", "yes"):
                return True
            if raw in ("n", "no"):
                return False
            self._err_line("Please enter y or n")

    def _edit_json(self, args=None):
        """
        General Purpose: Same edit fields as the menu walk, without the text menu.

        Prompts go to stderr. stdout stays unused until main emits one JSON object.
        EOF ends the walk and does not encode the open question.
        A direct edit verb may already name the folder or the file.
        requirement-python-json-output.
        Last updated: 2026-10-01
        """
        self.output.json_walk = True
        if not self.encoder.ensure_ffmpeg():
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
                self.output._remember(
                    "File not found: {}".format(file_preset),
                    "pass an existing MP4 with --file.",
                )
                self._err_line("ERROR: File not found: {}".format(file_preset))
                self._err_line("   Next: pass an existing MP4 with --file.")
                return 1
            duration = self.media.get_duration_cv2(video_path)
            if duration <= 0:
                self._err_line("Could not read duration for {}".format(video_path.name))
                return 1
        else:
            folder_path = Path(folder_preset) if folder_preset else None
            while True:
                if folder_path is None:
                    raw = self._prompt_line("Folder (Enter = current):")
                    if raw is None:
                        return 0
                    folder = raw.strip() or "."
                    folder_path = Path(folder)
                if not folder_path.is_dir():
                    self._err_line("ERROR: Not a directory: {}".format(folder_path))
                    folder_path = None
                    continue
                files = self.media.get_mp4_files(folder_path)
                if not files:
                    self._err_line("No MP4 files found!")
                    folder_path = None
                    continue
                break

            while True:
                for index, item in enumerate(files, 1):
                    self._err_line("{:2d}. {}".format(index, item.name))
                raw = self._prompt_line("Choose video (1–{}):".format(len(files)))
                if raw is None:
                    return 0
                try:
                    idx = int(raw.strip())
                except ValueError:
                    self._err_line("Please type a number")
                    continue
                if not 1 <= idx <= len(files):
                    self._err_line("Enter 1–{}".format(len(files)))
                    continue
                video_path = files[idx - 1]
                duration = self.media.get_duration_cv2(video_path)
                if duration <= 0:
                    self._err_line("Could not read duration for {}".format(video_path.name))
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
            and self.encoder.valid_cut_range(start_preset, end_preset, duration)
        )

        while True:
            if preset_cut:
                start = float(start_preset)
                end = float(end_preset)
                preset_cut = False
            else:
                start = self._prompt_float(start_label, start_default)
                if start is None:
                    return 0
                end_default = duration if end_preset is None else float(end_preset)
                end = self._prompt_float(
                    "End seconds [{:.3f}]:".format(end_default),
                    end_default,
                )
                if end is None:
                    return 0
                if not self.encoder.valid_cut_range(start, end, duration):
                    self._err_line("Invalid range! Need 0 ≤ start < end ≤ duration.")
                    continue
            ratio = self._prompt_float(ratio_label, ratio_default)
            if ratio is None:
                return 0
            if not self.encoder.valid_percent(ratio):
                self._err_line(
                    "Invalid percent! Use {}–{} (got {}).".format(
                        int(self.ratio_min), int(self.ratio_max), ratio
                    )
                )
                continue
            boomerang = self._prompt_yes_no(boom_label, default_no=boom_default_no)
            if boomerang is None:
                return 0
            result = self.encoder.process_job(video_path, start, end, ratio, boomerang)
            if result is None:
                return 1
            self.output._remember_job(video_path, start, end, ratio, boomerang, result)
            again = self._prompt_yes_no("Again? (y/n):", default_no=True)
            if again is None or not again:
                return 0

    def run_screen(
        self,
        tui,
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
        General Purpose: Domain steps on the open text screen.

        The front board stays up. Each question is typed in the bottom box.
        Esc returns to that board. A direct verb may already know the folder
        or the file, and may pre-fill percent or boomerang.
        requirement-domain-videospeed, requirement-python-tui,
        requirement-python-interactive-vs-noninteractive.
        Last updated: 2026-10-01
        """
        notes = []
        ok = self.output._call_sunk(
            self.output._collect_lines(notes), self.encoder.ensure_ffmpeg
        )
        if not ok:
            tui._tui_notice(
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
                tui._tui_notice(
                    screen,
                    model,
                    ["ERROR: File not found: {}".format(video)],
                )
                return
            probe_notes = []
            duration = self.output._call_sunk(
                self.output._collect_lines(probe_notes),
                lambda: self.media.get_duration_cv2(video_path),
            )
            if duration <= 0:
                detail = probe_notes[-1] if probe_notes else (
                    "Could not read duration for {}".format(video_path.name)
                )
                tui._tui_notice(screen, model, [detail])
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
                    raw = tui._tui_read(screen, model, folder_lines)
                    if raw is None:
                        return
                    folder = raw.strip() or "."
                    folder_path = Path(folder)
                if not folder_path.is_dir():
                    model.error = "ERROR: Not a directory: {}".format(folder_path)
                    folder_path = None
                    continue
                files = self.media.get_mp4_files(folder_path)
                if not files:
                    tui._tui_notice(screen, model, ["No MP4 files found!"])
                    return
                break

            listing = ["{:2d}. {}".format(i, item.name) for i, item in enumerate(files, 1)]
            choose_lines = listing + ["", "Choose video (1–{}):".format(len(files))]
            while True:
                sel = tui._tui_index(screen, model, choose_lines, len(files))
                if sel is None:
                    return
                video_path = files[sel]
                probe_notes = []
                duration = self.output._call_sunk(
                    self.output._collect_lines(probe_notes),
                    lambda: self.media.get_duration_cv2(video_path),
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
            "Duration: {} ({:.3f}s)".format(self.media.format_time(duration), duration),
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
            and self.encoder.valid_cut_range(start_preset, end_preset, duration)
        )
        while True:
            if preset_cut:
                start = float(start_preset)
                end = float(end_preset)
                preset_cut = False
            else:
                start = tui._tui_float(
                    screen,
                    model,
                    header + ["", "Step 1/4 – Cut segment", start_label],
                    default=start_default,
                )
                if start is None:
                    return
                end_default = duration if end_preset is None else float(end_preset)
                end = tui._tui_float(
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
                if not self.encoder.valid_cut_range(start, end, duration):
                    model.error = "Invalid range! Need 0 ≤ start < end ≤ duration."
                    continue

            ratio = tui._tui_float(
                screen,
                model,
                [
                    "Step 2/4 – Resize length ({}–{}%)".format(
                        int(self.ratio_min), int(self.ratio_max)
                    ),
                    ratio_label,
                ],
                default=ratio_default,
            )
            if ratio is None:
                return
            if not self.encoder.valid_percent(ratio):
                model.error = "Invalid percent! Use {}–{} (got {}).".format(
                    int(self.ratio_min), int(self.ratio_max), ratio
                )
                continue

            boomerang = tui._tui_yes_no(
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
            tui._paint_lines(screen, model, "edit", body, pin_last=False)

            def paint_job(msg, _is_err, _body=body):
                for part in str(msg).splitlines():
                    if part.strip():
                        _body.append(part)
                model.buffer = ""
                model.cursor = 0
                model.focus = "list"
                model.error = ""
                tui._paint_lines(screen, model, "edit", _body, pin_last=False)

            result = self.output._call_sunk(paint_job, lambda: self.encoder.process_job(
                video_path, start, end, ratio, boomerang
            ))
            self.encoder._restore_text_screen()
            if result is None:
                closing = "Not saved. Again? (y/n):"
            else:
                closing = "Saved {} — Again? (y/n):".format(Path(result).name)
            again = tui._tui_yes_no(
                screen,
                model,
                [closing],
                default_no=True,
            )
            if again is None:
                return
            if not again:
                tui._tui_notice(screen, model, ["Done."])
                return
