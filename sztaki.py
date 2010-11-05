#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
PySztaki
Translator script for console using the szotar.sztaki.hu database

A really short script, which uses the given dictionary (in first
parameter) to translate a word or an expression. It uses web-based
translator of szotar.sztaki.hu (parsed with BeautifulSoup
http://www.crummy.com/software/BeautifulSoup/). The translate()
function contains the actual translation code, it can be simply
reused.

Script home:
http://pysztaki.googlecode.com/

Copyright (c) 2008, Pek Daniel

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

import sys
from pysztaki import sztakiutils, sztakiconfig
import urllib

def print_results(results):
    """
    Prints the results with preferred encoding from
    locale.
    """
    import locale
    
    encoding = locale.getpreferredencoding()
    for word in results.keys():
        line = (word + u": " + u"; ".join(results[word])).encode(encoding, "replace")
        print line

def translate(form_data):
    """
    This function runs the actual query by sending the form in GET.
    Return value is an ordered dictionary which have lists as values
    in it, like {"word": ["tranlation1", "translation2", ...], ...} 
    """
    
    # compose GET line, download result page
    params = urllib.urlencode(sztakiutils.encode_dict(form_data, "iso8859-2"))
    page = urllib.urlopen(sztakiconfig.base_url + "?%s" % params)
    
    # parse the result page with BeautifulSoup 
    soup = sztakiutils.bs_preprocess(page)
    
    # Here starts the processing of soup tree 
    result = sztakiutils.odict()
    current_word = ""
    
    # get result <table>s, iterate
    result_tables = soup.findAll(name = "table", attrs = { 'class': 'results' })
    for result_table in result_tables:
        # find <tr>s, iterate
        result_rows = result_table.findAll(name = "tr")
        for result_row in result_rows:
            # in case of mainrow, maybe we should create a new key
            # put first meaning into the list
            if result_row['id'][:4] == "main":
                tds = result_row.findAll(name = "td")
                current_word = sztakiutils.strip_tags(tds[0])
                if current_word == "":
                    continue;
                meaning = sztakiutils.strip_tags(tds[1])
                if meaning == "":
                    continue;
                if result.has_key(current_word):
                    result[current_word].append(meaning)
                else:
                    result[current_word] = [meaning]
            # we just put the new meaning into the list
            else:
                td = result_row.find(name = "td")
                meaning = sztakiutils.strip_tags(td)
                if meaning == "":
                    continue;
                result[current_word].append(meaning)
    
    return result

if __name__ == '__main__':
    # pasrsing parameters, processing configfile
    import locale
    
    encoding = locale.getpreferredencoding()
    if len(sys.argv) < 2:
        sys.stderr.write(u"You should give at least one parameter!\n".encode(encoding))
        sys.exit(-1)
    
    # first parameter in default case is the dictionary, everything else
    # will be treated as part of the expression we would like to translate
    args = sztakiutils.decode_list(sys.argv, encoding)
    dict_id = args[1]
    word = u" ".join(args[2:])

    # form defaults from configfile
    form_data = sztakiconfig.form_data
    
    # if given dictionary exists, we use it
    # else, we concat to the beginning of the expression
    if sztakiconfig.dict_ids.has_key(dict_id):
        form_data['L'] = sztakiconfig.dict_ids[dict_id]
    else:
        word = " ".join([dict_id, word])
    
    form_data[sztakiconfig.word_param] = word
    
    # call translate()
    result = translate(form_data)
    
    print_results(result)
    