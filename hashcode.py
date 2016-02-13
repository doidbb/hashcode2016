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
    def loadDrone(newPos, newItem, droneNo, warehouseNo):
        self.dronePos = newPos
        self.droneLoad.append(newItem)
        self.droneUse = True
        return str(droneNo) + "L" + str(warehouseNo) + str(newItem) + "1"
    def deliver(newPos, itemDelivered, droneNo, warehouseNo):
        self.dronePos = newPos
        self.droneLoad.remove(itemDelivered)
        self.droneUse = False
        return str(droneNo) + "D" +  str(warehouseNo) + str(itemDelivered) + "1"
    def moveDrone(newPos):
        self.dronePos = newPos
    def wait(droneNo, turns):
        return str(droneNo) + "W" + str(turns)

class warehouse():
    def __init__(self,warehouseCoord):
        self.warehouseCoord = warehouseCoord
        self.warehouseLoad = []
        self.warehouseQty = []
    #the add* subroutine should be used ONLY when initialising the warehouse
    def addQty(amount):
        warehouseQty.append(amount)
    def changeQty(index,amount):
        warehouseQty[index] = warehouseQty[index] + amount

class order():
    def __init__(self,orderCoord):
        orderCoord = orderCoord
        orderProds = []
    def addToOrder(item):
        orderProds.append(item)
    def itemDelivered(item):
        orderProds.remove(item)

def parseFile():
    hashFile = sys.argv[1]
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

def init(lines):
    numWarehouses = int(lines[3])
    whInfoBegin = 4
    whInfoEnd = numWarehouses * 2
    whInfo = lines[whInfoBegin:whInfoEnd]
    warehouses = initWarehouse(whInfo,int(lines[1]))

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

def initDrones(lines):
    pass

#code for creating order classes goes here
def initOrders(lines, numOrders):
    pass

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
    init(lines)
main()
