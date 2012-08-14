# coding=utf8
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
  
from gi.repository import Gtk, Pango
import data

class option_window():
  def kill_ok(self):
    self.window.hide()

  def __init__(self, main_window):
    self.hanzi = ''
    self.romanisation = ''
    self.mw = main_window
    # Definition of the options window
    self.window = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
    self.window.set_size_request(300,180)
    self.window.set_title("Options")
    self.window.set_position(Gtk.WindowPosition.CENTER)
    self.window.connect("destroy", lambda x:self.window.destroy)

  def build(self):
    # Hanzi label
    hanzi_label = Gtk.Label()
    hanzi_label.set_text("<big>Chinese characters form:</big>")
    hanzi_label.set_justify(Gtk.Justification.LEFT)
    hanzi_label.set_use_markup(True)
    # hanzi box
    hanzi_box = Gtk.Grid()
    Traditional = Gtk.RadioButton.new_with_label_from_widget(None,
                                                             "Traditional")
    Traditional.connect("clicked", lambda x: self.set_hanzi("Traditional"))
    hanzi_box.add(Traditional)
    Simplified = Gtk.RadioButton.new_with_label_from_widget(Traditional,
                                                            "Simplified")
    Simplified.connect("clicked", lambda x: self.set_hanzi("Simplified"))
    hanzi_box.attach_next_to(Simplified,
                             Traditional,
                             Gtk.PositionType.RIGHT,1,1)
    hanzi_box.set_column_homogeneous(True)

    # Romanisation label
    romanisation_label = Gtk.Label()
    romanisation_label.set_text("<big>Pronunciation system:</big>")
    romanisation_label.set_justify(Gtk.Justification.LEFT)
    romanisation_label.set_use_markup(True)

    # romanisation box
    romanisation_box = Gtk.Grid()
    Zhu = Gtk.RadioButton.new_with_label_from_widget(None,"Zhuyin Fuhao")
    Zhu.connect("clicked", lambda x: self.set_romanisation("Zhuyin"))
    romanisation_box.add(Zhu)
    Pin = Gtk.RadioButton.new_with_label_from_widget(Zhu,"Hanyu Pinyin")
    Pin.connect("clicked", lambda x: self.set_romanisation("Pinyin"))
    romanisation_box.attach_next_to(Pin, Zhu, Gtk.PositionType.RIGHT,1,1)
    romanisation_box.set_column_homogeneous(True)
    # Horizontal separator
    option_horizontal_separator = Gtk.Separator()
    # Ok button
    ok_button = Gtk.Button("Ok")
    ok_button.connect("clicked", lambda x:self.kill_ok())
    # Mapping of the option window
    loption_vertical_box = Gtk.Grid()
    loption_vertical_box.add(hanzi_label)
    loption_vertical_box.attach_next_to(hanzi_box,
                                        hanzi_label,
                                        Gtk.PositionType.BOTTOM,1,1)
    loption_vertical_box.attach_next_to(romanisation_label,
                                        hanzi_box,
                                        Gtk.PositionType.BOTTOM,1,1)
    loption_vertical_box.attach_next_to(romanisation_box,
                                        romanisation_label,
                                        Gtk.PositionType.BOTTOM,1,1)
    loption_vertical_box.attach_next_to(option_horizontal_separator,
                                        romanisation_box,
                                        Gtk.PositionType.BOTTOM,1,1)
    loption_vertical_box.attach_next_to(ok_button,
                                        option_horizontal_separator,
                                        Gtk.PositionType.BOTTOM,1,2)
    loption_vertical_box.set_column_homogeneous(True)
    loption_vertical_box.set_row_homogeneous(True)

    # Adding them in the main window
    self.window.add(loption_vertical_box)

    # Eventually, show the option window and the widgetss
    self.window.show_all()

    if self.hanzi == "Traditional":
      Traditional.set_active(True)
    else:
      Simplified.set_active(True)
    if self.romanisation == "Zhuyin":
      Zhu.set_active(True)
    else:
      Pin.set_active(True)

  def set_romanisation(self, string):
    self.mw.romanisation = string

  def set_hanzi(self, string):
    self.mw.hanzi = string
# End of Option_window

def open_option(self):
  opt = option_window(self)
  opt.hanzi = self.hanzi
  opt.romanisation = self.romanisation
  opt.build()

