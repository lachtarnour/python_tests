import pickle
from src.Classes import BieniciFinder, Finder
from src.Reader import Reader


path = "data_engineer/files/"

# Define the client ID, client secret, and token needed to access the Qeeps API
client_id = "9w6iuead28xih09pd3hud7033"
client_secret = "b8t4mewlcp6y67vd8g1sjuw1n"
token = "vGtv4NivmgYaDt0l1yyBFh4Dym0Ce9"

# Define the email recipient
recipient = "nour.lachtar@live.fr"

# Create a Reader object to read the pickled data files in the specified directory
reader = Reader(path)

# Iterate over the files in the directory and process each one
for data in reader.read_files():
    # Open the pickled data file and load its contents
    with open(path+data, 'rb') as f:
        data = pickle.load(f)

    # Create a BieniciFinder object using the loaded data
    e1 = BieniciFinder(data)

    # Use the redirect_to_qeeps method of the BieniciFinder object to post the data to the Qeeps API
    e1.redirect_to_qeeps(client_id, client_secret, token, recipient)