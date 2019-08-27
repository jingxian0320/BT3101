### Analysis for Association Rule Mining ###
### Tang Jiahui ###
### A0119415J ###


import csv
import Orange
import numpy


#### Part 1: data structure pre-processing ####

# building a dict matrix of one categories and its corresponding apps
documents=["general.csv","life.csv","game.csv","fin.csv","edu.csv","baby.csv"]

for docu in documents:
    matrix = dict()
    with open(docu,"rb") as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        for row in reader:
            if row[0]=="device_id":
                pass
            elif row[0] in matrix: 
                # only record one occurrence per category for one device, avoid duplicate
                if row[2] not in matrix[row[0]]:
                    matrix[row[0]].append(row[2])
            else:
                matrix[row[0]] = [row[2],]

    transactions = list(matrix.values())

    ## write output into a format .basket that is suitable for Orange Package"
    with open("test.basket",'w') as f:
        writer = csv.writer(f,delimiter=',')
        for row in transactions:
            writer.writerow(row)
            
#### Part 2: method for association rule: orange package ####

    items= Orange.data.Table("test.basket")
    rules= Orange.associate.AssociationRulesSparseInducer(items, support = 0.1, maxItemSets=1000000)
    rules=sorted(rules, key = lambda r: r.lift, reverse=True )


#### Part 3: find the significant rules by taking top 10% ####
    lift = []
    support =[]
    confidence = []

    for r in rules:
        lift += [r.lift]
        support += [r.support]
        confidence += [r.confidence]
    parameter = [lift, support, confidence]
    thre = [] # threshold of top x% of rules
    # take the top 10% of significant rule
    for i in parameter:
        thre.append(numpy.percentile(numpy.array(i),99))

    rules_lift= rules
    rules_support=sorted(rules, key = lambda r: r.support, reverse=True)
    rules_confidence=sorted(rules, key = lambda r: r.confidence, reverse=True)
    rules_collection = [rules_lift, rules_support, rules_confidence]

    suffix = ["lift.csv","support.csv","confidence.csv"]
    for i in range(3):
        with open(docu[:-4]+"_sign_"+ suffix[i],"w") as f:
            writer1 = csv.writer(f, delimiter = ' ')
            writer2 = csv.writer(f, delimiter=',')
            writer1.writerow(["supp","conf","lift","rule"])
            for j in rules_collection[i]:
                if i==0 and (j.lift > thre[i]):
                    writer2.writerow(["%5.3f %5.3f %5.3f %s" % (j.support, j.confidence, j.lift, str(j))]) 
                elif i==1 and (j.support > thre[i]):
                    writer2.writerow(["%5.3f %5.3f %5.3f %s" % (j.support, j.confidence, j.lift, str(j))]) 
                elif i==2 and (j.confidence > thre[i]):
                    writer2.writerow(["%5.3f %5.3f %5.3f %s" % (j.support, j.confidence, j.lift, str(j))]) 

