import JsonHandler
import PyautoguiHandler
import Stores
import HtmlHandler
import Translations
import time
import sys

startTime = time.time()

configurationFile = "assets/json/configuration.json"
companiesFile = "assets/json/stores.json"
translationFile = "assets/json/translation.json"

jsonReader = JsonHandler.JsonReader()
autoguiHandler = PyautoguiHandler.AutoGui()
htmlReader = HtmlHandler.HtmlReader()

configurationData = jsonReader.ReadFile(configurationFile)
companiesData = jsonReader.ReadFile(companiesFile)['companies']
translationData = jsonReader.ReadFile(translationFile)

translator = Translations.Translator(translationData)

#autoguiHandler.GetMousePosition()

companiesDict = { }

for key in companiesData:
    companiesDict[key] = Stores.Company(companiesData[key])

for key, value in configurationData.items():
    autoguiHandler.NavigateTo(value)
    company = companiesDict[key]

    for stateBranch in company.StateBranches:
        for branch in stateBranch.Branches:
            branchId = branch.Id

            autoguiHandler.ChangeStore(key, company, branchId.replace("#", "") if "#" in branchId else branchId)
            pageHtml = autoguiHandler.GetHtml()

            priceTags = htmlReader.GetTags(key, True, pageHtml, company.PriceTags)
            stockTags = htmlReader.GetTags(key, False, pageHtml, company.StockTags)

            if (priceTags.__len__() > 0):
                branch.Price = htmlReader.CreatePrice(key, priceTags[0])
        
            if (stockTags.__len__() > 0):
                branch.Stock = htmlReader.CreateStock(key, stockTags[0])
                    
    jsonReader.CreateCompanyData(key, company, translator)
    autoguiHandler.Close()

jsonReader.CreateXLSX()
endTime = time.time()
print(endTime - startTime)
sys.exit()