# =============================================================================
# Temp staging and publish.
# requirement-python-oop — class FileStage.
# requirement-python-coding-style — publish with shutil.move.
# =============================================================================
from __future__ import print_function, unicode_literals

import os
import shutil
import tempfile
from pathlib import Path

from .run_output import log_instantiated


class FileStage:
    """Intermediate files and the publish step. One class, one module.

    System TMPDIR and removable media are often different filesystems.
    Move and publish files with shutil.move only.
    Do NOT call os.rename, os.replace, Path.rename, or Path.replace.
    Removable media (USB, SD, external disks) is often a different device from
    the system disk and from TMPDIR. Those calls raise EXDEV and do not copy.
    shutil.move renames on the same device and copies then removes the source
    on EXDEV. Prefer temps next to the final output when that parent is writable.
    Law: requirement-video-ffmpeg-pipeline, requirement-python-coding-style
    """

    def __init__(self, logger=None):
        self.logger = logger
        log_instantiated(logger, "FileStage")

    def staging_dir_for(self, dest_path):
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

    def make_temp_path(self, suffix, near_path):
        """
        General Purpose: Create a unique temp file path near near_path's directory
        (same FS when writable). File is created empty and closed; caller overwrites.
        """
        folder = self.staging_dir_for(near_path)
        fd, name = tempfile.mkstemp(suffix=suffix, prefix="videospeed_", dir=str(folder))
        os.close(fd)
        return Path(name)

    def promote_file(self, src, dest):
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
