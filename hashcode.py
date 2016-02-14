#!/usr/bin/env python

import sys

class drone():
    #dronePos in form "x,y"
    def __init__(self, dronePos, maxLoad):
        self.dronePos = dronePos
        self.madLoad = maxLoad
        self.droneLoad = []
        self.droneUse = False
    #newpos in form "x,y"
    #newload should be a list
    def loadDrone(self,newPos, newItem, droneNo, warehouseNo):
        self.dronePos = newPos
        self.droneLoad.append(newItem)
        self.droneUse = True
        return str(droneNo) + "L" + str(warehouseNo) + str(newItem) + "1"
    def deliver(self,newPos, itemDelivered, droneNo, warehouseNo):
        self.dronePos = newPos
        self.droneLoad.remove(itemDelivered)
        self.droneUse = False
        return str(droneNo) + "D" +  str(warehouseNo) + str(itemDelivered) + "1"
    def moveDrone(self,newPos):
        self.dronePos = newPos
    def wait(self,droneNo, turns):
        return str(droneNo) + "W" + str(turns)

class warehouse():
    def __init__(self,warehouseCoord):
        self.warehouseCoord = warehouseCoord
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
    def __init__(self,orderCoord):
        self.orderCoord = orderCoord
        self.orderProds = []
    def addToOrder(self,item):
        self.orderProds.append(item)
    def itemDelivered(self,item):
        self.orderProds.remove(item)
    def showItems(self):
        return self.orderProds
    def showCoord(self):
        return self.orderCoord

def parseFile():
    hashFile = "busy_day.in"#sys.argv[1]
    hashFile = open(hashFile, 'r+')
    hashLines = hashFile.read().split("\n")
    return hashLines
def nulll():
    hashInfo = hashLines[0].split()
    numRows = int(hashInfo[0])
    numColumns = int(hashInfo[1])
    dronesAvail = int(hashInfo[2])
    deadline = int(hashInfo[3])
    maxLoad = int(hashInfo[4])
    productTypes = hashLines[1].split()[0]
    productWeights = hashLines[2].split()
    numWarehouses = int(hashLines[3])
    warehouseLoc = []
    warehouseQty = []

    for i in range(5, (numWarehouses *2) + 4,2 ):
        warehouseLoc.append(hashLines[i])
        warehouseQty.append(hashLines[i+1].split())
    for item in warehouseQty:
        for otheritem in item:
            otheritem = eval(otheritem)

    numOrders = eval(hashLines[4+(numWarehouses * 2)])

    orderLoc = []
    orderQty = []
    orderItems = []
    fileForWriting = open("commands", "w+")
    for i in range(5+(numWarehouses * 2),(numOrders * 3) + (5 + (numWarehouses * 2)),3):
        orderLoc.append(hashLines[i])
        orderQty.append(hashLines[i+1])
        orderItems.append(hashLines[i+2])

def initObjs(lines):
    numWarehouses = int(lines[3])
    whInfoBegin = 4
    whInfoEnd = (numWarehouses * 2) + 4
    whInfo = lines[whInfoBegin:whInfoEnd]
    warehouses = initWarehouses(whInfo,int(lines[1]))
    firstWh = whInfo[0]
    numDrones = eval(lines[0].split()[2])
    maxLoad = eval(lines[0].split()[4])
    drones = initDrones(numDrones, maxLoad, firstWh)
    orderBegin = whInfoEnd + 1
    orderEnd = len(lines) - 1
    orderList = lines[orderBegin:orderEnd]
    orders = initOrders(orderList,orderEnd)

#code for creating warehouses goes here
def initWarehouses(lines, prodTypes):
    warehouses = []
    #create the warehouse with an empty product list
    for i in range(0, len(lines), 2):
        wh = warehouse(lines[i])
        for item in lines[i+1].split():
            wh.addQty(item)
        warehouses.append(wh)
    return warehouses

def initDrones(numDronesp, maxLoadp, whCoordp):
    drones = []
    for dr in range(numDronesp):
        newDrone = drone(whCoordp,maxLoadp)
        drones.append(newDrone)
    return drones

#code for creating order classes goes here
def initOrders(lines, numOrders):
    orders = []
    for i in range(0, len(lines), 3):
        ord = order(lines[i])
        for item in lines[i+2].split():
            ord.addToOrder(item)
        orders.append(ord)
    return orders

#code for making deliveries goes here
def droneDelivery():
    pass
    #should make sure that when picking up, the item exists in an order

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
