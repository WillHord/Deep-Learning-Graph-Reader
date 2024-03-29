import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import threading
import warnings

from functools import wraps


def loading_bar(func):
    """Decorator to add loading bar to GUI"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        self.progress.pack()
        self.progress.start(10)
        func(*args, **kwargs)
        self.progress.stop()
        self.progress.pack_forget()
    return wrapper


def start_in_thread(func):
    """Decorator to start function in new thread"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        threading.Thread(target=func, args=args,
                         kwargs=kwargs, daemon=True).start()
    return wrapper


class GUI:
    """
    GUI for Deep Learning Graph Reader
    """

    def __init__(self, converter=None):
        self.window = tk.Tk()
        self.window.title("Deep Learning Graph Reader")

        self.converter = converter
        self.build()

    def build(self):
        # Create left section for file input
        self.file_input_frame = tk.Frame(self.window)
        self.file_input_frame.grid(row=0, column=0, padx=10, pady=10)

        self.file_label = tk.Label(self.file_input_frame, text="Input File:")
        self.file_label.pack()

        self.file_entry = tk.Entry(self.file_input_frame)
        self.file_entry.pack()

        button_frame = tk.Frame(self.file_input_frame)
        button_frame.pack()

        self.browse_file_button = tk.Button(
            button_frame, text="Browse", command=lambda: self.browse_file(self.file_entry))
        self.browse_file_button.pack(side=tk.LEFT)

        self.upload_button = tk.Button(
            button_frame, text="Upload", command=self.upload_file)
        self.upload_button.pack(side=tk.LEFT)

        # Progress bar
        self.progress = ttk.Progressbar(
            self.file_input_frame, orient=tk.HORIZONTAL, length=100, mode='indeterminate')

        # Create right section for output and image display
        self.output_frame = tk.Frame(self.window)
        self.output_frame.grid(row=0, column=1, padx=10, pady=10)

        # Frame for the image
        self.image_frame = tk.Frame(self.output_frame)
        self.image_frame.pack()

        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack()

        self.output_label = tk.Label(self.output_frame, text="Output:")
        self.output_label.pack()

        self.output_table = tk.Text(self.output_frame)
        self.output_table.configure(state='disabled')
        self.output_table.pack()

    @start_in_thread
    @loading_bar
    def browse_file(self, path_entry):
        filepath = filedialog.askopenfilename()
        if filepath:
            path_entry.delete(0, tk.END)
            path_entry.insert(0, filepath)

    @start_in_thread
    @loading_bar
    def upload_file(self):
        filepath = self.file_entry.get()
        if filepath:
            img = Image.open(filepath)
            img.thumbnail((200, 200))
            img = ImageTk.PhotoImage(img)
            self.image_label.configure(image=img)
            self.image_label.image = img

            if self.converter:
                valid_image = self.converter.check_filetype(filepath)
                if valid_image:
                    chart_type, data = self.converter.convert_image_to_data(
                        filepath)
                    self.output_table.configure(state='normal')
                    self.output_table.delete(1.0, tk.END)
                    self.output_table.insert(1.0, data.to_string(index=False))
                    self.output_table.insert(
                        1.0, "Chart Type: " + chart_type + "\n")
                    self.output_table.configure(state='disabled')
                else:
                    self.output_table.configure(state='normal')
                    self.output_table.delete(1.0, tk.END)
                    self.output_table.insert(1.0, "ERROR: Invalid image file")
                    self.output_table.configure(state='disabled')
            else:
                self.output_table.configure(state='normal')
                self.output_table.delete(1.0, tk.END)
                self.output_table.insert(1.0, "ERROR: Converter not set")
                self.output_table.configure(state='disabled')
        else:
            # Display error message
            self.output_table.configure(state='normal')
            self.output_table.delete(1.0, tk.END)
            self.output_table.insert(1.0, "ERROR: No file selected")
            self.output_table.configure(state='disabled')
            pass

    def run(self):
        self.window.mainloop()


if __name__ == '__main__':
    warnings.warn("This is a module and should not be run directly\nConverter will not be loaded")
    gui = GUI()
    gui.run()
