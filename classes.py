import logging
from datetime import datetime

class Area():
    #ENUM
    Space, Port, Planet = range(0, 3)

class ChatLog():
    entries = []

    def add(self, entry):
        self.entries += [entry]

    def view(self):
        return self.entries

class ChatEntry:
    def __init__(self, player, msg):
        self.player_name = player.name
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
        return "<sector routes=" + str(self.routes) + " warps=" + str(self.warps) + " name=" + self.name + ">"

class Player:
    name = ""
    gold_coins = 0
    ship = None
    location = 0
    area = Area.Space

class Port:
    type = ""
    resources = {}
    buy_prices = {}
    sell_prices = {}
    strength = 0
    created_resources = {}

    def __str__(self):
        return str(self.type) + " resources=" + str(self.resources) + " strength=" + str(self.strength)

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
    buy_prices = { "food": 30, "iron": 100, "gold": 500, "diamond": 400 }
    sell_prices = { "tools": 10, "engines": 18 }
    strength = 10
    created_resources = { "tools": 100, "engines": 10  }

class FarmingPort(Port):
    type = "Farming Port"
    resources = { "wheat": 10000, "food": 200 }
    buy_prices = {"tools": 100, "engines": 500 }
    sell_prices = { "wheat": 10, "food": 18 }
    strength = 10
    created_resources = { "wheat": 100, "food": 10  }

class Stardock(Port):
    type = "StarDock"
    strength = 10000

class Ship:
    moves = 0
    total_moves = 0
    warp_drive  =False
    capacity = 0
    resources = {}
    price = 0
    name = ""
    defence=0
    attack=0

    def __init__(self):
        self.moves = self.total_moves

    def trade_in_value(self):
        return int(self.price * 0.80)

    def __str__(self):
        return self.name

class Junk(Ship):
    total_moves = 100
    warp_drive = False
    price = 1000
    name = "Junk"
    capacity = 20
    attack=50
    defence=50

class Fighter(Ship):
    total_moves = 95
    warp_drive = False
    price = 1000
    name = "Fighter"
    capacity = 10
    attack=90
    defence=10

class Scout(Ship):
    total_moves = 140
    warp_drive = False
    price = 1000
    name = "Scout"
    capacity = 5
    attack=10
    defence=20

class Destroyer(Ship):
    total_moves =70
    warp_drive = False
    price = 1000
    name = "Destroyer"
    capacity = 30
    attack=120
    defence=20

class Bomber(Ship):
    total_moves = 60
    warp_drive = False
    price = 1000
    name = "Bomber"
    capacity = 50
    attack=140
    defence=10

class Interceptor(Ship):
    total_moves = 120
    warp_drive = True
    price = 1000
    name = "Interceptor"
    capacity = 20
    attack=100
    defence=10

class Stealth_Fighter(Ship):
    total_moves = 95
    warp_drive = True
    price = 1000
    name = "Stealth Fighter"
    capacity = 20
    attack=70
    defence=20

class Assault_Fighter(Ship):
    total_moves = 85
    warp_drive = False
    price = 1000
    name = "Assault Fighter"
    capacity = 15
    attack=110
    defence=5

class Recon(Ship):
    total_moves = 130
    warp_drive = True
    price = 1000
    name = "Recon"
    capacity = 15
    attack=60
    defence=10

class Cutter(Ship):
    total_moves = 120
    warp_drive = False
    price = 1000
    name = "Cutter"
    capacity = 25
    attack=40
    defence=5

class Frigate(Ship):
    total_moves = 70
    warp_drive  =False
    capacity = 30
    price = 0
    name = "Frigate"
    defence=70
    attack=50

class Cruiser(Ship):
    total_moves = 60
    warp_drive  =False
    capacity = 40
    price = 0
    name = "Cruiser"
    defence=80
    attack=60

class Assault_Carrier(Ship):
    total_moves = 70
    warp_drive  =False
    capacity = 20
    price = 0
    name = "Assault Carrier"
    defence=100
    attack=10

class Freighter(Ship):
    total_moves = 35
    warp_drive  = True
    capacity = 100
    price = 0
    name = "Freighter"
    defence=130
    attack=0

class Repurposed_Freighter(Ship):
    total_moves = 35
    warp_drive = True
    capacity = 75
    price = 0
    name = "Repurposed Freighter"
    defence=130
    attack=40

class Blockade_Runner(Ship):
    total_moves = 120
    warp_drive  =True
    capacity = 10
    price = 0
    name = "Blockade Runner"
    defence=70
    attack=30

class Battle_Cruiser(Ship):
    total_moves = 50
    warp_drive  =True
    capacity = 0
    price = 0
    name = "Battle Cruiser"
    defence=100
    attack=70

class Missle_Boat(Ship):
    total_moves = 50
    warp_drive  =True
    capacity = 0
    price = 0
    name = "Missle Boat"
    defence=20
    attack=200

class BattleShip(Ship):
    moves = 40
    total_moves = 0
    warp_drive  =False
    capacity = 0
    price = 0
    name = "BattleShip"
    defence=100
    attack=90




