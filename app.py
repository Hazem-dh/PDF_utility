import tkinter as tk
from tkinter import ttk, Button, RIGHT, END, Listbox, messagebox, Radiobutton, Label, NORMAL, DISABLED, LEFT, CENTER, \
    Entry, IntVar
import tkinter.filedialog as fd
from pikepdf import Pdf
import os


class PdfTool:
    def __init__(self, master):
        # general config of the app
        self.master = master
        self.master.title("PDF tool")
        self.master.minsize(400, 300)
        root.iconbitmap("assets/PDF.ico")
        self.tab_control = ttk.Notebook(self.master)
        self.paths = []
        self.path = ""

        # creating tabs
        self.tab_merge = ttk.Frame(self.tab_control)
        Label(self.tab_merge, text="Choose pdf file you want to merge").pack()
        self.tab_split = ttk.Frame(self.tab_control)
        self.tab_extract = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_merge, text='merge')
        self.tab_control.add(self.tab_split, text='split')
        self.tab_control.add(self.tab_extract, text='extract')
        self.tab_control.pack(expand=1, fill="both")

        # Merge tab gadgets
        self.listbox = Listbox(self.tab_merge, selectmode='multiple')
        self.listbox.pack(expand=1, fill="both")
        self.label = tk.Label(self.tab_merge, text="Output file name")
        self.label.pack(expand=1)
        self.output_merge = Entry(self.tab_merge, justify=CENTER)
        self.output_merge["state"] = DISABLED
        self.output_merge.pack(expand=1)
        self.button_add_merge = Button(self.tab_merge, text="select files", width=10, height=2,
                                       command=self.upload_action)
        self.button_merge = Button(self.tab_merge, text="merge files", width=10, height=2, command=self.merge_files)
        self.button_delete_merge = Button(self.tab_merge, text="delete", width=10, height=2, command=self.delete)
        self.button_delete_all = Button(self.tab_merge, text="delete_all", width=10, height=2, command=self.delete_all)
        self.button_delete_merge["state"] = DISABLED
        self.button_delete_all["state"] = DISABLED
        self.button_merge["state"] = DISABLED
        self.button_delete_merge.pack(expand=1, fill="both", side=RIGHT)
        self.button_delete_all.pack(expand=1, fill="both", side=RIGHT)
        self.button_add_merge.pack(expand=1, fill="both", side=LEFT)
        self.button_merge.pack(expand=1, fill="both", side=LEFT)

        # extract tab gadgets
        Label(self.tab_extract, text="Choose pdf files you want to extract page(s) from").grid(row=0, column=1,
                                                                                               columnspan=3,
                                                                                               sticky="ew")
        self.button_add_extract = Button(self.tab_extract, text="select file", command=self.upload_action)
        self.button_add_extract.grid(row=1, column=1)
        self.file = Label(self.tab_extract, text="")
        self.file.grid(row=1, column=2, columnspan=2)
        self.var = IntVar(value=1)
        self.one = Radiobutton(self.tab_extract, variable=self.var, value=1,
                               command=self.intcheck, text="extract 1 page")
        self.one.grid(row=2, column=1, sticky="w")
        self.p_number = Entry(self.tab_extract, validate="key",
                              validatecommand=(self.tab_extract.register(self.only_numbers), '%S'), justify=CENTER)
        self.p_number.grid(row=2, column=2)
        self.two = Radiobutton(self.tab_extract, variable=self.var, value=2,
                               command=self.intcheck, text="extract a range of pages", )
        self.two.grid(row=3, column=1)
        self.start_number = Entry(self.tab_extract, validate="key",
                                  validatecommand=(self.tab_extract.register(self.only_numbers), '%S'), justify=CENTER)
        self.start_number.grid(row=3, column=2)
        self.start_number["state"] = DISABLED
        self.end_number = Entry(self.tab_extract, validate="key",
                                validatecommand=(self.tab_extract.register(self.only_numbers), '%S'), justify=CENTER)
        self.end_number.grid(row=3, column=3)
        self.end_number["state"] = DISABLED
        self.label = tk.Label(self.tab_extract, text="Output file name")
        self.label.grid(row=4, column=1, sticky="news")
        self.output_extract = Entry(self.tab_extract, justify=CENTER)
        self.output_extract.grid(row=4, column=2, sticky="ew")
        self.output_extract["state"] = DISABLED
        self.button_extract = Button(self.tab_extract, text="extract", command=self.extract)
        self.button_extract.grid(row=6, column=2, sticky="ew")
        self.button_extract["state"] = DISABLED
        self.button_delete_extract = Button(self.tab_extract, text="delete", command=self.delete)
        self.button_delete_extract.grid(row=5, column=2, sticky="news")
        self.button_delete_extract["state"] = DISABLED

    # function to validate mark entry
    @staticmethod
    def only_numbers(char):
        return char.isdigit()

    @staticmethod
    def switch(component):
        if component["state"] == NORMAL:
            component["state"] = DISABLED
        else:
            component["state"] = NORMAL

    def intcheck(self):
        if self.var.get() == 2:
            self.p_number.delete(0, 'end')
            self.switch(self.p_number)
            self.switch(self.start_number)
            self.switch(self.end_number)

        else:
            self.start_number.delete(0, END)
            self.end_number.delete(0, END)
            self.switch(self.p_number)
            self.switch(self.start_number)
            self.switch(self.end_number)

    def upload_action(self):
        current_tab = self.tab_control.index(self.tab_control.select())
        filenames = fd.askopenfilenames(filetypes=[("Text files", "*.pdf")],
                                        title='Choose pdfs to merge')
        if current_tab != 0 and len(filenames) > 1:  # check if user selected more than one file
            messagebox.showinfo("ERROR", "Please select only one file", icon='error')
            return

        for file in filenames:
            if current_tab == 0:
                self.listbox.insert(END, file.split("/")[-1])
                self.paths.append(file)
            else:
                self.file.config(text=file.split("/")[-1])
                self.path = file
                if self.button_delete_extract["state"] == DISABLED:
                    self.switch(self.button_delete_extract)
                    self.switch(self.button_extract)
                    self.switch(self.output_extract)

        if current_tab == 0:
            if self.listbox.size() > 0 and self.button_delete_merge["state"] == DISABLED:
                self.switch(self.button_delete_merge)
                self.switch(self.button_delete_all)
            if self.listbox.size() > 1 and self.output_merge["state"] == DISABLED:
                self.switch(self.output_merge)
                self.switch(self.button_merge)

    def merge_files(self):
        file_name = self.output_merge.get()
        if len(file_name) == 0:
            messagebox.showinfo("ERROR", "Please entre the name of the output file", icon='error')
            return
        folder_selected = fd.askdirectory()
        if folder_selected == "":
            return
        output = Pdf.new()
        for _pdf in self.paths:
            pdf = Pdf.open(_pdf)
            output.pages.extend(pdf.pages)
        output.save(os.path.join(folder_selected, file_name + ".pdf"))
        self.output_merge.delete(0, last=END)
        self.switch(self.output_merge)
        self.switch(self.button_merge)
        self.listbox.delete(0, last=END)
        self.paths = []
        messagebox.showinfo("RESULT", "pdfs merged successfully", icon='info')

    def extract(self):
        pdf = Pdf.open(self.path)
        if self.output_extract.get() == "":
            messagebox.showinfo("ERROR", "Please entre the name of the output file", icon='error')
            return
        if self.var.get() == 1:
            try:
                page_num = int(self.p_number.get())
            except ValueError:
                messagebox.showinfo("ERROR", "please enter page number", icon='error')
                return
            if page_num < 1 or page_num > len(pdf.pages):
                messagebox.showinfo("ERROR", "invalid page number", icon='error')
                return
            else:
                folder_selected = fd.askdirectory()
                if folder_selected == "":
                    return
                output = Pdf.new()
                output.pages.append(pdf.pages[page_num - 1])
                output.save(os.path.join(folder_selected, self.output_extract.get() + ".pdf"))
                self.output_extract.delete(0, last=END)
                self.p_number.delete(0, last=END)
                messagebox.showinfo("INFO", "page extracted successfully", icon='info')
        else:
            try:
                page_num_start = int(self.start_number.get())
                page_num_end = int(self.end_number.get())
            except ValueError:
                messagebox.showinfo("ERROR", "please enter page number", icon='error')
            if page_num_end < page_num_start or page_num_start < 1 or page_num_end > len(pdf.pages):
                messagebox.showinfo("ERROR", "invalid page numbers", icon='error')
            folder_selected = fd.askdirectory()
            if folder_selected == "":
                return
            output = Pdf.new()
            for i in range(page_num_end - page_num_start + 1):
                output.pages.append(pdf.pages[i])
            output.save(os.path.join(folder_selected, self.output_extract.get() + ".pdf"))
            self.output_extract.delete(0, last=END)
            self.start_number.delete(0, last=END)
            self.end_number.delete(0, last=END)
            messagebox.showinfo("INFO", "page extracted successfully", icon='info')

    def delete(self):
        current_tab = self.tab_control.index(self.tab_control.select())
        if current_tab == 0:
            selection = self.listbox.curselection()
            for index in selection[::-1]:
                self.listbox.delete(index)
                del (self.paths[index])
            if self.listbox.size() < 1:
                self.switch(self.button_delete_merge)
                self.switch(self.button_delete_all)
        if current_tab == 2:
            self.path = ""
            self.output_extract.delete(0, last=END)
            self.file.config(text="")
            self.switch(self.button_delete_extract)
            self.switch(self.button_extract)
            self.switch(self.output_extract)

    def delete_all(self):
        self.listbox.delete(0, END)
        self.paths = []
        self.switch(self.button_delete_merge)
        self.switch(self.button_delete_all)


if __name__ == '__main__':
    root = tk.Tk()
    my_gui = PdfTool(root)
    root.mainloop()
