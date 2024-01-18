import pytest
from unittest.mock import MagicMock, patch
from src.converter import GraphConverter
import pandas as pd
from PIL import Image

@pytest.fixture
def converter_instance():
    converter = GraphConverter('./models')
    return converter

def test_load_models(converter_instance):
    converter_instance.load_models()
    assert True

def test_process_prediction(converter_instance):
    data = "TITLE |  <0x0A> Time (h) | In[H:O2] <0x0A> 0 | 0 <0x0A> 6 | 1.32 <0x0A> 12 | 2.61 <0x0A> 18 | 1.93 <0x0A> 24 | 3.23"
    chart_type = 3

    ddata = converter_instance.process_prediction(data, chart_type)
    print(ddata)
    assert True
    
def test_check_filetype(converter_instance):
    assert converter_instance.check_filetype('./tests/imgs/test1.jpg') == True
    assert converter_instance.check_filetype('./tests/imgs/test1.png') == True
    assert converter_instance.check_filetype('./tests/imgs/test1.jpeg') == True
    assert converter_instance.check_filetype('./tests/imgs/test1.gif') == False
    assert converter_instance.check_filetype('./tests/imgs/test1.pdf') == False
    assert converter_instance.check_filetype('./tests/imgs/test1.txt') == False
    
def test_convert_image_to_data(converter_instance):
    converter_instance.load_models()
    chart_type_list = ['dot', 'horizontal_bar', 'vertical_bar', 'line', 'scatter']
    data = converter_instance.convert_image_to_data('./tests/imgs/test1.jpg')
    assert data[0] == chart_type_list[3]
    assert type(data[1]) == pd.core.frame.DataFrame
    
def test_predict_graph_type(converter_instance):
    converter_instance.load_models()
    chart_type_list = ['dot', 'horizontal_bar', 'vertical_bar', 'line', 'scatter']
    image = Image.open('./tests/imgs/test1.jpg').convert('RGB')
    predicted_type = converter_instance.predict_graph_type(image)
    assert chart_type_list[predicted_type] == 'line'