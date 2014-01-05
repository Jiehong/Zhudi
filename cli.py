#!/usr/bin/env python

from zhudi import prepare_data, get_argument_parser
from zhudi_processing import DictionaryTools, SegmentationTools


def get_arguments():
    parser = get_argument_parser()
    parser.add_argument('--exact', action='store_true')
    parser.add_argument('query', nargs='+')
    return parser.parse_args()


def main():
    args = get_arguments()
    query = args.query
    exact = args.exact

    data, hanzi, romanisation, language = prepare_data(args)
    dt = DictionaryTools()
    st = SegmentationTools()
    st.load(data)

    search_order = (
        data.translation,
        data.pinyin,
        data.simplified,
    )

    if len(query) == 1:
        sentence = st.sentence_segmentation(' '.join(query))
        if len(sentence) > 2:
            query = sentence
            exact = True
            search_order = (data.simplified, )

    for word in query:
        for dict in search_order:
            if exact:
                result = st.searchUnique(word, data)
                if result:
                    _print_result(result, data, dt)
            else:
                dt.search(dict, word)
                for result in dt.index:
                    _print_result(result, data, dt)


def _print_result(result, data, dt):
    chinese = data.simplified[result].strip()
    pronunciation = ' '.join([dt.unicode_pinyin(p) for p in data.pinyin[result].strip().split()])
    translation_variations = data.translation[result].strip().split('/')
    translations = '\n — — ⇾ '.join(translation_variations)
    print('{} — {} — {} '.format(chinese, pronunciation, translations))


if __name__ == '__main__':
    main()
