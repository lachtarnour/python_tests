from abc import ABC, abstractmethod
import re
import nylas
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import logging

class Finder(ABC):
    def __init__(self, email):
        assert type(email) == nylas.client.restful_models.Message
        self.email = email
    
    @abstractmethod
    def parse_email(self):
        pass

    @abstractmethod
    def redirect_to_qeeps(self, parsed_email):
        pass

class BieniciFinder(Finder):
    def parse_email(self):
        result = {}

        # professional
        try:
            for i in self.email["to"]:
                if "byqeeps.com" not in i['email']:
                    professional = i
                    break
        except KeyError:
            professional = None
            logging.warning("professionnel mail not found")
        result["professionnel"] = professional

        # date
        try:
            date = self.email["received_at"]
        except KeyError:
            date = None
            logging.warning("received_at not found")
        result["date"] = date

        # body of message object
        try:
            body_html = BeautifulSoup(self.email["body"], 'html.parser')
        except KeyError:
            logging.warning("body not found")

        # candidat :
        try:
            ContactInfo = body_html.find("table", class_="contactInfo").find_all("strong")
            ContactName = ContactInfo[0].text.replace("\xa0", " ")
            ContactPhone = ContactInfo[1].text.replace("\xa0", " ")
            ContactEmail = ContactInfo[2].text.replace("\xa0", " ")
            result["candidat"] = {"ContactName": ContactName, "ContactPhone": ContactPhone, "ContactEmail": ContactEmail}
        except (AttributeError, TypeError, KeyError, ValueError, IndexError) as e:
            logging.warning(f"An exception occurred: {type(e).__name__}")
            result['candidat'] = {"ContactName": '', "ContactPhone": '', "ContactEmail": ''}

        # proprety
        Title = body_html.find("div", class_="realEstateAd").find("td", class_="realEstateAdTitle").text
        Title = Title.replace("\xa0", " ")
        ### Extract the part of the string before the first number
        Type = re.search(r'^\D+', Title).group().strip()
        ### Extract the numerics in the string
        NumericValues = re.findall(r'\d+\.*\d*', Title)
        NumericValues = [float(numeric_value) if '.' in numeric_value else int(numeric_value) for numeric_value in NumericValues]
        NumPieces = NumericValues[0]
        ### Extract the second number in the string
        Space = NumericValues[1]

        # adress = postal_code ville arrandicement
        Adress = body_html.find("div", class_="realEstateAd").find("td", class_="realEstateAdAddress").text
        Adress = Adress.replace("\xa0", " ")
        ### Chercher le premier nombre avant l'espace dans la chaîne (le code postal)
        PostalCode = int(re.search(r'\d+\s', Adress).group(0).strip())
        ### Chercher le nom de la ville après le code postal
        City = re.search(r'\d+\s+(.*)', Adress).group(1)
        result["property"] = {"Type": Type, "NumPieces": NumPieces, "Space": Space, "adress": {"PostalCode": PostalCode, "City": City}}

        # message
        message = body_html.find("td", class_="preWrap contactMessage").text
        result["message"] = message

        # offre
        cost = body_html.find("div", class_="realEstateAd").find("td", class_="realEstateAdPrice").text
        cost = cost.replace("\xa0", " ").replace("€","€ ")
        ### cost
        price = float(re.search(r'\d+', cost).group())
        ### contract
        if "par mois" in cost[cost.find("€")+1:].lower():
            contract = "rent"
        else:
            contract = "sale"
        ### reference
        reference = body_html.find("div", class_="realEstateAd").find("td", class_="realEstateAdRef").text
        reference = reference.split(":")[1].strip()
        ### link
        link = body_html.find('table', class_="button secondaryButton").a["href"]
        result["offre"] = {"contract": contract, "Price": price, "Reference": reference, "link": link}

        return result

        
    def redirect_to_qeeps(self, client_id, client_secret, token, recipient):
        result = self.parse_email()

        def chaine(d, coef=0):
            # Initialize an empty string to store the formatted data
            MsgToRedirect = ""
            for key, value in d.items():
                MsgToRedirect += "&nbsp;" * (coef*8) + "• " + str(key)
                if type(value) != dict:
                    # If the value is not a dictionary, add it to the string 
                    MsgToRedirect += ' : ' + str(value) + "<br>"+"<br>"
                else:
                    # If the value is a dictionary, recursively call the function with increased indentation
                    MsgToRedirect += "<br>" + chaine(value, coef + 1) + "<br>"
            # Return the formatted string
            return MsgToRedirect


        def send_email(d):
            # Load environment variables
            load_dotenv()

            # Initialize Nylas API client
            nylas_api = nylas.APIClient(client_id, client_secret, token)

            # Create draft email
            draft = nylas_api.drafts.create()
            draft.subject = "candidat for Bienici announce"
            draft.body = chaine(d)
            draft.to = [{"name": "", "email": recipient}]

            try:
                # Send the email
                message = draft.send()
                logging.info(f"Email sent successfully with ID {message['id']} to address: {recipient}")
            except:
                # Handle errors
                logging.error(f"Failed to send email to address: {recipient}")

        send_email(result)
                


class SeLogerFinder(Finder):
    def parse_email(self):
        pass

    def redirect_to_qeeps(self):
        pass