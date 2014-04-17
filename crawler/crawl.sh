#!/bin/bash

scrapy crawl olx --logfile=log-olx.txt;
scrapy crawl gumtree --logfile=log-gumtree.txt;
scrapy crawl otodom --logfile=log-otodom.txt;
scrapy crawl morizon --logfile=log-morizon.txt;
scrapy crawl regiodom --logfile=log-regiodom.txt;
