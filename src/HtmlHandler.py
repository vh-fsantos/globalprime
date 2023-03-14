from bs4 import BeautifulSoup
import re

class HtmlReader:
    def FindElements(self, data, lookedUpTag, lookedUpPredicate):
        soup = BeautifulSoup(data, 'html5lib')

        if (lookedUpPredicate == ""):
            return soup.find_all(lookedUpTag)

        return soup.find_all(lookedUpTag, lookedUpPredicate)

    def CreatePrice(self, key, tag):
        if key == "menards":
            return tag.attrs['data-final-price'].replace(".", ",")

        spans = self.FindElements(f'<html>{tag}</html>', "span", "")
        
        if key == "lowes":
            return f'{spans[0].text.replace("$", "")},{spans[1].text.replace(".", "")}'

        return f'{spans[1].text},{spans[2].text}'

    def CreateStock(self, key, tag):
        if key == "homedepot":
            if tag.name == "div":
                if tag.text.__contains__("Today"):
                    return tag.text.replace(" in stock", "").replace("Today","")
                else:
                    return "0"
            return tag.text.replace(" in stock", "")
        if key == "lowes":
            spans = self.FindElements(f'<html>{tag}</html>', "span", "")
        else:
            if tag.text.__contains__("Not available"):
                return ""
            spans = self.FindElements(f'<html>{tag}</html>', "span", { "class": "font-weight-bold"})

        if (spans.__len__() > 0):
            if key == "lowes":
                return f'{spans[0].text.replace(" Available", "")}'

            return spans[0].text.replace('\n', '').lstrip().rstrip()


    def GetTags(self, companyKey, price, pageHtml, collection):
        menardsPrice = companyKey == "menards" and price

        for key, value in collection.items():
            tags = self.FindElements(pageHtml, key, { "id" if menardsPrice else "class": value })
            if (tags.__len__() != 0):
                return tags
        return []