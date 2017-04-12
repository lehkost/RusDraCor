import re
import os
import transliterate

play = 'Snegurochka'

o = open('./wikisource_raws/2/' + play + '.txt', 'r', encoding='utf-8')
text_text = o.read()
o.close()

o = open('./wikisource_raws/2/' + play + '.txt', 'r', encoding='utf-8')
text_lines = o
o.close()

header = open('./tei_header.xml', 'r', encoding='utf-8').read()

tei = open('./wikisource_tei/2/' + play + '.xml', 'w', encoding='utf-8')


def get_metadata(text):
    """This function returns the metadata of a play in a following order:
    title, subtitle, author, creation_date, print_date.
    If some of these are missing it returns and empty line instead of the missing value."""
    title = subtitle = author = creation_date = print_date = ''
    title_s = re.findall('НАЗВАНИЕ *?= ?(.*?)\n', text)
    if len(title_s) != 0:
        title = title_s[0]
    subtitle_s = re.findall('ПОДЗАГОЛОВОК *?= ?(.*?)\n', text)
    if len(subtitle_s) != 0:
        subtitle = subtitle_s[0]
    author_s = re.findall('АВТОР *?= ?\[?\[?(.*?)\]?\]?', text)
    if len(author_s) != 0:
        author_s = re.findall('АВТОР *?= (.*?)\n', text)
        if len(author_s) != 0:
            author = author_s[0]
    creation_date_s = re.findall('ДАТАСОЗДАНИЯ *?= ?(.*?)\n', text)
    if len(creation_date_s) != 0:
        creation_date = creation_date_s[0]
    print_date_s = re.findall('ДАТАПУБЛИКАЦИИ *?= ?(.*?)\n', text)
    if len(print_date_s) != 0:
        print_date = print_date_s[0]
    return title, subtitle, author, creation_date, print_date


def write_metadata(text, tei_file, tei_header):
    """This function writes the header filled with metadata to a new file with TEI-version of a play."""
    title = get_metadata(text)[0]
    subtitle = get_metadata(text)[1]
    author = get_metadata(text)[2]
    creation_date = get_metadata(text)[3]
    print_date = get_metadata(text)[4]
    tei_header = re.sub('<title type="main"></title>', '<title type="main">' + title + '</title>', tei_header)
    tei_header = re.sub('<title type="sub"></title>', '<title type="sub">' + subtitle + '</title>', tei_header)
    tei_header = re.sub('<author></author>', '<author>' + author + '</author>', tei_header)
    tei_header = re.sub('<date type="written"></date>', '<date type="written">' + creation_date + '</date>', tei_header)
    tei_header = re.sub('<date type="print"></date>', '<date type="print">' + print_date + '</date>', tei_header)
    tei_file.write(tei_header)


def get_castlist(text):
    castlist_part = re.search('== ?действующие лица ?==.*?=', text.lower(), re.DOTALL)
    if castlist_part is None:
        castlist_part = re.search("'''лица.*?=", text.lower(), re.DOTALL)
    return castlist_part.group(0)


write_metadata(text_text, tei, header)