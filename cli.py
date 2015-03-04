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
    st.load(data)

    search_order = (
        data.translation,
        data.pinyin,
        data.simplified,
        data.traditional,
    )

    sentence = st.sentence_segmentation(query)
    print(sentence)

    for dict in search_order:
        dt.search(dict, query)
        if dt.index:
            for result in dt.index:
                chinese = data.simplified[result].strip()
                pronunciation = ' '.join([dt.unicode_pinyin(p) for p in data.pinyin[result].strip().split()])
                translation_variations = data.translation[result].strip().split('/')
                translations = '\n — — ⇾ '.join(translation_variations)
                print('{} — {} — {} '.format(chinese, pronunciation, translations))


if __name__ == '__main__':
    main()
