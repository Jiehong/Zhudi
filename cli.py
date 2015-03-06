#!/usr/bin/env python
# coding: utf-8

from zhudi import prepare_data, get_argument_parser
from zhudi_processing import DictionaryTools, SegmentationTools, PreProcessing


def get_arguments():
    parser = get_argument_parser()
    parser.add_argument('--expand', action='store_true')
    parser.add_argument('query', nargs='+')
    return parser.parse_args()


def main():
    args = get_arguments()
    query = args.query
    expand = args.expand

    data, hanzi, romanisation, language = prepare_data(args)
    dt = DictionaryTools()
    st = SegmentationTools()
    pp = PreProcessing()
    st.load(data)
    config = pp.get_config()
    romanisation = _get_config_value('romanisation', config)
    hanzi = _get_config_value('hanzi', config)

    search_order = (
        data.translation,
        getattr(data, romanisation),
        getattr(data, hanzi),
    )

    potential_sentence = st.sentence_segmentation(' '.join(query))
    if len(potential_sentence) > 1:
        query = potential_sentence
        search_order = (getattr(data, hanzi), )

    for word in query:
        results = set()
        for dict in search_order:
            # TODO searchUnique seems to work only on chinese
            # implementation for pinyin/zhuyin and english/french/etc is needed
            if not expand:
                result = st.searchUnique(word, data)
                if result and result not in results:
                    results.add(result)
                    _print_result(result, data, dt, hanzi, romanisation)

            if expand or not results:
                dt.search(dict, word)
                for result in dt.index:
                    results.add(result)
                    _print_result(result, data, dt, hanzi, romanisation)


def _print_result(result, data, dt, hanzi, romanisation):
    chinese = getattr(data, hanzi)[result].strip()
    pronunciation = ' '.join([dt.unicode_pinyin(p) for p in
                              getattr(data, romanisation)[result]
                              .strip().split()])
    translation_variations = data.translation[result].strip().split('/')
    translations = '\n — — ⇾ '.join(translation_variations)
    print('{} — {} — {} '.format(chinese, pronunciation, translations))


def _get_config_value(key, config):
    return next(v for k, v in config if k == key)

if __name__ == '__main__':
    main()
