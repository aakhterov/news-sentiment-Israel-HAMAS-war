import argparse
from bbc_live_news_collector import BBCNewsCollector
from save_to_file import SaveToFile
from classificator import Classificator

if __name__ == "__main__":
    parser = argparse.ArgumentParser("news_collector")
    parser.add_argument("producer", type=str, help="Producer of the news", choices=['bbc'])
    parser.add_argument("path", type=str, help="Path for saving files")
    parser.add_argument("format", type=str, help="Files format", choices=['csv', 'parquet'])
    parser.add_argument("url", type=str, help="News page url", default=None)
    args = parser.parse_args()

    news = []
    if args.producer == 'bbc':
        bbc_collector = BBCNewsCollector()
        cl = Classificator()

        if args.url is None:
            news = bbc_collector.collect()
        else:
            news = bbc_collector.collect_all_pages(args.url)
        for idx, n in enumerate(news):
            news[idx]["pro_israel_score"] = cl.predict(n["text"])

    saver = SaveToFile()
    path = args.path if args.path[-1] == '/' else args.path + '/'
    if args.format == 'csv':
        saver.save(path, data=news, format='csv')
    else:
        saver.save(path, data=news, format='parquet')

# ['https://www.bbc.com/news/live/world-middle-east-67446662',
#  'https://www.bbc.com/news/live/world-middle-east-67423274',
#  'https://www.bbc.com/news/live/world-middle-east-67400490',
#  'https://www.bbc.com/news/live/world-middle-east-67385263',
#  'https://www.bbc.com/news/live/world-middle-east-67364296',
#  'https://www.bbc.com/news/live/world-middle-east-67339462',
#  'https://www.bbc.com/news/live/world-middle-east-67324897',
# 'https://www.bbc.com/news/live/world-middle-east-67466779'
# 'https://www.bbc.com/news/live/world-middle-east-67481139',
# 'https://www.bbc.com/news/live/world-middle-east-67504657'
# 'https://www.bbc.com/news/live/world-middle-east-67539313'
# 'https://www.bbc.com/news/live/world-middle-east-67527098',
# 'https://www.bbc.com/news/live/world-middle-east-67562488'
# 'https://www.bbc.com/news/live/world-middle-east-67584895'
# 'https://www.bbc.com/news/live/world-middle-east-67653615',
# 'https://www.bbc.com/news/live/world-middle-east-67672759',
# 'https://www.bbc.com/news/live/world-middle-east-67687628',
# 'https://www.bbc.com/news/live/world-middle-east-67709805',
# 'https://www.bbc.com/news/live/world-middle-east-67768062',
# 'https://www.bbc.com/news/live/world-middle-east-67746033',
# 'https://www.bbc.com/news/live/world-middle-east-67847427',
# 'https://www.bbc.com/news/live/world-middle-east-67732895',
# 'https://www.bbc.com/news/live/world-middle-east-67799517',
# 'https://www.bbc.com/news/live/world-middle-east-67831997']