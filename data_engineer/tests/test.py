# Import necessary libraries and modules
import sys 
import os
import pickle
import unittest
import inspect

# Define the path of the currently executing Python script
current_path = os.path.abspath(inspect.getsourcefile(lambda:0))
# Define the current directory
current_dir = os.path.dirname(current_path)
# Define the parent directory
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]
# Add the parent directory to the beginning of the module search path
sys.path.insert(0, parent_dir)

# Import the 'pickle' module and the 'BieniciFinder' and 'Finder' classes from the custom module 'src.Classes'
from src.Classes import BieniciFinder, Finder
# Import the 'Reader' function from the custom module 'src.Reader'
from src.Reader import Reader

# Define a class for testing the 'BieniciFinder' class
class TestBieniciFinder(unittest.TestCase):
    
    # This method is called before each test method and sets up the test environment
    def setUp(self):
        # Create an instance of the 'BieniciFinder' class with the argument 'data' and assign it to the instance variable 'self.e'
        self.e = BieniciFinder(data)
        print("setUp")
    
    # This method is called after each test method and cleans up the test environment
    def tearDown(self):
        print("____________")
        pass

    # Define a test method to check if the email instance is an instance of the 'BieniciFinder' class
    def test_email_is_instance_of_Nylas_email(self):
        print("test_email_is_instance_of_Nylas_email")
        self.assertIsInstance(self.e, BieniciFinder)

    # Define a test method to check if the required keys ('to', 'received_at', and 'body') are present in the 'self.e.email' dictionary
    def test_existence_input(self): 
        print("test_existence_input")
        self.assertIn("to", self.e.email)
        self.assertIn("received_at", self.e.email)
        self.assertIn("body", self.e.email)
    
    #Test whether the email can be parsed and contains all the expected data.

    def test_parse_existence(self):
        #Test whether the email can be parsed and contains all the expected data.
        print('test_parse_existence')
        result = self.e.parse_email()
        self.assertIsInstance(result, dict)
        self.assertIn("professionnel", result)
        self.assertIn("date", result)
        self.assertIn("candidat", result)
        self.assertIn("ContactName", result["candidat"])
        self.assertIn("ContactPhone", result["candidat"])
        self.assertIn("ContactEmail", result["candidat"])
        self.assertIn("property", result)
        self.assertIn("Type", result["property"])
        self.assertIn("NumPieces", result["property"])
        self.assertIn("Space", result["property"])
        self.assertIn("adress", result["property"])
        self.assertIn("PostalCode", result["property"]["adress"])
        self.assertIn("City", result["property"]["adress"])
        self.assertIn("offre", result)
        self.assertIn("contract", result["offre"])
        self.assertIn("Price", result["offre"])
        self.assertIn("Reference", result["offre"])
        self.assertIn("link", result["offre"])

    # Test whether the parsed email data is equal to the expected values
    def test_parse_equal(self):
        print('test_parse_equal')
        # html email modified for test
        with open("data_engineer/tests/test.html", 'r') as f:
            html_body_test = f.read()
        # change the body for the Nylas Email
        self.e.email.body = html_body_test
        # parse the email
        parsed_email = self.e.parse_email()
        # verify result
        self.assertEqual(parsed_email["candidat"]["ContactName"], "Lachtar Nour")
        self.assertEqual(parsed_email["candidat"]["ContactPhone"], "+216 22 55 18 21")
        self.assertEqual(parsed_email["candidat"]["ContactEmail"], "nour.lachtar@dauphine.eu")
        self.assertEqual(parsed_email["property"]["Type"], "Maison de compagne")
        self.assertEqual(parsed_email["property"]["NumPieces"], 4)
        self.assertEqual(parsed_email["property"]["Space"], 120)
        self.assertEqual(parsed_email["property"]["adress"]["PostalCode"], 31000)
        self.assertEqual(parsed_email["property"]["adress"]["City"], "Marseille ")
        self.assertEqual(parsed_email["offre"]["contract"], "sale")
        self.assertEqual(parsed_email["offre"]["Price"], 250000.0)
        self.assertEqual(parsed_email["offre"]["Reference"], "My_test")
        self.assertEqual(parsed_email["offre"]["link"], "http://test.com/")





if __name__=='__main__':
    # specify the path to the directory containing the pickled data files
    path = "data_engineer/files/"
    
    # create a Reader object to read the files in the specified directory
    reader = Reader(path)
    # iterate over the files in the directory and run the unit tests on each file
    for data in reader.read_files():
        # open the pickled data file and load its contents
        with open(path+data, 'rb') as f:
            data = pickle.load(f)
            unittest.main()

