from gi.repository import Gtk, Adw, Gdk

from zhudi.dictionaries import Dictionaries
from zhudi.preferences import Preferences
from zhudi.processing import DictionaryTools, SegmentationTools
from zhudi.ui.options import OptionsWidget
from zhudi.ui.dictionary import DictionaryWidget
from zhudi.ui.segmentation import SegmentationWidget


class MainWindow(Adw.ApplicationWindow):
    """Class that defines the welcome screen, and gives access to other layers."""

    def __init__(
        self,
        dictionaries: Dictionaries,
        language: str,
        preferences: Preferences,
        *args,
        **kwargs
    ):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.set_title("Zhudi")
        self.set_default_size(700, 1000)
        evk = Gtk.EventControllerKey.new()
        evk.connect("key-pressed", self.on_key_press)
        self.add_controller(evk)
        self.dictionaries: Dictionaries = dictionaries
        self.language: str = language
        self.preferences: Preferences = preferences
        self.dict_gui = None
        self.dict_settings = None
        self.seg_gui = None
        self.tab_box = None
        self.vbox = None

    def build(self):
        """Mandatory build function."""
        self.dictionaries.create_set_chinese_characters()

        # Tabs
        self.dict_settings, self.dict_gui = self.dictionary_gui()
        self.seg_gui = self.segmentation_gui()
        self.options_gui = self.options_gui()

        # Build the tab frame
        self.tab_box = Gtk.Notebook()
        self.tab_box.set_tab_pos(Gtk.PositionType.TOP)
        self.tab_box.append_page(self.dict_gui, None)
        self.tab_box.set_tab_label_text(self.dict_gui, "Dictionary")
        self.tab_box.append_page(self.seg_gui, None)
        self.tab_box.set_tab_label_text(self.seg_gui, "Segmentation")
        self.tab_box.append_page(self.options_gui, None)
        self.tab_box.set_tab_label_text(self.options_gui, "Options")

        header = Gtk.HeaderBar()
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        box.append(header)
        box.append(self.tab_box)

        self.set_content(box)

    def options_gui(self):
        """Options tab."""
        return OptionsWidget(self.preferences, self.dictionaries).build()

    def dictionary_gui(self):
        """Start the dictionary widget."""
        segmentation_tools = SegmentationTools()
        # segmentation_tools.load(self.data_object)
        ui = DictionaryWidget(self.dictionaries, self.preferences, segmentation_tools)
        ui.language = self.language
        return ui, ui.build()

    def segmentation_gui(self):
        """Start the segmentation widget."""
        segmentation_tools = SegmentationTools()
        # segmentation_tools.load(self.data_object)
        return SegmentationWidget(None, segmentation_tools, self.preferences).build()

    def on_key_press(self, event, keyval, keycode, state):
        # Stop with Ctrl-w
        if keyval == Gdk.KEY_w and state & Gdk.ModifierType.CONTROL_MASK:
            self.close()

        # Do nothing if random key
        if isinstance(event, Gtk.EventControllerKey):
            return

        # Navigate in the result list with arrows and select the items
        if self.tab_box.get_current_page() == 0:
            search_key = (
                len(event.string) > 0 and ord(event.string[0]) >= 0x20
            ) or event.keyval in {Gdk.KEY_Left, Gdk.KEY_Right, Gdk.KEY_BackSpace}
            if not self.dict_settings.search_field.has_focus() and search_key:
                if event.keyval == Gdk.KEY_Left or event.keyval == Gdk.KEY_Right:
                    self.dict_settings.search_field.grab_focus_without_selecting()
                else:
                    self.dict_settings.search_field.grab_focus()
            elif event.keyval in {
                Gdk.KEY_Up,
                Gdk.KEY_Down,
                Gdk.KEY_Page_Up,
                Gdk.KEY_Page_Down,
            }:
                self.dict_settings.results_tree.grab_focus()
