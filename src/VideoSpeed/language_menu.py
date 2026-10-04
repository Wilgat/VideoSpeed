# =============================================================================
# Menu language for the text screen.
# requirement-python-cli-language — codes, file, and the words that follow.
# requirement-python-oop — class LanguageMenu.
# The English row numbers stay on MenuPainter. This class does not paint.
# =============================================================================
from __future__ import annotations

import os

from .menu_painter import MenuPainter


class LanguageMenu:
    """Thirteen menu languages. English is the default. One class, one module.

    Load runs once, in this constructor. A later pick writes the file and
    changes the code for the rest of this process. It does not load again.
    """

    ENV_NAME = "VIDEOSPEED_LANG"
    FILE_NAME = "language"
    ASSIGNED = (
        ("en", 41, "English"),
        ("zh-Hans", 42, "简体中文"),
        ("zh-Hant", 43, "繁體中文"),
        ("es", 44, "Español"),
        ("ar", 45, "العربية"),
        ("fr", 46, "Français"),
        ("pt", 47, "Português"),
        ("ru", 48, "Русский"),
        ("de", 49, "Deutsch"),
        ("ja", 50, "日本語"),
        ("ko", 51, "한국어"),
        ("nl", 52, "Nederlands"),
        ("el", 53, "Ελληνικά"),
    )
    CODES = tuple(item[0] for item in ASSIGNED)
    RESERVED = (40, 54, 55, 56, 57, 58, 59)

    PATH_LABEL = {
        "en": "Path",
        "zh-Hans": "路径",
        "zh-Hant": "路徑",
        "es": "Ruta",
        "ar": "المسار",
        "fr": "Chemin",
        "pt": "Caminho",
        "ru": "Путь",
        "de": "Pfad",
        "ja": "パス",
        "ko": "경로",
        "nl": "Pad",
        "el": "Διαδρομή",
    }
    CAT_LANGUAGE = {
        "en": "language",
        "zh-Hans": "语言",
        "zh-Hant": "語言",
        "es": "idioma",
        "ar": "لغة",
        "fr": "langue",
        "pt": "idioma",
        "ru": "язык",
        "de": "Sprache",
        "ja": "言語",
        "ko": "언어",
        "nl": "taal",
        "el": "γλώσσα",
    }
    LANGUAGE_LONG = {
        "en": "display language for this menu",
        "zh-Hans": "这个菜单的显示语言",
        "zh-Hant": "這個選單的顯示語言",
        "es": "idioma de este menú",
        "ar": "لغة العرض لهذه القائمة",
        "fr": "langue d'affichage de ce menu",
        "pt": "idioma de exibição deste menu",
        "ru": "язык отображения этого меню",
        "de": "Anzeigesprache dieses Menüs",
        "ja": "このメニューの表示言語",
        "ko": "이 메뉴의 표시 언어",
        "nl": "weergavetaal van dit menu",
        "el": "γλώσσα εμφάνισης αυτού του μενού",
    }
    CAT_SYSTEM_LOG = {
        "en": "system-log",
        "zh-Hans": "系统日志",
        "zh-Hant": "系統日誌",
        "es": "registro",
        "ar": "السجل",
        "fr": "journal",
        "pt": "registo",
        "ru": "журнал",
        "de": "Systemprotokoll",
        "ja": "システムログ",
        "ko": "시스템-로그",
        "nl": "systeemlog",
        "el": "αρχείο-καταγραφής",
    }
    SYSTEM_LOG_LONG = {
        "en": "view, clear, and the log folder",
        "zh-Hans": "查看、清空，以及日志文件夹",
        "zh-Hant": "檢視、清空，以及日誌資料夾",
        "es": "ver, vaciar y la carpeta de registro",
        "ar": "عرض ومسح ومجلد السجل",
        "fr": "voir, vider, et le dossier du journal",
        "pt": "ver, esvaziar e a pasta de registo",
        "ru": "просмотр, очистка и папка журнала",
        "de": "ansehen, leeren und der Protokollordner",
        "ja": "表示、消去、およびログフォルダ",
        "ko": "보기, 비우기, 그리고 로그 폴더",
        "nl": "bekijken, legen en de logmap",
        "el": "προβολή, εκκένωση και ο φάκελος καταγραφής",
    }
    CAT_SELF = {
        "en": "self-management",
        "zh-Hans": "自我管理",
        "zh-Hant": "自我管理",
        "es": "autogestión",
        "ar": "إدارة-ذاتية",
        "fr": "autogestion",
        "pt": "autogestão",
        "ru": "самоуправление",
        "de": "Selbstverwaltung",
        "ja": "自己管理",
        "ko": "자기관리",
        "nl": "zelfbeheer",
        "el": "αυτοδιαχείριση",
    }
    SELF_LONG = {
        "en": "version, about, and pip lifecycle",
        "zh-Hans": "版本、关于，以及 pip 生命周期",
        "zh-Hant": "版本、關於，以及 pip 生命週期",
        "es": "versión, acerca de, y el ciclo de pip",
        "ar": "الإصدار وحول ودورة pip",
        "fr": "version, à propos, et le cycle pip",
        "pt": "versão, acerca de, e o ciclo do pip",
        "ru": "версия, о программе и цикл pip",
        "de": "Version, Info und pip-Lebenszyklus",
        "ja": "バージョン、概要、および pip のライフサイクル",
        "ko": "버전, 정보, 그리고 pip 수명 주기",
        "nl": "versie, info en de pip-levenscyclus",
        "el": "έκδοση, σχετικά και ο κύκλος pip",
    }
    EXIT_SHORT = {
        "en": "Exit",
        "zh-Hans": "离开",
        "zh-Hant": "離開",
        "es": "Salir",
        "ar": "خروج",
        "fr": "Quitter",
        "pt": "Sair",
        "ru": "Выход",
        "de": "Beenden",
        "ja": "終了",
        "ko": "종료",
        "nl": "Afsluiten",
        "el": "Έξοδος",
    }
    EXIT_LONG = {
        "en": "leave",
        "zh-Hans": "离开",
        "zh-Hant": "離開",
        "es": "salir",
        "ar": "خروج",
        "fr": "quitter",
        "pt": "sair",
        "ru": "выход",
        "de": "beenden",
        "ja": "終了",
        "ko": "종료",
        "nl": "afsluiten",
        "el": "έξοδος",
    }
    BACK_SHORT = {
        "en": "Back",
        "zh-Hans": "返回",
        "zh-Hant": "返回",
        "es": "Atrás",
        "ar": "رجوع",
        "fr": "Retour",
        "pt": "Voltar",
        "ru": "Назад",
        "de": "Zurück",
        "ja": "戻る",
        "ko": "뒤로",
        "nl": "Terug",
        "el": "Πίσω",
    }
    BACK_LONG = {
        "en": "return to the main menu",
        "zh-Hans": "返回主菜单",
        "zh-Hant": "返回主選單",
        "es": "volver al menú principal",
        "ar": "الرجوع إلى القائمة الرئيسية",
        "fr": "revenir au menu principal",
        "pt": "voltar ao menu principal",
        "ru": "вернуться в главное меню",
        "de": "zurück zum Hauptmenü",
        "ja": "メインメニューに戻る",
        "ko": "주 메뉴로 돌아가기",
        "nl": "terug naar het hoofdmenu",
        "el": "επιστροφή στο κύριο μενού",
    }
    MAIN_MENU = {
        "en": "main menu",
        "zh-Hans": "主菜单",
        "zh-Hant": "主選單",
        "es": "menú principal",
        "ar": "القائمة الرئيسية",
        "fr": "menu principal",
        "pt": "menu principal",
        "ru": "главное меню",
        "de": "Hauptmenü",
        "ja": "メインメニュー",
        "ko": "주 메뉴",
        "nl": "hoofdmenu",
        "el": "κύριο μενού",
    }
    UNKNOWN = {
        "en": "That choice is not on this list. Pick a listed number.",
        "zh-Hans": "这个选择不在清单上。请选一个列出的编号。",
        "zh-Hant": "這個選擇不在清單上。請選一個列出的編號。",
        "es": "Esa opción no está en esta lista. Elija un número de la lista.",
        "ar": "هذا الخيار ليس في هذه القائمة. اختر رقما معروضا.",
        "fr": "Ce choix n'est pas dans cette liste. Choisissez un numéro affiché.",
        "de": "Diese Auswahl steht nicht auf dieser Liste. Wählen Sie eine angezeigte Nummer.",
        "ja": "その選択はこの一覧にありません。表示された番号を選んでください。",
        "ko": "그 선택은 이 목록에 없습니다. 표시된 번호를 고르세요.",
        "pt": "Essa escolha não está nesta lista. Escolha um número listado.",
        "ru": "Этого пункта нет в списке. Выберите номер из списка.",
        "nl": "Die keuze staat niet op deze lijst. Kies een vermeld nummer.",
        "el": "Αυτή η επιλογή δεν είναι σε αυτή τη λίστα. Επιλέξτε έναν αριθμό της λίστας.",
    }
    SAVED = {
        "en": "Menu language is English",
        "zh-Hans": "菜单语言是简体中文",
        "zh-Hant": "選單語言是繁體中文",
        "es": "El idioma del menú es español",
        "ar": "لغة القائمة هي العربية",
        "fr": "La langue du menu est le français",
        "pt": "O idioma do menu é português",
        "ru": "Язык меню — русский",
        "de": "Die Menüsprache ist Deutsch",
        "ja": "メニューの言語は日本語",
        "ko": "메뉴 언어는 한국어",
        "nl": "De menutaal is Nederlands",
        "el": "Η γλώσσα του μενού είναι ελληνικά",
    }
    FAILED = {
        "en": "Could not save the menu language",
        "zh-Hans": "无法保存菜单语言",
        "zh-Hant": "無法儲存選單語言",
        "es": "No se pudo guardar el idioma del menú",
        "ar": "تعذر حفظ لغة القائمة",
        "fr": "Impossible d'enregistrer la langue du menu",
        "pt": "Não foi possível guardar o idioma do menu",
        "ru": "Не удалось сохранить язык меню",
        "de": "Die Menüsprache konnte nicht gespeichert werden",
        "ja": "メニューの言語を保存できませんでした",
        "ko": "메뉴 언어를 저장하지 못했습니다",
        "nl": "De menutaal kon niet worden opgeslagen",
        "el": "Δεν ήταν δυνατή η αποθήκευση της γλώσσας του μενού",
    }
    # Language-board explain for each UI code, in ASSIGNED order.
    # English explains live on MenuPainter.LANG_ROWS.
    LANG_LONG = {
        "zh-Hans": (
            "这个菜单改用英文",
            "这个菜单改用简体中文",
            "这个菜单改用繁体中文",
            "这个菜单改用西班牙文",
            "这个菜单改用阿拉伯文",
            "这个菜单改用法文",
            "这个菜单改用葡萄牙文",
            "这个菜单改用俄文",
            "这个菜单改用德文",
            "这个菜单改用日文",
            "这个菜单改用韩文",
            "这个菜单改用荷兰文",
            "这个菜单改用希腊文",
        ),
        "zh-Hant": (
            "這個選單改用英文",
            "這個選單改用簡體中文",
            "這個選單改用繁體中文",
            "這個選單改用西班牙文",
            "這個選單改用阿拉伯文",
            "這個選單改用法文",
            "這個選單改用葡萄牙文",
            "這個選單改用俄文",
            "這個選單改用德文",
            "這個選單改用日文",
            "這個選單改用韓文",
            "這個選單改用荷蘭文",
            "這個選單改用希臘文",
        ),
        "es": (
            "usar inglés en este menú",
            "usar chino simplificado en este menú",
            "usar chino tradicional en este menú",
            "usar español en este menú",
            "usar árabe en este menú",
            "usar francés en este menú",
            "usar portugués en este menú",
            "usar ruso en este menú",
            "usar alemán en este menú",
            "usar japonés en este menú",
            "usar coreano en este menú",
            "usar neerlandés en este menú",
            "usar griego en este menú",
        ),
        "ar": (
            "استخدام الإنجليزية لهذه القائمة",
            "استخدام الصينية المبسطة لهذه القائمة",
            "استخدام الصينية التقليدية لهذه القائمة",
            "استخدام الإسبانية لهذه القائمة",
            "استخدام العربية لهذه القائمة",
            "استخدام الفرنسية لهذه القائمة",
            "استخدام البرتغالية لهذه القائمة",
            "استخدام الروسية لهذه القائمة",
            "استخدام الألمانية لهذه القائمة",
            "استخدام اليابانية لهذه القائمة",
            "استخدام الكورية لهذه القائمة",
            "استخدام الهولندية لهذه القائمة",
            "استخدام اليونانية لهذه القائمة",
        ),
        "fr": (
            "utiliser l'anglais pour ce menu",
            "utiliser le chinois simplifié pour ce menu",
            "utiliser le chinois traditionnel pour ce menu",
            "utiliser l'espagnol pour ce menu",
            "utiliser l'arabe pour ce menu",
            "utiliser le français pour ce menu",
            "utiliser le portugais pour ce menu",
            "utiliser le russe pour ce menu",
            "utiliser l'allemand pour ce menu",
            "utiliser le japonais pour ce menu",
            "utiliser le coréen pour ce menu",
            "utiliser le néerlandais pour ce menu",
            "utiliser le grec pour ce menu",
        ),
        "pt": (
            "usar inglês neste menu",
            "usar chinês simplificado neste menu",
            "usar chinês tradicional neste menu",
            "usar espanhol neste menu",
            "usar árabe neste menu",
            "usar francês neste menu",
            "usar português neste menu",
            "usar russo neste menu",
            "usar alemão neste menu",
            "usar japonês neste menu",
            "usar coreano neste menu",
            "usar neerlandês neste menu",
            "usar grego neste menu",
        ),
        "ru": (
            "использовать английский для этого меню",
            "использовать упрощённый китайский для этого меню",
            "использовать традиционный китайский для этого меню",
            "использовать испанский для этого меню",
            "использовать арабский для этого меню",
            "использовать французский для этого меню",
            "использовать португальский для этого меню",
            "использовать русский для этого меню",
            "использовать немецкий для этого меню",
            "использовать японский для этого меню",
            "использовать корейский для этого меню",
            "использовать нидерландский для этого меню",
            "использовать греческий для этого меню",
        ),
        "de": (
            "Englisch für dieses Menü verwenden",
            "Vereinfachtes Chinesisch für dieses Menü verwenden",
            "Traditionelles Chinesisch für dieses Menü verwenden",
            "Spanisch für dieses Menü verwenden",
            "Arabisch für dieses Menü verwenden",
            "Französisch für dieses Menü verwenden",
            "Portugiesisch für dieses Menü verwenden",
            "Russisch für dieses Menü verwenden",
            "Deutsch für dieses Menü verwenden",
            "Japanisch für dieses Menü verwenden",
            "Koreanisch für dieses Menü verwenden",
            "Niederländisch für dieses Menü verwenden",
            "Griechisch für dieses Menü verwenden",
        ),
        "ja": (
            "このメニューを英語にする",
            "このメニューを簡体字中国語にする",
            "このメニューを繁体字中国語にする",
            "このメニューをスペイン語にする",
            "このメニューをアラビア語にする",
            "このメニューをフランス語にする",
            "このメニューをポルトガル語にする",
            "このメニューをロシア語にする",
            "このメニューをドイツ語にする",
            "このメニューを日本語にする",
            "このメニューを韓国語にする",
            "このメニューをオランダ語にする",
            "このメニューをギリシャ語にする",
        ),
        "ko": (
            "이 메뉴를 영어로",
            "이 메뉴를 간체 중국어로",
            "이 메뉴를 번체 중국어로",
            "이 메뉴를 스페인어로",
            "이 메뉴를 아랍어로",
            "이 메뉴를 프랑스어로",
            "이 메뉴를 포르투갈어로",
            "이 메뉴를 러시아어로",
            "이 메뉴를 독일어로",
            "이 메뉴를 일본어로",
            "이 메뉴를 한국어로",
            "이 메뉴를 네덜란드어로",
            "이 메뉴를 그리스어로",
        ),
        "nl": (
            "Engels voor dit menu gebruiken",
            "Vereenvoudigd Chinees voor dit menu gebruiken",
            "Traditioneel Chinees voor dit menu gebruiken",
            "Spaans voor dit menu gebruiken",
            "Arabisch voor dit menu gebruiken",
            "Frans voor dit menu gebruiken",
            "Portugees voor dit menu gebruiken",
            "Russisch voor dit menu gebruiken",
            "Duits voor dit menu gebruiken",
            "Japans voor dit menu gebruiken",
            "Koreaans voor dit menu gebruiken",
            "Nederlands voor dit menu gebruiken",
            "Grieks voor dit menu gebruiken",
        ),
        "el": (
            "χρήση αγγλικών για αυτό το μενού",
            "χρήση απλοποιημένων κινεζικών για αυτό το μενού",
            "χρήση παραδοσιακών κινεζικών για αυτό το μενού",
            "χρήση ισπανικών για αυτό το μενού",
            "χρήση αραβικών για αυτό το μενού",
            "χρήση γαλλικών για αυτό το μενού",
            "χρήση πορτογαλικών για αυτό το μενού",
            "χρήση ρωσικών για αυτό το μενού",
            "χρήση γερμανικών για αυτό το μενού",
            "χρήση ιαπωνικών για αυτό το μενού",
            "χρήση κορεατικών για αυτό το μενού",
            "χρήση ολλανδικών για αυτό το μενού",
            "χρήση ελληνικών για αυτό το μενού",
        ),
    }
    OPEN_TOKENS = (
        "language",
        "語言",
        "语言",
        "idioma",
        "langue",
        "Sprache",
        "sprache",
        "言語",
        "언어",
        "لغة",
        "язык",
        "taal",
        "γλώσσα",
    )
    ROW_TOKENS = {
        "en": ("english", "en", "English"),
        "zh-Hans": ("simplified-chinese", "zh-hans", "zh-Hans", "简体中文"),
        "zh-Hant": ("traditional-chinese", "zh-hant", "zh-Hant", "繁體中文"),
        "es": ("spanish", "es", "Español", "español"),
        "ar": ("arabic", "ar", "العربية", "عربي"),
        "fr": ("french", "fr", "Français", "français"),
        "pt": ("portuguese", "pt", "Português", "português", "portugues"),
        "ru": ("russian", "ru", "Русский", "русский"),
        "de": ("german", "de", "Deutsch", "deutsch"),
        "ja": ("japanese", "ja", "日本語"),
        "ko": ("korean", "ko", "한국어"),
        "nl": ("dutch", "nl", "Nederlands", "nederlands"),
        "el": ("greek", "el", "Ελληνικά", "ελληνικά"),
    }
    SELF_TOKENS = (
        "self-management",
        "自我管理",
        "autogestión",
        "autogestão",
        "autogestion",
        "Selbstverwaltung",
        "selbstverwaltung",
        "自己管理",
        "자기관리",
        "إدارة-ذاتية",
        "самоуправление",
        "zelfbeheer",
        "αυτοδιαχείριση",
    )

    def __init__(self, logger=None, app_name="VideoSpeed", home=None):
        self.logger = logger
        if logger is not None:
            logger.log_message("instantiated", component="LanguageMenu")
        self.app_name = app_name
        if home is None:
            home = os.path.expanduser("~")
        self.directory = os.path.join(home, ".local", app_name)
        self.code = "en"
        self._load()

    def path(self) -> str:
        """The language file. One line, mode 0600, under persistence."""
        return os.path.join(self.directory, self.FILE_NAME)

    def _load(self) -> None:
        """Once. A bad file stays on disk and this process uses English."""
        self.code = "en"
        try:
            with open(self.path(), encoding="utf-8", errors="replace") as handle:
                line = handle.readline()
        except OSError:
            line = ""
        line = line.replace("\r", "").strip("\n")
        if line in self.CODES:
            self.code = line
        env = os.environ.get(self.ENV_NAME, "")
        if env in self.CODES:
            self.code = env

    def save(self, code: str) -> bool:
        """Write one line. Set the code only after the write succeeds."""
        if code not in self.CODES:
            return False
        target = self.path()
        if self.logger is not None:
            self.logger.log_message(
                "save language path={0}".format(target),
                component="menu",
            )
        try:
            created = not os.path.isdir(self.directory)
            os.makedirs(self.directory, mode=0o700, exist_ok=True)
            if created:
                os.chmod(self.directory, 0o700)
            fd = os.open(
                target,
                os.O_WRONLY | os.O_CREAT | os.O_TRUNC,
                0o600,
            )
            try:
                os.write(fd, (code + "\n").encode("utf-8"))
            finally:
                os.close(fd)
            os.chmod(target, 0o600)
        except OSError:
            return False
        self.code = code
        return True

    def _pick(self, table: dict) -> str:
        return table.get(self.code, table["en"])

    def path_label(self) -> str:
        return self._pick(self.PATH_LABEL)

    def unknown_choice(self) -> str:
        return self._pick(self.UNKNOWN)

    def saved_line(self) -> str:
        return self._pick(self.SAVED)

    def failed_line(self) -> str:
        return self._pick(self.FAILED)

    def titles(self) -> dict:
        return {
            "front": self._pick(self.MAIN_MENU),
            "lang": self._pick(self.CAT_LANGUAGE),
            "log": self._pick(self.CAT_SYSTEM_LOG),
            "self": self._pick(self.CAT_SELF),
            "result": "result",
        }

    def _overlay(self, rows, shorts: dict, longs: dict) -> tuple:
        built = []
        for number, short, explain, kind in rows:
            built.append((
                number,
                shorts.get(kind, short),
                longs.get(kind, explain),
                kind,
            ))
        return tuple(built)

    def _front_maps(self):
        shorts = {
            "language": self._pick(self.CAT_LANGUAGE),
            "system-log": self._pick(self.CAT_SYSTEM_LOG),
            "self-management": self._pick(self.CAT_SELF),
            "exit": self._pick(self.EXIT_SHORT),
        }
        longs = {
            "language": self._pick(self.LANGUAGE_LONG),
            "system-log": self._pick(self.SYSTEM_LOG_LONG),
            "self-management": self._pick(self.SELF_LONG),
            "exit": self._pick(self.EXIT_LONG),
        }
        return shorts, longs

    def _lang_rows(self) -> tuple:
        pack = self.LANG_LONG.get(self.code)
        built = []
        for index, (code, number, endonym) in enumerate(self.ASSIGNED):
            if pack is None:
                explain = MenuPainter.LANG_ROWS[index][2]
            else:
                explain = pack[index]
            built.append((number, endonym, explain, code))
        built.append((
            0,
            self._pick(self.BACK_SHORT),
            self._pick(self.BACK_LONG),
            "back",
        ))
        return tuple(built)

    def boards(self) -> dict:
        """Row tuples for the four boards. Leaf shorts and leaf explains stay English."""
        if self.code == "en":
            return {
                "front": MenuPainter.MENU_ROWS,
                "self": MenuPainter.SELF_ROWS,
                "log": MenuPainter.LOG_ROWS,
                "lang": MenuPainter.LANG_ROWS,
            }
        front_shorts, front_longs = self._front_maps()
        back_shorts = {"back": self._pick(self.BACK_SHORT)}
        back_longs = {"back": self._pick(self.BACK_LONG)}
        return {
            "front": self._overlay(MenuPainter.MENU_ROWS, front_shorts, front_longs),
            "self": self._overlay(MenuPainter.SELF_ROWS, back_shorts, back_longs),
            "log": self._overlay(MenuPainter.LOG_ROWS, back_shorts, back_longs),
            "lang": self._lang_rows(),
        }

    def tokens(self) -> dict:
        """Typed token -> (kind, layer or None). None matches every layer."""
        found = {}
        for token in self.OPEN_TOKENS:
            found[token] = ("language", "front")
        for token in self.CAT_SYSTEM_LOG.values():
            found[token] = ("system-log", "front")
        found["system-log"] = ("system-log", "front")
        for token in self.SELF_TOKENS:
            found[token] = ("self-management", "front")
        for token in self.EXIT_SHORT.values():
            found[token] = ("exit", "front")
        found["exit"] = ("exit", "front")
        for token in self.BACK_SHORT.values():
            found[token] = ("back", None)
        found["back"] = ("back", None)
        for code, names in self.ROW_TOKENS.items():
            for token in names:
                found[token] = (code, "lang")
        return found

    def apply_to(self, model, painter) -> None:
        """Hand this language's rows and path word to the session. Not a constructor."""
        model.boards = self.boards()
        model.titles = self.titles()
        model.tokens = self.tokens()
        model.unknown_choice = self.unknown_choice()
        painter.set_path_label(self.path_label())
