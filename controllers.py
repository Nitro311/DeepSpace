import easygui
import logging
from actions import *
from classes import *

class ConsoleController():
    def __init__(self, world, player):
        self.world = world
        self.player = player

    def view_result(self, msg, actions):
        index = easygui.indexbox(msg, choices = [action.button for action in actions])
        return actions[index]

    def error_result(self, msg):
        easygui.msgbox(msg, "Oops")
        return SectorViewAction()

class SectorController(ConsoleController):
    def view(self):
        port = self.world.ports[self.player.location] if self.player.location in self.world.ports else None
        sector = self.world.sectors[self.player.location]
        msg = ""
        actions = []

        msg += "You are in sector " + str(self.player.location) + " : " + str(sector.name)
        msg += "  You have " + str(self.player.ship.moves) + " moves remaining."

        logging.info("In sector " + str(self.player.location) + " : " + str(sector))
        if (port):
            msg += "  There is a " + port.type + " here."
            actions += [PortEnterAction()]
        if self.player.ship.moves > 0:
            actions += [SectorMoveAction(location) for location in sector.routes]
        if self.player.ship.warp_drive:
            actions += [SectorWarpAction(location) for location in sector.warps]

        actions += [GameQuitAction()]

        return self.view_result(msg, actions)

    def move(self, location):
        location = int(location)
        if self.player.ship.moves <= 0:
            return self.error_result("Out of moves")
        potential_routes = self.world.sectors[self.player.location].routes
        if location in potential_routes:
            self.player.ship.moves -=1
            self.player.location = location

        return SectorViewAction()

    def warp(self, location):
        location = int(location)
        if self.player.ship.warp_drive == False:
            return self.error_result("Your ship has no warp drive")
        potential_routes = world.sectors[self.player.location].warps
        if location in potential_routes:
            self.player.location = location
            return SectorViewAction()
        else:
            return self.error_result("Can't move there from here")

class ShipController(ConsoleController):
    def buy(self, ship):
        if type(ship) == type(self.player.ship):
            return self.error_result("You already have that type of ship")

        trade_in_value= self.player.ship.trade_in_value()

        if (self.player.gold_coins + trade_in_value < ship.price):
            return self.error_result("You don't have enough to buy this ship")

        # TODO: Make sure the ship is for sale at this location

        remaining_moves = self.player.ship.moves
        possible_moves = self.player.ship.total_moves
        self.player.ship = ship
        self.player.ship.moves = int(ship.total_moves * (remaining_moves / possible_moves))
        self.player.gold_coins = self.player.gold_coins - ship.price + trade_in_value

        return PortViewAction()

class ChatController(ConsoleController):
    def view(self):
        easygui.textbox(title="Chat Log", text=[str(entry) + "\n" for entry in self.world.chat_log.view()])
        msg = easygui.enterbox("Chat Msg")
        if msg and len(msg) > 0:
            return ChatPostAction(msg)
        else:
            return PortViewAction()

    def post(self, msg):
       if msg and len(msg) > 0:
            self.world.chat_log.add(ChatEntry(self.player, msg))
       return PortViewAction()

class PortController(ConsoleController):
    def land(self):
        if not self.player.location in self.world.ports:
            return self.error_result("No port exists here")
        if not self.player.area == Area.Space:
            return self.error_result("You must be in space to land on a port")

        self.player.area = Area.Port

        return PortViewAction()

    def leave(self):
        if not self.player.location in self.world.ports:
            return self.error_result("No port exists here")
        if not self.player.area == Area.Port:
            return self.error_result("You must be on a port to leave it")

        self.player.area = Area.Space

        return SectorViewAction()

    def view(self):
        if not self.player.location in self.world.ports:
            return self.error_result("No port exists here")
        if not self.player.area == Area.Port:
            return self.error_result("You must be on a port to view it")

        port = self.world.ports[self.player.location]
        cargo = self.player.ship.resources

        actions = []
        msg = "You are in a " + port.type + ".  You have " + str(self.player.gold_coins) + " coins. You have cargo on board: " + str(cargo) + " " + str(port)

        for commodity in port.buy_prices.keys():
            if commodity in cargo and cargo[commodity] > 0:
                actions += [PortSellAction(commodity)]
        for commodity in port.sell_prices.keys():
            if self.player.gold_coins >= port.sell_prices[commodity]:
                actions += [PortBuyAction(commodity)]

        if isinstance(port, Stardock):
            msg += "  You have a " + str(self.player.ship) + "."
            ships_for_sale = [Junk(), Frigate(), Trireme(), Schooner()]
            trade_in_value = int(self.player.ship.price * 0.80)
            for ship in ships_for_sale:
                if not isinstance(self.player.ship, type(ship)) and self.player.gold_coins + trade_in_value >= ship.price:
                    actions += [ShipBuyAction(ship)]
            actions += [ChatViewAction()]

        actions += [PortLeaveAction()]

        return self.view_result(msg, actions)

    def buy_commodity(self, commodity):
        #TODO: Make sure this transaction can take place
        port = self.world.ports[self.player.location]
        cargo = self.player.ship.resources
        price = port.sell_prices[commodity]
        self.player.gold_coins -= price
        if commodity in cargo:
            cargo[commodity] += 1
        else:
            cargo[commodity] = 1

        return PortViewAction()

    def sell_commodity(self, commodity):
        #TODO: Make sure this transaction can take place
        port = self.world.ports[self.player.location]
        cargo = self.player.ship.resources
        price = port.buy_prices[commodity]
        self.player.gold_coins += price
        cargo[commodity] -= 1

        return PortViewAction()
