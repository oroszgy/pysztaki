#!/usr/bin/env python3

"""
PySztaki

Console interface for the http://szotar.sztaki.hu/

Copyright (c) 2008, Pek Daniel
Copyrigth (c) 2014, György Orosz <oroszgy@gmail.com>

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the <ORGANIZATION> nor the names of its
      contributors may be used to endorse or promote products derived from
      this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""

from urllib.request import urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup as bs
from argparse import ArgumentParser
from collections import OrderedDict

_base_url="http://szotar.sztaki.hu/search"
_from = "fromlang"
_to = "tolang"
_word = "searchWord"

class SztakiQueryParser:
    def __init__(self, base_url, from_lang, to_lang):
        self._base_url = base_url
        self._from = from_lang
        self._to = to_lang
        
    def build_query(self,word):
        return "{}?{}={}&{}={}&{}={}".format(self._base_url, _from, self._from, _to, self._to, _word, quote(word))
    
    def parse_html(self, res_file):
        content =  res_file.read().decode("utf8")
        soup = bs(content)
            
        ret = OrderedDict()
        for res in soup.findAll("div", { "class":"articlewrapper"}):
            head = self.parse_head(res)
            article = self.parse_article(res)
            ret[head]= article
            
        return ret
    
    def parse_head(self, div):
        return div.find("span", {"class":"prop_content"}).string.strip()
    
    def parse_article(self, div):
        act = div.find("ol")
        return [e.find("a").text.strip() for e in act.findAll("div", {"class":"translation"}) if not e.find("span", {"class":"type_text"})]
    
    def query(self, word):
        url = self.build_query(word)
        print(url)
        of = urlopen(url)
        return self.parse_html(of)
    

def main(word, from_lang, to_lang):
    sztakker = SztakiQueryParser(_base_url, from_lang, to_lang)
    for k,v in sztakker.query(word).items():
        print(k+":")
        print("\t", ", ".join(v))
    

if __name__ == "__main__":
    parser = ArgumentParser("sztaki.py", description="Console interface for Sztaki dictionaries.")
    parser.add_argument("word")
    parser.add_argument("from_lang", default="eng", nargs="?")
    parser.add_argument("to_lang", default="hun", nargs="?")
    
    args = parser.parse_args()
    main(args.word, args.from_lang, args.to_lang)
    
    
