import unittest
import sys
import os
import json
from flask import Flask
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "elonmusk"))

from tests.mock_dialogflow_utils import *

from elonmusk.main import cloud_function

class TestMisspellings(unittest.TestCase):

    def test_name(self):
        """Test that a correct response is returned when 'name' is misspelt"""
        app = Flask(__name__)

        with app.app_context():
            name_request = get_test_request("name_misspelt")
            response = cloud_function(name_request)
            result = json.loads(response.get_data(as_text=True))
            
            # Cannot use "Elon Musk" here since the default fallback message is 
            # "My engineers are working on this right now - thanks for talking to Elon Musk Bot"
            self.assertTrue(
                "CEO" in result["fulfillmentMessages"][0]["text"]["text"][0]
            )

    def test_tesla(self):
        """Test that a correct response is returned when 'tesla' is misspelt"""
        app = Flask(__name__)

        with app.app_context():
            tesla_request = get_test_request("tesla_misspelt")
            response = cloud_function(tesla_request)
            result = json.loads(response.get_data(as_text=True))
            
            self.assertTrue(
                "Tesla" in result["fulfillmentMessages"][0]["text"]["text"][0]
            )

    def test_neuralink(self):
        """Test that a correct response is returned when 'neuralink' is misspelt"""
        app = Flask(__name__)

        with app.app_context():
            neu_request = get_test_request("neuralink_misspelt")
            response = cloud_function(neu_request)
            result = json.loads(response.get_data(as_text=True))
            
            self.assertTrue(
                "Neuralink" in result["fulfillmentMessages"][0]["text"]["text"][0]
            )       
    
    def test_university(self):
        """Test that a correct response is returned when 'university' is misspelt"""
        app = Flask(__name__)

        with app.app_context():
            uni_request = get_test_request("uni_misspelt")
            response = cloud_function(uni_request)
            result = json.loads(response.get_data(as_text=True))

            print(result["fulfillmentMessages"][0]["text"]["text"][0])
            
            self.assertTrue(
                "University of Pennsylvania" in result["fulfillmentMessages"][0]["text"]["text"][0]
            )       

    
if __name__ == "__main__":
    unittest.main()