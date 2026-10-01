# =============================================================================
# User-facing lines and the one JSON object.
# requirement-python-oop — class RunOutput.
# requirement-python-json-output — object shape stays there.
# =============================================================================
from __future__ import print_function, unicode_literals

import json
import sys


def log_instantiated(logger, class_name):
    """Record one product object on the process logger. No second logger."""
    if logger is None:
        return
    logger.log_message("instantiated", component=class_name)


class RunOutput:
    """Stdout, stderr, the message sink, and the JSON result. One class, one module."""

    def __init__(self, app_name, version, logger=None):
        self.logger = logger
        log_instantiated(logger, "RunOutput")
        self.app_name = app_name
        self.version = version
        self.json_mode = False
        self.json_walk = False
        self.json_error = None
        self.json_next = None
        self.json_jobs = []
        self.message_sink = None

    def out_info(self, msg):
        """User-facing informational line (stdout, or the open text screen)."""
        if self.json_mode:
            return
        if self.message_sink is not None:
            self.message_sink(msg, False)
            return
        print(msg)

    def out_err(self, msg):
        """User-facing error line (stderr, or the open text screen)."""
        if self.message_sink is not None:
            self.message_sink(msg, True)
            return
        print(msg, file=sys.stderr)

    def _json_reset(self):
        """General Purpose: Clear the JSON result before a new main()."""
        self.json_mode = False
        self.json_walk = False
        self.json_error = None
        self.json_next = None
        self.json_jobs = []

    def _remember(self, message, next_step=None):
        """General Purpose: Keep the first terminal failure for the JSON object."""
        if not self.json_mode:
            return
        if self.json_error is None and message:
            self.json_error = message
        if next_step and self.json_next is None:
            self.json_next = next_step

    def _remember_job(self, video_path, start, end, percent, boomerang, output):
        """General Purpose: Append one finished job to the JSON result."""
        if not self.json_mode:
            return
        self.json_jobs.append({
            "file": str(video_path),
            "start": float(start),
            "end": float(end),
            "percent": float(percent),
            "boomerang": bool(boomerang),
            "output": str(output),
        })

    def _emit_json(self, mode, code):
        """General Purpose: Write the only stdout bytes for a --json run."""
        ok = code == 0 and self.json_error is None
        doc = {
            "ok": ok,
            "mode": mode,
            "app": self.app_name,
            "version": self.version,
            "error": self.json_error,
            "next": self.json_next,
            "jobs": list(self.json_jobs),
        }
        sys.stdout.write(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
        return 0 if ok else (code or 1)

    def _call_sunk(self, sink, fn):
        """General Purpose: Run fn while user-facing lines go to sink."""
        previous = self.message_sink
        self.message_sink = sink
        try:
            return fn()
        finally:
            self.message_sink = previous

    def _collect_lines(self, bucket):
        """General Purpose: Sink that keeps non-empty user-facing lines."""
        def sink(msg, _is_err):
            for part in str(msg).splitlines():
                if part.strip():
                    bucket.append(part)
        return sink
