# =============================================================================
# MP4 listing and duration.
# requirement-python-oop — class MediaInfo.
# =============================================================================
from __future__ import print_function, unicode_literals

from pathlib import Path




class MediaInfo:
    """MP4 paths, duration, and the clock format. One class, one module."""

    def __init__(self, output, logger=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="MediaInfo")
        self.output = output

    def get_mp4_files(self, folder="."):
        """General Purpose: Recursively list MP4 files under folder (case variants)."""
        folder = Path(folder)
        if not folder.is_dir():
            return []
        files = list(folder.rglob("*.mp4")) + list(folder.rglob("*.MP4"))
        files = [item for item in files if item.is_file()]
        seen = set()
        unique = []
        for item in files:
            key = str(item.resolve()) if item.exists() else str(item)
            if key not in seen:
                seen.add(key)
                unique.append(item)
        unique.sort(key=lambda found: found.name.lower())
        return unique

    def get_duration_cv2(self, video_path):
        """
        General Purpose: Probe duration via OpenCV (lazy import).
        Returns seconds; 0.0 if unreadable.
        """
        try:
            import cv2
        except ImportError:
            self.output.out_err("ERROR: OpenCV (cv2) is not installed.")
            self.output.out_err("   Install with: pip install 'opencv-python-headless>=5.0.0.93'")
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

    def format_time(self, seconds):
        """General Purpose: Format seconds as H:MM:SS.mmm or M:SS.mmm."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        if hours == 0:
            return "{:02d}:{:06.3f}".format(minutes, secs)
        return "{:02d}:{:02d}:{:06.3f}".format(hours, minutes, secs)
