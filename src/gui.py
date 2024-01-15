import tkinter as tk


class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Image Reader")

        # Create left section for file input
        self.file_input_frame = tk.Frame(self.window)
        self.file_input_frame.grid(row=0, column=0, padx=10, pady=10)

        self.file_label = tk.Label(self.file_input_frame, text="Input File:")
        self.file_label.pack()

        self.file_entry = tk.Entry(self.file_input_frame)
        self.file_entry.pack()
        
        self.upload_button = tk.Button(self.file_input_frame, text="Upload")
        self.upload_button.pack()

        # Create right section for output table
        self.output_frame = tk.Frame(self.window)
        self.output_frame.grid(row=0, column=1, padx=10, pady=10)

        self.output_label = tk.Label(self.output_frame, text="Output Table:")
        self.output_label.pack()

        self.output_table = tk.Text(self.output_frame)
        self.output_table.pack()

    def run(self):
        # Start the main event loop
        self.window.mainloop()

if __name__ == '__main__':
    gui = GUI()
    gui.run()
