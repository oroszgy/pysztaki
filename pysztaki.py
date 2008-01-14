#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
PySztaki
Konzolos fordito-script a sztaki adatbazis hasznalataval

Egyszeru script, mely a parameterkent kapott szot megkeresi
a szinten parameterkent kapott sztaki szotar-valtozatban a
szotar.sztaki.hu-n, majd BeautifulSouppal benyalja az oldalt,
es kiszedi a talalatokat. A script translate() fuggvenye vegzi
a tenyleges forditast, konnyen felhasznalhato mas projectben is.

Tovabbi informacio a project honlapjan:
http://code.google.com/p/pysztaki/

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

import sztakiconfig
import sys
import urllib
import sztakiutils

def print_results(results):
    import locale
    
    encoding = locale.getpreferredencoding(True)
    for word in results.keys():
        line = (word + u": " + u"; ".join(results[word])).encode(encoding)
        print line

def translate(form_data):
    """
    Ez a fuggveny vegzi a kapott form-adatok alapjan a lekerdezest.
    A visszaadott ertek egy multidict, ami tartalmazza az egyes szavak
    jelenteseit, mint egyszeru list objektumokat.
    """
    
    # parameterek rekombinalasa, eredmeny letoltese
    params = urllib.urlencode(sztakiutils.encode_dict(form_data, "iso8859-2"))
    page = urllib.urlopen(sztakiconfig.base_url + "?%s" % params)
    
    # az eredmenyt benyaljuk beautifulsouppal
    # hasznalunk egy util-fuggvenyt, ami lenyeli a whitespace-eket
    soup = sztakiutils.bs_preprocess(page)
    
    # adatok kinyerese
    result = sztakiutils.odict()
    current_word = ""
    
    # eredmenytablak megkeresese, vegigiteralunk rajtuk
    result_tables = soup.findAll(name = "table", attrs = { 'class': 'results' })
    for result_table in result_tables:
        # megkeressuk az osszes sort, vegigmegyunk rajtuk
        result_rows = result_table.findAll(name = "tr")
        for result_row in result_rows:
            # ha mainrow, akkor letrehozunk egy uj dict-keyt neki, es betesszuk
            # az elso jelentest a tombjebe
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
            # egyebkent csak hozzaadjuk az aktualis szo jelenteseihez
            else:
                td = result_row.find(name = "td")
                meaning = sztakiutils.strip_tags(td)
                if meaning == "":
                    continue;
                result[current_word].append(meaning)
    
    return result

if __name__ == '__main__':
    # parameterek parseolasa, config-fajl feldolgozasa
    import locale
    
    encoding = locale.getpreferredencoding(True)
    if len(sys.argv) < 2:
        sys.stderr.write(u"Helytelen paraméterezés!\n".encode(encoding))
    
    # az elso parameter alapesetben a nyelv, a tobbi a szo
    args = sztakiutils.decode_list(sys.argv, encoding)
    dict_id = args[1]
    word = u" ".join(args[2:])

    # form alapertekek kinyerese a config-fajlbol
    form_data = sztakiconfig.form_data
    
    # ha letezik a megadott nyelv-azonosito, akkor hasznaljuk,
    # ha nem, akkor default ertekkel dolgozunk, es hozzafuzzuk
    # az elso parametert is a forditando szohoz
    if sztakiconfig.dict_ids.has_key(dict_id):
        form_data['L'] = sztakiconfig.dict_ids[dict_id]
    else:
        word = " ".join([dict_id, word])
    
    form_data[sztakiconfig.word_param] = word
    
    # translate fuggveny meghivasa
    result = translate(form_data)
    
    print_results(result)
    