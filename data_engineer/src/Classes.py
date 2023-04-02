from abc import ABC, abstractmethod
import re
import nylas
from bs4 import BeautifulSoup


class Finder(ABC):
    def __init__(self, email):
        assert type(email)==nylas.client.restful_models.Message
        self.email = email
        
    @abstractmethod
    def parse_email(self):
        pass

    @abstractmethod
    def redirect_to_qeeps(self, parsed_email):
        pass

class BieniciFinder(Finder):
    def parse_email(self):
        d={}
        
        #professionnel
        try:
            for i in self.email["to"]:
                # a changer contain
                if "byqeeps.com" not in i['email']:
                    professionnel = i
                    break
        except KeyError:
            professionnel = None
            print("professionnel mail not found")
            
        d["professionnel"]=professionnel

        #date
        try :
            date=self.email["received_at"]   
        except KeyError:
            date=None
            print("received_at not found")
        d["date"]=date
        
        #body of message object
        try:
            body_html = BeautifulSoup(self.email["body"], 'html.parser')
        except KeyError:
            print("body not found")
            
        #candidat :
        try:
            contact_info = body_html.find("table", class_="contactInfo").find_all("strong")
            ContactName = contact_info[0].text.replace("\xa0", " ")
            ContactPhone = contact_info[1].text.replace("\xa0", " ")
            ContactEmail = contact_info[2].text.replace("\xa0", " ")
            d["candidat"]={"ContactName":ContactName,"ContactPhone":ContactPhone,"ContactEmail":ContactEmail}
        except (AttributeError, TypeError, KeyError, ValueError, IndexError) as e:
            print(f"An exception occurred: {type(e).__name__}")
            d['candidat']={"ContactName":'',"ContactPhone":'',"ContactEmail":''}


        #proprety
        Title=body_html.find("div",class_="realEstateAd").find("td",class_="realEstateAdTitle").text
        Title= Title.replace("\xa0", " ")
        ### Extract the part of the string before the first number
        Type=re.search(r'^\D+', Title).group().strip()
        ### Extract the numerics in the string
        text = "Maison de compagne 4 piÃ¨ces 120 mÂ²"
        numeric_values = re.findall(r'\d+\.*\d*', text)
        numeric_values = [float(numeric_value) if '.' in numeric_value else int(numeric_value) for numeric_value in numeric_values]
        NumPieces=numeric_values[0]
        ### Extract the second number in the string
        Space=numeric_values[1]
        ##adress = postal_code ville arrandicement
        Adress=body_html.find("div",class_="realEstateAd").find("td",class_="realEstateAdAddress").text
        Adress=Adress.replace("\xa0", " ")
        ### Chercher le premier nombre avant l'espace dans la chaîne (le code postal)
        PostalCode = int(re.search(r'\d+\s', Adress).group(0).strip())
        ### Chercher le nom de la ville après le code postal
        City = re.search(r'\d+\s+(.*)', Adress).group(1)
        d["property"]={"Type":Type,"NumPieces":NumPieces,"Space":Space,"adress":{"PostalCode":PostalCode,"City":City}}

        #message
        message=body_html.find("td",class_="preWrap contactMessage").text
        d["message"]=message

        ##offre
        Cost=body_html.find("div",class_="realEstateAd").find("td",class_="realEstateAdPrice").text
        Cost=Cost.replace("\xa0", " ").replace("€","€ ")
        ###cost
        Price = float(re.search(r'\d+', Cost).group())
        ###contract
        if "par mois" in Cost[Cost.find("€")+1:].lower():
            contract = "rent"
        else:
            contract = "sale"
        ##reference
        Reference=body_html.find("div",class_="realEstateAd").find("td",class_="realEstateAdRef").text
        Reference = Reference.split(":")[1].strip()
        lien=body_html.find('table',class_="button secondaryButton").a["href"]
        d["offre"]={"contract":contract,"Price":Price,
                    "Reference":Reference,"lien":lien}
        return(d)

        
    def redirect_to_qeeps(self):
        return(self.parse_email())


class SeLogerFinder(Finder):
    def parse_email(self):
        pass

    def redirect_to_qeeps(self):
        pass