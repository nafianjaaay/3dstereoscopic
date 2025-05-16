import tkinter as tk
from tkinter import Canvas, Toplevel
from PIL import Image, ImageTk


class Nimp2(tk.Frame):
    def __init__(self, parent, controller, images, rotations):
        super().__init__(parent, bg='#1a1a1a')
        self.controller = controller
        self.images = images
        self.rotations = rotations
        self.anchor_points = [None, None, None, None]

        # Main Frame
        self.main_frame = tk.Frame(self, bg='#1a1a1a')
        self.main_frame.place(relx=0.5, rely=0.5, anchor='center')

        self.preview_labels = []
        self.choose_buttons = []
        self.anchor_labels = []
        self.reset_buttons = []

        # Build UI for 4 photos
        for col in range(4):
            if images[col] is not None:
                # Apply rotation
                rotated_img = images[col].rotate(rotations[col], expand=True)
                self.images[col] = rotated_img

                # Preview Frame
                preview_frame = tk.Frame(self.main_frame, bg='#1a1a1a', width=360, height=640, 
                                         highlightthickness=2, highlightbackground='#1a1a1a')
                preview_frame.grid(row=0, column=col, padx=20, pady=10)
                preview_frame.grid_propagate(False)

                # Image Preview
                img_resized = self.resize_image(rotated_img, 360, 640)
                img_tk = ImageTk.PhotoImage(img_resized)
                preview_label = tk.Label(preview_frame, image=img_tk, bg='#000')
                preview_label.image = img_tk
                preview_label.pack(fill='both', expand=True)
                self.preview_labels.append(preview_label)

                # Anchor Point Info
                anchor_label = tk.Label(self.main_frame, text="Anchor Point: None", 
                                        font=('Helvetica', 14), bg='#1a1a1a', fg='gray')
                anchor_label.grid(row=1, column=col, pady=(0, 5))
                self.anchor_labels.append(anchor_label)

                # Choose Anchor Button
                choose_button = tk.Button(self.main_frame, text='Choose Anchor Point', 
                                          command=lambda idx=col: self.open_anchor_selector(idx), 
                                          font=('Helvetica', 14), bg='#444', fg='white', width=20, bd=0)
                choose_button.grid(row=2, column=col, pady=(0, 5))
                self.choose_buttons.append(choose_button)

                # Reset Anchor Button
                reset_button = tk.Button(self.main_frame, text='Reset Anchor Point', 
                                         command=lambda idx=col: self.reset_anchor_point(idx),
                                         font=('Helvetica', 14), bg='#555', fg='white', width=20, bd=0)
                reset_button.grid(row=3, column=col, pady=(0, 10))
                self.reset_buttons.append(reset_button)

        # Bottom fixed frame for Back, Reset All, and Next buttons
        self.bottom_frame = tk.Frame(self, bg='#1a1a1a')
        self.bottom_frame.place(relx=0.5, rely=1.0, anchor='s', y=-20)

        # Back Button
        self.back_button = tk.Button(self.bottom_frame, text='Back', 
                                     command=lambda: controller.show_frame("Nimp1"),
                                     font=('Helvetica', 18, 'bold'), bg='#666', fg='white', width=15, bd=0)
        self.back_button.pack(side='left', padx=20)

        # Reset All Button
        self.reset_all_btn = tk.Button(self.bottom_frame, text='Reset All', command=self.reset_all_anchor_points,
                                       font=('Helvetica', 18, 'bold'), bg='#aa4444', fg='white', width=15, bd=0)
        self.reset_all_btn.pack(side='left', padx=20)

        # Next Button
        self.next_button = tk.Button(self.bottom_frame, text='Next', 
                                     command=self.next_menu, font=('Helvetica', 18, 'bold'), 
                                     bg='#5577cc', fg='white', width=15, bd=0)
        self.next_button.pack(side='left', padx=20)

    def resize_image(self, img, target_width, target_height):
        img_w, img_h = img.size
        scale = min(target_width / img_w, target_height / img_h)
        new_size = (int(img_w * scale), int(img_h * scale))
        return img.resize(new_size, Image.Resampling.LANCZOS)

    def open_anchor_selector(self, index):
        anchor_window = Toplevel(self)
        anchor_window.attributes('-fullscreen', True)
        anchor_window.configure(bg='black')
        
        # Hide mouse pointer
        anchor_window.config(cursor="none")
        
        # Create a Canvas for zoom and pan
        canvas = Canvas(anchor_window, bg='black')
        canvas.pack(fill='both', expand=True)
        
        # Load and display the image
        rotated_img = self.images[index]
        img_tk = ImageTk.PhotoImage(rotated_img)
        image_id = canvas.create_image(0, 0, anchor='nw', image=img_tk)
        canvas.image = img_tk
        
        # Center image
        img_w, img_h = rotated_img.size
        screen_w = anchor_window.winfo_screenwidth()
        screen_h = anchor_window.winfo_screenheight()
        offset_x = (screen_w - img_w) // 2
        offset_y = (screen_h - img_h) // 2
        canvas.move(image_id, offset_x, offset_y)

        # Store image position and scale
        self.img_offset = [offset_x, offset_y]
        self.scale_factor = 1.0

        # Crosshair
        h_line = canvas.create_line(0, screen_h // 2, screen_w, screen_h // 2, fill='red', width=2)
        v_line = canvas.create_line(screen_w // 2, 0, screen_w // 2, screen_h, fill='red', width=2)

        # Update crosshair on mouse movement
        def update_crosshair(event):
            canvas.coords(h_line, 0, event.y, screen_w, event.y)
            canvas.coords(v_line, event.x, 0, event.x, screen_h)

        # Save anchor point on click
        def save_anchor(event):
            img_x = (event.x - self.img_offset[0]) / self.scale_factor
            img_y = (event.y - self.img_offset[1]) / self.scale_factor
            self.anchor_points[index] = (img_x, img_y)
            self.anchor_labels[index].config(text=f"Anchor Point: ({int(img_x)}, {int(img_y)})", fg='white')
            anchor_window.destroy()

        # Bind keys for movement and zoom
        def on_key_press(event):
            step = 10
            if event.keysym in ['w', 'Up']:
                canvas.move(image_id, 0, -step)
            elif event.keysym in ['s', 'Down']:
                canvas.move(image_id, 0, step)
            elif event.keysym in ['a', 'Left']:
                canvas.move(image_id, -step, 0)
            elif event.keysym in ['d', 'Right']:
                canvas.move(image_id, step, 0)
            elif event.keysym == '=':
                zoom(1.1)
            elif event.keysym == '-':
                zoom(0.9)

        # Zoom function
        def zoom(scale):
            self.scale_factor *= scale
            canvas.scale('all', screen_w // 2, screen_h // 2, scale, scale)

        # Bind events
        canvas.bind('<Motion>', update_crosshair)
        canvas.bind('<Button-1>', save_anchor)
        anchor_window.bind("<KeyPress>", on_key_press)
        anchor_window.focus_set()

    def reset_anchor_point(self, index):
        self.anchor_points[index] = None
        self.anchor_labels[index].config(text="Anchor Point: None", fg='gray')

    def reset_all_anchor_points(self):
        for i in range(4):
            self.reset_anchor_point(i)

    def next_menu(self):
        print("Next...")
