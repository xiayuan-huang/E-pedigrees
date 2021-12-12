'''

@author: xiayuanhuang
'''
import readDataV2
import networkx as nx
import csv
import datetime


class familyTree(object):
    def __init__(self, dt):
        #d = readDataV2.ReadData()
        #d.readAddress(addressFile)
        #d.readName(nameFile)
        #d.readDemo(demoFile)
        #d.readAccount(accountFile)

        self.parent = {}    #    child is the key and parent is the mapped value
        self.child = {}     #    parent is the key and child is the mapped value
        self.gender = dt.gender
        self.address = dt.address
        self.age = dt.age
        self.dob = dt.dob
        self.dateOfDeceased = dt.dateOfDeceased
        self.edges = []
        self.male = set()
        self.female = set()
        self.lastName = dt.lastName
        self.account = dt.account
        self.phone = dt.phone

    def filter(self, outputFile):
        f = open(outputFile, 'r')
        for i in f:
            i = i.strip().split('\t')
            if i[0] in self.child:
                self.child[i[0]].add(i[1])
            else:
                child = set()
                child.add(i[1])
                self.child[i[0]] = child
            if i[1] in self.parent:
                self.parent[i[1]].add(i[0])
            else:
                parent = set()
                parent.add(i[0])
                self.parent[i[1]] = parent
        # filtering out incorrect parents
        for i in self.parent:
            ch = set()
            for j in self.parent[i]:
                a = self.parent[i]
                b = self.child[j]
                if len(a.intersection(b))!=0:
                    ch.add(j)
                    self.child[j].remove(i)
            newch = self.parent[i] - ch
            if newch == '':
                self.parent.pop(i, None)
            else:
                self.parent[i] = newch
        f.close()
    
    def parentsFiltering(self):
        self.lessProbParents = {}

    def buildTree(self):
        self.filteringPa = {}   #
        self.onePa = {}
        for i in self.parent:
            if len(self.parent[i])>2:
                parentList = []
                for j in sorted(self.parent[i]):
                    newList = list(sorted(self.parent[i]))
                    newList.remove(j)
                    for k in newList:
                        if j!=k:
                            flagAcc = False
                            flagPhone = False
                            if j in self.account and k in self.account:
                                acc1 = list(self.account[j].keys())
                                acc2 = list(self.account[k].keys())
                                interacc = list(set(acc1).intersection(set(acc2)))
                                if len(interacc) == 0:
                                    pass
                                else:
                                    for acc in interacc:
                                        for year_range_id1 in self.account[j][acc]:
                                            for year_range_id2 in self.account[k][acc]:
                                                newy1 = year_range_id1[0]
                                                newy2 = year_range_id1[1]
                                                newy3 = year_range_id2[0]
                                                newy4 = year_range_id2[1]
                                                if newy1 == '':
                                                    newy1 = 0
                                                else:
                                                    newy1 = int(newy1)
                                                if newy2 == '':
                                                    newy2 = datetime.datetime.now().year
                                                else:
                                                    newy2 = int(newy2)
                                                if newy3 == '':
                                                    newy3 = 0
                                                else:
                                                    newy3 = int(newy3)
                                                if newy4 == '':
                                                    newy4 = datetime.datetime.now().year
                                                else:
                                                    newy4 = int(newy4)
                                                newa = range(newy1, newy2+1)
                                                newb = range(newy3, newy4+1)
                                                if len(set(newa).intersection(set(newb)))>=1:
                                                    flagAcc = True
                                                    break
                                            else:
                                                continue
                                            break
                            if j in self.phone and k in self.phone:
                                phone1 = list(self.phone[j].keys())
                                phone2 = list(self.phone[k].keys())
                                interpho = list(set(phone1).intersection(set(phone2)))
                                if len(interpho) == 0:
                                    pass
                                else:
                                    for ph in interpho:
                                        for year_range_id1 in self.phone[j][ph]:
                                            for year_range_id2 in self.phone[k][ph]:
                                                newy1 = year_range_id1[0]
                                                newy2 = year_range_id1[1]
                                                newy3 = year_range_id2[0]
                                                newy4 = year_range_id2[1]
                                                if newy1 == '':
                                                    newy1 = 0
                                                else:
                                                    newy1 = int(newy1)
                                                if newy2 == '':
                                                    newy2 = datetime.datetime.now().year
                                                else:
                                                    newy2 = int(newy2)
                                                if newy3 == '':
                                                    newy3 = 0
                                                else:
                                                    newy3 = int(newy3)
                                                if newy4 == '':
                                                    newy4 = datetime.datetime.now().year
                                                else:
                                                    newy4 = int(newy4)
                                                newa = range(newy1, newy2+1)
                                                newb = range(newy3, newy4+1)
                                                if len(set(newa).intersection(set(newb)))>=1:
                                                    flagPhone = True
                                                    break
                                            else:
                                                continue
                                            break
                            # here only considering two parents for one child, further refinement can
                            # consider removing one parent and keep the most possible parent
                            # this logic will keep the most probable parents pairs with reliable account and phone info
                            if (flagAcc or flagPhone) and self.gender[j]!=self.gender[k]:
                                self.filteringPa[i] = [j, k]
                                parentList.append((j, k))
                                #self.edges.append((i, j))
                                #self.edges.append((i, k))
                if len(parentList) == 1:
                    self.filteringPa[i] = [parentList[0][0], parentList[0][1]]
                    self.edges.append((i, parentList[0][0]))
                    self.edges.append((i, parentList[0][1]))
                if len(parentList) > 1:
                    ageFlag = datetime.datetime.now().year
                    eldestPair = []
                    for pairs in parentList:
                        pairA = pairs[0]
                        pairB = pairs[1]
                        #   check the eldest age for one pair of parents
                        if int(self.age[pairA]) < int(self.age[pairB]):
                            yearOfAge = int(self.age[pairB])
                        else:
                            yearOfAge = int(self.age[pairA])
                        if yearOfAge < ageFlag:
                            ageFlag = yearOfAge
                            eldestPair.append(pairA)
                            eldestPair.append(pairB)
                    self.filteringPa[i] = [eldestPair[0], eldestPair[1]]
                    self.edges.append((i, eldestPair[0]))
                    self.edges.append((i, eldestPair[1]))
            elif len(self.parent[i])==2:
                li = list(sorted(self.parent[i]))
                a = li[0]
                b = li[1]

                #self.filteringPa[i] = [a,b]
                if self.gender[a]==self.gender[b]:
                    # compare to current year
                    # choose the parent has the earlier time of overlap same last name
                    yearA = datetime.datetime.now().year
                    yearB = datetime.datetime.now().year
                    names1 = list(self.lastName[i].keys())
                    names2 = list(self.lastName[a].keys())
                    names3 = list(self.lastName[b].keys())
                    intername1 = list(set(names1).intersection(set(names2)))
                    intername2 = list(set(names1).intersection(set(names3)))
                    
                    for iters in intername1:
                        for year_range1 in self.lastName[i][iters]:
                            for year_range2 in self.lastName[a][iters]:
                                newy1 = year_range1[0]
                                newy2 = year_range1[1]
                                newy3 = year_range2[0]
                                newy4 = year_range2[1]
                                if newy1 == '':
                                    newy1 = 0
                                else:
                                    newy1 = int(newy1)
                                if newy2 == '':
                                    newy2 = datetime.datetime.now().year
                                else:
                                    newy2 = int(newy2)
                                if newy3 == '':
                                    newy3 = 0
                                else:
                                    newy3 = int(newy3)
                                if newy4 == '':
                                    newy4 = datetime.datetime.now().year
                                else:
                                    newy4 = int(newy4)
                                newa = range(newy1, newy2+1)
                                newb = range(newy3, newy4+1)
                                if len(set(newa).intersection(set(newb)))>=3:
                                    if newy1 < yearA:
                                        yearA = newy1
                            """ year1 = year_range[0]
                            year2 = year_range[1]
                            if year1 == '':
                                year1 = 0
                            else:
                                year1 = int(year1)
                            if year1 < yearA:
                                yearA = year1 """
                    for iters in intername2:
                        for year_range1 in self.lastName[i][iters]:
                            for year_range2 in self.lastName[b][iters]:
                                newy1 = year_range1[0]
                                newy2 = year_range1[1]
                                newy3 = year_range2[0]
                                newy4 = year_range2[1]
                                if newy1 == '':
                                    newy1 = 0
                                else:
                                    newy1 = int(newy1)
                                if newy2 == '':
                                    newy2 = datetime.datetime.now().year
                                else:
                                    newy2 = int(newy2)
                                if newy3 == '':
                                    newy3 = 0
                                else:
                                    newy3 = int(newy3)
                                if newy4 == '':
                                    newy4 = datetime.datetime.now().year
                                else:
                                    newy4 = int(newy4)
                                newa = range(newy1, newy2+1)
                                newb = range(newy3, newy4+1)
                                if len(set(newa).intersection(set(newb)))>=3:
                                    if newy1 < yearB:
                                        yearB = newy1
                        """ year1 = self.lastName[i][iters][0]
                        if year1 == '':
                            year1 = 0
                        else:
                            year1 = int(year1)
                        if year1 < yearB:
                            yearB = year1 """
                    if yearA == 0 and yearB == 0:
                        if int(self.age[a]) < int(self.age[b]):
                            self.edges.append((i, a))
                            self.filteringPa[i] = [a]
                        else:
                            self.edges.append((i, b))
                            self.filteringPa[i] = [b]
                    else:
                        if yearA<=yearB:
                            self.edges.append((i, a))
                            self.filteringPa[i] = [a]
                        else:
                            self.edges.append((i, b))
                            self.filteringPa[i] = [b]
                else:
                    self.filteringPa[i] = [a,b]
                    self.edges.append((i,a))
                    self.edges.append((i,b))
            else:
                li = list(self.parent[i])
                a = li[0]
                self.filteringPa[i] = [a]
                self.edges.append((i,a))
                self.onePa[i] = [a]
                if self.gender[a] == 'M':
                    self.male.add(a)
                if self.gender[a] == 'F':
                    self.female.add(a)

    def connected(self, familyTreeOutput):
        G = nx.Graph()
        G.add_edges_from(self.edges)
        self.graphs=list(nx.connected_components(G))
        self.size = []
        self.sub = []
        for i in self.graphs:
            ## .nodes() was deprecated
            
            #self.sub.append(i.nodes())
            #self.size.append(len(i.nodes()))
            self.sub.append(i)
            self.size.append(len(i))
        f = open(familyTreeOutput, 'w')
#         print('family total', len(self.sub))
#         f = open('family_tree.csv', 'w')

        writer = csv.writer(f)
        writer.writerow(['familyID', 'family_member', 'study_ID', 'StudyID_MATERNAL', 'StudyID_PATERNAL', 'Sex'])
        num = 1
        for i in range(len(self.sub)):
            for j in self.sub[i]:
                lit = []
                lit.append(str(num))
                lit.append(str(self.size[i]))
                lit.append(j)
                if j in self.filteringPa:
                    m = ''
                    f = ''
                    for k in self.filteringPa[j]:
                        if self.gender[k] == 'F':
                            m = k
                        if self.gender[k] == 'M':
                            f = k
                    lit.append(m)
                    lit.append(f)
                    lit.append(self.gender[j])
                else:
                    lit.append('')
                    lit.append('')
                    lit.append(self.gender[j])

                writer.writerow(lit)
            num += 1