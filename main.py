import customtkinter as ctk
from tkinter import filedialog

BACKGROUND_COLOR = '#120f24'
HOVER_COLOR = '#241e48'

class App(ctk.CTk):
    def __init__(self):

        # window setup
        super().__init__(fg_color = BACKGROUND_COLOR)
        self.geometry('600x500+104+104')
        self.overrideredirect(True)
        self.bind('<Escape>', lambda event: self.quit())

        # data
        self.file = None

        # widgets
        self.title_menu = TitleMenu(self, self.open_file, self.save_file)

        self.textbox = ctk.CTkTextbox(self, fg_color = BACKGROUND_COLOR, font=ctk.CTkFont(family='Calibri', size = 16))
        self.textbox.pack(expand = True, fill = 'both', padx = 5, pady = 5)

        self.bind('<Control-KeyRelease-s>', lambda event: self.save_file())

        self.mainloop()

    def open_file(self, ask_for_file = True):
        if ask_for_file:
            try:
                self.file = filedialog.askopenfilename()
            except:
                pass

        if self.file:
            self.textbox.delete('0.0', 'end')

            filename = self.file.split('/')[len(self.file.split('/')) - 1]
            self.title_menu.text_var.set(filename)

            with open(self.file, 'r', encoding='UTF-8') as file:
                self.textbox.insert('0.0', file.read())

    def save_file(self):
        if self.file:
            # write to the file
            with open(self.file, 'w', encoding='UTF-8') as file:
                file.write(self.textbox.get('0.0', 'end'))
        else:
            try:
                # ask to set the file name
                self.file = filedialog.asksaveasfilename() + '.txt'
            except:
                pass

            if self.file == '.txt':
                self.file = None

            if self.file:
                # write to the file
                with open(self.file, 'w', encoding='UTF-8') as file:
                    file.write(self.textbox.get('0.0', 'end'))

                # open the file with it's new name
                self.open_file(False)

class TitleMenu(ctk.CTkFrame):
    def __init__(self, parent, open_file_func, save_file_func):
        super().__init__(master = parent, fg_color = BACKGROUND_COLOR, height = 30)
        self.pack(fill = 'x')

        # data
        self.parent = parent
        self.text_var = ctk.StringVar(value = 'Untitled.txt')
        self.start_pos = None

        self.open_file_func = open_file_func
        self.save_file_func = save_file_func

        # options
        self.optionmenu = ctk.CTkOptionMenu(self, values=["Open", "Save"], width = 100, command = self.optionmenu_callback, button_color=BACKGROUND_COLOR, button_hover_color=HOVER_COLOR, bg_color=BACKGROUND_COLOR, fg_color=BACKGROUND_COLOR, dropdown_fg_color=BACKGROUND_COLOR, dropdown_hover_color=HOVER_COLOR)
        self.optionmenu.set("File")
        self.optionmenu.place(relx = 0, rely = 0, anchor = 'nw')

        # window title
        self.title_text = ctk.CTkLabel(self, text = 'Untitled.txt', textvariable = self.text_var, font = ctk.CTkFont(family = 'Calibri', size = 16, weight = 'normal'))
        self.title_text.place(relx = 0.5, rely = 0.5, anchor = 'center')

        # exit button
        exit_button = ctk.CTkButton(self, text='X', width = 30, font = ctk.CTkFont(family = 'Calibri', size = 16, weight = 'bold'), fg_color=BACKGROUND_COLOR, hover_color=HOVER_COLOR, command = lambda: self.quit())
        exit_button.place(relx = 1, rely = 0, anchor = 'ne')

        # handle window dragging
        self.bind('<Button>', self.get_coordinate)
        self.bind('<Motion>', self.move_window)
        self.bind('<ButtonRelease>', self.remove_coordinate)

    def get_coordinate(self, event):
        if event.num == 1: # left click
            self.start_pos = (event.x, event.y)

    def move_window(self, event):
        if self.start_pos:

            # get the distance moved by the mouse
            x_distance = event.x - self.start_pos[0]
            y_distance = event.y - self.start_pos[1]

            # move the window based on the distance
            self.parent.geometry(f'{600}x{500}+{self.parent.winfo_x() + x_distance}+{self.parent.winfo_y() + y_distance}')

    def remove_coordinate(self, event):
        if event.num == 1: # left click
            self.start_pos = None

    def optionmenu_callback(self, event):
        match event:
            case 'Open': self.open_file_func()
            case 'Save': self.save_file_func()
        self.optionmenu.set("File")

if __name__ == "__main__":
    App()