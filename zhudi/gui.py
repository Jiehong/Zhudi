# coding: utf-8
''' Zhudi provides a Chinese - language dictionnary based on the
    C[E|F]DICT project Copyright - 2011 - Ma Jiehong

    Zhudi is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Zhudi is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
    or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
    License for more details.

    You should have received a copy of the GNU General Public License
    If not, see <http://www.gnu.org/licenses/>.

'''

from gi import require_version
require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango, Gdk
import zhudi


CANGJIE5_OBJ = zhudi.chinese_table.Cangjie5Table()
ARRAY30_OBJ = zhudi.chinese_table.Array30Table()
WUBI86_OBJ = zhudi.chinese_table.Wubi86Table()


class DictionaryWidgetMain(object):
    """ Dictionary tab gui. """
    def __init__(self, data_object):
        self.data_object = data_object
        self.language = ""
        self.results_list = []
        self.lock = False
        self.search_field = None
        self.translation_box = None

    def build(self):
        """ Mandatory build() function. """
        # Search label
        search_label = Gtk.Label()

        # Search field
        search_field = Gtk.Entry()
        search_field.set_visible(True)
        search_field.connect("activate",
                             lambda x: self.search_asked(search_field))
        search_field.set_placeholder_text("Looking for something?")
        self.search_field = search_field

        # Go, search! button
        go_button = Gtk.Button("Search")
        go_button.connect("clicked",
                          lambda x: self.search_asked(search_field))

        # Search + button box
        sb_box = Gtk.Grid()
        sb_box.attach(search_field, 0, 0, 5, 1)
        sb_box.attach_next_to(go_button,
                              search_field,
                              Gtk.PositionType.RIGHT, 1, 1)
        sb_box.set_column_homogeneous(True)

        # Search label zone
        frame_search = Gtk.Frame()
        frame_search.set_label_widget(search_label)
        frame_search.add(sb_box)

        # Results part in a list
        self.results_list = Gtk.ListStore(str)
        results_tree = Gtk.TreeView(self.results_list)
        renderer = Gtk.CellRendererText()
        results_tree.tvcolumn = Gtk.TreeViewColumn("Results", renderer, text=0)
        results_tree.append_column(results_tree.tvcolumn)
        self.results_list.cell = Gtk.CellRendererText()
        results_tree.tvcolumn.pack_start(self.results_list.cell, True)
        results_tree.set_enable_search(False)
        results_tree.tvcolumn.set_sort_column_id(-1)
        results_tree.set_reorderable(False)
        select = results_tree.get_selection()
        select.connect("changed", self.display_another_result)

        results_scroll = Gtk.ScrolledWindow()
        # No horizontal bar, automatic vertical bar
        results_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        results_scroll.add_with_viewport(results_tree)

        frame_results = Gtk.Frame()
        frame_results.add(results_scroll)

        # Translation Label
        translation_label = Gtk.Label()
        translation_label.set_text("<big>Translation</big>")
        translation_label.set_use_markup(True)

        # Translation view
        self.translation_box = Gtk.TextView(buffer=None)
        self.translation_box.set_editable(False)
        self.translation_box.set_cursor_visible(False)

        # No horizontal bar, vertical bar if needed
        self.translation_box.set_wrap_mode(Gtk.WrapMode.WORD)

        translation_scroll = Gtk.ScrolledWindow()
        translation_scroll.add_with_viewport(self.translation_box)

        frame_translation = Gtk.Frame()
        frame_translation.set_label_widget(translation_label)
        frame_translation.add(translation_scroll)

        # Mapping of the main window
        left_vertical_box = Gtk.Grid()
        left_vertical_box.add(frame_search)
        left_vertical_box.attach_next_to(frame_results,
                                         frame_search,
                                         Gtk.PositionType.BOTTOM, 1, 9)
        left_vertical_box.set_row_homogeneous(True)
        left_vertical_box.set_column_homogeneous(True)

        right_vertical_box = Gtk.Grid()
        right_vertical_box.add(frame_translation)
        right_vertical_box.set_column_homogeneous(True)
        right_vertical_box.set_row_homogeneous(True)

        horizontal_box = Gtk.Grid()
        horizontal_box.attach(left_vertical_box, 0, 0, 1, 1)
        horizontal_box.attach_next_to(right_vertical_box,
                                      left_vertical_box,
                                      Gtk.PositionType.RIGHT, 1, 1)
        horizontal_box.set_column_homogeneous(True)
        horizontal_box.set_row_homogeneous(True)
        return horizontal_box

    def search_asked(self, searchfield):
        """ Start search when users hit ENTER or the search button. """
        text = searchfield.get_text()
        if text == "":
            self.lock = True
            DICTIONARY_TOOLS_OBJECT.index = []
            self.results_list.clear()
            self.display_translation(0)
        else:
            self.lock = False
            self.language = self.determine_language(text)
            if self.language == "Latin":
                given_list = self.data_object.translation
            elif self.data_object.hanzi == "Traditional":
                given_list = self.data_object.traditional
            else:
                given_list = self.data_object.simplified
            DICTIONARY_TOOLS_OBJECT.search(given_list, text)
            self.update_results()
            self.display_translation(0)
    # end of search_asked

    @staticmethod
    def determine_language(input_text):
        """
        Determine the language of the input text, according to its content

        """

        if SEGMENTATION_TOOLS_OBJECT.is_not_chinese(input_text):
            return "Latin"
        else:
            return "Chinese"

    def display_translation(self, which):
        """ Handles the display of the translation for the selected element. """

        translation_buffer = self.translation_box.get_buffer()
        if len(DICTIONARY_TOOLS_OBJECT.index) == 0:
            translation_buffer.set_text("Nothing found.")
            if len(self.results_list) == 0:
                self.results_list.append(["Nothing found."])
            return
        else:
            index = DICTIONARY_TOOLS_OBJECT.index[which]

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
        for l in range(len(trans_index)):
            if trans_index[l] == "/":
                slash_list.append(l)
        temp = 0
        trans = []
        for local_index in range(len(slash_list)):
            trans.append(str(local_index + 1) + ". " + trans_index[temp:slash_list[local_index]])
            temp = slash_list[local_index] + 1
        trans.append(str(len(slash_list) + 1) + ". " + trans_index[temp:len(trans_index)])
        string = ""
        for i in range(len(slash_list) + 1):
            string = string + trans[i] + "\n"

        # Add [] arround the pronounciation parts
        p_string = romanisation_dic[index].split()
        pronounciation_string = []
        for point in range(len(p_string)):
            if self.data_object.romanisation == "pinyin":
                pronounciation_string.append(DICTIONARY_TOOLS_OBJECT.unicode_pinyin(p_string[point]))
                pronounciation_string.append(" ")
            else:
                pronounciation_string.append("[")
                pronounciation_string.append(p_string[point])
                pronounciation_string.append("]")
        # Display the cangjie of the entry
        cangjie5_displayed = ""
        for hanzi in hanzi_dic[index]:
            if hanzi != "\n":
                key_code, displayed_code = CANGJIE5_OBJ.proceed(hanzi, self.data_object.cangjie5)
                cangjie5_displayed += "["
                cangjie5_displayed += displayed_code
                cangjie5_displayed += "]"
        # Display the array30 of the entry
        array30_displayed = ""
        for hanzi in hanzi_dic[index]:
            if hanzi != "\n":
                key_code, displayed_code = ARRAY30_OBJ.proceed(hanzi, self.data_object.array30)
                array30_displayed += "["
                array30_displayed += displayed_code
                array30_displayed += "]"
        # Display the array30 of the entry (here code = displayed)
        wubi86_code = ""
        for hanzi in hanzi_dic[index]:
            if hanzi != "\n":
                key_code, displayed_code = WUBI86_OBJ.proceed(hanzi, self.data_object.wubi86)
                wubi86_code += "["
                wubi86_code += key_code
                wubi86_code += "]"
        # Display in the Translation box
        translation_buffer.set_text("Chinese\n" + hanzi_dic[index] + "\n\n" +
                                    "Pronunciation\n" + ''.join(pronounciation_string) + "\n\n" +
                                    "Meaning\n" + string +
                                    "Input methods codes:\n" +
                                    "Array30 (行列30): \n" + array30_displayed + "\n\n" +
                                    "Cangjie5 (倉頡5): \n" + cangjie5_displayed + "\n\n" +
                                    "Wubi86 (五筆86): \n" + wubi86_code)
        bold = translation_buffer.create_tag(weight=Pango.Weight.BOLD)
        big = translation_buffer.create_tag(size=30 * Pango.SCALE)
        medium = translation_buffer.create_tag(size=15 * Pango.SCALE)
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
        translation_buffer.apply_tag(medium, start_3, end_3)

        # "Meaning" in bold
        start_3 = translation_buffer.get_iter_at_line(7)
        end_3 = translation_buffer.get_iter_at_line(7)
        end_3.forward_to_line_end()
        translation_buffer.apply_tag(bold, start_3, end_3)
        guess = string.count("\n")

        # "Input methods codes" in bold
        start_4 = translation_buffer.get_iter_at_line(guess+7)
        end_4 = translation_buffer.get_iter_at_line(guess+7)
        end_4.forward_to_line_end()
        translation_buffer.apply_tag(bold, start_4, end_4)

    def update_results(self):
        """ Clear, and refill the result list. """
        self.results_list.clear()
        displayed_index = 1
        threashold = 40  # threshold for line wrap
        for k in DICTIONARY_TOOLS_OBJECT.index:
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
        """ Display the newly selected result. """
        if not self.lock:
            model, treeiter = selection.get_selected()
            if treeiter is not None:
                self.display_translation(model[treeiter].path[0])


