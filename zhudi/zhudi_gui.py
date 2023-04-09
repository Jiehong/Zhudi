#!/usr/bin/env python
from zhudi.dictionaries import Dictionaries
from zhudi.preferences import Preferences
from zhudi.ui.application import ZhudiApplication
from zhudi.__init__ import get_argument_parser


def main():
    """
    Preparing, and launching the main window

    """

    parser = get_argument_parser()
    options = parser.parse_args()

    preferences = Preferences()
    dictionaries = Dictionaries()

    app = ZhudiApplication(
        dictionaries=dictionaries, language="Chinese", preferences=preferences
    )
    app.run()


if __name__ == "__main__":
    main()
