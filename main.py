import random
import yaml
import logging
from classes import *
from controllers import *
from actions import *
from world import World

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
            if world.stardock_location == player.location:
                controller = StardockController()
                controller.view(world, player)
            else:
                port = world.ports[player.location]
                enter_port(port, player)
        elif verb == "QUIT":
            return

def route(world, player, action):
    if not action:
        raise Exception("Controller method did not return an Action")
    if not isinstance(action, Action):
        raise Exception("Action not valid" + str(type(action)))

    if action.controller == "sector":
        controller = SectorController(world, player)
        if action.method == "view":
            return controller.view()
        elif action.method == "move":
            return controller.move(action.data["sector"])
        elif action.method == "warp":
            return controller.warp(action.data["sector"])
    elif action.controller == "port":
        controller = PortController(world, player)
        if action.method == "view":
            return controller.view()
        elif action.method == "land":
            return controller.land()
        elif action.method == "leave":
            return controller.leave()
        elif action.method == "buy":
            return controller.buy_commodity(action.data["commodity"])
        elif action.method == "sell":
            return controller.sell_commodity(action.data["commodity"])
    elif action.controller == "ship":
        controller = ShipController(world, player)
        if action.method == "buy":
            return controller.buy(action.data["ship"])

    # TODO: Finish rest of routes

    raise Exception("Could not route action: " + str(type(action)))

def configure_logging():
    logging.basicConfig(level=logging.DEBUG)
    logging.info("Logging configured")

if __name__ == "__main__":
    configure_logging()
    world = World.load("default")
    player = Player()
    player.location = world.stardock_location
    player.area = Area.Space
    player.gold_coins = 9200
    player.ship = Junk()
    player.ship.moves = player.ship.total_moves
    player.ship.resources = { "wheat": 10, "food": 18, "iron": 1000 }
    player.name = "BlackBeard"
    action = SectorViewAction()
    while not isinstance(action, GameQuitAction):
        action = route(world, player, action)
    world.save()
