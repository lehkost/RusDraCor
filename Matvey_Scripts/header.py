header = '''<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/css" href="../../css/tei.css"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <teiHeader>
    <fileDesc>
      <titleStmt>
        <title type="main">###name###</title>
        <title type="sub">Драма</title>
        <author>###author###</author>
      </titleStmt>
      <publicationStmt>
        <publisher xml:id="RusDraCor">RusDraCor</publisher>
        <idno type="URL"/>
        <availability>
          <licence>
            <ab>CC BY 4.0</ab>
            <ref target="https://creativecommons.org/licenses/by/4.0/legalcode">Licence</ref>
          </licence>
        </availability>
      </publicationStmt>
      <sourceDesc>
        <bibl type="digitalSource">
          <name>Wikisource</name>
          <idno type="URL">###url###</idno>
          <availability>
            <licence>
              <ab>CC BY-SA 3.0</ab>
              <ref target="https://creativecommons.org/licenses/by-sa/3.0/deed.ru">Licence</ref>
            </licence>
          </availability>
          <bibl type="originalSource">
            <title/>
            <date type="print">###date_p###</date>
            <date type="premiere">###date_pp###</date>
            <date type="written">###date_c###</date>
          </bibl>
        </bibl>
      </sourceDesc>
    </fileDesc>'''

closer = '''
</body>
  </text>
</TEI>'''
