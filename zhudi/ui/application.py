from gi import require_version

require_version("Gtk", "4.0")
require_version("Adw", "1")

from zhudi.dictionaries import Dictionaries
from zhudi.preferences import Preferences

from gi.repository import Adw

from zhudi.ui.main_window import MainWindow


class ZhudiApplication(Adw.Application):
    def __init__(
        self, dictionaries: Dictionaries, language: str, preferences: Preferences
    ):
        super().__init__(application_id="com.github.jiehong.zhudi")
        self.dictionaries = dictionaries
        self.language = language
        self.preferences = preferences

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = MainWindow(
                dictionaries=self.dictionaries,
                language=self.language,
                preferences=self.preferences,
                application=self,
            )
            win.build()
        win.present()
