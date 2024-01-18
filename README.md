# Deep Learning Graph Reader

A deep learning powered program to convert an image of a graph into a table of data

## Description

The Deep Learning Graph Reader is a powerful tool that leverages machine learning to convert various types of graphs, including bar charts, scatter plots, and more, into structured data tables. This program utilizes a combination of transformer model ([Google DePlot](https://huggingface.co/google/deplot)) and a fine-tuned Convolutional Neural Network ([Resnet50](https://pytorch.org/vision/main/models/generated/torchvision.models.resnet50.html)) to efficiently extract valuable insights from graphical representations. The models were fine tuned on the Kaggle [Benetech - Making Graphs Accessible](https://www.kaggle.com/competitions/benetech-making-graphs-accessible) competition dataset

## Getting Started

### Dependencies

- [Python 3.8](https://www.python.org/) or higher

### Installing
1. Clone the repo
```
git clone git@github.com:WillHord/Deep-Learning-Graph-Reader.git
```
2. Install required libraries
```
pip install -r requirements.txt
```

### Executing program
Start the program with the GUI by running the command:
```
python graph_reader.py
```
Or use the command line version by running:
```
python graph_reader.py --cmd -i IMAGE_FILE
```

### Testing
If you want to test and verify the program is working as intended run the command:
```
python -m coverage run -m pytest tests/converter_tests.py
```
## Help
If you need help use the command:
```
python graph_reader.py --help
```

## Authors

Program made by
- [Will Hord](https://github.com/WillHord)

Model training/fine-tuning and pipeline design made in collaboration with:
- Sion Daniel
- Kai Hay
- Brendon Chen
- Qingmei Chen

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
