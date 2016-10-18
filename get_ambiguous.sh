#!/bin/bash

declare -A authors
authors['WeiWang']='http://dblp.uni-trier.de/search/author?q=Wei%24+Wang%24'
authors['WeiZhang']='http://dblp.uni-trier.de/search/author?q=Wei%24+Zhang%24'
authors['WenGao']='http://dblp.uni-trier.de/search/author?q=Wen%24+Gao%24+0001%24'
authors['YuZhang']='http://dblp.uni-trier.de/search/author?q=Yu%24+Zhang%24'
authors['JingLi']='http://dblp.uni-trier.de/search/author?q=Jing%24+Li%24'
authors['LiZhang']='http://dblp.uni-trier.de/search/author?q=Li%24+Zhang%24'
authors['JunLiu']='http://dblp.uni-trier.de/search/author?q=Jun%24+Liu%24'
authors['YangLiu']='http://dblp.uni-trier.de/search/author?q=Yang%24+Liu%24'
authors['XiaodongWang']='http://dblp.uni-trier.de/search/author?q=Xiaodong%24+Wang%24'
authors['JunWang']='http://dblp.uni-trier.de/search/author?q=Jun%24+Wang%24'
authors['WeiLi']='http://dblp.uni-trier.de/search/author?q=Wei%24+Li%24'
authors['JunZhang']='http://dblp.uni-trier.de/search/author?q=Jun%24+Zhang%24'
authors['JingWang']='http://dblp.uni-trier.de/search/author?q=Jing%24+Wang%24'
authors['XinWang']='http://dblp.uni-trier.de/search/author?q=Xin%24+Wang%24'
authors['LeiZhang']='http://dblp.uni-trier.de/search/author?q=Lei%24+Zhang%24'

for a in ${!authors[@]}
do
    echo ''; echo '';
    echo 'Getting data from author: ' $a
    echo 'url: ' ${authors[$a]}
    python crawler.py --author=$a --author-page=${authors[$a]} --depth=2 --output=data/dblp_$a.pckl
    echo ''; echo '';
done

# python crawler.py --author-page=http://dblp.uni-trier.de/search/author?q=Wei%24+Wang%24 --depth=2 --output=hahah.pckl --restart
