import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import threading

class Nimp1(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='#1a1a1a')

        # Inisialisasi atribut
        self.images = [None, None, None, None]
        self.file_names = ['', '', '', '']
        self.rotations = [0, 0, 0, 0]

        # Main frame untuk konten utama
        self.main_frame = tk.Frame(self, bg='#1a1a1a')
        self.main_frame.place(relx=0.5, rely=0.5, anchor='center')

        self.import_buttons = []
        self.preview_labels = []
        self.file_name_labels = []
        self.buttons_frames = []
        self.preview_frames = []

        # Build UI untuk 4 foto
        for col in range(4):
            # Tombol Import
            import_btn = tk.Button(self.main_frame, text=f'Import Photo {col+1}',
                                   command=lambda idx=col: self.import_photo(idx),
                                   font=('Helvetica', 16), bg='#444', fg='white', width=20, bd=0)
            import_btn.grid(row=0, column=col, padx=20, pady=10)
            self.import_buttons.append(import_btn)

            # Frame untuk preview
            preview_frame = tk.Frame(self.main_frame, bg='#1a1a1a', width=360, height=640,
                                     highlightthickness=2, highlightbackground='#1a1a1a')
            preview_frame.grid(row=1, column=col, padx=20, pady=10)
            preview_frame.grid_propagate(False)
            self.preview_frames.append(preview_frame)

            # Label untuk preview gambar
            preview_label = tk.Label(preview_frame, bg='#000', relief='flat')
            preview_label.pack(fill='both', expand=True)
            self.preview_labels.append(preview_label)

            # Label untuk nama file
            file_name_label = tk.Label(self.main_frame, text='No Image', font=('Helvetica', 14), bg='#1a1a1a', fg='gray')
            file_name_label.grid(row=2, column=col, padx=20, pady=(5,5))
            self.file_name_labels.append(file_name_label)

            # Frame untuk tombol rotate dan reset
            btn_frame = tk.Frame(self.main_frame, bg='#1a1a1a')
            btn_frame.grid(row=3, column=col, padx=20, pady=(0,15))
            self.buttons_frames.append(btn_frame)

            # Tombol Rotate Left
            rotate_left_btn = tk.Button(btn_frame, text='⟲ Rotate Left',
                                        command=lambda idx=col: self.rotate_image(idx, -90),
                                        font=('Helvetica', 12), bg='#666', fg='white', bd=0, width=12)
            rotate_left_btn.pack(side='left', padx=3)

            # Tombol Reset
            reset_btn = tk.Button(btn_frame, text='⟲ Reset',
                                  command=lambda idx=col: self.reset_image(idx),
                                  font=('Helvetica', 12), bg='#666', fg='white', bd=0, width=12)
            reset_btn.pack(side='left', padx=3)

            # Tombol Rotate Right
            rotate_right_btn = tk.Button(btn_frame, text='⟳ Rotate Right',
                                         command=lambda idx=col: self.rotate_image(idx, 90),
                                         font=('Helvetica', 12), bg='#666', fg='white', bd=0, width=12)
            rotate_right_btn.pack(side='left', padx=3)

        # Bottom fixed frame untuk tombol Reset All dan Next
        self.bottom_frame = tk.Frame(self, bg='#1a1a1a')
        self.bottom_frame.place(relx=0.5, rely=1.0, anchor='s', y=-20)

        # Tombol Reset All
        self.reset_all_btn = tk.Button(self.bottom_frame, text='Reset All', command=self.reset_all,
                                       font=('Helvetica', 18, 'bold'), bg='#aa4444', fg='white', width=15, bd=0)
        self.reset_all_btn.pack(side='left', padx=20)

        # Tombol Next (aktif jika minimal 2 foto)
        self.next_button = tk.Button(self.bottom_frame, text='Next', 
                                     command=controller.navigate_to_page2,  
                                     font=('Helvetica', 18, 'bold'), 
                                     bg='#555', fg='white', width=15, bd=0, state='disabled')
        self.next_button.pack(side='right', padx=20)

    def import_photo(self, index):
        filepath = filedialog.askopenfilename(title=f'Select Photo {index+1}',
                                              filetypes=[('Image Files', '*.jpg *.jpeg *.png *.bmp')])
        if filepath:
            self.images[index] = Image.open(filepath)
            self.file_names[index] = filepath.split('/')[-1]
            self.rotations[index] = 0
            self.update_preview(index)
            self.highlight_preview(index)
            self.validate_photos()

            # Hide the import button
            self.import_buttons[index].grid_remove()

    def update_preview(self, index):
        preview_label = self.preview_labels[index]
        file_name_label = self.file_name_labels[index]
        img = self.images[index]

        if img is None:
            preview_label.configure(image='', bg='#000')
            preview_label.image = None
            file_name_label.configure(text='No Image', fg='gray')
            self.preview_frames[index].configure(highlightbackground='#1a1a1a')
            return

        rotated_img = img.rotate(self.rotations[index], expand=True)
        frame_width, frame_height = 360, 640
        img_w, img_h = rotated_img.size
        scale = min(frame_width / img_w, frame_height / img_h)
        new_size = (int(img_w * scale), int(img_h * scale))

        img_resized = rotated_img.resize(new_size, Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img_resized)

        preview_label.configure(image=img_tk, bg='#000')
        preview_label.image = img_tk

        file_name_label.configure(text=self.file_names[index], fg='white')
        self.preview_frames[index].configure(highlightbackground='#1a1a1a')

    def rotate_image(self, index, degrees):
        if self.images[index] is not None:
            self.rotations[index] = (self.rotations[index] + degrees) % 360
            self.update_preview(index)

    def reset_image(self, index):
        self.images[index] = None
        self.file_names[index] = ''
        self.rotations[index] = 0
        self.update_preview(index)
        self.validate_photos()

        # Show the import button again
        self.import_buttons[index].grid()

    def reset_all(self):
        for i in range(4):
            self.reset_image(i)

    def validate_photos(self):
        valid_photos = sum(img is not None for img in self.images)
        if valid_photos >= 2:
            self.next_button.config(state='normal', bg='#5577cc')
        else:
            self.next_button.config(state='disabled', bg='#555')

    def highlight_preview(self, index):
        def clear_highlight():
            self.preview_frames[index].configure(highlightbackground='#1a1a1a')

        self.preview_frames[index].configure(highlightbackground='#55aaff')
        threading.Timer(0.8, clear_highlight).start()
