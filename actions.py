import logging

class Action():
    button = ""
    controller = None
    method = None
    data = None

class SectorViewAction(Action):
    def __init__(self, button_name = ""):
        self.button = button_name
        self.controller = "sector"
        self.method = "view"

class SectorMoveAction(Action):
    def __init__(self, sector):
        self.button = "MOVE " + str(sector)
        self.controller = "sector"
        self.method = "move"
        self.data = { "sector": str(sector) }

class SectorWarpAction(Action):
    def __init__(self, sector):
        self.button = "WARP " + str(sector)
        self.controller = "sector"
        self.method = "warp"
        self.data = { "sector": str(sector) }

class PortViewAction(Action):
    def __init__(self):
        self.controller = "port"
        self.method = "view"

class PortEnterAction(Action):
    def __init__(self):
        self.button = "LAND"
        self.controller = "port"
        self.method = "land"

class PortLeaveAction(Action):
    def __init__(self):
        self.button = "TAKE OFF"
        self.controller = "port"
        self.method = "leave"

class PortBuyAction(Action):
    def __init__(self, commodity):
        self.button = "BUY: " + str(commodity)
        self.controller = "port"
        self.method = "buy"
        self.data = { "commodity": str(commodity) }

class PortSellAction(Action):
    def __init__(self, commodity):
        self.button = "SELL: " + str(commodity)
        self.controller = "port"
        self.method = "sell"
        self.data = { "commodity": str(commodity) }

class ShipBuyAction(Action):
    def __init__(self, ship):
        self.button = "Buy: " + ship.name
        self.controller = "ship"
        self.method = "buy"
        self.data = { "ship": ship }

class ChatViewAction(Action):
    def __init__(self):
        self.button = "View Chat"
        self.controller = "chat"
        self.method = "view"

class ChatPostAction(Action):
    def __init__(self, msg):
        self.controller = "chat"
        self.method = "post"
        self.data = { msg: msg }

class GameQuitAction(Action):
    def __init__(self):
        self.button = "QUIT"
