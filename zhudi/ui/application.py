from gi import require_version

require_version("Gtk", "4.0")
require_version("Adw", "1")

from gi.repository import Adw

from zhudi.ui.main_window import MainWindow


class ZhudiApplication(Adw.Application):
    def __init__(self, data_object, language):
        super().__init__(application_id="com.github.jiehong.zhudi")
        # self.connect('activate', self.on_activate)
        self.data_object = data_object
        self.language = language

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = MainWindow(
                data_object=self.data_object, language=self.language, application=self
            )
            win.build()
        win.present()
