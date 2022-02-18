import datetime
import subprocess
import os
import platform
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors


def createPdf(data_vector):
    doc = SimpleDocTemplate("form_letter.pdf", pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=48, bottomMargin=18)

    Story = []
    logo = "cancerInstitute.jpg"

    date = datetime.date.today()
    department_name = "Supsi Cancer Department"
    department_address = ["Via la Santa 1", "CH-6962 Lugano - Viganello"]

    im = Image(logo, 2*inch, 2*inch)
    Story.append(im)
    Story.append(Spacer(1, 48))

    styles = getSampleStyleSheet()
    ptext = '%s' % date

    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))

    ptext = '%s' % department_name
    Story.append(Paragraph(ptext, styles["Normal"]))
    for part in department_address:
        ptext = '%s' % part.strip()
        Story.append(Paragraph(ptext, styles["Normal"]))

    Story.append(Spacer(1, 48))
    ptext = 'Dear Patient,'
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))

    ptext = 'After careful analysis of your data our department concluded the following:'

    #vector = [111, '2', "abaghjaa", '4', '5']

    data = [['Stage T', 'Stage N', 'Overall Stage', 'Histology', 'Life expectancy'],
            [data_vector[0], data_vector[1], data_vector[2], data_vector[3], data_vector[4]]]
    table = Table(data)
    table.setStyle(TableStyle([('ALIGN', (1, 1), (-2, -2), 'RIGHT'),
                               ('VALIGN', (0, 0), (0, -1), 'TOP'),
                               ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
                               ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                               ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                               ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
                               ]))

    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 36))
    Story.append(table)


    Story.append(Spacer(1, 60))

    ptext = 'Hoping to have the ability to continue to help you the best we can.'
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 36))
    ptext = 'Sincerely,'
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    ptext = 'Doctor Name'
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    doc.build(Story)

    # creates PDF file, different OS
    if platform.system() == 'Windows':
        os.startfile("form_letter.pdf")
    elif platform.system() == 'Darwin':
        subprocess.call(('open', "form_letter.pdf"))
    else:
        subprocess.call(('xdg-open', "form_letter.pdf"))
