#!/usr/bin/env python
# coding: utf-8

import gui
from __init__ import prepare_data, get_argument_parser, WrongInputException


def main():
    """
    Preparing, and launching the main window

    """

    parser = get_argument_parser()
    options = parser.parse_args()

    try:
        data_object = prepare_data(options)
    except WrongInputException:
        parser.print_help()

    mw = gui.MainWindow(data_object, language="Chinese")
    mw.build()
    mw.loop()


if __name__ == "__main__":
    main()
