class World:
    def __init__(self, name, sectors, ports, stardock_location, players):
        self.name = name
        self.sectors = sectors
        self.ports = ports
        self.stardock_location = stardock_location
        self.players = players

class Sector:
    def __init__(self, warps, routes, name):
        self.warps = warps
        self.routes = routes
        self.name = name

    def __str__(self):
        return "<sector routes=" + str(self.routes) + " warps=" + str(self.warps) + " name="+self.name +">"

class Player:
    name=""
    gold_coins=0
    ship = None
    location = 0
    
class Port:
    type=""
    resources = {}
    buy_prices = {}
    sell_prices = {}
    strength= 0
    created_resources = {}

    def __str__(self):
        return "<port type=" + str(self.type) + " resources=" + str(self.resources) + " strength="+ str(self.strength) +">"

class MiningPort(Port):
    type = "mining"
    resources = { "ore": 10000, "iron": 500, "gold": 100, "diamond": 25 }
    buy_prices = { "food": 20, "tools": 100 }
    sell_prices = { "ore": 10, "iron": 18, "gold": 100, "diamond": 300 }
    strength = 10
    created_resources = { "ore": 100, "iron": 10, "gold": 5, "diamond": 1 }

class ManufacturingPort(Port):
    type = "manufacturing"
    resources = { "tools": 10000, "engines": 200 }
    buy_prices = { "food": 30, "iron": 100, "gold": 500, "diamond":400 }
    sell_prices = { "tools": 10, "engines": 18 }
    strength = 10
    created_resources = { "tools": 100, "engines": 10  }
    
class FarmingPort(Port):
    type = "farming"
    resources = { "wheat": 10000, "food": 200 }
    buy_prices = {"tools": 100, "engines":500 }
    sell_prices = { "wheat": 10, "food": 18 }
    strength = 10
    created_resources = { "wheat": 100, "food": 10  }

class Stardock(Port):
    strength = 10000
    

class Ship:
    moves= 0
    warp_drive=False
    max_weight=100
    min_weight = 0
    resources = {}

class Junk(Ship):
    moves = 3
    warp_drive = False
    
class Frigate(Ship):
    moves=50
    warp_drive=False

class Trireme(Ship):
    moves = 75
    warp_drive = True
