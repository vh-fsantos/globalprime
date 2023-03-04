import JsonHandler
import PyautoguiHandler
import Stores
import HtmlHander
import Translations

configurationFile = "assets/json/configuration.json"
companiesFile = "assets/json/stores.json"
translationFile = "assets/json/translation.json"

jsonReader = JsonHandler.JsonReader()
autoguiHandler = PyautoguiHandler.AutoGui()
htmlReader = HtmlHander.HtmlReader()

configurationData = jsonReader.ReadFile(configurationFile)
companiesData = jsonReader.ReadFile(companiesFile)['companies']
translationData = jsonReader.ReadFile(translationFile)

translator = Translations.Translator(translationData)

companiesDict = { }

for key in companiesData:
    companiesDict[key] = Stores.Company(companiesData[key])

for key, value in configurationData.items():
    autoguiHandler.NavigateTo(value)
    company = companiesDict[key]

    for stateBranch in company.StateBranches:
        for branch in stateBranch.Branches:
            autoguiHandler.ChangeStore(company, branch.Id.replace("#", ""))
            pageHtml = autoguiHandler.GetHtml()

            priceTags = htmlReader.GetTags(pageHtml, company.PriceTags)
            stockTags = htmlReader.GetTags(pageHtml, company.StockTags)

            if (priceTags.__len__() > 0):
                branch.Price = htmlReader.CreatePrice(priceTags[0])
        
            if (stockTags.__len__() > 0):
                branch.Stock = stockTags[0].text.replace(" in stock", "")

    autoguiHandler.Close()
    jsonReader.CreateCompanyData(key, company, translator)

jsonReader.CreateXLSX()