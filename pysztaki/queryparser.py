from urllib.request import urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup as bs
from collections import OrderedDict

from .config import BASE_URL, FROM_KW, TO_KW, WORD_KW, Languages


class SztakiQueryParser:
    def __init__(self, from_lang=Languages.English,
                 to_lang=Languages.Hungarian, base_url=BASE_URL):
        self._base_url = base_url
        self._from = from_lang
        self._to = to_lang

    def build_query(self, word):
        return "{}?{}={}&{}={}&{}={}&in_pysztaki=1".format(
            self._base_url, FROM_KW, self._from, TO_KW, self._to,
            WORD_KW, quote(word))

    def parse_html(self, res_file):
        content = res_file.read().decode("utf8")
        soup = bs(content)

        ret = OrderedDict()
        for res in soup.findAll("div", {"class": "articlewrapper"}):
            head = self.parse_head(res)
            article = self.parse_article(res)
            ret[head] = article

        return ret

    def parse_head(self, div):
        return div.find("span", {"class": "prop_content"}).string.strip()

    def parse_article(self, div):
        act = div.find("ol")
        return [e.find("a").text.strip() for e in
                act.findAll("div", {"class": "translation"})
                if not e.find("span", {"class": "type_text"})]

    def query(self, word):
        url = self.build_query(word)
        of = urlopen(url)
        return self.parse_html(of)
