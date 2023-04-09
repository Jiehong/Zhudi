#!/usr/bin/env python

import argparse

from zhudi import data, processing, chinese_table


def get_argument_parser():
    """
    Handle parsing the input arguments.

    """

    parser = argparse.ArgumentParser(
        description="Zhudi, GTK4 interface for EDICT dictonaries"
    )
    return parser
