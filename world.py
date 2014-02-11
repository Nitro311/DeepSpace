import logging
import random
import yaml
from classes import *

class World:
    def __init__(self, name, sectors, ports, stardock_location, players, chat_log):
        self.name = name
        self.sectors = sectors
        self.ports = ports
        self.stardock_location = stardock_location
        self.players = players
        self.chat_log = chat_log

    def load(world_name):
        sectors = load_sectors(world_name)
        if not sectors:
            sectors = generate_sectors()
        ports = load_ports(world_name)
        if not ports:
            ports = generate_ports(sectors)
        stardock_location = [location for location in ports if isinstance(ports[location], Stardock)][0]
        chat_log = load_chat_log(world_name)
        if not chat_log:
            chat_log = ChatLog()
        # TODO: Load players
        players = []

        return World(world_name, sectors, ports, stardock_location, players, chat_log)

    def save(self):
        save_sectors(self.name, self.sectors)
        save_ports(self.name, self.ports)
        save_chat_log(self.name, self.chat_log)

def load_file(world_name, file_name):
    try:
        full_path = "worlds/" + world_name + "/" + file_name + ".yaml"
        with open(full_path) as file_data:
            logging.info("Loading file " + full_path)
            return yaml.load(file_data)
    except IOError:
        return None

def save_file(world_name, file_name, obj):
    full_path = "worlds/" + world_name + "/" + file_name + ".yaml"
    with open(full_path, 'w') as file_data:
        logging.info("Saving file " + full_path)
        yaml.dump(obj, file_data)

def load_sectors(world_name):
    return load_file(world_name, "sectors")

def save_sectors(world_name, sectors):
    save_file(world_name, "sectors", sectors)

def load_ports(world_name):
    return load_file(world_name, "ports")

def save_ports(world_name, ports):
    save_file(world_name, "ports", ports)

def save_chat_log(world_name, chat_log):
    save_file(world_name, "chat_log", chat_log)

def load_chat_log(world_name):
    return load_file(world_name, "chat_log")

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
