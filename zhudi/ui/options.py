from gi.repository import Gtk

from zhudi.data import Data


class OptionsWidget(object):
    """Class defining the Options/About tab layout"""

    def __init__(self, data_object: Data):
        self.data_object: Data = data_object

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
        romanization_dropdown = Gtk.DropDown.new_from_strings(["Pinyin", "Zhuyin"])
        # Set active the saved value
        if self.data_object.romanisation == "zhuyin":
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
            ["Simplified", "Traditional"]
        )
        if self.data_object.hanzi == "traditional":
            characters_dropdown.set_selected(1)
        else:
            characters_dropdown.set_selected(0)
        characters_dropdown.connect("notify::selected", self.on_characters_selected)
        horizontal_box.append(characters_dropdown)
        horizontal_box.set_homogeneous(True)
        space = Gtk.Label(label="")
        horizontal_box.append(space)
        vertical_box.append(horizontal_box)

        about_text = Gtk.Frame()
        about_text.set_label("Zhudi, 2011-2023")
        about_text.set_label_align(1.0)
        about_text.set_valign(Gtk.Align.END)
        vertical_box.append(about_text)
        about_text.set_vexpand(True)
        return vertical_box

    def on_romanization_selected(self, dropdown: Gtk.DropDown, _ignore) -> None:
        selected = dropdown.get_selected_item().get_string()
        if selected is not None:
            self.data_object.romanisation = selected.lower()
            self.data_object.save_config()

    def on_characters_selected(self, dropdown: Gtk.DropDown, _ignore) -> None:
        selected = dropdown.get_selected_item().get_string()
        if selected is not None:
            self.data_object.hanzi = selected.lower()
            self.data_object.save_config()
