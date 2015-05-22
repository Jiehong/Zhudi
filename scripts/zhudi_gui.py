#!/usr/bin/env python
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


from zhudi import gui, prepare_data, get_argument_parser, WrongInputException


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
