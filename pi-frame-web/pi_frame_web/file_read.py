import json


class JsonReader:
    def __init__(self, filename):
        self.FileName = filename

    def write(self, dictionary):
        out_file = open(self.FileName, "w")
        json.dump(dictionary, out_file, indent=4)
        out_file.close()

    def read(self):
        in_file = open(self.FileName, "r")
        in_dict = json.load(in_file)
        in_file.close()
        return in_dict
