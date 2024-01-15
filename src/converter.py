from PIL import Image
import os
import pandas as pd

import torch
import torchvision.transforms as transforms
from transformers import AutoProcessor, Pix2StructConfig, Pix2StructForConditionalGeneration


class GraphConverter:
    def __init__(self, model_path):
        self.device = torch.device(
            "cuda:0" if torch.cuda.is_available() else "cpu")
        print("Using device:", self.device)
        os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

        self.transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[
                                 0.229, 0.224, 0.225]),
        ])

        self.chart_type_list = ['dot', 'horizontal_bar',
                                'vertical_bar', 'line', 'scatter']

        self.CNN = None
        self.DePlot_Model = None
        self.DePlot_Processor = None
        self.load_models(str(model_path))

    def load_models(self, model_path):
        # Load Resnet50 pretrained model
        if os.path.exists(model_path + '/resnet50'):
            print("Loading Resnet50 model...")
            # If using CPU, load the model to CPU
            if self.device == torch.device("cpu"):
                self.CNN = torch.load(
                    model_path + '/resnet50', map_location=torch.device('cpu'))
            else:
                self.CNN = torch.load(model_path + '/resnet50').to(self.device)
        else:
            raise Exception(
                "Pretrained Resnet50 model not found at " + model_path + "/resnet50")

        # Load DePlot pretrained model
        if os.path.exists(model_path + '/deplot_model.bin') and os.path.exists(model_path + '/deplot_processor.bin'):
            print("Loading DePlot model...")
            self.DePlot_Model = Pix2StructForConditionalGeneration.from_pretrained(
                model_path + '/deplot_model.bin').to(self.device)
            self.DePlot_Processor = AutoProcessor.from_pretrained(
                model_path + '/deplot_processor.bin')
        else:
            print("Downloading DePlot model...")
            self.DePlot_Model = Pix2StructForConditionalGeneration.from_pretrained(
                "google/deplot").to(self.device)
            self.DePlot_Processor = AutoProcessor.from_pretrained(
                "google/deplot")

            self.DePlot_Model.save_pretrained(model_path + '/deplot_model.bin')
            self.DePlot_Processor.save_pretrained(
                model_path + '/deplot_processor.bin')
        print("Models loaded successfully!")

    def predict_graph_type(self, image):
        print("Predicting graph type...")
        input_tensor = self.transform(image)
        input_tensor = input_tensor.unsqueeze(0)  # Add batch dimension

        # Move the input tensor to the device
        input_tensor = input_tensor.to(self.device)

        with torch.no_grad():
            output = self.CNN(input_tensor)
        _, predicted_idx = torch.max(output, 1)
        predicted_label = predicted_idx.item()

        return predicted_label

    def convert_image_to_data(self, image_path):
        image = Image.open(image_path).convert('RGB')
        predicted_type = self.predict_graph_type(image)
        predicted_type_str = self.chart_type_list[predicted_type]
        
        print("Converting image to data...")
        inputs = self.DePlot_Processor(
            images=image, text=f"Generate underlying data table of the {predicted_type_str.replace('_', ' ')} graph below:", return_tensors="pt").to(self.device)
        predictions = self.DePlot_Model.generate(**inputs, max_new_tokens=512)
        data = self.DePlot_Processor.decode(
            predictions[0], skip_special_tokens=True)

        processed_data, chart_type = self.process_prediction(
            data, predicted_type)
        return chart_type, processed_data

    def process_prediction(self, data, chart_type):
        print("Processing prediction...")
        # Split the 'data' string into separate lines
        lines = data.split("<0x0A>")

        # Remove the first line (headers)
        header = lines[0]
        axes = [x.strip() for x in lines[1].split("|")]
        lines = lines[2:]

        chart_type = self.chart_type_list[chart_type]

        # Process each line to extract the required information to a pandas dataframe
        table = pd.DataFrame(columns=[axes[0], axes[1]])
        for line in lines:
            # Skip empty lines
            if not line:
                table = pd.concat(
                    [table, pd.DataFrame({axes[0]: 0, axes[1]: 0})])
                continue

            # Split the line by '|' and remove leading/trailing whitespaces
            parts = [part.strip() for part in line.split("|")]

            # Skip lines where the number of parts is not equal to 2
            if len(parts) < 2:
                continue

            # Add the values to the dataframe
            table = pd.concat([table, pd.DataFrame(
                {axes[0]: [parts[0]], axes[1]: [parts[1]]})])
        if table.empty:
            table = pd.concat(
                [table, pd.DataFrame({axes[0]: [0], axes[1]: [0]})])

        # Save the dataframe as a csv file in the ../output folder
        # TODO: Auto make output folder, allow for custom output folder
        # table.to_csv(f"./output/{chart_type}.csv", index=False)
        return table, chart_type


if __name__ == '__main__':
    chart_type_list = ['dot', 'horizontal_bar',
                       'vertical_bar', 'line', 'scatter']
    converter = GraphConverter('../models/')
    # converter.convert_image_to_data('../tests/imgs/test1.jpg')

    data = "TITLE |  <0x0A> Time (h) | In[H:O2] <0x0A> 0 | 0 <0x0A> 6 | 1.32 <0x0A> 12 | 2.61 <0x0A> 18 | 1.93 <0x0A> 24 | 3.23"
    chart_type = 3

    ddata = converter.process_prediction(data, chart_type)
    print(ddata)
    # predicted_type = converter.predict_graph_type('../tests/imgs/test1.jpg')
    # print(f"Predicted type: {chart_type_list[predicted_type]}")
