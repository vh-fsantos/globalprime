class Branch:
    def __init__(self, data):
        self.Id = data['branchid']
        self.Price = "0"
        self.Stock = "0"

class StateBranch:
    def __init__(self, stateBranchObj):
        self.State = stateBranchObj['state']
        self.Branches = []
        for obj in stateBranchObj['branches']:
            self.Branches.append(Branch(obj))

class Company:
    def __init__(self, data):
        self.PointChangeStore = data["pointChangeStore"]
        self.PointFindOthers = data["pointFindOthers"]
        self.PointLabel = data["pointLabel"]
        self.PointSelectStore = data["pointSelectStore"]
        self.PriceTags = data["priceTags"]
        self.HasStockTags = data["hasStockTags"]
        self.StockTags = data["stockTags"]
        self.IdsIncreaseY = data["idsIncreaseY"]
        self.StateBranches = []
        for obj in data["stateBranches"]:
            self.StateBranches.append(StateBranch(obj))  
        