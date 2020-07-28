#!/bin/bash
# Downloads newswire data from 2009.

curl -C - http://data.statmt.org/news-crawl/en/news.2009.en.shuffled.deduped.gz -o "news.2009.gz" 
gunzip "news.2009.gz"
mv "~/Desktop/case-restoration/src/news.2009" "~/Desktop/case-restoration/data"
