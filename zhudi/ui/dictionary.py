import re
from typing import List

from gi.repository import Gtk, GLib, Gio, GObject

from zhudi.dictionaries import Dictionaries
from zhudi.preferences import Preferences
from zhudi.processing import DictionaryTools, SegmentationTools
from zhudi.chinese_table import ChineseTable, Cangjie5Table, Array30Table, Wubi86Table
from zhudi.row import Row


class Value(GObject.GObject):
    value: str

    def __init__(self, value: str):
        GObject.GObject.__init__(self)
        self.value = value


class DictionaryWidget(object):
    """Dictionary tab gui."""

    def __init__(
        self,
        dictionaries: Dictionaries,
        preferences: Preferences,
        segmentation_tools: SegmentationTools,
    ):
        self.dictionaries: Dictionaries = dictionaries
        self.preferences: Preferences = preferences
        self.language: str = ""
        self.results_list: Gio.ListStore = None
        self.results_tree = None
        self.search_field = None
        self.chinese_label = None
        self.translation_box = None
        self.segmentation_tools: SegmentationTools = segmentation_tools
        self.cangjie5: ChineseTable = Cangjie5Table()
        self.array30: ChineseTable = Array30Table()
        self.wubi86: ChineseTable = Wubi86Table()
        self.full_results: List[Row] = []

    @staticmethod
    def setup_result_view(widget: Gtk.ListView, list_item: Gtk.ListItem) -> None:
        """
        Callback for the setup signal
        In charge of creating the inner structure of the ListItem widget.
        """
        label = Gtk.Label()
        label.set_halign(Gtk.Align.START)
        list_item.set_child(label)

    @staticmethod
    def bind_result_view(widget: Gtk.ListView, list_item: Gtk.ListItem) -> None:
        """
        Callback for the bind signal
        In charge of finalizing the widget's content and signals just before
        it is presented (at creation or reuse)
        """
        label = list_item.get_child()
        o = list_item.get_item()
        label.set_label(o.value)

    def build(self) -> Gtk.Grid:
        # Search field
        search_field = Gtk.Entry()
        search_field.set_visible(True)
        search_field.connect("activate", self.search_asked)
        search_field.set_placeholder_text("Looking for something?")
        search_field.set_margin_end(10)
        search_field.set_hexpand(True)
        self.search_field = search_field

        # Go, search! button
        go_button = Gtk.Button(label="Search")
        go_button.connect("clicked", self.search_asked)

        # Search + button box
        search_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        search_box.append(search_field)
        search_box.append(go_button)

        # Results part in a list
        results = Gtk.ColumnView()
        results.set_show_column_separators(False)
        results.set_show_row_separators(False)
        results.set_reorderable(False)

        self.results_list = Gio.ListStore.new(Value)
        selection = Gtk.SingleSelection.new(self.results_list)
        selection.connect("selection-changed", self.display_another_result)
        results.set_model(selection)

        results_column = Gtk.ColumnViewColumn.new("Results")
        results_column.set_resizable(False)
        results_column.set_expand(True)

        factory = Gtk.SignalListItemFactory()
        factory.connect("setup", DictionaryWidget.setup_result_view)
        factory.connect("bind", DictionaryWidget.bind_result_view)
        results_column.set_factory(factory)

        results.append_column(results_column)

        results_scroll = Gtk.ScrolledWindow()
        # No horizontal bar, automatic vertical bar
        results_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        results_scroll.set_child(results)

        frame_results = Gtk.Frame()
        frame_results.set_child(results_scroll)
        frame_results.set_vexpand(True)
        frame_results.set_margin_top(10)

        # Translation Label
        translation_label = Gtk.Label()
        translation_label.set_text("<big>Translation</big>")
        translation_label.set_use_markup(True)

        # Chinese label
        self.chinese_label = Gtk.Label()
        self.chinese_label.set_selectable(True)
        self.chinese_label.set_focus_on_click(False)
        # self.chinese_label.set_track_visited_links(False)
        self.chinese_label.connect("activate-link", self.on_character_clicked)

        # Translation view
        self.translation_box = Gtk.TextView()
        self.translation_box.set_editable(False)
        self.translation_box.set_cursor_visible(False)
        self.translation_box.set_wrap_mode(Gtk.WrapMode.WORD)

        # No horizontal bar, vertical bar if needed
        translation_scroll = Gtk.ScrolledWindow()
        translation_scroll.set_child(self.translation_box)
        translation_scroll.set_vexpand(True)

        # Mapping of the main window
        left_vertical_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        left_vertical_box.append(search_box)
        left_vertical_box.append(frame_results)
        left_vertical_box.set_margin_top(10)
        left_vertical_box.set_margin_start(10)
        left_vertical_box.set_margin_bottom(10)
        left_vertical_box.set_margin_end(10)

        right_vertical_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        right_vertical_box.append(self.chinese_label)
        right_vertical_box.append(translation_scroll)

        frame_translation = Gtk.Frame()
        frame_translation.set_label_widget(translation_label)
        frame_translation.set_child(right_vertical_box)
        frame_translation.set_hexpand(True)

        horizontal_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        horizontal_box.append(left_vertical_box)
        horizontal_box.append(frame_translation)
        horizontal_box.set_homogeneous(True)
        return horizontal_box

    def on_character_clicked(self, chinese_label, href) -> None:
        self.search_field.set_text(href)
        self.search_asked(self.search_field)

    def search_asked(self, search_field: Gtk.Entry) -> None:
        """Start search when users hit ENTER or the search button."""
        search_field.grab_focus()
        text = search_field.get_text()
        if text == "":
            self.results_list.remove_all()
            self.display_translation(0)
        else:
            results = self.dictionaries.search(text)
            self.language = self.determine_language(text)
            self.update_results(results)
            self.display_translation(0)

    # end of search_asked

    def determine_language(self, input_text):
        """
        Determine the language of the input text, according to its content

        """

        if self.segmentation_tools.is_not_chinese(input_text):
            return "Latin"
        else:
            return "Chinese"

    @staticmethod
    def _format_codes(sets: ChineseTable, characters: str) -> str:
        codes = []
        for hanzi in characters:
            potential_codes = sets.proceed(hanzi)
            if not potential_codes:
                code = f"[{hanzi}]"
            else:
                code = f"[{potential_codes[1]}]"
            codes.append(code)
        return "".join(codes)

    def display_translation(self, index):
        """Handles the display of the translation for the selected element."""

        if len(self.full_results) == 0:
            self.translation_box.get_buffer().set_text("")
            if len(self.results_list) == 0:
                self.results_list.append(Value("Nothing found."))
            return

        result: Row = self.full_results[index]

        if self.preferences.get_character_set() == "traditional":
            characters = result.traditional
        else:
            characters = result.simplified

        # Add pronunciation in definitions too when they appear within []
        filled_definitions = []
        for definition in result.definitions:
            # TODO: make it work for zhuyin as well by fixing DictionaryTools.romanize
            d = re.sub(
                r"\[(.*?)\]",
                lambda x: "[" + DictionaryTools.romanize_pinyin(x.group(1)) + "]",
                definition,
            )
            filled_definitions.append(d)
        result.definitions = filled_definitions

        numbered_translations = "".join(
            f"{i+1}. {t}\n" for i, t in enumerate(result.definitions)
        )

        if self.preferences.get_romanization() == "zhuyin":
            pronunciation_string = result.zhuyin
        else:
            pronunciation_string = DictionaryTools.romanize_pinyin(result.pinyin)

        # Display different writing methods for the entry
        cangjie5_codes = DictionaryWidget._format_codes(self.cangjie5, characters)
        array30_codes = DictionaryWidget._format_codes(self.array30, characters)
        wubi86_codes = DictionaryWidget._format_codes(self.wubi86, characters)

        # Display in the Translation box
        # The very tiny space is there so that clicking on a character searches for the correct character.
        # Not sure why but it seems to help
        self.chinese_label.set_markup(
            '<span size="1pt"> </span>'.join(
                f'<a href="{ch}"><span size="48pt" underline="none">{ch}</span></a>'
                for ch in characters
            )
        )
        translation_buffer = self.translation_box.get_buffer()
        translation_buffer.set_text("")
        translation_buffer.insert_markup(
            iter=translation_buffer.get_end_iter(),
            markup="<b>Pronunciation</b>\n<span size=\"14pt\"foreground='#268bd2'>"
            + pronunciation_string
            + "</span>\n\n"
            + "<b>Meaning</b>\n"
            + GLib.markup_escape_text(numbered_translations, -1)
            + "\n<b>Input methods codes</b>\n"
            + "Array30 (行列30): \n"
            + array30_codes
            + "\n\n"
            + "Cangjie5 (倉頡5): \n"
            + cangjie5_codes
            + "\n\n"
            + "Wubi86 (五筆86): \n"
            + wubi86_codes,
            len=-1,
        )

    def update_results(self, results: List[Row]) -> None:
        """Clear, and refill the result list."""
        self.full_results = results
        self.results_list.remove_all()
        displayed_index = 1
        threashold = 40  # threshold for line wrap
        for row in self.full_results:
            if self.language == "latin":
                string = row.definitions[0]
            elif self.preferences.get_character_set() == "traditional":
                string = row.traditional
            else:
                string = row.simplified
            if len(string) > threashold:
                string = str(displayed_index) + ". " + string[0:threashold] + "…"
            else:
                string = str(displayed_index) + ". " + string
            self.results_list.append(Value(string))
            displayed_index += 1

    def display_another_result(self, selection: Gtk.SingleSelection, b: int, c: int):
        """Display the newly selected result."""
        index = selection.get_selected()
        if index is not None:
            self.display_translation(index)
