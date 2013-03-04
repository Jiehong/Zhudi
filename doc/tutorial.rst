Tutorial
========

Installation
------------

If you use Archlinux, this is very simple since the package is in AUR.
Therefore, just type:
.. code-block::
    yaourt -S zhudi

If you are not using Archlinux, but still use a Linux distribution, follow
those steps:

 1. Clone the git repo into a local directory:
 ::
     git clone https://github.com/Jiehong/Zhudi.git

 2. Install Zhudi:
 ::
     python setup.py install --prefix=/usr --optimize=1

Zhudi is now installed, and you can try to launch it by typing *zhudi*.

.. note::
    Zhudi depends on the following packages to work:
     - python 3+
     - python-gobject
     - pygobject-devel
     - gobject-introspection
     - pango

First use of Zhudi
------------------

However, using Zhudi means you need to choose and download a source of data.
Please, download the dictionary database you would like to use in the *.u8
format.

When this is done, you need to prepare the data for Zhudi to use. To do so,
type (assuming you have downloaded cedict):
::
    python zhudi.py -s cedict.u8

The previous command will launch zhudi in *split* mode, and will created the
following files:
 - pinyin;
 - zhuyin;
 - simplified;
 - traditional;
 - translation.

You need to move those files in *~/.zhudi*.

When the process is finished, you can discard your *.u8 file if you want.

Launch Zhudi
------------

Now, Zhudi is ready to be used, and can be simply launched by typing *zhudi* in
a terminal!
