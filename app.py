import os
from PIL import Image
import customtkinter
from customtkinter import CTkLabel, CTkButton, CTkEntry, CTkRadioButton, CTkFrame, CTkImage, CTkFont, CTkOptionMenu

from tkinter import ttk, Listbox, messagebox, Entry, IntVar, NORMAL, DISABLED, RIGHT, END, \
    LEFT, CENTER
import tkinter.filedialog as fd
from utils import merge_pdfs, get_num_pages, extract_pages_from_pdf, extract_page_from_pdf


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("PDF tool")
        self.geometry("700x450")
        self.minsize(600, 450)
        try:  # launch the exe from anywhere without needing the icon
            self.iconbitmap("assets/PDF.ico")
        except:
            pass
        self.paths = []
        self.path = ""
        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")
        self.logo_image = CTkImage(Image.open(os.path.join(image_path, "PDF.png")), size=(26, 26))
        self.image_icon_image = CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")),
                                         size=(20, 20))
        self.merge_image = CTkImage(light_image=Image.open(os.path.join(image_path, "merge_dark.png")),
                                    dark_image=Image.open(os.path.join(image_path, "merge_light.png")),
                                    size=(30, 30))
        self.chat_image = CTkImage(light_image=Image.open(os.path.join(image_path, "extract.png")),
                                   dark_image=Image.open(os.path.join(image_path, "extract.png")),
                                   size=(30, 30))

        # create navigation frame
        self.navigation_frame = CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = CTkLabel(self.navigation_frame, text="PDF Tool",
                                               image=self.logo_image,
                                               compound="left",
                                               font=CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.frame_merge_button = CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                            text="Merge",
                                            fg_color="transparent", text_color=("gray10", "gray90"),
                                            hover_color=("gray70", "gray30"),
                                            image=self.merge_image, anchor="w", command=self.frame_merge_button_event)
        self.frame_merge_button.grid(row=1, column=0, sticky="ew")

        self.frame_extract_button = CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                              border_spacing=10, text="Extract",
                                              fg_color="transparent", text_color=("gray10", "gray90"),
                                              hover_color=("gray70", "gray30"),
                                              image=self.chat_image, anchor="w",
                                              command=self.frame_extract_button_event)
        self.frame_extract_button.grid(row=2, column=0, sticky="ew")

        self.appearance_mode_menu = CTkOptionMenu(self.navigation_frame,
                                                  values=["Light", "Dark", "System"],
                                                  command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create merge Frame
        self.merge_frame = CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.merge_frame.grid_columnconfigure(0, weight=1)

        # merge Frame gadgets
        self.merge_title = CTkLabel(master=self.merge_frame, font=("Helvetica", 16),
                                    text="Choose pdf file you want to merge")
        self.merge_title.grid(row=0, column=0, padx=20, pady=(15, 0))
        self.listbox = Listbox(self.merge_frame, width=1000, selectmode='multiple')
        self.listbox.grid(row=1, column=0, padx=20, pady=(10, 0))
        self.output_title = CTkLabel(master=self.merge_frame, font=("Helvetica", 13),
                                     text="Output file name")
        self.output_title.grid(row=2, column=0, padx=20, pady=(10, 0))
        self.output_merge = CTkEntry(self.merge_frame, state=DISABLED)
        self.output_merge.grid(row=3, column=0, padx=20, pady=(10, 0))

        self.button_select = CTkButton(self.merge_frame, text="Select files",
                                       image=self.image_icon_image, corner_radius=10,
                                       compound="left", command=self.upload_handler)
        self.button_select.grid(row=4, column=0, padx=20, pady=5)
        self.button_merge = CTkButton(self.merge_frame, text="Merge files",
                                      image=self.image_icon_image, corner_radius=10,
                                      compound="left", state=DISABLED)
        self.button_merge.grid(row=5, column=0, padx=20, pady=5)
        self.button_delete = CTkButton(self.merge_frame, text="Delete",
                                       image=self.image_icon_image, corner_radius=10,
                                       compound="left", state=DISABLED)
        self.button_delete.grid(row=6, column=0, padx=20, pady=5)
        self.button_delete_all = CTkButton(self.merge_frame, text="Delete all",
                                           image=self.image_icon_image, corner_radius=10,
                                           compound="left", state=DISABLED)
        self.button_delete_all.grid(row=7, column=0, padx=20, pady=5)

        # create extract frame
        self.extract_frame = CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.extract_frame.grid_columnconfigure(1, weight=1)

        # extract Frame gadgets
        self.extract_title = CTkLabel(master=self.extract_frame, font=("Helvetica", 16),
                                      text="Choose the pdf file you want to extract page(s) from")
        self.extract_title.grid(row=0, column=0, columnspan=2, padx=20, pady=15)
        self.button_add_extract = CTkButton(self.extract_frame, text="select file", command=self.upload_handler)
        self.button_add_extract.grid(row=1, column=0, padx=30)
        self.file = CTkLabel(self.extract_frame, font=("Arial", 13))
        self.file.grid(row=1, column=1, padx=30, pady=10)
        self.var = IntVar(value=1)
        self.one = CTkRadioButton(self.extract_frame, variable=self.var, value=1,
                                  command=self.radio_button_handler, text="extract 1 page")
        self.one.grid(row=2, column=0, pady=(10, 10))

        self.page_number = CTkEntry(self.extract_frame, validate="key",
                                    validatecommand=(self.extract_frame.register(self.only_numbers), '%S'),
                                    justify=CENTER)
        self.page_number.grid(row=2, column=1, pady=(10, 10))
        self.two = CTkRadioButton(self.extract_frame, variable=self.var, value=2,
                                  command=self.radio_button_handler, text="extract a range of pages", )
        self.two.grid(row=3, column=0)
        self.start_number = CTkEntry(self.extract_frame, validate="key",
                                     validatecommand=(
                                         self.extract_frame.register(self.only_numbers), '%S'),
                                     justify=CENTER, state=DISABLED)
        self.start_number.grid(row=3, column=1)
        self.end_number = CTkEntry(self.extract_frame, validate="key",
                                   validatecommand=(self.extract_frame.register(self.only_numbers), '%S'),
                                   justify=CENTER, state=DISABLED)
        self.end_number.grid(row=3, column=1)
        self.label = CTkLabel(self.extract_frame, text="Output file name")
        self.label.grid(row=4, column=0, pady=(10, 10))
        self.output_extract = CTkEntry(self.extract_frame, justify=CENTER, state=DISABLED)
        self.output_extract.grid(row=4, column=1, pady=(10, 10))
        self.button_extract = CTkButton(self.extract_frame, text="extract", command=self.extract_handler,
                                        state=DISABLED)
        self.button_extract.grid(row=5, column=1)
        self.button_delete_extract = CTkButton(self.extract_frame, text="delete", command=self.delete_handler,
                                               state=DISABLED)
        self.button_delete_extract.grid(row=5, column=2, sticky="news", pady=(10, 10), )

        # select default frame
        self.select_frame_by_name("merge")

    @staticmethod
    def only_numbers(char):
        """
        function to validate mark entry
        :param char
        :return: boolean
        """
        return char.isdigit()

    @staticmethod
    def switch(component):
        """
        switch the state of a component
        :param component
        """
        if component["state"] == NORMAL:
            component.configure(state=DISABLED)
        else:
            component.configure(state=NORMAL)

    def radio_button_handler(self):
        """
        handles switching between extracting one page
        or a range of pages
        """
        if self.var.get() == 1:
            self.start_number.delete(0, END)
            self.end_number.delete(0, END)
            self.page_number.configure(state=NORMAL)
            self.start_number.configure(state=DISABLED)
            self.end_number.configure(state=DISABLED)

        if self.var.get() == 2:
            self.page_number.delete(0, 'end')
            self.page_number.configure(state=DISABLED)
            self.start_number.configure(state=NORMAL)
            self.end_number.configure(state=NORMAL)

    def upload_handler(self):
        """
        handles uploaded pdf files
        """
        print(dir(self.extract_frame))  # frame 2 is merge and 3 is extract
        print(self.extract_frame.winfo_name())
        print(self.grab_current())

        current_tab = 0  # self.tab_control.index(self.tab_control.select())
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

    def merge_handler(self):
        """
        handles merging pdf files
        """
        file_name = self.output_merge.get()
        if len(file_name) == 0:
            messagebox.showinfo("ERROR", "Please entre the name of the output file", icon='error')
            return
        folder_selected = fd.askdirectory()
        if folder_selected == "":
            return
        merge_pdfs(self.paths, folder_selected, file_name)
        self.output_merge.delete(0, last=END)
        self.switch(self.output_merge)
        self.switch(self.button_merge)
        self.switch(self.button_delete_merge)
        self.switch(self.button_delete_all)
        self.listbox.delete(0, last=END)
        self.paths = []
        messagebox.showinfo("RESULT", "pdfs merged successfully", icon='info')

    def extract_handler(self):
        """
        handles extractin page(s) from pdf file
        """
        num_pages = get_num_pages(self.path)
        if self.output_extract.get() == "":
            messagebox.showinfo("ERROR", "Please enter the name of the output file", icon='error')
            return
        if self.var.get() == 1:
            try:
                page_num = int(self.page_number.get())
            except ValueError:
                messagebox.showinfo("ERROR", "please enter page number", icon='error')
                return
            if page_num < 1 or page_num > num_pages:
                messagebox.showinfo("ERROR", "invalid page number", icon='error')
                return
            else:
                folder_selected = fd.askdirectory()
                if folder_selected == "":
                    return
                extract_page_from_pdf(self.path, page_num, folder_selected, self.output_extract.get())
                self.output_extract.delete(0, last=END)
                self.page_number.delete(0, last=END)
                messagebox.showinfo("INFO", "page extracted successfully", icon='info')
        else:
            try:
                page_num_start = int(self.start_number.get())
                page_num_end = int(self.end_number.get())
            except ValueError:
                messagebox.showinfo("ERROR", "please enter page number", icon='error')
                return
            if page_num_end < page_num_start or page_num_start < 1 or page_num_end > num_pages:
                messagebox.showinfo("ERROR", "invalid page numbers", icon='error')
                return
            folder_selected = fd.askdirectory()
            if folder_selected == "":
                return
            extract_pages_from_pdf(self.path, page_num_start, page_num_end, folder_selected, self.output_extract.get())
            self.output_extract.delete(0, last=END)
            self.start_number.delete(0, last=END)
            self.end_number.delete(0, last=END)
            self.switch(self.output_extract)
            messagebox.showinfo("INFO", "page extracted successfully", icon='info')

    def delete_handler(self):
        """
        handles deleting the uploaded file(s) from selection
        """
        current_tab = self.tab_control.index(self.tab_control.select())
        if current_tab == 0:
            selection = self.listbox.curselection()
            if len(selection) > 0:
                for index in selection[::-1]:
                    self.listbox.delete(index)
                    del (self.paths[index])
                if self.listbox.size() == 1:
                    self.output_merge.delete(0, last=END)
                    self.switch(self.output_merge)
                    self.switch(self.button_merge)
                if self.listbox.size() < 1:
                    self.switch(self.button_delete_merge)
                    self.switch(self.button_delete_all)
        if current_tab == 1:
            self.path = ""
            self.output_extract.delete(0, last=END)
            self.file.config(text="")
            self.switch(self.button_delete_extract)
            self.switch(self.button_extract)
            self.switch(self.output_extract)

    def delete_all_handler(self):
        """
        handles deleting all the uploaded files from selection
        """
        self.listbox.delete(0, END)
        self.paths = []
        self.switch(self.button_delete_merge)
        self.switch(self.button_delete_all)
        self.output_merge.delete(0, last=END)
        self.output_merge["state"] = DISABLED
        self.button_merge["state"] = DISABLED

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.frame_merge_button.configure(fg_color=("gray75", "gray25") if name == "merge" else "transparent")
        self.frame_extract_button.configure(fg_color=("gray75", "gray25") if name == "extract" else "transparent")

        # show selected frame
        if name == "merge":
            self.merge_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.merge_frame.grid_forget()
        if name == "extract":
            self.extract_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.extract_frame.grid_forget()

    def frame_merge_button_event(self):
        self.select_frame_by_name("merge")

    def frame_extract_button_event(self):
        self.select_frame_by_name("extract")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()
