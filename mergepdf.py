import PyPDF2


def merge_pdfs(_pdfs):
    merger = PyPDF2.PdfFileMerger()
    for _pdf in _pdfs:
        merger.append(PyPDF2.PdfFileReader(_pdf, 'rb'))
    merger.write("result.pdf")


