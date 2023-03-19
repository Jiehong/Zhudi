from gi.repository import Gtk, Pango

from zhudi.data import Data
from zhudi.processing import DictionaryTools, SegmentationTools
from zhudi.chinese_table import ChineseTable, Cangjie5Table, Array30Table, Wubi86Table


class SegmentationWidget(object):
    """Class that defines the segmentation GUI layer."""

    def __init__(self, data_object: Data, segmentation_tools: SegmentationTools):
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
        self.cangjie5: ChineseTable = Cangjie5Table()
        self.array30: ChineseTable = Array30Table()
        self.wubi86: ChineseTable = Wubi86Table()

    def build(self):
        """Mandatory GUI build method."""
        # Frame label
        self.frame_label = Gtk.Label()
        self.frame_label.set_text("<big>Chinese text to process:</big>")
        self.frame_label.set_use_markup(True)

        # Horzontal separator
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
        select = results_tree.get_selection()
        select.connect("changed", self.word_selected)

        results_scroll = Gtk.ScrolledWindow()
        # No horizontal bar, automatic vertical bar
        results_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        results_scroll.set_child(results_tree)

        self.frame_results = Gtk.Frame()
        self.frame_results.set_child(results_scroll)

        # Mapping of window
        self.left_vertical_box = Gtk.Grid()
        # self.left_vertical_box.append(self.title_box)
        self.left_vertical_box.attach_next_to(
            self.scrolledwindow, self.title_box, Gtk.PositionType.BOTTOM, 1, 2
        )
        self.left_vertical_box.attach_next_to(
            self.frame_results, self.scrolledwindow, Gtk.PositionType.BOTTOM, 1, 8
        )
        self.left_vertical_box.set_column_homogeneous(True)
        self.left_vertical_box.set_row_homogeneous(True)

        # Results frame
        self.results_label = Gtk.Label()
        self.results_label.set_text("<big>Translation</big>")
        self.results_label.set_use_markup(True)
        self.results_field = Gtk.TextView()
        self.results_field.set_editable(False)
        self.results_field.set_cursor_visible(False)
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

        if self.data_object.hanzi == "traditional":
            hanzi_dic = self.data_object.traditional
        else:
            hanzi_dic = self.data_object.simplified

        if self.data_object.romanisation == "zhuyin":
            romanisation_dic = self.data_object.zhuyin
        else:
            romanisation_dic = self.data_object.pinyin

        slash_list = []
        trans_index = self.data_object.translation[index]
        for line in range(len(trans_index)):
            if trans_index[line] == "/":
                slash_list.append(line)
        temp = 0
        trans = []
        for key in range(len(slash_list)):
            trans.append(str(key + 1) + ". " + trans_index[temp : slash_list[key]])
            temp = slash_list[key] + 1
        trans.append(
            str(len(slash_list) + 1) + ". " + trans_index[temp : len(trans_index)]
        )
        string = ""
        for local_index in range(len(slash_list) + 1):
            string = string + trans[local_index] + "\n"

        # Add [] around the pronunciation parts
        p_string = romanisation_dic[index].split("/", 1)[0].split()
        pronunciation_string = []
        for point in range(len(p_string)):
            if self.data_object.romanisation == "pinyin":
                pronunciation_string.append(
                    DictionaryTools.unicode_pinyin(p_string[point])
                )
                pronunciation_string.append(" ")
            else:
                pronunciation_string.append("[")
                pronunciation_string.append(p_string[point])
                pronunciation_string.append("]")
        # Display the cangjie of the entry
        cangjie5_displayed = ""
        for hanzi in hanzi_dic[index]:
            if hanzi != "\n":
                key_code, displayed_code = self.cangjie5.proceed(
                    hanzi, self.data_object.cangjie5
                )
                cangjie5_displayed += "["
                cangjie5_displayed += displayed_code
                cangjie5_displayed += "]"
        # Display the array30 of the entry
        array30_displayed = ""
        for hanzi in hanzi_dic[index]:
            if hanzi != "\n":
                key_code, displayed_code = self.array30.proceed(
                    hanzi, self.data_object.array30
                )
                array30_displayed += "["
                array30_displayed += displayed_code
                array30_displayed += "]"
        # Display the array30 of the entry (here code = displayed)
        wubi86_code = ""
        for hanzi in hanzi_dic[index]:
            if hanzi != "\n":
                key_code, displayed_code = self.wubi86.proceed(
                    hanzi, self.data_object.wubi86
                )
                wubi86_code += "["
                wubi86_code += key_code
                wubi86_code += "]"
        # Display in the Translation box
        translation_buffer.set_text(
            "Chinese\n"
            + hanzi_dic[index]
            + "\n\n"
            + "Pronunciation\n"
            + "".join(pronunciation_string)
            + "\n\n"
            "Meaning\n"
            + string
            + "Input methods codes:\n"
            + "Array30 (行列30): \n"
            + array30_displayed
            + "\n\n"
            + "Cangjie5 (倉頡5): \n"
            + cangjie5_displayed
            + "\n\n"
            + "Wubi86 (五筆86): \n"
            + wubi86_code
        )
        bold = translation_buffer.create_tag(weight=Pango.Weight.BOLD)
        big = translation_buffer.create_tag(size=30 * Pango.SCALE)
        blue = translation_buffer.create_tag(foreground="#268bd2")

        # "Chinese" in bold
        start_1 = translation_buffer.get_iter_at_line(0)
        end_1 = translation_buffer.get_iter_at_line(0)
        end_1.forward_to_line_end()
        translation_buffer.apply_tag(bold, start_1, end_1)

        # Bigger Chinese
        start_c = translation_buffer.get_iter_at_line(1)
        end_c = translation_buffer.get_iter_at_line(1)
        end_c.forward_to_line_end()
        translation_buffer.apply_tag(big, start_c, end_c)

        # "Pronunciation" in bold
        start_2 = translation_buffer.get_iter_at_line(4)
        end_2 = translation_buffer.get_iter_at_line(4)
        end_2.forward_to_line_end()
        translation_buffer.apply_tag(bold, start_2, end_2)

        # "Pronunciation" in blue
        start_3 = translation_buffer.get_iter_at_line(5)
        end_3 = translation_buffer.get_iter_at_line(5)
        end_3.forward_to_line_end()
        translation_buffer.apply_tag(blue, start_3, end_3)

        # "Meaning" in bold
        start_3 = translation_buffer.get_iter_at_line(7)
        end_3 = translation_buffer.get_iter_at_line(7)
        end_3.forward_to_line_end()
        translation_buffer.apply_tag(bold, start_3, end_3)
        guess = string.count("\n")

        # "Input methods codes" in bold
        start_4 = translation_buffer.get_iter_at_line(guess + 7)
        end_4 = translation_buffer.get_iter_at_line(guess + 7)
        end_4.forward_to_line_end()
        translation_buffer.apply_tag(bold, start_4, end_4)

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
