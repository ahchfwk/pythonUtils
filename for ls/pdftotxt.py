#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import codecs
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
from cStringIO import StringIO


def pdfparser(data):
    outfile = data+'.txt'
    fp = file(data, 'rb')
    outfp = file(outfile, 'w')
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = "utf-8"
    laparams = LAParams()
    device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=laparams)
    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # Process each page contained in the document.

    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
        data = retstr.getvalue()

    print data

    device.close()
    outfp.close()


if __name__ == '__main__':
    pdfparser("ui2code.pdf")