from PyPDF2 import PdfFileReader, PdfFileWriter
import os   

# Method to split the pdf at every given n pages.
def split_at_every(self,infile , step = 1):

    # Copy the input file path to a local variable infile
    input_pdf = PdfFileReader(open(infile, "rb"))
    pdf_len = input_pdf.number_of_pages

    # Get the complete file name along with its path and split the text to take only the first part.
    fname = os.path.splitext(os.path.basename(infile))[0]

    # Get the list of page numbers in the order of given step
    # If there are 10 pages in a pdf, and the step is 2
    # page_numbers = [0,2,4,6,8]
    page_numbers = list(range(0,pdf_len,step))

    # Loop through the pdf pages
    for ind,val in enumerate(page_numbers):

        # Check if the index is last in the given page numbers
        # If the index is not the last one, carry on with the If block.
        if(ind+1 != len(page_numbers)):

            # Initialize the PDF Writer
            output_1 = PdfFileWriter()

            # Loop through the pdf pages starting from the value of current index till the value of next index
            # Ex : page numbers = [0,2,4,6,8]
            # If the current index is 0, loop from 1st page till the 2nd page in the pdf doc.
            for page in range(page_numbers[ind], page_numbers[ind+1]):

                # Get the data from the given page number
                page_data = input_pdf.getPage(page)

                # Add the page data to the pdf_writer
                output_1.addPage(page_data)

                # Frame the output file name
                output_1_filename = '{}_page_{}.pdf'.format(fname, page + 1)

            # Write the output content to the file and save it.
            self.write_to_file(output_1_filename, output_1)

        else:

            output_final = PdfFileWriter()
            output_final_filename = "Last_Pages"

            # Loop through the pdf pages starting from the value of current index till the last page of the pdf doc.
            # Ex : page numbers = [0,2,4,6,8]
            # If the current index is 8, loop from 8th page till the last page in the pdf doc.

            for page in range(page_numbers[ind], pdf_len):
                # Get the data from the given page number
                page_data = input_pdf.getPage(page)

                # Add the page data to the pdf_writer
                output_final.addPage(page_data)

                # Frame the output file name
                output_final_filename = '{}_page_{}.pdf'.format(fname, page + 1)

            # Write the output content to the file and save it.
            self.write_to_file(output_final_filename,output_final)
