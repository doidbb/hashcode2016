#!/usr/bin/env python

import sys

def main():
    hashFile = sys.argv[1]
    hashFile = open(hashFile, 'r+')
    hashLines = hashFile.read().split("\n")
    hashInfo = hashLines[0].split()
    numRows = hashInfo[0]
    numColumns = hashInfo[1]
    dronesAvail = hashInfo[2]
    deadline = hashInfo[3]
    maxLoad = hashInfo[4]
    productTypes = hashLines[1].split()[0]
    productWeights = hashLines[2].split()
    numWarehouses = hashLines[3]
    
    print(maxLoad)

main()
