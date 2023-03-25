import re
from gi.repository import Gtk, GLib

from zhudi.data import Data
from zhudi.processing import DictionaryTools, SegmentationTools
from zhudi.chinese_table import ChineseTable, Cangjie5Table, Array30Table, Wubi86Table


class DictionaryWidget(object):
    """Dictionary tab gui."""

    def __init__(
        self,
        data_object: Data,
        dictionary_tools: DictionaryTools,
        segmentation_tools: SegmentationTools,
    ):
        self.data_object: Data = data_object
        self.language = ""
        self.results_list = []
        self.results_tree = None
        self.search_field = None
        self.chinese_label = None
        self.translation_box = None
        self.dictionary_tools: DictionaryTools = dictionary_tools
        self.segmentation_tools: SegmentationTools = segmentation_tools
        self.cangjie5: ChineseTable = Cangjie5Table()
        self.array30: ChineseTable = Array30Table()
        self.wubi86: ChineseTable = Wubi86Table()

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
        self.results_list = Gtk.ListStore(str)
        results_tree = Gtk.TreeView(model=self.results_list)
        renderer = Gtk.CellRendererText()
        results_tree.tvcolumn = Gtk.TreeViewColumn("Results", renderer, text=0)
        results_tree.append_column(results_tree.tvcolumn)
        self.results_list.cell = Gtk.CellRendererText()
        results_tree.tvcolumn.pack_start(self.results_list.cell, True)
        results_tree.set_enable_search(False)
        results_tree.tvcolumn.set_sort_column_id(-1)
        results_tree.set_reorderable(False)
        self.results_tree = results_tree
        select = results_tree.get_selection()
        select.connect("changed", self.display_another_result)

        results_scroll = Gtk.ScrolledWindow()
        # No horizontal bar, automatic vertical bar
        results_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        results_scroll.set_child(results_tree)

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
        self.dictionary_tools.reset_search()
        if text == "":
            self.results_list.clear()
            self.display_translation(0)
        else:
            self.language = self.determine_language(text)
            if self.language == "Latin":
                self.dictionary_tools.search(self.data_object.translation, text)
                self.dictionary_tools.search(self.data_object.pinyin, text)
            elif self.data_object.hanzi == "Traditional":
                self.dictionary_tools.search(self.data_object.traditional, text)
            else:
                self.dictionary_tools.search(self.data_object.simplified, text)
            self.dictionary_tools.finish_search(self.data_object)
            self.update_results()
            self.results_tree.grab_focus()
            self.display_translation(0)
        self.results_tree.scroll_to_cell([0])

    # end of search_asked

    def determine_language(self, input_text):
        """
        Determine the language of the input text, according to its content

        """

        if self.segmentation_tools.is_not_chinese(input_text):
            return "Latin"
        else:
            return "Chinese"

    def display_translation(self, which):
        """Handles the display of the translation for the selected element."""

        if len(self.dictionary_tools.index) == 0:
            self.translation_box.get_buffer().set_text("")
            if len(self.results_list) == 0:
                self.results_list.append(["Nothing found."])
            return
        else:
            index = self.dictionary_tools.index[which]

        characters = self.data_object.get_chinese(index)

        translation = re.sub(
            r"\[(.*?)\]",
            lambda x: "[" + DictionaryTools.romanize_pinyin(x.group(1)) + "]",
            self.data_object.translation[index],
        )
        numbered_translations = "".join(
            f"{i+1}. {t}\n" for i, t in enumerate(translation.split("/"))
        )

        pronunciation_string = DictionaryTools.romanize(self.data_object, index)

        # Display different writing methods for the entry
        cangjie5_displayed = "".join(
            f"[{self.cangjie5.proceed(hanzi, self.data_object.cangjie5)[1]}]"
            for hanzi in characters
        )
        array30_displayed = "".join(
            f"[{self.array30.proceed(hanzi, self.data_object.array30)[1]}]"
            for hanzi in characters
        )
        wubi86_code = "".join(
            f"[{self.wubi86.proceed(hanzi, self.data_object.wubi86)[1]}]"
            for hanzi in characters
        )

        # Display in the Translation box
        # The very tiny space is there so that clicking on a character searches for the correct character.
        # Not sure why but it seems to help
        self.chinese_label.set_markup(
            '<span size="1pt"> </span>'.join(
                f'<a href="{ch}"><span size="60pt" underline="none">{ch}</span></a>'
                for ch in characters
            )
        )
        translation_buffer = self.translation_box.get_buffer()
        translation_buffer.set_text("")
        translation_buffer.insert_markup(
            iter=translation_buffer.get_end_iter(),
            markup="<b>Pronunciation</b>\n<span foreground='#268bd2'>"
            + pronunciation_string
            + "</span>\n\n"
            + "<b>Meaning</b>\n"
            + GLib.markup_escape_text(numbered_translations, -1)
            + "<b>Input methods codes</b>\n"
            + "Array30 (行列30): \n"
            + array30_displayed
            + "\n\n"
            + "Cangjie5 (倉頡5): \n"
            + cangjie5_displayed
            + "\n\n"
            + "Wubi86 (五筆86): \n"
            + wubi86_code,
            len=-1,
        )

    def update_results(self):
        """Clear, and refill the result list."""
        self.results_list.clear()
        displayed_index = 1
        threashold = 40  # threshold for line wrap
        for k in self.dictionary_tools.index:
            if self.language == "latin":
                string = self.data_object.translation[k]
            elif self.data_object.hanzi == "traditional":
                string = self.data_object.traditional[k]
            else:
                string = self.data_object.simplified[k]
            if len(string) > threashold:
                string = str(displayed_index) + ". " + string[0:threashold] + "…"
            else:
                string = str(displayed_index) + ". " + string
            string = string[:-1]  # no \n
            self.results_list.append([string])
            displayed_index += 1

    def display_another_result(self, selection):
        """Display the newly selected result."""
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            self.display_translation(model[treeiter].path[0])
