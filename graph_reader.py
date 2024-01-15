import argparse
import tkinter as tk
import pathlib
import os
from datetime import datetime

from src import converter

# TODO: Check image type

class GraphReader:
    def __init__(self):
        self.parser = self.create_parser()
        self.converter = None
        self.args = None

    def create_parser(self):
        parser = argparse.ArgumentParser(description='Deep Learning Graph Reader')
        parser.add_argument('--cmd', action='store_true', help='Use Command Line interface')
        parser.add_argument('-o', '--output_dir', default="./output", help='Chose Output Directory')
        parser.add_argument('-m', '--model_dir', default="./models", type=pathlib.Path, help='Chose Model Directory')
        parser.add_argument('-i', '--input_file', type=open, help='Chose Input File')
        return parser

    def run(self):
        self.args = self.parser.parse_args()

        if self.args.cmd:
            self.converter = converter.GraphConverter(self.args.model_dir)
            self.run_command_line()
        else:
            raise NotImplementedError("GUI not implemented yet - please use command line interface (--cmd)")
            # self.run_gui()

    def run_gui(self):
        # GUI implementation goes here
        root = tk.Tk()
        root.mainloop()

    def run_command_line(self):
        # Command line implementation goes here
        print("Running command line interface")
        print("-_-_-_-_-_-_-_-_-_-_")
        if self.args.input_file:
            print("Input File: " + self.args.input_file.name)
            chart_type, data = self.converter.convert_image_to_data(self.args.input_file.name)
            print("Chart Type: " + chart_type)
            print("Data: ")
            print(data.to_string(index=False))
            
            self.save_data(data)
        else:
            raise Exception("No input file specified")
            
    def save_data(self, data):
        print("Saving data to " + self.args.output_dir)
        if not os.path.exists(self.args.output_dir):
            os.makedirs(self.args.output_dir)
        data.to_csv(self.args.output_dir + f"/{datetime.now().strftime('%Y%m%d-%H%M%S')}-output.csv", index=False)
            
        

if __name__ == '__main__':
    graph_reader = GraphReader()
    graph_reader.run()
