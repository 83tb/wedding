# -*- encoding: utf-8 -*-

'''
Wedding Invitation Generator


It's just a very simple pdf generator. It takes csv file column and put each row text, formats it and inserts into the pdf.
Obviously it will generate a lot of pdfs if you have a lot of rows in a csv file(it takes seconds to generate hundreds, so..)
You can use to generate any type of pdf files which requires embedding different text in each file.

Just put your template pdf file, font file and csv file in the folder with the script and configure settings below

When you're done, just do:
python wedding.py

'''


# MANDATORY
# pdf template
PDF_TEMPLATE = 'template.pdf'
PDF_SIZE = (425,595) # in pixels

# csv data
CSV_FILE = 'guests.csv'
COLUMN = 'text'

# text properties
FONT_NAME = 'mozz.ttf'
# hpostion is counted from the top
HPOSITION = 160 # this means 160 pixels from the top, your text will be centered
FONT_SIZE = 15


# OPTIONAL
# generated files
FILENAME_LENGTH = 12
# this is base filename length - 3 more chars will be added at the end, so you can have non-unique csv fields
# (cause filenames are generated from your csv fields too)

# if the csv field was empty we don't generate pdf file, if you want other behaviour, change this
GENERATE_EMPTY = False


import StringIO
import csv

from codegen import fetch_code
from reportlab.platypus import Paragraph
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet, TA_CENTER
from pyPdf import PdfFileWriter, PdfFileReader

# fonts import
pdfmetrics.registerFont(TTFont('Font', FONT_NAME))


# data import
data = csv.reader(open(CSV_FILE))

# read the column names from the first line of the file
fields = data.next()

for row in data:
    item = dict(zip(fields, row))



    # importing 'base' file on which we write stuff
    input = PdfFileReader(file(PDF_TEMPLATE, "rb"))

    packet = StringIO.StringIO()
    c = canvas.Canvas(packet, pagesize=PDF_SIZE)
    width, height = PDF_SIZE


    # word number 1
    stylesheet=getSampleStyleSheet()
    styleN = stylesheet['Normal']
    styleN.alignment = TA_CENTER
    styleN.fontSize = FONT_SIZE
    styleN.fontName = 'Font'
    # changing the size of the font depending on the lenght of the word

    p = Paragraph(u'<font color="black">' + item[COLUMN].decode('utf-8')+u'</font>', styleN)
    # width/height of the paragraph
    w,h = p.wrap(width, height)
    # x/y axis when the paragraph should be added
    p.drawOn(c, 0, height-HPOSITION)


    # saving canvas
    c.save()
    packet.seek(0)
    text = PdfFileReader(packet)
    output = PdfFileWriter()
    # merging text with base
    page = input.getPage(0)
    page.mergePage(text.getPage(0))
    output.addPage(page)

    # saving file
    if str(item[COLUMN]) != "" or GENERATE_EMPTY:
        filename = item[COLUMN].replace(" ", "")[0:FILENAME_LENGTH] + fetch_code() + ".pdf"
        outputStream = file("output/" + filename, "wb")
        output.write(outputStream)
        outputStream.close()