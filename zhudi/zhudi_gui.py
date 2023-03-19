#!/usr/bin/env python
# coding: utf-8

from zhudi.ui.application import ZhudiApplication
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

    app = ZhudiApplication(data_object=data_object, language="Chinese")
    app.run()


if __name__ == "__main__":
    main()
