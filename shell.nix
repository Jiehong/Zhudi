with import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/0040164e473509b4aee6aedb3b923e400d6df10b.tar.gz") {};
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
    (python310.withPackages ( ps: with ps; [ pycairo dbus-python pygobject3 ]))
  ];

  inputs = basePackages;

  # define shell startup command
  hooks = ''
    echo 'first time: poetry install'
    echo 'then: poetry run python zhudi/zhudi_gui.py'
    echo 'OR python -m zhudi'
  '';

in mkShell {
  buildInputs = inputs;
  shellHook = hooks;
}
