#!/usr/bin/env python3

import sys

def outputFormatPrint(ordersNumber, maxOrderName, maxOrderSize, ordersDatabase, where):
    print(f"Number of orders: {ordersNumber}.", file=where)
    print(f"The hungriest person today was { maxOrderName.strip()}!", file=where)
    print(f"The largest order size was {maxOrderSize}.", file=where)
    print(f"Item totals: ", file=where)
    for item in ordersDatabase:
            print(f"   {item}  {ordersDatabase[item]}", file=where)
    return

def main():
    fOpen=open(sys.argv[1], "r")
    print(f"Proccesing {sys.argv[1]}")
    fWrite=open("orders_report.txt", "w")                       
    
    ordersNumber=0                                                                    
    maxOrderName=""
    maxOrderSize=0
    ordersDatabase={}
    

    fOpenLine=fOpen.readline()                                                        
    tempOrderPerson=fOpenLine                                                         


    while fOpenLine:
        currentOrderSize=int(fOpen.readline())
        tempOrderSize=0
    
        for i in range(currentOrderSize):
            tempLine=fOpen.readline().strip().split(": ")
            ordersDatabase[tempLine[0]]=ordersDatabase.setdefault(tempLine[0],0)+float(tempLine[1])
            tempOrderSize=tempOrderSize+float(tempLine[1])

        if tempOrderSize>maxOrderSize:
            maxOrderSize=tempOrderSize
            maxOrderName=tempOrderPerson
            
         
        tempOrderPerson=fOpen.readline()
        ordersNumber+=1
        fOpenLine=tempOrderPerson
    outputFormatPrint(ordersNumber, maxOrderName, maxOrderSize, ordersDatabase, fWrite)
    outputFormatPrint(ordersNumber, maxOrderName, maxOrderSize, ordersDatabase, sys.stdout)
    fOpen.close()
    fWrite.close()

main()


    

