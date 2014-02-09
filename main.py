import easygui
import random

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

def generate_map():
    map = {}
    for id in range(100, 999):
        map[id] = Sector(routes = [], warps = [], name = "")
        
    new_pool = map.keys()
    new_pool.remove(100)
    current_pool = [100]
    
    sector_names = [line.strip() for line in open('starnames.txt')]
    
    while len(new_pool) > 0:
        new_id = random.choice(new_pool)
        new_pool.remove(new_id)
        
        current_id = random.choice(current_pool)
        map[current_id].routes = map[current_id].routes + [new_id]
        map[new_id].routes = map[new_id].routes + [current_id]
        sector_name = random.choice(sector_names)
        map[new_id].name = sector_name
        sector_names.remove(sector_name)
        
        current_pool = current_pool + [new_id]

    # Add 50 warps
    for i in range(0,50):
        from_id = random.choice(map.keys())
        to_id = random.choice(map.keys())
        
        map[from_id].warps += [to_id]

    return map        
        
def generate_ports(map):
    ports = {}
    places_without_port = map.keys()
    
    for i in range(0, 100):
        id = random.choice(places_without_port)
        ports[id] = MiningPort()
        places_without_port.remove(id)
        
    for i in range(0, 100):
        id = random.choice(places_without_port)
        ports[id] = ManufacturingPort()
        places_without_port.remove(id)
        
    for i in range(0, 100):
        id = random.choice(places_without_port)
        ports[id] = FarmingPort()
        places_without_port.remove(id)

    stardock_id = 100
    for id in places_without_port:
        if len(map[id].routes) > len(map[stardock_id].routes):
            stardock_id = id
    map[stardock_id].name = "Star Dock"
    ports[stardock_id] = Stardock()
        
    return ports, stardock_id
    
def enter_port(port, player):
    
    cargo = player.ship.resources
    
    while True:
        actions = []

        for commodity in port.buy_prices.keys():
            if commodity in cargo and cargo[commodity] > 0:
                actions += ["SELL: " + commodity + " @" + str(port.buy_prices[commodity])]
        for commodity in port.sell_prices.keys():
            if player.gold_coins >= port.sell_prices[commodity]:
                actions += ["BUY: " + commodity + " @" + str(port.sell_prices[commodity])]
        actions += ["BEAM UP"]
        
        msg = "You are in a " + port.type + " port.  You have " + str(player.gold_coins) + " coins. You have cargo on board: " + str(cargo) + " " + str(port)
        
        action = easygui.buttonbox(msg, choices = actions)
        
        verb = action.split(":")[0]
        
        if verb == "BUY":
            commodity = action.split(" ")[1]
            price = port.sell_prices[commodity]
            player.gold_coins -= price
            if commodity in cargo:
                cargo[commodity] += 1
            else:
                cargo[commodity] = 1
        elif verb == "SELL":
            commodity = action.split(" ")[1]
            price = port.buy_prices[commodity]
            player.gold_coins += price
            cargo[commodity] -= 1
        elif verb == "BEAM UP":
            return    
            
def generate_player(location):
    player = Player()
    player.location = location
    player.gold_coins = 10
    player.ship = Frigate()
    player.ship.resources = { "wheat": 10, "food": 18, "iron": 1000 }
    return player
    
def play_game():
    having_fun = True
    map = generate_map()
    ports, stardock_id = generate_ports(map)
    player = generate_player(stardock_id)
    current_id = player.location
            


    while (having_fun):
        sector = map[current_id]
        port = ports[current_id] if current_id in ports else None
        msg = ""
        actions = []
        
        msg += "You are in sector " + str(current_id) + " : " + str(sector.name)
        msg += "  You have " + str(player.ship.moves) + " moves remaining."

        print("In sector " + str(current_id) + " : " + str(sector))
        if (port):
            print("There is a port here of type: " + port.type)
            msg += "  There is a " + port.type + " port here."
            actions += ["LAND"]
        if player.ship.moves > 0:
            actions += ["MOVE: " + str(route) for route in sector.routes]
        if player.ship.warp_drive:
            actions += ["WARP: " + str(warp) for warp in sector.warps]
        
        actions += ["QUIT"]
        
        action = easygui.buttonbox(msg, choices = actions)
        print("Perform action: " + str(action))
        
        verb = action.split(":")[0]
        if verb == "WARP":
            current_id = int(action[-3:])
        elif verb == "MOVE":
            current_id = int(action[-3:])
            player.ship.moves -= 1
        elif verb == "LAND":
            enter_port(port, player)
        elif verb == "QUIT":
            having_fun = False
        
        #if ship.moves==0:
           #easygui.msgbox("You Have Run Out Of Moves.")
           

if __name__ == "__main__":
    play_game()