class main_window ():
  def __init__(self, dictionary):
    self.hanzi = ""
    self.romanisation = ""
    self.language = ""
    self.dictionary = dictionary
    self.lock = False
    # Definition of the main window
    self.window = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
    self.window.set_default_size(800,494) # Gold number ratio
    self.window.set_title("Zhudi")
    self.window.set_position(Gtk.WindowPosition.CENTER)

  def build(self):
    # Search label
    search_label = Gtk.Label()
    search_label.set_text("<big>Searching area</big>")
    search_label.set_use_markup(True)

    # Search field
    search_field = Gtk.Entry()
    search_field.set_visible(True)
    search_field.connect("activate",
                         lambda x: self.search_asked(search_field))
    search_field.set_placeholder_text("Type your query here…")

    # Go, search! button
    go_button = Gtk.Button("Search")
    go_button.connect("clicked",
                      lambda x: self.search_asked(search_field))

    # Options button
    option_button = Gtk.Button("Options")
    option_button.connect("clicked", lambda x: open_option(self))

    # Search + button box
    SB_box = Gtk.Grid()
    SB_box.attach(search_field,0,0,4,1)
    SB_box.attach_next_to(go_button,
                          search_field,
                          Gtk.PositionType.RIGHT,1,1)
    SB_box.attach_next_to(option_button,
                          go_button,
                          Gtk.PositionType.RIGHT,1,1)
    SB_box.set_column_homogeneous(True)

    # Search label zone
    frame_search = Gtk.Frame()
    frame_search.set_label_widget(search_label)
    frame_search.add(SB_box)

    # Language box
    language_box = Gtk.Grid()
    Chinese = Gtk.RadioButton.new_with_label_from_widget(None,
                                                         "From Chinese")
    Chinese.connect("clicked", lambda x: self.set_language("Chinese"))
    language_box.add(Chinese)
    Latin = Gtk.RadioButton.new_with_label_from_widget(Chinese,
                                                       "To Chinese")
    Latin.connect("clicked", lambda x: self.set_language("Latin"))
    language_box.attach_next_to(Latin,Chinese,Gtk.PositionType.RIGHT,1,1)
    language_box.set_column_homogeneous(True)
    Chinese.set_active(True)

    # Results part in a list
    self.results_list = Gtk.ListStore(str)
    results_tree = Gtk.TreeView(self.results_list)
    renderer = Gtk.CellRendererText()
    results_tree.tvcolumn = Gtk.TreeViewColumn("Results", renderer, text=0)
    results_tree.append_column(results_tree.tvcolumn)
    self.results_list.cell = Gtk.CellRendererText()
    results_tree.tvcolumn.pack_start(self.results_list.cell, True)
    results_tree.set_enable_search(False)
    results_tree.tvcolumn.set_sort_column_id(False)
    results_tree.set_reorderable(False)
    select = results_tree.get_selection()
    select.connect("changed", self.display_another_result)

    results_scroll = Gtk.ScrolledWindow()
    # No horizontal bar, automatic vertical bar
    results_scroll.set_policy(Gtk.PolicyType.NEVER,
                              Gtk.PolicyType.AUTOMATIC)
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
    tr = self.translation_box.get_buffer()
    bold = tr.create_tag(weight=Pango.Weight.BOLD)
    big = tr.create_tag(size=30*Pango.SCALE)
    medium = tr.create_tag(size=15*Pango.SCALE)
    blue = tr.create_tag(foreground="blue")

    translation_scroll = Gtk.ScrolledWindow()
    translation_scroll.add_with_viewport(self.translation_box)

    frame_translation = Gtk.Frame()
    frame_translation.set_label_widget(translation_label)
    frame_translation.add(translation_scroll)

    # Mapping of the main window
    left_vertical_box = Gtk.Grid()
    left_vertical_box.add(frame_search)
    left_vertical_box.attach_next_to(language_box,
                                     frame_search,
                                     Gtk.PositionType.BOTTOM,1,1)
    left_vertical_box.attach_next_to(frame_results,
                                     language_box,
                                     Gtk.PositionType.BOTTOM, 1, 7)
    left_vertical_box.set_row_homogeneous(True)
    left_vertical_box.set_column_homogeneous(True)

    right_vertical_box = Gtk.Grid()
    right_vertical_box.add(frame_translation)
    right_vertical_box.set_column_homogeneous(True)
    right_vertical_box.set_row_homogeneous(True)

    horizontal_box = Gtk.Grid()
    horizontal_box.attach(left_vertical_box,0,0,1,1)
    horizontal_box.attach_next_to(right_vertical_box,
                                  left_vertical_box,
                                  Gtk.PositionType.RIGHT,1,1)
    horizontal_box.set_column_homogeneous(True)
    horizontal_box.set_row_homogeneous(True)

    # Adding them in the main window
    self.window.add(horizontal_box)

    self.window.connect("destroy",Gtk.main_quit)
    self.window.show_all()

  def search_asked(self, searchfield):
    text = searchfield.get_text()
    if text == "":
      self.lock = True
      self.dictionary.index_list = []
      self.results_list.clear()
      self.display_translation(0)
    else:
      self.lock = False
      if self.language == "Latin":
        given_list = self.dictionary.translation
      elif self.hanzi == "Traditional":
        given_list = self.dictionary.traditional
      else:
        given_list = self.dictionary.simplified
      self.dictionary.search(given_list, text)
      self.update_results()
      self.display_translation(0)
  # end of search_asked

  def set_language(self, string):
    self.language = string

  def display_translation(self, which):
    tr = self.translation_box.get_buffer()
    if len(self.dictionary.index_list) == 0:
      tr.set_text("Nothing found.")
      if len(self.results_list) == 0:
        self.results_list.append(["Nothing found."])
      return
    else:
      index = self.dictionary.index_list[which]

    if self.hanzi == "Traditional":
      hanzi_dic = self.dictionary.traditional
    else:
      hanzi_dic = self.dictionary.simplified
    if self.romanisation == "Zhuyin":
      romanisation_dic = self.dictionary.zhuyin
    else:
      romanisation_dic = self.dictionary.pinyin

    slash_list = []
    t = self.dictionary.translation[index]
    for l in range(len(t)):
      if t[l] == "/":
        slash_list.append(l)
    temp = 0
    trans = []
    for k in range(len(slash_list)):
      trans.append(str(k+1)+". "+t[temp:slash_list[k]])
      temp = slash_list[k]+1
    trans.append(str(len(slash_list)+1)+". "+t[temp:len(t)])
    string = ""
    for i in range(len(slash_list)+1):
      string = string + trans[i]+"\n"

    # Add [] arround the pronounciation parts
    p_string = romanisation_dic[index].split()
    pronounciation_string = []
    for point in range(len(p_string)):
      pronounciation_string.append("[")
      pronounciation_string.append(p_string[point])
      pronounciation_string.append("]")
    # pronounciation_string = p_string
    tr.set_text("Chinese\n"+hanzi_dic[index]+
                "\n\n"+"Pronunciation\n"+''.join(pronounciation_string)+
                "\n\nMeaning\n"+string) # Display in the Translation box
    bold = tr.create_tag(weight=Pango.Weight.BOLD)
    big = tr.create_tag(size=30*Pango.SCALE)
    medium = tr.create_tag(size=15*Pango.SCALE)
    blue = tr.create_tag(foreground="blue")
    # "Chinese" in bold
    start_1 = tr.get_iter_at_line(0)
    end_1 = tr.get_iter_at_line(0)
    end_1.forward_to_line_end()
    tr.apply_tag(bold, start_1, end_1)
    # Bigger Chinese
    start_c = tr.get_iter_at_line(1)
    end_c = tr.get_iter_at_line(1)
    end_c.forward_to_line_end()
    tr.apply_tag(big, start_c, end_c)
    # "Pronunciation" in bold
    start_2 = tr.get_iter_at_line(4)
    end_2 = tr.get_iter_at_line(4)
    end_2.forward_to_line_end()
    tr.apply_tag(bold, start_2, end_2)
    # "Pronunciation" in blue
    start_3 = tr.get_iter_at_line(5)
    end_3 = tr.get_iter_at_line(5)
    end_3.forward_to_line_end()
    tr.apply_tag(blue, start_3, end_3)
    tr.apply_tag(medium,start_3, end_3)
    # "Meaning" in bold
    start_3 = tr.get_iter_at_line(7)
    end_3 = tr.get_iter_at_line(7)
    end_3.forward_to_line_end()
    tr.apply_tag(bold, start_3, end_3)

  def update_results(self):
    self.results_list.clear()
    displayed_index = 1
    t = 40 # threshold for line wrap
    for k in self.dictionary.index_list:
      if self.language == "Latin":
        string = self.dictionary.translation[k]
      elif self.hanzi == "Traditional":
        string = self.dictionary.traditional[k]
      else:
        string = self.dictionary.simplified[k]
      if len(string) > t:
        string = str(displayed_index)+". "+string[0:t]+"…"
      else:
        string = str(displayed_index)+". "+string
      string = string[:-1] # no \n
      self.results_list.append([string])
      displayed_index += 1

  def display_another_result(self, selection):
    if not self.lock:
      model, treeiter = selection.get_selected()
      if treeiter is not None:
        row = model[treeiter][0]
        t = 0
        if row is not None:
          while row[t] != ".":
            t += 1
          figure = row[0:t]
          self.display_translation(int(figure)-1)

  def loop(self):
    Gtk.main()
# end of main_Window
