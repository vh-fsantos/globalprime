from bs4 import BeautifulSoup

class HtmlReader:
    def FindElements(self, data, lookedUpTag, lookedUpPredicate):
        soup = BeautifulSoup(data, 'html5lib')

        if (lookedUpPredicate == ""):
            return soup.find_all(lookedUpTag)

        return soup.find_all(lookedUpTag, lookedUpPredicate)

    def CreatePrice(self, tag):
        spans = self.FindElements(f'<html>{tag}</html>', "span", "")
        return f'{spans[1].text},{spans[2].text}'

    def CreateStock(self, tag):
        spans = self.FindElements(f'<html{tag}</html>', "span", { "class": "alert-inline__message"})
        if (spans.count() > 0):
            return f'{spans[0].text}'.replace(" in stock", "")

    def GetTags(self, pageHtml, collection):
        for key, value in collection.items():
            tags = self.FindElements(pageHtml, key, { "class": value })
            if (tags != ""):
                return tags
        return []