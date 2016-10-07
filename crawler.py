import argparse
import mechanize
import re
from BeautifulSoup import BeautifulSoup as bs


def parse_args():
    '''
    Parses the node2vec arguments.
    '''
    parser = argparse.ArgumentParser(description="Get node embeddings.")

    parser.add_argument('--output', default='dblp-data.csv',
                        help='Output file.')

    parser.add_argument('--verbose', dest='verbose', action='store_true',
                        help='Stdout gensim info. Default is false. Only used if log-output is false.')

    return parser.parse_args()


authors = set()


# http://dblp.uni-trier.de/pers/hd/z/Zhang:Shao_Jie
# http://dblp.uni-trier.de/pers/hd/g/Gao_0001:Wen?q=Wen%24+Gao%24+0001%24
# http://dblp.uni-trier.de/pers/hd/p/Poor:H=_Vincent?q=H.%24+Vincent%24+Poor%24
def get_author_id_from_url(url):
    regex = 'http:\/\/dblp\.uni-trier\.de\/pers\/hd\/\w\/([^\?\n]+)(\?q=)?'
    m = re.match(regex, url)
    if not m:
        raise Exception("Error with url %s being parsed as author" % url)

    return m.groups()[0]


def parse_author_page(page, name):
    print '\tGetting author: %s' % (name)
    print '\t\t%s' % get_author_id_from_url(page.geturl())
    author = get_author_id_from_url(page.geturl())
    if author in authors:
        return
    authors.add(get_author_id_from_url(page.geturl()))

    # soup = bs(page)


def parse_disambiguation_page(br, name):
    print '\tDisambiguating: %s' % (name)

    for link in br.links(url_regex="pers\/hd\/"):
        crawl_page(br, link)


def crawl_page(br, link):
    # if link.url in crawl_page.crawled:
    #     return
    # crawl_page.crawled.add(link.url)

    page = br.follow_link(link)

    page_title = br.title()
    name = link.text

    regex = 'dblp: Author search for '
    if re.match(regex, page_title):
        parse_disambiguation_page(br, name)
    else:
        parse_author_page(page, name)

    br.back()
# crawl_page.crawled = set()


def crawl_prolific_page(index):
    prolific_page = 'http://dblp.uni-trier.de/statistics/prolific%d' % index
    print prolific_page

    br = mechanize.Browser()
    br.open(prolific_page)

    for link in br.links(url_regex="search\/author\?q\="):
        crawl_page(br, link)


def main(args):
    if args.verbose:
        print 'Verbose'

    for index in range(1, 12):
        crawl_prolific_page(index)


if __name__ == '__main__':
    args = parse_args()
    main(args)
