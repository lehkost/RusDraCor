import re
import os
import transliterate

o = open('./wikisource_raws/2/Sgovor Kutejkina.txt', 'r', encoding='utf-8')
text_text = o.read()
o.close()

o = open('./wikisource_raws/2/Sgovor Kutejkina.txt', 'r', encoding='utf-8')
text_lines = o
o.close()


def get_metadata(text):
