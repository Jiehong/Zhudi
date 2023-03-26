from gi import require_version

from zhudi.data import Data
from zhudi.preferences import Preferences

require_version("Gtk", "4.0")
require_version("Adw", "1")

from gi.repository import Adw

from zhudi.ui.main_window import MainWindow


class ZhudiApplication(Adw.Application):
    def __init__(self, data_object: Data, language: str, preferences: Preferences):
        super().__init__(application_id="com.github.jiehong.zhudi")
        self.data_object = data_object
        self.language = language
        self.preferences = preferences

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = MainWindow(
                data_object=self.data_object,
                language=self.language,
                preferences=self.preferences,
                application=self,
            )
            win.build()
        win.present()
