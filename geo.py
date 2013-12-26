from math import radians, cos, sin, asin, sqrt
import csv
from pprint import pprint
import numpy
from scipy.spatial import cKDTree

class geo:

    def __init__(self):

        self.data = []
        self.regions = []

        for row in csv.DictReader(open('postcodes.csv', 'rb'),  ["id","postcode","lat","lng"]):
            self.data.append(row)

        for row in csv.DictReader(open('postcodeareas.csv', 'rU'), ["initial","region"]):
            self.regions.append(row)

        for row in self.data:
            row["area"] = self.postcodeToAreaCode(row["postcode"])
            for r in self.regions:
                if r["initial"] == row["area"]:
                    row["region"] = r["region"]

        self.tree = cKDTree(self.getCordinates())



    def postcodeToAreaCode(self, postcode):
        r = ""
        t = True
        for l in postcode:
            if l.isdigit() == False:
                if t == True:
                    r+=str(l)
            else:
                t = False
        return r

    def getCordinates(self):
        return [[float(record["lat"]),float(record["lng"])] for record in self.data]

    def getPostCodes(self):
        return list(set([record["postcode"] for record in self.data]))

    def getPostCodeRegions(self):
        return list(set([record["area"] for record in self.data]))
        #return self.dataRegion.keys()

    def getRegions(self):
        return list(set([record["region"] for record in self.data]))


    def findNearestPostCode(self, long, lat, k = 2):
        r = []
        dists, indexes = self.tree.query(numpy.array([long , lat]), k)
        if k > 1:
            for dist, index in zip(dists, indexes):
                tmp = self.data[index]
                tmp["distance"] = dist
                r.append(tmp)
        else:
            tmp = self.data[indexes]
            tmp["distance"] = dists
            r.append(tmp)

        return r

    def getPostCodesInArea(self, area):
        tmp = []
        for row in self.data:
            if row["area"] == area:
                tmp.append(row)
        return tmp

    def getPostCodeRegonsInRegon(self, regon):
        tmp = []
        for row in self.data:
            if row["region"] == regon:
                tmp.append(row)
        return tmp


def main():
    g = geo()
    pprint(g.getPostCodesInArea("DN"))
    pprint(g.findNearestPostCode(53.954343, -1.079407, 1));

if __name__ == "__main__":
    main()