from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch, cm
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, PageBreak

from datetime import date
from NewsPull import pull_news
from confidential import path

NEWS = pull_news()
REPORT_NAME = str(date.today().strftime("%m-%d-%y")) + " News Report"
NEWLINE = Spacer(1,12)
KEY_IDEAS = Paragraph("Key Ideas:", style = getSampleStyleSheet()["Heading4"])
PATH = path

#return: path: a path to the pdf generated
def build_report():
    report = SimpleDocTemplate(PATH + REPORT_NAME + ".pdf")
    flowables = []

    title = Paragraph(REPORT_NAME, style=getSampleStyleSheet()["title"])
    flowables.append(title)

    for i in range(0, len(NEWS)):
        if i != 0 and i % 4 == 0:
            flowables.append(PageBreak())

        headline = Paragraph("<u>" + NEWS[i][0] + "</u>", style = getSampleStyleSheet()["Heading3"])
        text = Paragraph(NEWS[i][1], style = getSampleStyleSheet()["Normal"])
        link = Paragraph("<a href=" + NEWS[i][2] + ''' color="Blue"><u>Full Article</u></a>''', style = getSampleStyleSheet()["Normal"])

        flowables.append(headline)
        flowables.append(text)
        if len(NEWS[i][3]) > 0:
            flowables.append(KEY_IDEAS)
            for idea in NEWS[i][3]:
                bullet = Paragraph('• ' + idea, getSampleStyleSheet()["Normal"])
                flowables.append(bullet)
        flowables.append(NEWLINE)
        flowables.append(link)
        flowables.append(NEWLINE)
        flowables.append(NEWLINE)

    report.build(flowables)
    return PATH + REPORT_NAME + ".pdf"
