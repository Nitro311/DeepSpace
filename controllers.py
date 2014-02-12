import logging

class SectorController():
    def view(self, sector, world, player):
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

        return msg, actions

class PlayerController():
    def move_to(self, player, world, location):
        if player.ship.moves <= 0:
            return
        potential_routes = world.sectors[player.location].routes
        if location in potential_routes:
            player.ship.moves -=1
            player.location = location

    def warp(self, player, world, location):
        if player.ship.warp_drive == False:
            return
        potential_routes = world.sectors[player.location].warps
        if location in potential_routes:
            player.location = location
