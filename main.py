import easygui
import random
import yaml
import logging
from classes import *

def load_file(world_name, file_name):
    try:
        full_path = "worlds/" + world_name + "/" + file_name + ".yaml"
        with open(full_path) as file_data:
            return yaml.load(file_data)
    except IOError:
        return None

def save_file(world_name, file_name, obj):
    full_path = "worlds/" + world_name + "/" + file_name + ".yaml"
    with open(full_path, 'w') as file_data:
        yaml.dump(obj, file_data)
        
def load_sectors(world_name):
    return load_file(world_name, "sectors")

def save_sectors(world_name, sectors):
    save_file(world_name, "sectors", sectors)

def load_ports(world_name):
    return load_file(world_name, "ports")

def save_ports(world_name, ports):
    save_file(world_name, "ports", ports)

def generate_sectors():
    sectors = {}
    for id in range(100, 999):
        sectors[id] = Sector(routes = [], warps = [], name = "")
        
    new_pool = list(sectors.keys())
    new_pool.remove(100)
    current_pool = [100]
    
    sector_names = [line.strip() for line in open('data/starnames.txt')]
    
    while len(new_pool) > 0:
        new_id = random.choice(new_pool)
        new_pool.remove(new_id)
        
        current_id = random.choice(current_pool)
        sectors[current_id].routes = sectors[current_id].routes + [new_id]
        sectors[new_id].routes = sectors[new_id].routes + [current_id]
        sector_name = random.choice(sector_names)
        sectors[new_id].name = sector_name
        sector_names.remove(sector_name)
        
        current_pool = current_pool + [new_id]

    # Add 50 warps
    for i in range(0,50):
        from_id = random.choice(list(sectors.keys()))
        to_id = random.choice(list(sectors.keys()))
        
        sectors[from_id].warps += [to_id]

    return sectors        
        
def generate_ports(sectors):
    ports = {}
    places_without_port = list(sectors.keys())

    for i in range(0, 100):
        location = random.choice(places_without_port)
        ports[location] = MiningPort()
        places_without_port.remove(location)
        
    for i in range(0, 100):
        location = random.choice(places_without_port)
        ports[location] = ManufacturingPort()
        places_without_port.remove(location)
        
    for i in range(0, 100):
        location = random.choice(places_without_port)
        ports[location] = FarmingPort()
        places_without_port.remove(location)

    stardock_location = 100
    for location in places_without_port:
        if len(sectors[location].routes) > len(sectors[stardock_location].routes):
            stardock_location = location
    sectors[stardock_location].name = "Star Dock"
    ports[stardock_location] = Stardock()
   
    return ports

def enter_stardock(world, port, player):
    while True:
        msg = ""
        actions = []
        if not isinstance(player.ship, Junk)and player.gold_coins >= Junk.price:
            actions += ["Buy ship: Junk"]     
        if not isinstance(player.ship, Frigate)and player.gold_coins >= Frigate.price:
            actions += ["Buy ship: Frigate"]
        if not isinstance(player.ship, Trireme)and player.gold_coins >= Trireme.price:
            actions += ["Buy ship: Trireme"]
        actions += ["Chat"]
        
        actions += ["Take Off"]
        msg += "You are at the Stardock.  You have a " + str(type(player.ship)) + " ship."

        action = easygui.buttonbox(msg, choices = actions)
        
        verb = action.split(":")[0]

        logging.info("verb: [" + verb + "]")
        if verb == "Buy ship":            
            ship_type = action[10:]
            print("Buying ship " + ship_type)
            if ship_type == "Junk":
                player.ship = Junk()
                player.gold_coins -= Junk.price   
            elif ship_type == "Frigate":
                player.ship = Frigate()
                player.gold_coins -= Frigate.price
            elif ship_type == "Trireme":
                player.ship = Trireme()
                player.gold_coins -= Trireme.price
        if verb == "Take Off":
            
            return
        if verb == "Chat":
            easygui.textbox(title="Chat Log", text=[str(entry) + "\n" for entry in world.chat_log])
            msg = easygui.enterbox("Chat Msg")
            if msg and len(msg) > 0:
                world.chat_log += [ChatEntry(player.name, msg)]

    
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
        actions += ["Take Off"]
        
        msg = "You are in a " + port.type + ".  You have " + str(player.gold_coins) + " coins. You have cargo on board: " + str(cargo) + " " + str(port)
        
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
        elif verb == "Take Off":
            return    
            
def generate_player(location):
    player = Player()
    player.location = location
    player.gold_coins = 100000
    player.ship = Frigate()
    player.ship.resources = { "wheat": 10, "food": 18, "iron": 1000 }
    player.name = "BlackBeard"
    return player

class Action():
    pass

class MoveAction():
    pass

def enter_sector(player, world):
    having_fun = True
    while (having_fun):
        sector = world.sectors[player.location]
        port = world.ports[player.location] if player.location in world.ports else None
        msg = ""
        actions = []
        
        msg += "You are in sector " + str(player.location) + " : " + str(sector.name)
        msg += "  You have " + str(player.ship.moves) + " moves remaining."

        print("In sector " + str(player.location) + " : " + str(sector))
        if (port):
            msg += "  There is a " + port.type + " here."
            actions += ["LAND"]
        if player.ship.moves > 0:
            actions += ["MOVE: " + str(route) for route in sector.routes]
        if player.ship.warp_drive:
            actions += ["WARP: " + str(warp) for warp in sector.warps]
        
        actions += ["QUIT"]
        
        action = easygui.buttonbox(msg, choices = actions)
        logger.info("Perform action: " + str(action))
        
        verb = action.split(":")[0]
        if verb == "WARP":
            player.location = int(action[-3:])
        elif verb == "MOVE":
            player.location = int(action[-3:])
            player.ship.moves -= 1
        elif verb == "LAND":
            if isinstance(port, Stardock):
                enter_stardock(world, port, player)
            else:
                enter_port(port, player)
        elif verb == "QUIT":
            having_fun = False
        
        #if ship.moves==0:
           #easygui.msgbox("You Have Run Out Of Moves.")


def load_world(world_name):
    sectors = load_sectors(world_name)
    if not sectors:
        sectors = generate_sectors()
    ports = load_ports(world_name)
    if not ports:
        ports = generate_ports(sectors)
    stardock_location = [location for location in ports if isinstance(ports[location], Stardock)][0]
    # TODO: Load players
    players = []
    chat_log = []
    
    return World(world_name, sectors, ports, stardock_location, players, chat_log)

def save_world(world):
    save_sectors(world.name, world.sectors)
    save_ports(world.name, world.ports)
   
def play_game(world_name):
    world = load_world(world_name)
    player = generate_player(world.stardock_location)
    enter_sector(player, world)
   # save_world(world)

def configure_logging():
    logger = logging.getLogger("deepspace")
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.info("Logging configured")
    return logger

if __name__ == "__main__":
    logger = configure_logging()
    play_game("default")
