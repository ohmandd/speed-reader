# Builds a small EPUB 3 for testing: preface, chapters, an in-file anchor, a footnote ref, an &nbsp; entity.
import zipfile, sys

def page(title, body):
    return f'''<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops"><head><title>{title}</title></head>
<body>{body}</body></html>'''

pre = page('Preface', '<h1>Preface</h1><p>This little book exists to test a speed reader. Each word should flash in the same place, with its focus letter in red.</p><p>Longer words, such as extraordinarily, should linger a moment longer. Sentences end with a short pause; paragraphs with a longer one.</p>')
ch1 = page('One', '<h1>Chapter One</h1><p>The river ran quietly past the old mill, carrying leaves toward the sea.<sup><a epub:type="noteref" href="#n1">1</a></sup> Nobody remembered when the wheel had last turned.</p><p>Margaret walked along the bank every morning — rain or shine — and counted the herons.</p>')
ch23 = '<h1>Chapter Two</h1><p>Spring arrived late that year, and the orchards bloomed all at once.</p><p>Everyone agreed it was the most beautiful week anyone could remember.</p><h1 id="ch3">Chapter Three</h1><p>By summer the mill had new owners, and the wheel turned again.</p><p>Margaret still counted the herons. There were eleven.</p>'
ch23 = page('Two and Three', ch23).replace('most beautiful', 'most&nbsp;beautiful')  # &nbsp; is invalid XML -> forces HTML fallback

nav = page('Contents', '<nav epub:type="toc"><ol><li><a href="pre.xhtml">Preface</a></li><li><a href="ch1.xhtml">Chapter One</a></li><li><a href="ch23.xhtml">Chapter Two</a></li><li><a href="ch23.xhtml#ch3">Chapter Three</a></li></ol></nav>')
opf = '''<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="id">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:identifier id="id">test-1</dc:identifier><dc:title>The Mill on the River</dc:title><dc:creator>Test Author</dc:creator><dc:language>en</dc:language></metadata>
<manifest><item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
<item id="pre" href="pre.xhtml" media-type="application/xhtml+xml"/><item id="ch1" href="ch1.xhtml" media-type="application/xhtml+xml"/>
<item id="ch23" href="ch23.xhtml" media-type="application/xhtml+xml"/></manifest>
<spine><itemref idref="pre"/><itemref idref="ch1"/><itemref idref="ch23"/></spine></package>'''
container = '<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>'

with zipfile.ZipFile(sys.argv[1], 'w') as z:
    z.writestr('mimetype', 'application/epub+zip', compress_type=zipfile.ZIP_STORED)
    z.writestr('META-INF/container.xml', container, compress_type=zipfile.ZIP_DEFLATED)
    for name, data in [('content.opf', opf), ('nav.xhtml', nav), ('pre.xhtml', pre), ('ch1.xhtml', ch1), ('ch23.xhtml', ch23)]:
        z.writestr('OEBPS/' + name, data, compress_type=zipfile.ZIP_DEFLATED)
