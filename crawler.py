import argparse
import mechanize
import re
from bs4 import BeautifulSoup, SoupStrainer
import pickle

def parse_args():
    '''
    Parses the node2vec arguments.
    '''
    parser = argparse.ArgumentParser(description="Get node embeddings.")

    parser.add_argument('--output', default='dblp-data.pckl',
                        help='Output file.')

    parser.add_argument('--verbose', dest='verbose', action='store_true',
                        help='Stdout gensim info. Default is false. Only used if log-output is false.')

    return parser.parse_args()


authors = set()
coauthors = {}
ambiguous = {}


# http://dblp.uni-trier.de/pers/hd/z/Zhang:Shao_Jie
# http://dblp.uni-trier.de/pers/hd/g/Gao_0001:Wen?q=Wen%24+Gao%24+0001%24
# http://dblp.uni-trier.de/pers/hd/p/Poor:H=_Vincent?q=H.%24+Vincent%24+Poor%24
def get_author_id_from_url(url):
    regex = 'http:\/\/dblp\.uni-trier\.de\/pers\/hd\/[\w=]\/([^\?\n]+)(\?q=)?'
    m = re.match(regex, url)
    if not m:
        raise Exception("Error with url %s being parsed as author" % url)

    return m.groups()[0]


# <div class="data" itemprop="headline">
#     <span itemprop="author" itemscope="" itemtype="http://schema.org/Person">
#         <a href="http://dblp.uni-trier.de/pers/hd/l/Liu:Xinwang" itemprop="url">
#             <span itemprop="name">Xinwang Liu
#             </span>
#         </a>
#     </span>, 
#     <span itemprop="author" itemscope="" itemtype="http://schema.org/Person">
#         <span class="this-person" itemprop="name">Jianping Yin
#         </span>
#     </span>, 
#     <span itemprop="author" itemscope="" itemtype="http://schema.org/Person">
#         <a href="http://dblp.uni-trier.de/pers/hd/z/Zhang:Changwang" itemprop="url">
#             <span itemprop="name">Changwang Zhang
#             </span>
#         </a>
#     </span>:
#     <br> 
#     <span class="title" itemprop="name">A Max-Margin Learning Algorithm with Additional Features.
#     </span> 
#     <a href="http://dblp.uni-trier.de/db/conf/faw/faw2009.html#LiuYZZLZ09">
#         <span itemprop="isPartOf" itemscope="" itemtype="http://schema.org/Series">
#             <span itemprop="name">FAW
#             </span>
#         </span> 
#         <span itemprop="datePublished">2009
#         </span>
#     </a>: 
#     <span itemprop="pagination">196-206
#     </span>
# </div>

def parse_author_page(page, name):
    global coauthors, authors
    author_id = get_author_id_from_url(page.geturl())
    if author_id in authors:
        return
    authors.add(author_id)
    coauthors[author_id] = []

    print '\tGetting author: %s' % (author_id)

    strainer = SoupStrainer('div', attrs={'class': 'data', 'itemprop': 'headline'})
    soup = BeautifulSoup(page, 'lxml', parse_only=strainer)

    for tag in soup.find_all('span', {'itemprop': 'author'}):
        if tag.a: # Author is not self
            coauthor_url = tag.a['href']
            coauthor_id = get_author_id_from_url(coauthor_url)

            coauthors[author_id] += [coauthor_id]

    return author_id


def parse_disambiguation_page(br, name):
    global ambiguous
    print '\tDisambiguating: %s' % (name)
    ambiguous[name] = []

    for link in br.links(url_regex="pers\/hd\/"):
        author_id = crawl_page(br, link)
        ambiguous[name] += [author_id]

    return None


def crawl_page(br, link):
    page = br.follow_link(link)

    page_title = br.title()
    name = link.text

    regex = 'dblp: Author search for '
    if re.match(regex, page_title):
        result = parse_disambiguation_page(br, name)
    else:
        result = parse_author_page(page, name)

    br.back()
    return result


def crawl_prolific_page(index):
    prolific_page = 'http://dblp.uni-trier.de/statistics/prolific%d' % index
    print prolific_page

    br = mechanize.Browser()
    br.open(prolific_page)

    for link in br.links(url_regex="search\/author\?q\="):
        crawl_page(br, link)


def save_data(args):
    global coauthors, authors, ambiguous
    data = (coauthors, authors, ambiguous)
    with open(args.output, 'wb') as output:
        pickle.dump(data, output)


def main(args):
    if args.verbose:
        print 'Verbose'

    for index in range(1, 12):
        crawl_prolific_page(index)
    # try:
    #     for index in range(1, 12):
    #         crawl_prolific_page(index)
    # except Exception as e:
    #     print 'Error ocurred! Saving temp data'
    #     print e

    save_data(args)


if __name__ == '__main__':
    args = parse_args()
    main(args)
