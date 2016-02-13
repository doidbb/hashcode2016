#!/usr/bin/env python

import sys

class drone():
    #dronePos in form "x,y"
    def __init__(self, dronePos, droneLoad, droneUse):
        self.dronePos = dronePos
        self.droneLoad = []
        self.droneUse = False
    #newpos in form "x,y"
    #newload should be a list
    def loadDrone(newPos, newItem, droneNo, warehouseNo):
        self.dronePos = newPos
        self.droneLoad.append(newItem)
        self.droneUse = True
        return str(droneNo) + "L" + str(warehouseNo) + str(newItem) + "1"
        

def parse():
    hashFile = sys.argv[1]
    hashFile = open(hashFile, 'r+')
    hashLines = hashFile.read().split("\n")
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

def drone():
    #0 is location
    #1 is items
    #2 weight
    droneAttrs = ([],[],[])
    #0 means unused, 1 means in use
    droneIndex = 0
    dronesUnused = []
    ordersMade = 0
    for i in range(dronesAvail):
        dronesUnused.append(0)
        droneAttrs[0].append("0 0")
        droneAttrs[1].append([])
        droneAttrs[2].append(0)
    while (ordersMade != numOrders):
        droneNum = 0
        for drone in droneAttrs[0]:
            if drone == "0 0":
            #we get the drone index
                for i in range(len(dronesUnused)):
                    if drone == 0:
                        droneIndex = i
                        if droneAttrs[0][i] == 0:
                            #we assume it's in it's the default depo
                            droneAttrs[0][i] = warehouseLoc[0]
                #we get the index of the warehouse
                warehouseIndex = 0
                for i in range(len(warehouseLoc)):
                    if warehouseLoc[i] == droneAttrs[1][droneIndex]:
                        warehouseIndex = i
                droneItems = []
                droneMass = 0
                full = False
                while (not full):
                    for i in range(len(warehouseIndex)):
                        print(i)
                        itemWeight = productWeights[i]
                        if warehouseQty[warehouseIndex][i] != 0:
                            ordered = False
                            for item in productTypes:
                                print(item)
                                for orderItem in orderItems:
                                    print(orderItem)
                                    if item in orderItem.split():
                                        ordered = True
                                        droneAttrs[1][droneIndex].append(item)
                                        fileForWriting.write(str(droneIndex) + " L " + str(i) + item + " 1 ")
                            if (eval(itemWeight) < droneMass) and ordered:
                                droneAttrs[2][droneIndex] += itemWeight
                                droneItems.append(productTypes[i])
                                #decrease qty
                                warehouseQty[warehouseIndex][i] = warehouseQty - 1
                            else:
                                full = True
                droneAttrs[1][droneIndex] = droneItems
            oldDist = 9999999999
            for j in range(len(orderLoc)):

                nextDist = shortestDistance(orderLoc[j],droneAttrs[0][droneIndex])
                #once the next closest thing is found, we need to see if that place has items that the drone holds
                thisItems = orderItems[j]
                hasItems = False
                for item in droneAttrs[1]:
                    if item in orderItems[j].split():
                        hasItems = True
                if nextDist < oldDist or hasItems:
                    oldDist = nextDist
                    orderIndex = j
            #make delivery
            droneAttrs[0][droneIndex] = orderLoc[orderIndex]
            for item in droneAttrs[1][droneIndex]:
                if item in orderItems[j].split():
                    droneAttrs[1][droneIndex].remove(item)
            ordersMade += 1
            #go to next warehouse
            oldWareDist = 999999999
            for a in range(len(warehouseLoc)):
                newnextDist = shortestDistance(warehouseLoc[a],droneAttrs[0][droneIndex])
                if newnextDist < oldWareDist:
                    oldWareDist = newnextDist
                    newloc = a
            droneAttrs[0][droneIndex] = warehouseLoc[a]
            #the while loop should repeat
def shortestDistance(loc1,loc2):
    loc1 = str(loc1).split()
    loc2 = str(loc2).split()
    xSq = (eval(loc1[0]) - eval(loc2[0])) ** 2
    ySq = (eval(loc1[1]) - eval(loc2[1])) ** 2
    pythag = (xSq + ySq) ** 0.5
    return pythag

def main():
    parse()

main()
