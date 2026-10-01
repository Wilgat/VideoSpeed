# =============================================================================
# About page composer.
# requirement-python-oop — class AboutPage. Line text stays on requirement-python-about.
# =============================================================================
from __future__ import print_function, unicode_literals

import os

from .check_system import CheckSystem
from .run_output import log_instantiated


class AboutPage:
    """Identity lines, install sentence, and the star box. One class, one module.

    The host check is CheckSystem. This class calls that object.
    """

    def __init__(
        self,
        check,
        app_name,
        version,
        major,
        minor,
        patch,
        author,
        updated,
        homepage,
        download_url,
        usage,
        console_name,
        logger=None,
    ):
        self.logger = logger
        log_instantiated(logger, "AboutPage")
        self.check = check if check is not None else CheckSystem(logger=logger)
        self.app_name = app_name
        self.version = version
        self.major = major
        self.minor = minor
        self.patch = patch
        self.author = author
        self.updated = updated
        self.homepage = homepage
        self.download_url = download_url
        self.usage = usage
        self.console_name = console_name

    def _is_source_checkout(self, path):
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

    def install_kind(self, path):
        """
        General Purpose: global, local, or uninstalled for an about location.
        A source checkout is uninstalled. A copy under the home directory is local.
        """
        path = os.path.realpath(path)
        parts = path.split(os.sep)
        packaged = "site-packages" in parts or "dist-packages" in parts
        if not packaged and self._is_source_checkout(path):
            return "uninstalled"
        home = os.path.realpath(os.path.expanduser("~"))
        in_home = path == home or path.startswith(home + os.sep)
        base = os.path.basename(path)
        if in_home and (packaged or base in (self.console_name, self.app_name)):
            return "local"
        if path.startswith("/usr/") or path.startswith("/opt/") or path.startswith("/bin/"):
            return "global"
        if packaged and not in_home:
            return "global"
        return "uninstalled"

    def install_sentence(self, kind):
        """General Purpose: The location sentence inside the about box."""
        if kind == "global":
            return "You are using the GLOBAL INSTALLED version, location:"
        if kind == "local":
            return "You are using the LOCAL INSTALLED version, location:"
        return "You are using an UNINSTALLED version, location:"

    def about_box_lines(
        self,
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
            usage = self.usage
        if location is None:
            location = self.check.self_location()
        if kind is None:
            kind = self.install_kind(location)
        if homepage is None:
            homepage = self.homepage
        if download_url is None:
            download_url = self.download_url
        if author is None:
            author = self.author
        if updated is None:
            updated = self.updated
        app = self.install_sentence(kind)
        python_exe = self.check.python_executable_name() or "python3"
        msg1 = "{} ({}.{}.{}) by {} on {}".format(
            self.app_name, self.major, self.minor, self.patch, author, updated
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
        for index in range(0, max_line):
            if len(msg[index]) > max_len:
                max_len = len(msg[index])
        boxed = []
        for index in range(0, max_line):
            boxed.append(msg[index] + (" " * (max_len - len(msg[index]))))
        star = "*" * (max_len + 4)
        blank = " " * max_len
        lines = [star, "* {} *".format(blank)]
        for row in boxed:
            lines.append("* {} *".format(row))
        lines.append("* {} *".format(blank))
        lines.append(star)
        return lines

    def framework_about(self):
        """
        General Purpose: About text for the menu result page.
        requirement-python-about: identity, host check, and the install box.
        """
        lines = [
            "{} {}".format(self.app_name, self.version),
            "Domain: Cut → speed/length → optional boomerang for MP4",
            "Runtime tools: FFmpeg (encode), OpenCV (duration probe)",
            "Entry points: video-speed, python -m VideoSpeed",
            "",
        ]
        lines.extend(self.check.check_system_lines())
        lines.append("")
        lines.extend(self.about_box_lines())
        return "\n".join(lines)
