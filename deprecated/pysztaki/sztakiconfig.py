# -*- encoding: utf-8 -*-

# SZTAKI URL
base_url = u"http://szotar.sztaki.hu/search"

# Unknown form-parameters
#form_data = {
#    u'flash':   u"",
#    u'E':       u"1",
#    u'in_form': u"1",
#
## Known form-parameters
#    u'L':      u"ENG:HUN:EngHunDict",   # default dictionary
#    u'M':      u"1",                    # match
#                                        # 2 - any
#                                        # 1 - word prefix
#                                        # 0 - whole word
#                                        # 3 - full match
#    u'C':      u"0",                    # ignore case
#    u'A':      u"0",                    # ignore accents
#}



# normally, you shouldn't modify these
# command line -> sztaki notation
#dict_ids = {
#    u'enhu':    u"ENG:HUN:EngHunDict",
#    u'huen':    u"HUN:ENG:EngHunDict",
#    u'gehu':    u"GER:HUN:GerHunDict",
#    u'huge':    u"HUN:GER:GerHunDict",
#    u'frhu':    u"FRA:HUN:FraHunDict",
#    u'hufr':    u"HUN:FRA:FraHunDict",
#    u'ithu':    u"ITA:HUN:ItaHunDict",
#    u'huit':    u"HUN:ITA:ItaHunDict",
#    u'hohu':    u"HOL:HUN:HolHunDict",
#    u'huho':    u"HUN:HOL:HolHunDict",
#    u'pohu':    u"POL:HUN:PolHunDict",
#    u'hupo':    u"HUN:POL:PolHunDict",
#}

# Sztaki form parameters
word_param = u"searchWord"

# Form values which the script depends on
#form_data.update({
#    u'P':               u"0",    # no pronounciation
#    u'T':               u"1",    # use tables
#    u'hallatlan_inc':   u"0",    # no sign language
#    u'in_pysztaki':     u"1",    # for sztaki
#})
