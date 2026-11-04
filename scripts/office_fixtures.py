"""Build tiny, valid .docx and .xlsx files with the standard library (for tests and fixtures)."""
import zipfile
from xml.sax.saxutils import escape


def make_docx(path, paragraphs):
    """paragraphs: list of str, or ("h1", str) for a heading."""
    body = []
    for p in paragraphs:
        style = ""
        if isinstance(p, tuple):
            style = f'<w:pPr><w:pStyle w:val="Heading1"/></w:pPr>'
            p = p[1]
        body.append(f'<w:p>{style}<w:r><w:t xml:space="preserve">{escape(p)}</w:t></w:r></w:p>')
    doc = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
           '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>'
           + "".join(body) + "</w:body></w:document>")
    ct = ('<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="xml" ContentType="application/xml"/>'
          '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>')
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ct)
        z.writestr("_rels/.rels", rels)
        z.writestr("word/document.xml", doc)


def _col(n):
    s = ""
    n += 1
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def make_xlsx(path, sheets):
    """sheets: dict of sheet name -> list of rows (lists of str/int/float/None)."""
    names = list(sheets)
    strings, index = [], {}

    def sid(v):
        if v not in index:
            index[v] = len(strings)
            strings.append(v)
        return index[v]

    sheet_xml = []
    for name in names:
        rows = []
        for r, row in enumerate(sheets[name], start=1):
            cells = []
            for c, v in enumerate(row):
                if v is None:
                    continue
                ref = f"{_col(c)}{r}"
                if isinstance(v, (int, float)):
                    cells.append(f'<c r="{ref}"><v>{v}</v></c>')
                else:
                    cells.append(f'<c r="{ref}" t="s"><v>{sid(str(v))}</v></c>')
            rows.append(f'<row r="{r}">{"".join(cells)}</row>')
        sheet_xml.append('<?xml version="1.0" encoding="UTF-8"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
                         f'<sheetData>{"".join(rows)}</sheetData></worksheet>')
    wb = ('<?xml version="1.0" encoding="UTF-8"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
          'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>'
          + "".join(f'<sheet name="{escape(n)}" sheetId="{i}" r:id="rId{i}"/>' for i, n in enumerate(names, 1)) + "</sheets></workbook>")
    wbrels = ('<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
              + "".join(f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>'
                        for i in range(1, len(names) + 1)) + "</Relationships>")
    sst = ('<?xml version="1.0" encoding="UTF-8"?><sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
           + "".join(f'<si><t xml:space="preserve">{escape(s)}</t></si>' for s in strings) + "</sst>")
    ct = ('<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="xml" ContentType="application/xml"/>'
          '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/></Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>')
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ct)
        z.writestr("_rels/.rels", rels)
        z.writestr("xl/workbook.xml", wb)
        z.writestr("xl/_rels/workbook.xml.rels", wbrels)
        z.writestr("xl/sharedStrings.xml", sst)
        for i, x in enumerate(sheet_xml, 1):
            z.writestr(f"xl/worksheets/sheet{i}.xml", x)
