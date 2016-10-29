"""
   Convex Hull Assignment: COSC262 (2016)
   Student Name: David Fey
   Usercode: dfe32
"""

def giftwrap(listPts):
    chull = []
    #make new list to modify while preserving indexes of old list
    pts = list(listPts)
    start = lowestPoint(pts)
    n = len(pts)
    i = 0
    v = 0
    pts.append(start)
    k = pts.index(start)
    chull.append(k)
    while k!=n:
        pts[i], pts[k] = pts[k], pts[i]
        minAngle = 361
        for j in range(i+1, n+1):
            ang = angle(pts[j], pts[i])
            if ang<minAngle and ang>v and pts[j]!=pts[i]:
                minAngle = ang
                k=j
        #make sure we dont include the first point as we close the hull
        if k!=n:
            chull.append(listPts.index(pts[k]))
        i+=1
        v=minAngle
    return chull

#implements the graham scan algorithm for finding a convex hull
def grahamscan(listPts):
    chull = []
    n = len(listPts)
    pts = list(listPts)
    start = lowestPoint(pts)
    L = sortByAngle(pts, start)
    stack = [start, L[0], L[1]]
    chull.append(listPts.index(start))
    chull.append(listPts.index(L[0]))
    chull.append(listPts.index(L[1]))
    del L[0:2]
    for i in range(0, n-3):
        while isCCW(stack[-2], stack[-1], L[i])==False:
            stack.pop()
            chull.pop()
        stack.append(L[i])
        chull.append(listPts.index(L[i]))
    return chull

def amethod(listPts):
    #Implementing 'Andrew's monotone chain algorithm'
    #Finds top half of convex hull, then bottom half.
    chull = []
    pts = sorted(set(listPts))
    #Form lower half of convex hull
    lower = []
    for p in pts:
        while len(lower) >= 2 and isCCW(lower[-2], lower[-1], p):
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper)>=2 and isCCW(upper[-2], upper[-1], p):
            upper.pop()
        upper.append(p)
    #Remove the last two points of the two halves, as they are excess, and combine them
    hullPts = lower[:-1] + upper[:-1]
    for i in hullPts:
        chull.append(listPts.index(i))
    return chull

#read data points from a file and place them into a list
def readDataPts(filename):
    listPts = []
    for line in open(filename, 'r'):
        item = line.rstrip()
        if (' ' in item) == False:
            global size
            size = int(item)
        else:
            listPts.append(tuple(int (i) for i in item.split(' ')))
    return listPts

#return the lowest point in a set of points on a 2-d plane
def lowestPoint(listPts):
    low = 800
    lowX = 0
    lowPt = (0,0)
    for point in listPts:
        if(point[1] < low):
            low = point[1]
            lowPt = point
        if(point[1] == low and point[0] > lowX):
            low = point[1]
            lowPt = point
    return lowPt

#return the angle between two points and a horizontal plane
def angle(a, b):
    dy = a[1]-b[1]
    dx = a[0]-b[0]
    if abs(dx)<1.e-4 and abs(dy)<1.e-4:
        t = 0
    else:
        t = float(dy)/(abs(dx)+abs(dy))
    if dx < 0:
        t=2-t
    elif dy < 0:
        t = 4+t
    angle = t*90
    if angle == 0:
        return 360
    else:
        return angle

#return how three points are arranged in 2-dimensional space relative to each other
def lineFn(ptA, ptB, ptC):
    return (ptB[0]-ptA[0])*(ptC[1]-ptA[1])-(ptB[1]-ptA[1])*(ptC[0]-ptA[0])

#Return true if the points are ordered in a counter clockwise manner
def isCCW(ptA, ptB, ptC):
    return lineFn(ptA, ptB, ptC) > 0

#return a new list that sorts all other points in order of increasing angle relative to starting point
def sortByAngle(listPts, start):
    dict = {}
    listPts.remove(start)
    for i in range(0, len(listPts)):
        ang = angle(listPts[i], start)
        dict[listPts[i]]=ang
    return sorted(dict, key=dict.__getitem__)

#This method checks the output from the given algorithm with the output file
#Only works for Gift Wrap and Graham Scan, as it requires points to be in correct order
def checkOutput(list, expectedOutFile, algorithm):
    correct = 'Correct'
    f = open(expectedOutFile, 'r')
    correctList = f.read().split()
    #If the lists are different lengths, the result is incorrect by default
    if(len(correctList)!=len(list)):
        return ('File {} is: Incorrect'.format(expectedOutFile[:-4]))
    for i in range (0, len(list)):
        if(int(correctList[i])!=list[i]):
            correct = 'Incorrect'
    return ('File {} is: {} for the {} algorithm'.format(expectedOutFile[:-4], correct, algorithm))

#------------------------------------------------------------------------
#Where to input specific file/data set to run on and execute the actual code
#Place data file in fileName
#Place expected output in expectedOut
#------------------------------------------------------------------------
def main():
    fileName = 'A_6000.dat'
    expectedOut = 'A_6000.out'
    listPts = readDataPts(fileName)
    print checkOutput(giftwrap(listPts), expectedOut, 'giftwrap')
    print checkOutput(grahamscan(listPts), expectedOut, 'grahamscan')
    print 'Andrews monotone chain algorithm returns: ', amethod(listPts)
    #Timed Algorithms here
    """from time import time
    gift = 0
    graham = 0
    monotone = 0
    for i in range(10):
        t0 = time()
        giftwrap(listPts)
        t1=time()
        grahamscan(listPts)
        t2=time()
        amethod(listPts)
        t3=time()
        gift += (t1-t0)
        graham += (t2-t1)
        monotone+= (t3-t2)
    print 'Giftwrap algorithm takes: ', (gift/10)
    print 'Grahamscan algorithm takes: ', (graham/10)
    print 'Monotone chain algorithm takes: ', (monotone/10)"""

if __name__  ==  "__main__":
    main()
