from datetime import datetime

class World:
    def __init__(self, name, sectors, ports, stardock_location, players, chat_log):
        self.name = name
        self.sectors = sectors
        self.ports = ports
        self.stardock_location = stardock_location
        self.players = players
        self.chat_log = chat_log
        
class ChatEntry:
    def __init__(self, player_name, msg):
        self.player_name = player_name
        self.msg = msg
        self.date = datetime.now()
    def __str__(self):
        return "[" + self.player_name + "] " + self.date.strftime("%a %I:%M%p") + " " + self.msg

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
    type = "Mining Port"
    resources = { "ore": 10000, "iron": 500, "gold": 100, "diamond": 25 }
    buy_prices = { "food": 20, "tools": 100 }
    sell_prices = { "ore": 10, "iron": 18, "gold": 100, "diamond": 300 }
    strength = 10
    created_resources = { "ore": 100, "iron": 10, "gold": 5, "diamond": 1 }

class ManufacturingPort(Port):
    type = "Manufacturing Port"
    resources = { "tools": 10000, "engines": 200 }
    buy_prices = { "food": 30, "iron": 100, "gold": 500, "diamond":400 }
    sell_prices = { "tools": 10, "engines": 18 }
    strength = 10
    created_resources = { "tools": 100, "engines": 10  }
    
class FarmingPort(Port):
    type = "Farming Port"
    resources = { "wheat": 10000, "food": 200 }
    buy_prices = {"tools": 100, "engines":500 }
    sell_prices = { "wheat": 10, "food": 18 }
    strength = 10
    created_resources = { "wheat": 100, "food": 10  }

class Stardock(Port):
    type = "StarDock"
    strength = 10000
    

class Ship:
    moves= 0
    warp_drive=False
    max_weight=100
    min_weight = 0
    resources = {}
    price =0

class Junk(Ship):
    moves = 25
    warp_drive = False
    price = 1000
    
class Frigate(Ship):
    moves=50
    warp_drive=False
    price = 10000

class Trireme(Ship):
    moves = 75
    warp_drive = True
    price = 100000

