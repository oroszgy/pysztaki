# -*- encoding: iso8859-2 -*-

import BeautifulSoup as bs
import re
from UserDict import IterableUserDict

def bs_preprocess(file):
    """remove distracting whitespaces and newline characters"""
    html = file.read()
#    pat = re.compile('[\s]+', re.MULTILINE)
#    html = re.sub('\n', ' ', html)     # convert newlines to spaces
#    html = re.sub(pat, ' ', html)       # remove leading and trailing whitespaces
#    html = re.sub('[\s]+<([^uib])', '<$1', html) # remove whitespaces before opening tags
#    html = re.sub('([^uib])>[\s]+', '$1>', html) # remove whitespaces after closing tags

    html = re.sub('Medián WebAudit SZTAKI szótár Angol-magyar szótár', ' ', html)

    return bs.BeautifulSoup(unicode(html, "utf-8"), convertEntities = bs.BeautifulStoneSoup.HTML_ENTITIES)

def strip_tags(tag, recursive = False):
    """
    This util-function gets a BeautifulSoup tag, and returns the not-tag
    information from it. It throws away comments, and strings start with => 
    """
    
    pat = re.compile(u"[\s]+", re.MULTILINE)
    
    if isinstance(tag, bs.Comment):
        return u""
    if tag.string == None:
        str = u""
        for content in tag.contents:
            str += strip_tags(content, True)
        if (not recursive):
            retval = re.sub(pat, u" ", str).strip()
        else:
            retval = str
        return retval
    else:
        if tag.string[0:2] == u"=>":
            return u""
        else:
            if (not recursive):
                retval = tag.string.strip()
            else:
                retval = tag.string
            return retval

def decode_list(list, encoding):
    """
    Decodes all elements of a list
    """
    
    new_list = []
    
    for str in list:
        new_list.append(str.decode(encoding))
    
    return new_list

def encode_dict(dictionary, encoding):
    """
    Encodes all elements of a list
    """
    
    new_dict = {}
    
    for key in dictionary:
        new_dict[key.encode(encoding)] = dictionary[key].encode(encoding)
        
    return new_dict

class odict(IterableUserDict):
    def __init__(self, dict = None):
        self._keys = []
        IterableUserDict.__init__(self, dict)

    def __delitem__(self, key):
        IterableUserDict.__delitem__(self, key)
        self._keys.remove(key)

    def __setitem__(self, key, item):
        IterableUserDict.__setitem__(self, key, item)
        if key not in self._keys: self._keys.append(key)

    def clear(self):
        IterableUserDict.clear(self)
        self._keys = []

    def copy(self):
        dict = IterableUserDict.copy(self)
        dict._keys = self._keys[:]
        return dict

    def items(self):
        return zip(self._keys, self.values())

    def keys(self):
        return self._keys

    def popitem(self):
        try:
            key = self._keys[-1]
        except IndexError:
            raise KeyError('dictionary is empty')

        val = self[key]
        del self[key]

        return (key, val)

    def setdefault(self, key, failobj = None):
        IterableUserDict.setdefault(self, key, failobj)
        if key not in self._keys: self._keys.append(key)

    def update(self, dict):
        IterableUserDict.update(self, dict)
        for key in dict.keys():
            if key not in self._keys: self._keys.append(key)

    def values(self):
        return map(self.get, self._keys)
