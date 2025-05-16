import tkinter as tk
from nimp1 import Nimp1
from nimp2 import Nimp2

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Nimslo 3D Stereoscopic Creator')
        self.state('zoomed')

        container = tk.Frame(self)
        container.pack(fill='both', expand=True)

        # Agar grid di container bisa expand
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Inisialisasi dictionary untuk menyimpan frame
        self.frames = {}

        # Page 1 (Import & Rotate)
        self.page1 = Nimp1(container, self)
        self.frames['Nimp1'] = self.page1
        self.page1.grid(row=0, column=0, sticky='nsew')
        self.show_frame('Nimp1')

        # Page 2 (Anchor Points) - Awalnya None, akan diinisialisasi saat Next button ditekan
        self.page2 = None

    def navigate_to_page2(self):
        # Update page2 with current images and rotations from page1
        self.page2 = Nimp2(self.page1.master, self, self.page1.images, self.page1.rotations)
        self.frames['Nimp2'] = self.page2
        self.page2.grid(row=0, column=0, sticky='nsew')
        self.show_frame('Nimp2')


    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()

if __name__ == '__main__':
    app = MainApp()
    app.mainloop()
