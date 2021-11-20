#!/usr/bin/env python3
import sys

if __name__ == '__main__':
    fOpen=open(sys.argv[1], "r")
    fWrite=open(sys.argv[2], "w")
    x=float(input("Please enter number that has to be added to numbers in file: "))
    fOpenLine=fOpen.readline()
    while fOpenLine:
        temp=float(fOpenLine)
        tempLine=str(temp+x) + "\n"
        fWrite.write(tempLine)
        fOpenLine=fOpen.readline()
    print("Done.")
    fOpen.close()
    fWrite.close()