class SegmentationWidget(object):
    """ Class that defines the segmentation GUI layer.
    """

    def __init__(self, data_object):
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
        self.data_object = data_object

    def build(self):
        """ Mandatory GUI build method. """
        # Frame label
        self.frame_label = Gtk.Label()
        self.frame_label.set_text("<big>Chinese text to process:</big>")
        self.frame_label.set_use_markup(True)

        # Horzontal separator
        self.horizontal_separator = Gtk.Separator()

        # Go! button
        self.go_button = Gtk.Button("Go!")
        self.go_button.connect("clicked",
                               lambda x: self.go_segment(self.text_field.get_buffer()))
        # Frame title + Go! button
        self.title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=3)
        self.title_box.pack_start(self.frame_label, False, False, 0)
        self.title_box.pack_start(self.horizontal_separator, True, False, 0)
        self.title_box.pack_start(self.go_button, True, True, 0)

        # Text field (to process)
        self.text_field = Gtk.TextView()
        self.text_field.set_editable(True)
        self.text_field.set_cursor_visible(True)
        self.text_field.set_wrap_mode(Gtk.WrapMode.CHAR)
        self.scrolledwindow = Gtk.ScrolledWindow()
        self.scrolledwindow.set_hexpand(True)
        self.scrolledwindow.set_vexpand(True)
        self.scrolledwindow.add(self.text_field)

        # Results part in a list
        self.results_list = Gtk.ListStore(str)
        results_tree = Gtk.TreeView(self.results_list)
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
        results_scroll.add_with_viewport(results_tree)

        self.frame_results = Gtk.Frame()
        self.frame_results.add(results_scroll)

        # Mapping of window
        self.left_vertical_box = Gtk.Grid()
        self.left_vertical_box.add(self.title_box)
        self.left_vertical_box.attach_next_to(self.scrolledwindow,
                                              self.title_box,
                                              Gtk.PositionType.BOTTOM, 1, 2)
        self.left_vertical_box.attach_next_to(self.frame_results,
                                              self.scrolledwindow,
                                              Gtk.PositionType.BOTTOM, 1, 8)
        self.left_vertical_box.set_column_homogeneous(True)
        self.left_vertical_box.set_row_homogeneous(True)

        # Results frame
        self.results_label = Gtk.Label()
        self.results_label.set_text("<big>Translation</big>")
        self.results_label.set_use_markup(True)
        self.results_field = Gtk.TextView(buffer=None)
        self.results_field.set_editable(False)
        self.results_field.set_cursor_visible(False)
        # No horizontal bar, vertical bar if needed
        self.results_field.set_wrap_mode(Gtk.WrapMode.WORD)

        self.results_scroll = Gtk.ScrolledWindow()
        self.results_scroll.add_with_viewport(self.results_field)

        self.results_frame = Gtk.Frame()
        self.results_frame.set_label_widget(self.results_label)
        self.results_frame.add(self.results_scroll)

        self.right_vertical_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        self.right_vertical_box.pack_start(self.results_frame, True, True, 0)

        self.horizontal_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
        self.horizontal_box.pack_start(self.left_vertical_box, False, True, 0)
        self.horizontal_box.pack_start(self.right_vertical_box, False, True, 0)
        self.horizontal_box.set_homogeneous(True)
        return self.horizontal_box

    def go_segment(self, text_buffer):
        """ Get the input text to segment, and display the words. """
        beginning = text_buffer.get_start_iter()
        end = text_buffer.get_end_iter()
        # grab hidden characters
        text = text_buffer.get_text(beginning, end, True)
        text = text.replace(" ", "")
        segmented_text = SEGMENTATION_TOOLS_OBJECT.sentence_segmentation(text)
        self.display_results(segmented_text, text_buffer)
        self.display_selectable_words(segmented_text)

    def display_selectable_words(self, segmented_text):
        """ Add in the results the segmented words. """
        widget = self.results_list
        widget.clear()
        for word in segmented_text:
            widget.append([word])

    @staticmethod
    def display_results(text, results_buffer):
        """ Display the segmentation result directly in the input area.
        This has a nice side effect: allowing you to copy the result.

        """
        text_to_display = ""
        for item in text:
            text_to_display += item
            text_to_display += "    "
        results_buffer.set_text(text_to_display)

    def display_translation(self, index, bypass=False):
        """ Display the given index [of a word] in a nicely formatted output.
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
            trans.append(str(key+1) + ". " + trans_index[temp:slash_list[key]])
            temp = slash_list[key]+1
        trans.append(str(len(slash_list) + 1) + ". " + trans_index[temp:len(trans_index)])
        string = ""
        for local_index in range(len(slash_list) + 1):
            string = string + trans[local_index] + "\n"

        # Add [] arround the pronounciation parts
        p_string = romanisation_dic[index].split()
        pronounciation_string = []
        for point in range(len(p_string)):
            if self.data_object.romanisation == "pinyin":
                pronounciation_string.append(DICTIONARY_TOOLS_OBJECT.unicode_pinyin(p_string[point]))
                pronounciation_string.append(" ")
            else:
                pronounciation_string.append("[")
                pronounciation_string.append(p_string[point])
                pronounciation_string.append("]")
        # Display the cangjie of the entry
        cangjie5_displayed = ""
        for hanzi in hanzi_dic[index]:
            if hanzi != "\n":
                key_code, displayed_code = CANGJIE5_OBJ.proceed(hanzi, self.data_object.cangjie5)
                cangjie5_displayed += "["
                cangjie5_displayed += displayed_code
                cangjie5_displayed += "]"
        # Display the array30 of the entry
        array30_displayed = ""
        for hanzi in hanzi_dic[index]:
            if hanzi != "\n":
                key_code, displayed_code = ARRAY30_OBJ.proceed(hanzi, self.data_object.array30)
                array30_displayed += "["
                array30_displayed += displayed_code
                array30_displayed += "]"
        # Display the array30 of the entry (here code = displayed)
        wubi86_code = ""
        for hanzi in hanzi_dic[index]:
            if hanzi != "\n":
                key_code, displayed_code = WUBI86_OBJ.proceed(hanzi, self.data_object.wubi86)
                wubi86_code += "["
                wubi86_code += key_code
                wubi86_code += "]"
        # Display in the Translation box
        translation_buffer.set_text("Chinese\n" + hanzi_dic[index] + "\n\n" +
                                    "Pronunciation\n" + ''.join(pronounciation_string) + "\n\n"
                                    "Meaning\n" + string +
                                    "Input methods codes:\n" +
                                    "Array30 (行列30): \n" + array30_displayed + "\n\n" +
                                    "Cangjie5 (倉頡5): \n" + cangjie5_displayed + "\n\n" +
                                    "Wubi86 (五筆86): \n" + wubi86_code)
        bold = translation_buffer.create_tag(weight=Pango.Weight.BOLD)
        big = translation_buffer.create_tag(size=30*Pango.SCALE)
        medium = translation_buffer.create_tag(size=15*Pango.SCALE)
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
        translation_buffer.apply_tag(medium, start_3, end_3)

        # "Meaning" in bold
        start_3 = translation_buffer.get_iter_at_line(7)
        end_3 = translation_buffer.get_iter_at_line(7)
        end_3.forward_to_line_end()
        translation_buffer.apply_tag(bold, start_3, end_3)
        guess = string.count("\n")

        # "Input methods codes" in bold
        start_4 = translation_buffer.get_iter_at_line(guess+7)
        end_4 = translation_buffer.get_iter_at_line(guess+7)
        end_4.forward_to_line_end()
        translation_buffer.apply_tag(bold, start_4, end_4)

    def word_selected(self, selection):
        """ Display the selected word in the translation area. """
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            word = model[treeiter][0]
            if word is not None:
                index = SEGMENTATION_TOOLS_OBJECT.search_unique(word, self.data_object)
                if index is None:
                    self.display_translation(word, True)
                else:
                    self.display_translation(index)

class OptionsWidget(object):
    """ Class defining the Options/About tab layout """

    def __init__(self, data_object):
        self.data_object = data_object

    def build(self):
        vertical_box = Gtk.Box()
        vertical_box.set_orientation(Gtk.Orientation.VERTICAL)
        vertical_box.set_homogeneous(False)

        title = Gtk.Label("")
        vertical_box.pack_start(title, False, True, 20)

        horizontal_box = Gtk.Box()
        label = Gtk.Label("Romanisation:")
        horizontal_box.pack_start(label, True, True, 0)
        # List of romanisation available
        name_store = Gtk.ListStore(str)
        rom = ["Pinyin", "Zhuyin"]
        for value in rom:
            name_store.append([value])
        combo = Gtk.ComboBox.new_with_model(name_store)
        renderer_text = Gtk.CellRendererText()
        combo.pack_start(renderer_text, True)
        combo.add_attribute(renderer_text, "text", 0)
        # Set active the saved value
        if self.data_object.romanisation == 'zhuyin':
            combo.set_active(1)
        else:
            combo.set_active(0)
        combo.connect("changed", self.on_rom_combo)
        horizontal_box.pack_start(combo, True, True, 0)
        # Empty space
        space = Gtk.Label("")
        horizontal_box.pack_start(space, True, True, 20)
        horizontal_box.set_homogeneous(True)
        vertical_box.pack_start(horizontal_box, False, True, 5)

        horizontal_box = Gtk.Box()
        label = Gtk.Label("Character set:")
        horizontal_box.pack_start(label, True, True, 0)
                # List of romanisation available
        name_store = Gtk.ListStore(str)
        rom = ["Simplified", "Traditional"]
        for value in rom:
            name_store.append([value])
        combo = Gtk.ComboBox.new_with_model(name_store)
        renderer_text = Gtk.CellRendererText()
        combo.pack_start(renderer_text, True)
        combo.add_attribute(renderer_text, "text", 0)
        if self.data_object.hanzi == 'traditional':
            combo.set_active(1)
        else:
            combo.set_active(0)
        combo.connect("changed", self.on_char_combo)
        horizontal_box.pack_start(combo, True, True, 0)

        space = Gtk.Label("")
        horizontal_box.pack_start(space, True, True, 20)
        horizontal_box.set_homogeneous(True)
        vertical_box.pack_start(horizontal_box, False, True, 5)

        about_text = Gtk.Frame(label_yalign=1, label_xalign=1)
        about_text.set_label("\n\n\n\n"
                             "Zhudi, 2011-2019")
        vertical_box.pack_start(about_text, True, True, 5)
        return vertical_box

    def on_rom_combo(self, combo):
        """ Action when the romanisation is changed. """
        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            value = model[tree_iter][0]
            self.data_object.romanisation = value.lower()
            self.data_object.save_config()

    def on_char_combo(self, combo):
        """ Action when the set is changed. """
        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            value = model[tree_iter][0]
            self.data_object.hanzi = value.lower()
            self.data_object.save_config()


class MainWindow(object):
    """ Class that defines the welcome screen, and gives access to other layers.
    """

    def __init__(self, data_object, language):
        self.window = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
        self.window.set_default_size(700, 500)
        self.window.set_title("Zhudi")
        self.window.set_position(Gtk.WindowPosition.CENTER)
        self.window.connect("key-press-event", self.on_key_press)
        self.window.connect("key-release-event", self.on_key_release)
        self.data_object = data_object
        self.language = language
        self.dict_gui = None
        self.dict_settings = None
        self.seg_gui = None
        self.tab_box = None
        self.vbox = None

    @staticmethod
    def loop():
        """ Starting things! """
        Gtk.main()

    def build(self):
        """ Mandatory build function. """
        self.data_object.create_set_chinese_characters()
        global DICTIONARY_TOOLS_OBJECT
        DICTIONARY_TOOLS_OBJECT = zhudi.processing.DictionaryTools()
        global SEGMENTATION_TOOLS_OBJECT
        SEGMENTATION_TOOLS_OBJECT = zhudi.processing.SegmentationTools()
        SEGMENTATION_TOOLS_OBJECT.load(self.data_object)
        # Welcome tab
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)

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

        self.window.add(self.tab_box)
        self.window.connect("destroy", Gtk.main_quit)
        self.window.show_all()


    def options_gui(self):
        """ Options tab. """
        return OptionsWidget(self.data_object).build()

    def dictionary_gui(self):
        """ Start the dictionary widget. """
        ui = DictionaryWidgetMain(self.data_object)
        ui.language = self.language
        return ui, ui.build()

    def segmentation_gui(self):
        """ Start the segmentation widget. """
        return SegmentationWidget(self.data_object).build()

    def on_key_press(self, widget, event, data=None):
        if self.tab_box.get_current_page() == 0 and not self.dict_settings.search_field.has_focus() and event.keyval not in {Gdk.KEY_Up, Gdk.KEY_Down}:
            if event.keyval == Gdk.KEY_Left or event.keyval == Gdk.KEY_Right:
                self.dict_settings.search_field.grab_focus_without_selecting()
            else:
                self.dict_settings.search_field.grab_focus()

    @staticmethod
    def on_key_release(widget, event, data=None):
        """
        Crtl-w to quit the application.

        """
        if event.keyval == Gdk.KEY_w and event.state & Gdk.ModifierType.CONTROL_MASK:
            Gtk.main_quit()
