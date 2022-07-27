from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


# defining the function to convert an HTML file to a PDF file
def html_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


import io
import tempfile
from contextlib import contextmanager

import requests
import pdfrw


@contextmanager
def as_file(url):
    with tempfile.NamedTemporaryFile(suffix='.pdf') as tfile:
        tfile.write(requests.get(url).content)
        tfile.flush()
        yield tfile.name


def write_fillable_pdf(input_pdf_path, output_pdf_path, data_dict):
    template_pdf = pdfrw.PdfReader(input_pdf_path)

    # PDF is modified here

    buf = io.BytesIO()
    print(buf.getbuffer().nbytes)  # Prints "0"!
    pdfrw.PdfWriter().write(buf, template_pdf)
    buf.seek(0)
    return buf
