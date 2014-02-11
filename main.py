import easygui
import random
import yaml
import logging
from classes import *
from world import World

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
        msg += "You are at the Stardock.  You have a " + str(player.ship) + "."

        action = easygui.buttonbox(msg, choices = actions)

        verb = action.split(":")[0]

        logging.info("verb: [" + verb + "]")
        if verb == "Buy ship":
            ship_type = action[10:]
            logging.info("Buying ship " + ship_type)
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

        logging.info("In sector " + str(player.location) + " : " + str(sector))
        if (port):
            msg += "  There is a " + port.type + " here."
            actions += ["LAND"]
        if player.ship.moves > 0:
            actions += ["MOVE: " + str(route) for route in sector.routes]
        if player.ship.warp_drive:
            actions += ["WARP: " + str(warp) for warp in sector.warps]

        actions += ["QUIT"]

        action = easygui.buttonbox(msg, choices = actions)
        logging.info("Perform action: " + str(action))

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




def play_game(world_name):
    world = World.load(world_name)
    player = Player()
    player.location = world.stardock_location
    player.gold_coins = 100000
    player.ship = Frigate()
    player.ship.resources = { "wheat": 10, "food": 18, "iron": 1000 }
    player.name = "BlackBeard"
    enter_sector(player, world)
    world.save()

def configure_logging():
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Logging configured")

if __name__ == "__main__":
    configure_logging()
    play_game("default")
