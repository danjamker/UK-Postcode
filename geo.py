import csv
from pprint import pprint
import numpy
from scipy.spatial import cKDTree

class Geo:

    def __init__(self):

        self.data = []
        self.regions = []

        for row in csv.DictReader(open('postcodes.csv', 'rb'), ["id", "postcode", "lat", "lng"]):
            self.data.append(row)

        for row in csv.DictReader(open('postcodeareas.csv', 'rU'), ["initial", "region"]):
            self.regions.append(row)

        for row in self.data:
            row["area"] = self.postcodeToAreaCode(row["postcode"])
            for r in self.regions:
                if r["initial"] == row["area"]:
                    row["region"] = r["region"]

        self.tree = cKDTree(self.getCordinates())

    @staticmethod
    def postcodetoareacode(self, postcode):
        '''Returns the post code region for a post code

        This truncates the f substring of letter e.g. YO26 -> YO

        '''
        r = ""
        t = True
        for l in postcode:
            if l.isdigit() == False:
                if t == True:
                    r += str(l)
            else:
                t = False
        return r

    def coordinates(self):
        '''Returns a list of all the coordinates of all the postcodes in the list

        '''
        return [[float(record["lat"]), float(record["lng"])] for record in self.data]

    def postcodes(self):
        '''
        Returns a list of all the post codes
        '''
        return list(set([record["postcode"] for record in self.data]))

    def postcoderegions(self):
        '''
        Returnes a list of all the post code regions
        '''
        return list(set([record["area"] for record in self.data]))

    def regions(self):
        '''
        Returns a list of all the regions
        '''
        return list(set([record["region"] for record in self.data]))

    def findnearestpostcode(self, long, lat, k=2):
        '''
        Returns a list of k nearest nabours of points in the UK
        '''
        r = []
        dists, indexes = self.tree.query(numpy.array([long, lat]), k)
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

    def postcodesinarea(self, area):
        '''
        Returnes a list of all the postcodes in an area.
        '''
        tmp = []
        for row in self.data:
            if row["area"] == area:
                tmp.append(row)
        return tmp

    def postcoderegonsinregon(self, region):
        '''
        List all the post code in a region
        '''
        tmp = []
        for row in self.data:
            if row["region"] == region:
                tmp.append(row)
        return tmp

def main():
    g = Geo()
    pprint(g.getPostCodesInArea("DN"))
    pprint(g.findNearestPostCode(53.954343, -1.079407, 1));


if __name__ == "__main__":
    main()
