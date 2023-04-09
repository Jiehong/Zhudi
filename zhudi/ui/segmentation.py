import re

from gi.repository import Gtk, GLib

from zhudi.data import Data
from zhudi.preferences import Preferences
from zhudi.processing import DictionaryTools, SegmentationTools
from zhudi.chinese_table import ChineseTable, Cangjie5Table, Array30Table, Wubi86Table


class SegmentationWidget(object):
    """Class that defines the segmentation GUI layer."""

    def __init__(
        self,
        data_object: Data,
        segmentation_tools: SegmentationTools,
        preferences: Preferences,
    ):
        self.frame_label = None
        self.horizontal_separator = None
        self.go_button = None
        self.title_box = None
        self.text_field = None
        self.scrolledwindow = None
        self.results_list = []
        self.frame_results = None
        self.left_vertical_box = None
        self.right_vertical_box = None
        self.results_label = None
        self.results_field = None
        self.results_scroll = None
        self.results_frame = None
        self.horizontal_box = None
        self.data_object: Data = data_object
        self.segmentation_tools: SegmentationTools = segmentation_tools
        self.preferences: Preferences = preferences
        self.cangjie5: ChineseTable = Cangjie5Table()
        self.array30: ChineseTable = Array30Table()
        self.wubi86: ChineseTable = Wubi86Table()

    def build(self):
        # Frame label
        self.frame_label = Gtk.Label()
        self.frame_label.set_text("<big>Chinese text to process:</big>")
        self.frame_label.set_use_markup(True)

        # Horizontal separator
        self.horizontal_separator = Gtk.Separator()

        # Go! button
        self.go_button = Gtk.Button(label="Go!")
        self.go_button.connect(
            "clicked", lambda x: self.go_segment(self.text_field.get_buffer())
        )
        # Frame title + Go! button
        self.title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=3)
        self.title_box.append(self.frame_label)
        self.title_box.append(self.horizontal_separator)
        self.title_box.append(self.go_button)

        # Text field (to process)
        self.text_field = Gtk.TextView()
        self.text_field.set_editable(True)
        self.text_field.set_cursor_visible(True)
        self.text_field.set_wrap_mode(Gtk.WrapMode.CHAR)
        self.scrolledwindow = Gtk.ScrolledWindow()
        self.scrolledwindow.set_hexpand(True)
        self.scrolledwindow.set_vexpand(True)
        self.scrolledwindow.set_child(self.text_field)

        # Results in a list
        self.results_list = Gtk.ListStore(str)

        results = Gtk.ColumnView(model=Gtk.SingleSelection())
        # results.set_enable_search(False)
        # results.set_reorderable(False)
        # select = results.get_selection()
        # select.connect("changed", self.word_selected)
        #
        # first_column = Gtk.ColumnViewColumn()
        # first_column.set_title("Results")
        # renderer = Gtk.CellRendererText()
        # first_column.pack_start(renderer, True)
        # first_column.add_attribute(renderer, "text", 0)
        # results.append_column(first_column)

        results_scroll = Gtk.ScrolledWindow()
        # No horizontal bar, automatic vertical bar
        results_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        results_scroll.set_child(results)

        self.frame_results = Gtk.Frame()
        self.frame_results.set_child(results_scroll)

        # Mapping of window
        self.left_vertical_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.left_vertical_box.append(self.title_box)
        self.left_vertical_box.append(self.scrolledwindow)
        self.left_vertical_box.append(self.frame_results)
        self.left_vertical_box.set_homogeneous(False)

        # Results frame
        self.results_label = Gtk.Label()
        self.results_label.set_text("<big>Translation</big>")
        self.results_label.set_use_markup(True)
        self.results_field = Gtk.TextView()
        self.results_field.set_editable(False)
        self.results_field.set_cursor_visible(False)
        self.results_field.set_vexpand(True)
        # No horizontal bar, vertical bar if needed
        self.results_field.set_wrap_mode(Gtk.WrapMode.WORD)

        self.results_scroll = Gtk.ScrolledWindow()
        self.results_scroll.set_child(self.results_field)

        self.results_frame = Gtk.Frame()
        self.results_frame.set_label_widget(self.results_label)
        self.results_frame.set_child(self.results_scroll)

        self.right_vertical_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=2
        )
        self.right_vertical_box.append(self.results_frame)

        self.horizontal_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
        self.horizontal_box.append(self.left_vertical_box)
        self.horizontal_box.append(self.right_vertical_box)
        self.horizontal_box.set_homogeneous(True)
        return self.horizontal_box

    def go_segment(self, text_buffer):
        """Get the input text to segment, and display the words."""
        beginning = text_buffer.get_start_iter()
        end = text_buffer.get_end_iter()
        # grab hidden characters
        text = text_buffer.get_text(beginning, end, True)
        text = text.replace(" ", "")
        segmented_text = self.segmentation_tools.sentence_segmentation(text)
        self.display_results(segmented_text, text_buffer)
        self.display_selectable_words(segmented_text)

    def display_selectable_words(self, segmented_text):
        """Add in the results the segmented words."""
        widget = self.results_list
        widget.clear()
        for word in segmented_text:
            widget.append([word])

    @staticmethod
    def display_results(text, results_buffer):
        """Display the segmentation result directly in the input area.
        This has a nice side effect: allowing you to copy the result.

        """
        text_to_display = ""
        for item in text:
            text_to_display += item
            text_to_display += "    "
        results_buffer.set_text(text_to_display)

    def display_translation(self, index, bypass=False):
        """Display the given index [of a word] in a nicely formatted output.
        If bypass is True, then the index variable is a string that has to
        be displayed as it.

        """
        translation_buffer = self.results_field.get_buffer()

        if bypass:
            translation_buffer.set_text(index)
            return

        characters = self.data_object.get_chinese(index, self.preferences)

        translation = re.sub(
            r"\[(.*?)\]",
            lambda x: "[" + DictionaryTools.romanize_pinyin(x.group(1)) + "]",
            self.data_object.translation[index],
        )
        numbered_translations = "".join(
            f"{i+1}. {t}\n" for i, t in enumerate(translation.split("/"))
        )

        pronunciation_string = DictionaryTools.romanize(
            self.data_object, index, self.preferences
        )

        # Display different writing methods for the entry
        cangjie5_displayed = "".join(
            f"[{self.cangjie5.proceed(hanzi)[1]}]" for hanzi in characters
        )
        array30_displayed = "".join(
            f"[{self.array30.proceed(hanzi)[1]}]" for hanzi in characters
        )
        wubi86_code = "".join(
            f"[{self.wubi86.proceed(hanzi)[0]}]" for hanzi in characters
        )

        # Display in the Translation box
        # translation_buffer = self.translation_box.get_buffer()
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

    def word_selected(self, selection):
        """Display the selected word in the translation area."""
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            word = model[treeiter][0]
            if word is not None:
                index = self.segmentation_tools.search_unique(word, self.data_object)
                if index is None:
                    self.display_translation(word, True)
                else:
                    self.display_translation(index)
