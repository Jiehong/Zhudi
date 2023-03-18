with import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/cd34d6ed7ba7d5c4e44b04a53dc97edb52f2766c.tar.gz") {};
let
  basePackages = [
    poetry
    gtk4
    pango
    glib
    gobject-introspection
    gdk-pixbuf
    python3
    libnotify
    libadwaita
    (python3.withPackages ( ps: with ps; [ pycairo dbus-python pygobject3 ]))
  ];

  inputs = basePackages;

  # define shell startup command
  hooks = ''
    echo 'first time: poetry install'
    echo 'then: poetry run python zhudi/zhudi_gui.py -p tests/pinyin -z tests/zhuyin -tr tests/translation -td tests/traditional -sd tests/simplified'
  '';

in mkShell {
  buildInputs = inputs;
  shellHook = hooks;
}
