# TP-PRE — runtime prerequisites (requirement-runtime-prerequisites, L-FFMPEG-01, L-IMPORT-01)
from __future__ import print_function, unicode_literals

import io
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from VideoSpeed import cli  # noqa: E402
from VideoSpeed.encoder import Encoder  # noqa: E402
from VideoSpeed.file_stage import FileStage  # noqa: E402
from VideoSpeed.media_info import MediaInfo  # noqa: E402
from VideoSpeed.run_output import RunOutput  # noqa: E402


class TestPrereq(unittest.TestCase):
    def test_tp_pre_01_missing_ffmpeg_preflight(self):
        """TP-PRE-01: missing ffmpeg → preflight error, no encode."""
        import shutil

        if shutil.which("ffmpeg") is not None:
            self.skipTest("ffmpeg is on PATH; cannot prove missing-binary path here")
        buf = io.StringIO()
        old = sys.stderr
        try:
            sys.stderr = buf
            output = RunOutput(cli.APP_NAME, cli._PKG_VERSION)
            encoder = Encoder(
                output, MediaInfo(output), FileStage(), cli.RATIO_MIN, cli.RATIO_MAX
            )
            ok = encoder.ensure_ffmpeg()
        finally:
            sys.stderr = old
        self.assertFalse(ok)
        text = buf.getvalue()
        self.assertIn("ffmpeg not found", text)
        self.assertIn("Install FFmpeg", text)

    def test_tp_pre_02_missing_opencv_duration(self):
        """TP-PRE-02: missing OpenCV → clear error on duration probe."""
        if "cv2" in sys.modules:
            self.skipTest("cv2 already imported")
        buf = io.StringIO()
        old = sys.stderr
        try:
            sys.stderr = buf
            output = RunOutput(cli.APP_NAME, cli._PKG_VERSION)
            dur = MediaInfo(output).get_duration_cv2(Path("/tmp/no-such-videospeed.mp4"))
        finally:
            sys.stderr = old
        self.assertEqual(dur, 0.0)
        text = buf.getvalue()
        if "cv2" not in sys.modules:
            self.assertIn("OpenCV", text)


if __name__ == "__main__":
    unittest.main()
