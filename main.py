import easygui
import random
#name= easygui.buttonbox("What is Your Name?", choices =['Whatever','IDC','IDK'])

class Sector:
    warps = []
    routes = []
    name=""

    def __init__(self, warps = [], routes = [], name=""):
        self.warps = warps
        self.routes = routes
        self.name = name

    def __str__(self):
        return "<sector routes=" + str(self.routes) + " warps=" + str(self.warps) + " name="+self.name +">"
class Ship:
    moves= 0
    warp_drive=False
    

class Junk(Ship):
    moves = 3
    warp_drive = False
    
class Frigate(Ship):
    moves=50
    warp_drive=False
    

def generate_map_old():
    map = { 100: Sector(routes = [], name = "Star Dock") }

    min_spokes = 3
    max_spokes = 9
    
    names = ["Sohiri", "Ufrarth", "Wuaria", "Uplerth", "Wieeclite", "Egslorth", "Doaatania", "Oswxoth", "Ceypauturn", "Obestion"]
        
    spokes = random.randint(min_spokes, max_spokes)
    
    for id in range(2, spokes):
        name = random.choice(names)
        #names.remove(name)
        
        routes = [100]
        
        map[100 * id] = Sector(routes = routes, name = name)
        print("Created sector " + str(100 * id) + " - " + str(map[100 * id]))
    #    100: Sector(routes = [200,300,400], name = "Star Dock"), 
    #    200: Sector(routes = [100]), 
    #    300: Sector(routes = [100,301,302], warps=[400]), 
    #    301: Sector(routes = [300]), 
    #    302: Sector(routes = [300]), 
    #    400: Sector(routes = [100]) }

    map[100].routes = map.keys()
    map[100].routes.remove(100)
    
    
    print("Spokes are complete")
    main_sectors = map[100].routes
    completed_sectors = []
    
    for main_sector_id in main_sectors:
        spokes = random.randint(min_spokes, max_spokes)
        for id in range(2, spokes):
            name = random.choice(names)
            #names.remove(name)
            
            routes = [main_sector_id]
            map[main_sector_id + id] = Sector(routes = routes, name = name)
            print("Created sector " + str(main_sector_id + id) + " - " + str(map[main_sector_id + id]))
            
    return map


def generate_map():
    map = {}
    for id in range(100, 999):
        map[id] = Sector()
        
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
        
    return map        
        


having_fun = True
map = generate_map()
ship= Frigate()
current_id = 100
for id in map.keys():
    if len(map[id].routes) > len(map[current_id].routes):
        current_id = id
        
map[current_id].name = "Star Dock"

while (having_fun and ship.moves > 0):
    sector = map[current_id]
    msg = "You are in sector " + str(current_id) + " : " + str(sector.name)
    msg = msg + "   Where do you want to move?"
    choices = sector.routes
    if ship.warp_drive:
        choices = choices + sector.warps
        
    move_to = easygui.buttonbox(msg, choices = choices)
    print("Move you to " + str(move_to))
    current_id= move_to
    
    ship.moves=ship.moves -1
    
    
    #if (easygui.buttonbox("Are you still having fun?", choices = ["Yes", "No"]) == "No"):
        #having_fun = False
    
raw_input()    