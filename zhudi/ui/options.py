from gi.repository import Gtk

from zhudi.dictionaries import Dictionaries
from zhudi.preferences import Preferences


class OptionsWidget(object):
    """Class defining the Options/About tab layout"""

    def __init__(self, preferences: Preferences, dictionaries: Dictionaries):
        self.preferences: Preferences = preferences
        self.dictionaries: Dictionaries = dictionaries

    def build(self) -> Gtk.Box:
        vertical_box = Gtk.Box()
        vertical_box.set_orientation(Gtk.Orientation.VERTICAL)
        vertical_box.set_homogeneous(False)
        vertical_box.set_spacing(10)

        title = Gtk.Label(label="")
        vertical_box.append(title)

        horizontal_box = Gtk.Box()
        label = Gtk.Label(label="Romanisation:")
        horizontal_box.append(label)
        romanization_dropdown = Gtk.DropDown.new_from_strings(["pinyin", "zhuyin"])
        # Set active the saved value
        if self.preferences.get_romanization() == "zhuyin":
            romanization_dropdown.set_selected(1)
        else:
            romanization_dropdown.set_selected(0)
        romanization_dropdown.connect("notify::selected", self.on_romanization_selected)
        horizontal_box.append(romanization_dropdown)
        # Empty space
        space = Gtk.Label(label="")
        horizontal_box.append(space)
        horizontal_box.set_homogeneous(True)
        vertical_box.append(horizontal_box)

        horizontal_box = Gtk.Box()
        label = Gtk.Label(label="Character set:")
        horizontal_box.append(label)
        characters_dropdown = Gtk.DropDown.new_from_strings(
            ["simplified", "traditional"]
        )
        if self.preferences.get_character_set() == "traditional":
            characters_dropdown.set_selected(1)
        else:
            characters_dropdown.set_selected(0)
        characters_dropdown.connect("notify::selected", self.on_characters_selected)
        horizontal_box.append(characters_dropdown)
        horizontal_box.set_homogeneous(True)
        space = Gtk.Label(label="")
        horizontal_box.append(space)
        vertical_box.append(horizontal_box)

        horizontal_box = Gtk.Box()
        label = Gtk.Label(label="Language:")
        horizontal_box.append(label)
        languages = self.dictionaries.get_languages()
        language_dropdown = Gtk.DropDown.new_from_strings(languages)
        i = languages.index(self.preferences.get_language())
        language_dropdown.set_selected(i)
        language_dropdown.connect("notify::selected", self.on_language_selected)
        horizontal_box.append(language_dropdown)
        horizontal_box.set_homogeneous(True)
        space = Gtk.Label(label="")
        horizontal_box.append(space)
        vertical_box.append(horizontal_box)

        about_text = Gtk.Frame()
        about_text.set_label(
            "CEDICT (English-Chinese) under CC BY-SA 4.0\n"
            "CFDICT (French-English) under CC BY-SA 3.0\n"
            "HanDeDict (German-English) under CC BY-SA 2.0 EN\n\n"
            "Zhudi, 2011-2023"
        )
        about_text.set_label_align(0)
        about_text.set_valign(Gtk.Align.END)
        vertical_box.append(about_text)
        about_text.set_vexpand(True)
        return vertical_box

    def on_romanization_selected(self, dropdown: Gtk.DropDown, _ignore) -> None:
        selected = dropdown.get_selected_item().get_string()
        if selected is not None:
            self.preferences.set_romanization(selected)

    def on_characters_selected(self, dropdown: Gtk.DropDown, _ignore) -> None:
        selected = dropdown.get_selected_item().get_string()
        if selected is not None:
            self.preferences.set_character_set(selected)

    def on_language_selected(self, dropdown: Gtk.DropDown, _ignore) -> None:
        selected = dropdown.get_selected_item().get_string()
        if selected is not None:
            self.preferences.set_language(selected)
