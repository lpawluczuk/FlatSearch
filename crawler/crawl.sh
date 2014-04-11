#!/bin/bash

scrapy crawl tablica --logfile=log-tablica.txt;
scrapy crawl gumtree --logfile=log-gumtree.txt;
scrapy crawl otodom --logfile=log-otodom.txt;
