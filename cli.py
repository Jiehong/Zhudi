#!/usr/bin/env python

from zhudi import prepare_data, get_argument_parser
from zhudi_processing import DictionaryTools, SegmentationTools


def get_arguments():
    parser = get_argument_parser()
    parser.add_argument('query', nargs='+')
    return parser.parse_args()


def main():
    args = get_arguments()
    query = ' '.join(args.query)

    data, hanzi, romanisation, language = prepare_data(args)
    dt = DictionaryTools()
    st = SegmentationTools()

    search_order = (
        data.translation,
        data.pinyin,
        data.simplified,
        data.traditional)

    for dict in search_order:
        dt.search(dict, query)
        if dt.index:
            for result in dt.index:
                print('{}    ({})    —    {}'.format(
                    data.simplified[result].strip(),
                    data.pinyin[result].strip(),
                    data.translation[result].strip()))
        break

if __name__ == '__main__':
    main()
