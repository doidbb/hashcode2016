#!/usr/bin/env python

import sys

class drone():
    #dronePos in form "x,y"
    def __init__(self, dronePos,maxLoad,orderAllocated,droneID, hasOrder):
        self.dronePos = dronePos
        self.maxLoad = maxLoad
        self.droneLoad = []
        self.inUse = False
        self.orderAllocated = orderAllocated
        self.hasOrder = hasOrder
        self.droneID = droneID
    #newpos in form "x,y"
    #newload should be a list
    def loadDrone(self, newItem, warehouseNo):
        self.droneLoad.append(newItem)
        return str(self.droneID) + " L " + str(warehouseNo) + " " + str(newItem) + " 1"
    def deliver(self, itemDelivered):
        self.droneLoad.remove(itemDelivered)
        return str(self.droneID) + " D " +  str(self.orderAllocated.orderID) + " " + str(itemDelivered) + " 1"
    def moveDrone(self,newPos):
        self.dronePos = newPos
    def wait(self,droneNo, turns):
        return str(droneNo) + "W" + str(turns)

class warehouse():
    def __init__(self,warehouseCoord,warehouseID):
        self.warehouseCoord = warehouseCoord
        self.warehouseID = warehouseID
        self.warehouseQty = []
    #the add* subroutine should be used ONLY when initialising the warehouse
    def addQty(self,amount):
        self.warehouseQty.append(amount)
    def changeQty(self,index,amount):
        self.warehouseQty[index] = warehouseQty[index] + amount
    def showQty(self):
        return self.warehouseQty
    def showLoc(self):
        return self.warehouseCoord

class order():
    def __init__(self,orderCoord,orderID):
        self.orderCoord = orderCoord
        self.orderProds = []
        self.orderID = orderID
    def addToOrder(self,item):
        self.orderProds.append(item)
    def itemDelivered(self,item):
        self.orderProds.remove(item)
    def showItems(self):
        return self.orderProds
    def showCoord(self):
        return self.orderCoord

def parseFile():
    global hashFilename
    hashFilename = "redundancy.in"#sys.argv[1]
    hashFile = open(hashFilename, 'r+')
    hashLines = hashFile.read().split("\n")
    return hashLines

def initWarehouses(lines, prodTypes):
    warehouses = []
    #create the warehouse with an empty product list
    for i in range(0, len(lines), 2):
        wh = warehouse(lines[i],i//2,)
        for item in lines[i+1].split():
            wh.addQty(eval(item))
        warehouses.append(wh)
    return warehouses

def initDrones(numDronesp, maxLoadp, whCoordp,orders):
    drones = []
    ordIndex = 0
    for dr in range(numDronesp):
        if ordIndex < len(orders):
            newDrone = drone(whCoordp,maxLoadp,orders[ordIndex],ordIndex, True)
            orders.remove(orders[ordIndex])
        else:
            newDrone = drone(whCoordp,maxLoadp,"none",ordIndex, False)
        ordIndex += 1
        drones.append(newDrone)
        
    return drones,orders

#code for creating order classes goes here
def initOrders(lines, numOrders):
    orders = []
    for i in range(0, len(lines), 3):
        ord = order(lines[i],i//3)
        for item in lines[i+2].split():
            ord.addToOrder(eval(item))
        orders.append(ord)
    return orders
            
def initObjs(lines):
    outfile = hashFilename[:-3]
    commands = open(outfile,"w+")
    numWarehouses = int(lines[3])
    prodWeights = list(map(int,lines[2].split()))
    whInfoBegin = 4
    whInfoEnd = (numWarehouses * 2) + 4
    whInfo = lines[whInfoBegin:whInfoEnd]
    warehouses = initWarehouses(whInfo,int(lines[1]))
    firstWh = whInfo[0]
    orderBegin = whInfoEnd + 1
    orderEnd = len(lines) - 1
    orderList = lines[orderBegin:orderEnd]
    orders = initOrders(orderList,orderEnd)
    numOrders = lines[whInfoEnd]
    numDrones = eval(lines[0].split()[2])
    maxLoad = eval(lines[0].split()[4])
    drones, orders = initDrones(numDrones, maxLoad, firstWh, orders)
    ordersMade = 0
    while len(orders) > 0:
        #deliver everything that the drones have been given
        deliver(drones,orders,warehouses,prodWeights,commands)
        #give them more orders!
        drones, orders = initDrones(numDrones, maxLoad, firstWh, orders)

        

def deliver(dronesp,ordersp,warehousesp,prodWeightsp,outfile):
    for dr in dronesp:
        if dr.hasOrder:
            droneFill(dr,warehousesp,prodWeightsp,outfile)


def droneFill(dronep,whsp,weightsp,outfile):
    #create a list of closest warehouses to the order
    distances = ([],[])
    for wh in whsp:
        distances[0].append(shortestDistance(wh.warehouseCoord,dronep.orderAllocated.orderCoord))
        distances[1].append(wh.warehouseID)
    #cheeky insertion sort
    for i in range(1,len(distances[0])):
        j = i
        while j > 0 and distances[0][j] < distances[0][j-1]:
            distances[0][j], distances[0][j-1] = distances[0][j-1], distances[0][j]
            distances[1][j], distances[1][j-1] = distances[1][j-1], distances[1][j]
            j -= 1
    #start filling
    totalLoad = 0
    for item in dronep.orderAllocated.orderProds:
        for wh in distances[1]:
            itm = whsp[wh].warehouseQty[item]
            itemWeight = weightsp[item]
            if itm > 0 and totalLoad < dronep.maxLoad:
                print(dronep.loadDrone(itm,wh), file=outfile)
                totalLoad += itemWeight
                whsp[wh].warehouseQty[item] = whsp[wh].warehouseQty[item] - 1
    #start delivering
    for item in dronep.droneLoad:
        print(dronep.deliver(item), file=outfile)
        #dronep.droneLoad.remove(item)
    #add one to the orders made

def hasItems(orderp,whp):
    for item in orderp.showItems():
        if item not in whp.showQty():
            #terminates the function early and returns false
            return False
    #else it will return true
    return True

def shortestDistance(loc1,loc2):
    loc1 = str(loc1).split()
    loc2 = str(loc2).split()
    xSq = (eval(loc1[0]) - eval(loc2[0])) ** 2
    ySq = (eval(loc1[1]) - eval(loc2[1])) ** 2
    distance = (xSq + ySq) ** 0.5
    return distance

def main():
    lines = parseFile()
    initObjs(lines)
main()
