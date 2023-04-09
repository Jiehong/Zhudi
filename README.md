# What is Zhudi?

Zhudi is a GTK4 graphical interface to the EDICT dictionaries. The following ones are
included by default:

* [CEDICT](https://www.mdbg.net/chinese/dictionary?page=cedict) for English-Chinsese ;
* [CFDICT](https://www.chine-informations.com/chinois/open/CFDICT/) for French-Chinese ;
* [HanDeDict](http://www.handedict.de/chinesisch_deutsch.php) For German-Chinese ;

## Features

- Traditional & Simplified Chinese characters;
- Zhuyin & Pinyin pronunciation;
- Display of shape-based input methods: [cangjie5/倉頡5](https://en.wikipedia.org/wiki/Cangjie_input_method), [array30/行列30](https://zh.wikipedia.org/wiki/%E8%A1%8C%E5%88%97%E8%BC%B8%E5%85%A5%E6%B3%95), [wubi86/五筆86](https://en.wikipedia.org/wiki/Wubi_method);
- Runs entirely locally on your own device;
- Follows the [XDG spec](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html).

## What platforms are supported?

Since this project is written in Python 3.10+ & GTK4, it should be able to run on any given platform.
However, I only have tested it under GNU/Linux (Gnome).

## What are the dependencies of Zhudi?

In order to run Zhudi, you need the following packages:
* python 3.10+
* python-gobject
* pygobject-devel
* gobject-introspection

You also need to have GTK 4 installed.

## Installation

### Pip

Zhudi can be installed using python's package manager `pip` as follows:

    pip install git+https://github.com/Jiehong/Zhudi

### Launching

Run it by invoking it directly:

```shell
zhudi
```

You should see the GUI up and running:

![GUI screenshot](gui_screenshot.png)

## Development

Locally, you can use poetry.

First time:

```shell
poetry install
```

Then:

```shell
poetry run python -m zhudi
```

### Command line usage

You also have access to a limited command line search as follows:

    $ zhu 我
    我    ㄨㄛˇ    I
               ⇾ me

Unlike the GUI, this only provides the first and best match so far.

### Unit tests

dict_test.u8 is used to test the splitting of the dictionary, and then for the rest of the unittests.

First, test that splitting the dictionary is working well:

```shell
poetry run python test_cli.py
```

Then, test the rest of the units:

```shell
poetry run python -m unittest
```

### Formatting

Source files are formatted with `black`:

```shell
poetry run python -m black zhudi && poetry run python -m black tests
```

### New Dictionaries

Download any EDICT dictionary with the `*.u8` format, and modify `db_fill.py` to read it.

Then run:

```shell
poetry run python db_fill.py
```
