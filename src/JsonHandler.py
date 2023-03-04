import json
import jpype
from datetime import date

class JsonReader:
    def __init__(self):
        self.FinalJSONFile = {
            "Empresa": [],
            "Codigo Loja": [],
            "Estado": [],
            "Preco": [],
            "Estoque": [],
            "Data": []
        }

    def ReadFile(self, fileName):
        with open(fileName) as file:
            data = json.load(file)
        return data
    
    def CreateCompanyData(self, key, company, translator):
        stateBranches = company.StateBranches
        for stateBranch in stateBranches:
            for branch in stateBranch.Branches:
                self.FinalJSONFile["Empresa"].append(translator.Translations[key])
                self.FinalJSONFile["Codigo Loja"].append(branch.Id)
                self.FinalJSONFile["Estado"].append(translator.Translations[stateBranch.State])
                self.FinalJSONFile["Preco"].append(branch.Price)
                self.FinalJSONFile["Estoque"].append(branch.Stock)
                self.FinalJSONFile["Data"].append(date.today().strftime("%d/%m/%Y"))    

        print(self.FinalJSONFile)

    def CreateXLSX(self):
        jpype.startJVM()
        from asposecells.api import Workbook
        filename = "assets/json/finaljson.json"
        with open(filename, "w") as outfile:
            json.dump(self.FinalJSONFile, outfile)
        workbook = Workbook(filename)
        workbook.save("output/report.xlsx")
        jpype.shutdownJVM()
