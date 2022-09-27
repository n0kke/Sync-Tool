#!/usr/bin/python

import json
import os
import shutil
import time
import sys
import io

# SERVER
class Server:
    'Entity that represents a server'

    def __init__(self, address, serverTypes):
      self._address = address
      self._serverTypes = serverTypes

    def GetAddress(self):
       return self._address

    def isOfType(self, type):
     if type in self._serverTypes:
       return True


# CONFIGURATION
class Configuration:
    'Represents the list of servers'
    
    def __init__(self, filepath):
       self._filepath = filepath
       self._servers = []
       self.readfile()

    def readfile(self): 
        with io.open(self._filepath,'rt', encoding='utf-8') as serversFile: 
			serversFileRead = serversFile.read()
			servers = json.loads(serversFileRead)
			for s in servers:
				server = Server(s['address'], s['serverTypes'])
				self._servers.append(server)
				
			serversFile.close()
# ORDER
class Order: 
    'Order to be executed'
    servers = []
    inputPath = ""
    outputPath = ""

    def __init__(self, servers, inputPath, outputPath):
        self.inputPath = inputPath
        self.outputPath = outputPath
        self.servers = servers

# ORDER SPECIFICATION
class OrderSpecification:
    'Specification of the work to do'

    def __init__(self, filepath):
        self._orders = []
        self._specification = self.readfile(filepath)

    def readfile(self, filepath):
        with io.open(filepath,'rt', encoding='utf-8') as entries:
			ordersRead = entries.read()
			orders = json.loads(ordersRead)
			
			for o in orders:
				order = Order(o['serverName'], o['inputPath'], o['outputPath'])
				self._orders.append(order)
				
			entries.close()

    # PRECISAS DE OBTER A LISTA DE ORDENS A PARTIR DO OBJETO
    def get_orders(self):
        return self._orders

# SYNC HANDLER
class SyncHandler:
    'Handles the syncing of the contents of servers'

    def __init__(self, configuration, orderSpecification):
        self._configuration = configuration
        self._orderSpecification = orderSpecification

    def sync(self, srv_address, input_path, output_path):
        # Logic of execution for rsync
        # rsync srv_address order.inputPath order.outputPath
        command = "rsync -avzh %s %s %s"% (input_path, output_path, srv_address)
        os.system(command)

    def run(self):
        # AQUI, TENS QUE BUSCAR AS ORDENS À LISTA DE ORDENS CONTIDA NA ESPECIFICAÇÃO
        for order in self._orderSpecification.get_orders():
            for serverName in order.servers:
                srv_address = self._configuration.getAddressByName(serverName)
                self.sync(srv_address, order.inputPath, order.outputPath)


# MAIN
def main():
	args_vector =  sys.argv
	configuration = Configuration("cmfsync.config.json")
    # retrieve filepath from python arguments:
    # Example:
    # python cmfsync.py order.json
    # file = args[2] (neeeds to be studied)
	orderSpecification = OrderSpecification(args_vector[1])
    
    # Run the syncing
	handler = SyncHandler(configuration, orderSpecification)
	handler.run()

    
if __name__ == "__main__":
    main()
