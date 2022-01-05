import tkinter as tk
from tkinter import ttk, Button, RIGHT, END, Listbox, messagebox, Radiobutton, Label, NORMAL, DISABLED, LEFT, CENTER, \
    Entry, IntVar
import tkinter.filedialog as fd
import PyPDF2
import pikepdf
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

        # creating tabs
        self.tab_merge = ttk.Frame(self.tab_control)
        Label(self.tab_merge, text="Choose pdf files you want to merge").pack()
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
        self.entry = Entry(self.tab_merge, justify=CENTER)
        self.entry["state"] = DISABLED
        self.entry.pack(expand=1)
        self.button_add = Button(self.tab_merge, text="select files", width=10, height=2, command=self.upload_action)
        self.button_merge = Button(self.tab_merge, text="merge files", width=10, height=2, command=self.merge_files)
        self.button_delete = Button(self.tab_merge, text="delete", width=10, height=2, command=self.delete)
        self.button_delete_all = Button(self.tab_merge, text="delete_all", width=10, height=2, command=self.delete_all)
        self.button_delete["state"] = DISABLED
        self.button_delete_all["state"] = DISABLED
        self.button_merge["state"] = DISABLED
        self.button_delete.pack(expand=1, fill="both", side=RIGHT)
        self.button_delete_all.pack(expand=1, fill="both", side=RIGHT)
        self.button_add.pack(expand=1, fill="both", side=LEFT)
        self.button_merge.pack(expand=1, fill="both", side=LEFT)

        var = IntVar(value=1)
        self.p_number = Entry(self.tab_extract, validate="key",
                              validatecommand=(self.tab_extract.register(self.only_numbers), '%S'), justify=CENTER)
        self.p_number.grid(row=0, column=2)
        self.one = Radiobutton(self.tab_extract, variable=var, value=1,
                               command=lambda e=self.p_number, text="extract 1 page", v=var: self.naccheck(e, v))
        self.one.grid(row=0, column=1, sticky="w")
        self.start_number = Entry(self.tab_extract, validate="key",
                                  validatecommand=(self.tab_extract.register(self.only_numbers), '%S'), justify=CENTER)
        self.start_number.grid(row=1, column=2)
        self.two = Radiobutton(self.tab_extract, variable=var, value=2,
                               command=lambda e=self.start_number, text="extract a range of pages",
                                              v=var: self.naccheck(e, v))
        self.two.grid(row=1, column=1)

        self.end_number = Entry(self.tab_extract, validate="key",
                                validatecommand=(self.tab_extract.register(self.only_numbers), '%S'), justify=CENTER)
        self.end_number.grid(row=1, column=3)

    # function to validate mark entry
    @staticmethod
    def only_numbers(char):
        return char.isdigit()

    @staticmethod
    def naccheck(entry, var3):
        if var3.get() != 2:
            entry.configure(state='disabled')
        else:
            entry.configure(state='normal')

    @staticmethod
    def switch(component):
        if component["state"] == NORMAL:
            component["state"] = DISABLED
        else:
            component["state"] = NORMAL

    def upload_action(self):
        filenames = fd.askopenfilenames(filetypes=[("Text files", "*.pdf")], title='Choose pdfs to merge')
        for file in filenames:
            self.listbox.insert(END, file.split("/")[-1])
            self.paths.append(file)
        if self.listbox.size() > 0 and self.button_delete["state"] == DISABLED:
            self.switch(self.button_delete)
            self.switch(self.button_delete_all)
        if self.listbox.size() > 1 and self.entry["state"] == DISABLED:
            self.switch(self.entry)
            self.switch(self.button_merge)

    def merge_files(self):
        merger = PyPDF2.PdfFileMerger()
        file_name = self.entry.get()
        if len(file_name) == 0:
            messagebox.showinfo("ERROR", "Please entre the name of the output file", icon='error')
            return
        for _pdf in self.paths:
            pdf = PyPDF2.PdfFileReader(_pdf, 'rb')
            if not pdf.isEncrypted:
                merger.append(pdf)
            else:
                # handling encrypted pdf without passwords
                temp = pikepdf.open(_pdf)
                temp_path = _pdf + "temp"
                temp.save(temp_path)
                pdf = PyPDF2.PdfFileReader(temp_path, 'rb')
                merger.append(pdf)
                os.remove(temp_path)
        folder_selected = fd.askdirectory()
        merger.write(os.path.join(folder_selected, file_name + ".pdf"))
        self.entry.delete(0, last=END)
        self.switch(self.entry)
        self.switch(self.button_merge)
        self.paths = []
        messagebox.showinfo("RESULT", "pdfs merged successfully", icon='info')

    def delete(self):
        selection = self.listbox.curselection()
        for index in selection[::-1]:
            self.listbox.delete(index)
            del (self.paths[index])
        if self.listbox.size() < 1:
            self.switch(self.button_delete)
            self.switch(self.button_delete_all)

    def delete_all(self):
        self.listbox.delete(0, END)
        self.paths = []
        self.switch(self.button_delete)
        self.switch(self.button_delete_all)


if __name__ == '__main__':
    root = tk.Tk()
    my_gui = PdfTool(root)
    root.mainloop()
