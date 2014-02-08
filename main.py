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
    
class Ship:
    moves= 0
    warp_drive=False
    max_weight=100
    min_weight = 0

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
        
def get_stardock(map):
    stardock_id = 100
    #for id in map.keys():
    #    if len(map[id].routes) > len(map[stardock_id].routes):
    #        stardock_id = id

    #HACK to pick something with warps
    for id in map.keys():
        if len(map[id].warps) > len(map[stardock_id].warps):
            stardock_id = id
            
    return stardock_id

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
        
    return ports
    
def enter_port(port):
    
    while True:
        actions = ["BUY", "SELL", "BEAM UP"]
        msg = str(port)
        
        action = easygui.buttonbox(msg, choices = actions)
        
        if action == "BUY":
            pass
        elif action == "SELL":
            pass
        elif action == "BEAM UP":
            return    
    
def play_game():
    having_fun = True
    map = generate_map()
    ship = Frigate()
    stardock_id = get_stardock(map)
    map[stardock_id].name = "Star Dock"
    current_id = stardock_id
    ports = generate_ports(map)            


    while (having_fun):
        sector = map[current_id]
        port = ports[current_id] if current_id in ports else None
        msg = ""
        actions = []
        
        msg += "You are in sector " + str(current_id) + " : " + str(sector.name)
        msg += "  You have " + str(ship.moves) + " moves remaining."

        print("In sector " + str(current_id) + " : " + str(sector))
        if (port):
            print("There is a port here of type: " + port.type)
            msg += "  There is a " + port.type + " port here."
            actions += ["LAND"]
        if ship.moves > 0:
            actions += ["MOVE: " + str(route) for route in sector.routes]
        if ship.warp_drive:
            actions += ["WARP: " + str(warp) for warp in sector.warps]
        
        actions += ["QUIT"]
        
        action = easygui.buttonbox(msg, choices = actions)
        print("Perform action: " + str(action))
        
        verb = action.split(":")[0]
        if verb == "WARP":
            current_id = int(action[-3:])
        elif verb == "MOVE":
            current_id = int(action[-3:])
            ship.moves = ship.moves -1
        elif verb == "LAND":
            enter_port(port)
        elif verb == "QUIT":
            having_fun = False
        
        #if ship.moves==0:
           #easygui.msgbox("You Have Run Out Of Moves.")
           

if __name__ == "__main__":
    play_game()