# -*- encoding: utf-8 -*-

# A sztaki kereso-urlje
base_url = u"http://szotar.sztaki.hu/dict_search.php"

# ismeretlen celu form-parameterek
form_data = {
    u'flash':   u"",
    u'E':       u"1",
    u'in_form': u"1",

# ismert form-parameterek
    u'L':      u"ENG:HUN:EngHunDict",   # nyelv
    u'M':      u"1",                    # egyezes
                                        # 2 - barmilyen
                                        # 1 - szoeleji
                                        # 0 - csak teljes szavak
                                        # 3 - teljes egyezes
    u'C':      u"0",                    # kis-nagybetu nem szamit
    u'A':      u"0",                    # ekezet nem szamit 
}



# A tovabbi beallitasokat csak akkor modositsd, ha jol tudod, mit csinalsz
# megfeleltetesek a sztaki-s es a parancssori jelolesek kozott
dict_ids = {
    u'enhu':    u"ENG:HUN:EngHunDict",
    u'huen':    u"HUN:ENG:EngHunDict",
    u'gehu':    u"GER:HUN:GerHunDict",
    u'huge':    u"HUN:GER:GerHunDict",
    u'frhu':    u"FRA:HUN:FraHunDict",
    u'hufr':    u"HUN:FRA:FraHunDict",
    u'ithu':    u"ITA:HUN:ItaHunDict",
    u'huit':    u"HUN:ITA:ItaHunDict",
    u'hohu':    u"HOL:HUN:HolHunDict",
    u'huho':    u"HUN:HOL:HolHunDict",
    u'pohu':    u"POL:HUN:PolHunDict",
    u'hupo':    u"HUN:POL:PolHunDict",
}

# Sztaki form-valtozok
word_param = u"W"

# Sztaki parameterek, amelyek megvaltoztatasa esetleg a python kod valtoztatasat igenylik
form_data.update({
    u'P':               u"0",    # kiejtes nelkul
    u'T':               u"1",    # tablazatos megjelenites
    u'hallatlan_inc':   u"0",    # jelbeszed megjelenitese
    u'in_pysztaki':     u"1",    # bejelezzuk, hogy a mi programunk generalt
})
