PySztaki
========

Translator script for console using the http://szotar.sztaki.hu database

A really short script, which uses the given dictionaries (in first two
parameters) to translate a word or an expression. It uses web-based
translator of szotar.sztaki.hu (parsed with BeautifulSoup
http://www.crummy.com/software/BeautifulSoup/). The ``SztakiQueryParser``
class contains the actual translation code, it can be simply
reused.

## Script home

* http://pysztaki.googlecode.com/
* https://github.com/oroszgy/pysztaki

Copyright (c) 2008, Pek Daniel </br>
Copyright (c) 2014, György Orosz

## Requirements

- Python interpreter, tested with 3.4.
- The script depends on BeautifulSoup python module,
  which can be downloaded from
  http://www.crummy.com/software/BeautifulSoup/


Since this is a very immature script, it may contain errors. Every
feedback, bugreport would be welcomed.

## Usage


    pysztaki.py <word/expression> [from_lang] [to_lang] 

Available languages
* eng
* hun
* ger
* pol
* fre
* ita
* bul
    