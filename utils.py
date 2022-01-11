from pikepdf import Pdf
import os


def merge_pdfs(pdfs, folder, output_file_name):
    output = Pdf.new()
    for _pdf in pdfs:
        pdf = Pdf.open(_pdf)
        output.pages.extend(pdf.pages)
    output.save(os.path.join(folder, output_file_name + ".pdf"))


def extract_page_from_pdf(pdf, page, folder, output_file_name):
    pdf = Pdf.open(pdf)
    output = Pdf.new()
    output.pages.append(pdf.pages[page - 1])
    output.save(os.path.join(folder, output_file_name + ".pdf"))


def extract_pages_from_pdf(pdf, start_page, end_page, folder, output_file_name):
    pdf = Pdf.open(pdf)
    output = Pdf.new()
    for i in range(end_page - start_page + 1):
        output.pages.append(pdf.pages[i])
    output.save(os.path.join(folder, output_file_name + ".pdf"))


def get_num_pages(file):
    pdf = Pdf.open(file)
    return len(pdf.pages)
