import sys 
import os
import pickle
import unittest
import inspect


current_path = os.path.abspath(inspect.getsourcefile(lambda:0))
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]
sys.path.insert(0, parent_dir)

import pickle
from src.Classes import BieniciFinder, Finder
from src.Reader import Reader


class TestBieniciFinder(unittest.TestCase):
    def setUp(self):
        self.e=BieniciFinder(data)
        print("setUp")
    
    def tearDown(self):
        print("____________")
        pass

    def test_email_is_instance_of_Nylas_email(self):
        print("test_email_is_instance_of_Nylas_email")
        self.assertIsInstance(self.e, BieniciFinder)

    def test_existance_input(self):
        print("test_existance")
        self.assertIn("to",self.e.email)
        self.assertIn("received_at",self.e.email)
        self.assertIn("body",self.e.email)
    
    def test_perse_existance(self):
        print('test_perse_existance')
        result=self.e.parse_email()
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
        self.assertIn("lien", result["offre"])

    def test_perse_equal(self):
        print('test_perse_equal')
        #html email modified for test
        with open("data_engineer/tests/test.html", 'r') as f:
            html_body_test = f.read()
        #change the body for the Nylas Email 
        self.e.email.body=html_body_test
        #parse the email
        parsed_email=self.e.parse_email()
        #verify result
        self.assertEqual( parsed_email["candidat"]["ContactName"], "Lachtar Nour")
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
        self.assertEqual(parsed_email["offre"]["lien"], "http://test.com/")




if __name__=='__main__':
    path="data_engineer/files"
    reader=Reader(path)
    for data in reader.read_files():
        with open("data_engineer/files/"+data, 'rb') as f:
            data = pickle.load(f)
        unittest.main()

