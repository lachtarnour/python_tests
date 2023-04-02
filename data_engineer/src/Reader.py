import os

class Reader():
    def __init__(self, path: str):
        self.path = path

    def read_files(self):
        files = os.listdir(self.path)
        return files