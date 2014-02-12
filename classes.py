import logging
from datetime import datetime

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
        return "<sector routes=" + str(self.routes) + " warps=" + str(self.warps) + " name="+self.name +">"

class Player:
    name=""
    gold_coins = 0
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
        return str(self.type) + " resources=" + str(self.resources) + " strength="+ str(self.strength)

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
    total_moves = 0
    warp_drive=False
    capacity=0
    resources = {}
    price =0
    name=""
    def __str__(self):
        return self.name


class Junk(Ship):
    total_moves = 25
    warp_drive = False
    price = 1000
    name="Junk"
    capacity=20

class Frigate(Ship):
    total_moves=50
    warp_drive=False
    price = 10000
    name= "Frigate"
    capacity=50

class Trireme(Ship):
    total_moves = 75
    warp_drive = True
    price = 100000
    name="Trireme"
    capacity=75

class Schooner(Ship):
    total_moves = 100
    warp_drive = True
    price = 1000000
    name="Schooner"
    capacity=100

