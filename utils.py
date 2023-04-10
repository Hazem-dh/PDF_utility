from pikepdf import Pdf, Encryption
import os


def merge_pdfs(pdf_paths, folder, output_file_name):
    new_pdf = Pdf.new()
    for pdf_path in pdf_paths:
        pdf = Pdf.open(pdf_path)
        new_pdf.pages.extend(pdf.pages)
    new_pdf.save(os.path.join(folder, output_file_name + ".pdf"))


def extract_page_from_pdf(pdf_path, page, folder, output_file_name):
    pdf = Pdf.open(pdf_path)
    new_pdf = Pdf.new()
    new_pdf.pages.append(pdf.pages[page - 1])
    new_pdf.save(os.path.join(folder, output_file_name + ".pdf"))


def extract_pages_from_pdf(pdf_path, start_page, end_page, folder, output_file_name):
    pdf = Pdf.open(pdf_path)
    new_pdf = Pdf.new()
    for i in range(end_page - start_page + 1):
        new_pdf.pages.append(pdf.pages[i])
    new_pdf.save(os.path.join(folder, output_file_name + ".pdf"))


def lock_pdf(pdf_path, password, folder):
    pdf_file = Pdf.open(pdf_path)
    new_pdf = Pdf.new()
    for page in pdf_file.pages:
        new_pdf.pages.append(page)
    new_pdf.save(os.path.join(folder, pdf_path.split("/")[-1]),
                 encryption=Encryption(user=password, owner=password, R=4))


def get_num_pages(file):
    pdf = Pdf.open(file)
    return len(pdf.pages)
