#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Vector:

    def __init__(self, coordinatelist):
        self.coordinatelist = coordinatelist

    def addVector(self, anothervector):
        if anothervector.dimension() > self.dimension():
            listmax = anothervector.showList()
            listmin = self.coordinatelist
        else:
            listmin = anothervector.showList()
            listmax = self.coordinatelist
        for i in xrange(len(listmin)):
            listmax[i] += listmin[i]
        self.coordinatelist = listmax

    def dimension(self):
        return(len(self.coordinatelist))

    def multiplyScalarly(self, anothervector):
        if anothervector.dimension() > self.dimension():
            listmax = anothervector.showList()
            listmin = self.coordinatelist
        else:
            listmin = anothervector.showList()
            listmax = self.coordinatelist
        result = 0
        for i in xrange(len(listmin)):
            result += (listmin[i] * listmax[i])
        return(result)

    def showList(self):
        return(self.coordinatelist)

    def multiplyByValue(self, value):
        for i in xrange(len(self.coordinatelist)):
            self.coordinatelist[i] *= value

    def printMe(self):
        print(self.coordinatelist)

v1 = Vector([1, 2, 7])
v2 = Vector([3, 5, 0])

ms = v1.multiplyScalarly(v2)
print(ms)

v1.multiplyByValue(3)
v1.printMe()

v2.addVector(v1)
v2.printMe()
