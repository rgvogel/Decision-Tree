
from math import log
import sys 
import copy 
attributesDict = {}
numTargets = 0
numExamples = 0
mostCommonTar = ''
attList = []
tarCount ={}
leafC = 0

def organize(File):
    
    targetList = []
    
    # open file go line by line    
    with open(File, 'r') as f: 
        count = 0
        numAtt = 0
        for line in f:
            
            splitline = line.split(',')
            #keep solid count on number of targets
            if count == 0:
                numTargets = int(splitline[0])
            if count == 2:
                numAtt = int(splitline[0])
            # create dictionary with all the variables for each attribute
            if count >2 and count < numAtt+3:
                #print count
                
                atts = splitline[2:]
                attList.append(splitline[0])
                #print splitline[0]
                attributesDict[splitline[0]] = splitline[2:]
                #print attributesDict[splitline[0]]
            if count == numAtt+3:
                numExamples = int(splitline[0])

            if count > numAtt+3:
                targetList.append(splitline)
                attTot = len(splitline) -1
        #        tarCount[splitline[attTot]] = tarCount[splitline[attTot]] +1

            count = count +1 
    largest=0
    #for i in tarCount:
     #  if tarCount[i]> largest:
      #      largest = tarCount[i]
       #     mostCommonTar = i

    return targetList

#create dictionary where has specific value of an attribute, target is the key
def targetSplit(rows,value,col):
    rlength =  len(rows[0])-1
    targetDict = {}

    for line in rows:
        if value==line[col]:
            if line[rlength] not in targetDict:
                targetDict[line[rlength]] = []
                targetDict[line[rlength]].append(line[0:rlength+1])

            else:
                targetDict[line[rlength]].append(line[0:rlength+1])
                #print targetDict[line[rlength]]
    
    return targetDict

def targetSplitStart(rows):
    rlength =  len(rows[0])-1
    targetDict = {}
    for line in rows:
        if line[rlength] not in targetDict:
            targetDict[line[rlength]] = []
            targetDict[line[rlength]].append(line[0:rlength+1])

        else:
            targetDict[line[rlength]].append(line[0:rlength+1])

    return targetDict

#calculates entropy using the negative sumation of p *log2(p)
def entropy(targetDict):
     tLength = 0
     log2 = lambda x:log(x)/log(2)
     entropy = 0.0
     #print tLength
     for target in targetDict:
        tLength = len(targetDict[target])+ tLength
     #print tLength
     for target in targetDict:
        #print target
        tarlen = len(targetDict[target])
        #print tarlen
        p = float(tarlen)/tLength
# returns target value will be leaf
        if p == 1.0:
            #print target
            return target
        entropy = entropy - p*log2(p)
         
     #print entropy
     return entropy 
leafC =0
nodeC = 0
def treeBuild(rows,totDict,usedAtt):
    
    startTar = targetSplitStart(rows)
    #print startTar
    #print startTar.keys()
    startEnt = entropy(startTar)
    #print rows
    #print startTar.keys()
    #print startTar
    #print "start"
    #print startEnt
    #print "end start"
    bestGain = 0.0
    bestDict = {}
    tDict = {}
    bestAtt = ""
# hold the top layer with name of attribute
    dictAtt = {}
    totLength = len(rows)
    attTot = len(rows[0]) -1
    for col in range(0,attTot):
        dictAtt = {}
        attVals = set([r[col] for r in rows])
        #attribute dictionary values based on values of each attribute
        attDict = {}
        gain = 0.0
        entTot =0.0
        for value in attVals:
            tLength = 0.0
            tDict = targetSplit(rows,value,col)
            #attribute value list
            attValue = []
            for t in tDict:
                tLength = len(tDict[t]) + tLength
                #print tDict[t]
                for i in tDict[t]:
                    attValue.append(i)
            attDict[value] = attValue
            ent = entropy(tDict)
            if type(ent)!= str:
                entTot = entTot - (float(tLength)/totLength) *ent
            else:
#is lead        
                #print ent
                attDict[value] = ent
                #print attList[col]
                #print value
                #print ent
               
        dictAtt[attList[col]]= attDict
        gain = startEnt + entTot
        if gain> bestGain and attList[col] not in usedAtt:
            bestAtt = attList[col]    
            bestGain = gain
            bestDict = dictAtt
            #print bestGain
            #print bestDict
    
    if len(totDict) == 0:
        totDict = bestDict
    usedAtt.append(bestAtt)
#recursi vely fill dictionary with values based on gain
    count = 0
    for k in totDict:
        print k 
        global nodeC
        nodeC = nodeC +1
        for p in totDict[k]:
            print p
            emptyDict = {}
        #if string then it is an anwser
            if type(totDict[k][p]) != str:
                uA = copy.copy(usedAtt)
                tD = copy.copy(totDict)
                tD[k][p]= treeBuild(tD[k][p],emptyDict,uA)
            #elif totDict[k][p]=={}:

             #   totDict[k][p] = mostCommonTar
            else:
                global leafC
                leafC= leafC +1
                print totDict[k][p]
                
        return totDict

def tester(rows,tDict):
    #print tDict 
    for tD in tDict:
        col = attList.index(tD)


    

if __name__=="__main__":
    tlist = []
    tDict = {}
    usedAtt = [] 
    car = "car.csv"
    fish = "fish.csv"
    lense = 'Lenses.csv'
    train = "train_car.csv"
    test = "test_car.csv"
    #testList = organize(test)
    trainlist = organize(car)
    
    #print tlist
    trainDict =treeBuild(trainlist,tDict,usedAtt)
    tester(test,trainDict)
    print leafC
    
