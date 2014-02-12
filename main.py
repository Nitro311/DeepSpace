import easygui
import random
import yaml
import logging
from classes import *
from controllers import *
from world import World

def enter_stardock(world, port, player):
    while True:
        msg = ""
        actions = []
        ships_for_sale = [Junk(), Frigate(), Trireme(), Schooner()]
        trade_in_value = int(player.ship.price*.8)
        for ship in ships_for_sale:
            if not isinstance(player.ship, type(ship))and player.gold_coins+trade_in_value >= ship.price:
                actions += ["Buy: " + ship.name]

        actions += ["Chat"]

        actions += ["Take Off"]
        msg += "You are at the Stardock.  You have a " + str(player.ship) + "."

        action = easygui.buttonbox(msg, choices = actions)

        verb = action.split(":")[0]

        logging.info("verb: [" + verb + "]")

        if verb == "Buy":
            ship_type = action[5:]
            for ship in ships_for_sale:
                if ship_type == ship.name and player.gold_coins+trade_in_value >= ship.price:
                    remaining_moves = player.ship.moves
                    possible_moves = player.ship.total_moves
                    player.ship = ship
                    player.ship.moves = int(ship.total_moves * (remaining_moves / possible_moves))
                    player.gold_coins -= ship.price
                    player.gold_coins +=trade_in_value
        if verb == "Take Off":
            return
        if verb == "Chat":
            easygui.textbox(title="Chat Log", text=[str(entry) + "\n" for entry in world.chat_log.view()])
            msg = easygui.enterbox("Chat Msg")
            if msg and len(msg) > 0:
                world.chat_log.add(ChatEntry(player, msg))
        print (player.gold_coins)

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

def main_loop(world, player):
    while True:
        controller = SectorController()
        sector = world.sectors[player.location]
        msg, actions = controller.view(sector, world, player)

        action = easygui.buttonbox(msg, choices = actions)
        logging.info("Perform action: " + str(action))

        verb = action.split(":")[0]
        if verb == "WARP":
            controller = PlayerController()
            controller.warp(int(action[-3:]))
        elif verb == "MOVE":
            controller = PlayerController()
            controller.move_to(player, world, int(action[-3:]))
        elif verb == "LAND":
            port = world.ports[player.location]
            if isinstance(port, Stardock):
                enter_stardock(world, port, player)
            else:
                enter_port(port, player)
        elif verb == "QUIT":
            return

def configure_logging():
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Logging configured")

if __name__ == "__main__":
    configure_logging()
    world = World.load("default")
    player = Player()
    player.location = world.stardock_location
    player.gold_coins = 9200
    player.ship = Junk()
    player.ship.moves = player.ship.total_moves
    player.ship.resources = { "wheat": 10, "food": 18, "iron": 1000 }
    player.name = "BlackBeard"
    main_loop(world, player)
    world.save()
