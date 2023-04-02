import pickle
from src.Classes import BieniciFinder, Finder
from src.Reader import Reader


path="data_engineer/files"



reader=Reader(path)
for data in reader.read_files():
    with open("data_engineer/files/"+data, 'rb') as f:
        data = pickle.load(f)
    e1=BieniciFinder(data)
    d=e1.redirect_to_qeeps()
    print(d)
