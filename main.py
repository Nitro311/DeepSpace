import easygui
import random
import yaml
import logging
from classes import *
from controllers import *
from actions import *
from world import World

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

def choose_player(world):
    players = [p.name for p in world.players] + ["Guest", "New"]
    player = None

    index = easygui.indexbox(msg="Pick Player", choices=players)
    if index < len(world.players):
        return world.players[index]

    fieldnames = ["Name", "Coins"]
    fieldvalues = ["BlackBeard " + str(random.randrange(1, 1000)), 9200]
    results = easygui.multenterbox(msg="Customize your player", title="Guest Player", fields=fieldnames, values=fieldvalues)

    player = Player()
    player.location = world.stardock_location
    player.area = Area.Space
    player.gold_coins = int(results[1])
    player.ship = Junk()
    player.ship.moves = player.ship.total_moves
    player.ship.resources = { "wheat": 10, "food": 18, "iron": 1000 }
    player.name = results[0]

    if index == len(players) - 1:
        world.players += [player]

    return player

if __name__ == "__main__":
    configure_logging()
    world = World.load("default")
    player = choose_player(world)
    action = SectorViewAction()
    while not isinstance(action, GameQuitAction):
        action = route(world, player, action)
    world.save()
