import re
import os
import transliterate


def opening(play):
    """This function opens necessary files and reads them as it's required for the processing."""
    o = open('./wikisource_raws/2/' + play + '.txt', 'r', encoding='utf-8')
    text_text = o.read()
    o.close()
    o = open('./wikisource_raws/2/' + play + '.txt', 'r', encoding='utf-8')
    text_lines = o
    o.close()
    header = open('./tei_header.xml', 'r', encoding='utf-8').read()
    tei = open('./wikisource_tei/2/' + play + '.xml', 'w', encoding='utf-8')
    return text_text, text_lines, header, tei


def get_metadata(play):
    """This function returns the metadata of a play in the following order:
    title, subtitle, author, creation_date, print_date.
    If some of these are missing it returns and empty line instead of the missing value."""
    text = opening(play)[0]
    title = subtitle = author = creation_date = print_date = ''
    title_s = re.findall('НАЗВАНИЕ *?= ?(.*?)\n', text)
    if len(title_s) != 0:
        title = title_s[0]
    subtitle_s = re.findall('ПОДЗАГОЛОВОК *?= ?(.*?)\n', text)
    if len(subtitle_s) != 0:
        subtitle = subtitle_s[0]
    author_s = re.findall('АВТОР *?= ?\[\[(.*?)\]\]', text)
    if len(author_s) != 0:
        author = author_s[0]
    else:
        author_s = re.findall('АВТОР *?= ?(.*?)\n', text)
        if len(author_s) != 0:
            author = author_s[0]
    creation_date_s = re.findall('ДАТАСОЗДАНИЯ *?= ?(.*?)\n', text)
    if len(creation_date_s) != 0:
        creation_date = creation_date_s[0]
    print_date_s = re.findall('ДАТАПУБЛИКАЦИИ *?= ?(.*?)\n', text)
    if len(print_date_s) != 0:
        print_date = print_date_s[0]
    return title, subtitle, author, creation_date, print_date


def write_metadata(play):
    """This function writes the header filled with metadata to a new file with TEI-version of a play."""
    text = opening(play)[0]
    tei_file = opening(play)[3]
    tei_header = opening(play)[2]
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


# BAD - some files have completely different format
def get_castList(play):
    """This function finds a piece of text with castList description and returns list of castItems = castList"""
    text = opening(play)[0]
    castList_part = re.search('== ?Действующие лица.*?==.*?=', text, re.DOTALL)
    if castList_part is None:
        castList_part = re.search('== ?(ДЕЙСТВУЮЩИЕ)? ЛИЦА.*?==.*?=', text, re.DOTALL)
        if castList_part is None:
            castList_part = re.search("'''ЛИЦА.*?=", text, re.DOTALL)
            castList_part = castList_part.group(0)
        else: castList_part = castList_part.group(0)
    else: castList_part = castList_part.group(0)
    castItems = re.findall('\{\{[Rr]azr\|(.*?)\}\}', castList_part)
    return castItems


for files in os.walk('./wikisource_raws/2/'):
    for file in files[2]:
        if file.endswith('.txt'):
            print(file)
            play_title = file.split('.txt')[0]
            print(get_castList(play_title))