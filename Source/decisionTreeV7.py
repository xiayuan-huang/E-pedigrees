'''

@author: xiayuanhuang
'''

'''
    debugging child's age larger than parents'age
'''

import readDataV2
import datetime

class DT(object):
    def __init__(self, addressFile, nameFile, demoFile, accountFile):
        d = readDataV2.ReadData()
        d.readAddress(addressFile)
        d.readName(nameFile)
        d.readDemo(demoFile)
        d.readAccount(accountFile)
#        d.readAddress('/Users/xiayuanhuang/documents/project/address_deid.csv')
#        d.readName('/Users/xiayuanhuang/documents/project/name_deid.csv')
#        d.readDemo('/Users/xiayuanhuang/documents/project/demo_deid.csv')
#        d.readAccount('/Users/xiayuanhuang/documents/project/account_deid.csv')

#         d.readAddress('test_address.txt')
#         d.readName('test_name.txt')
#         d.readDemo('test_demo.txt')
#         d.readAccount('test_account.txt')
        self.data = d.data
        self.data2 = d.data2
        self.data3 = d.data3
        self.data4 = d.data4
        self.address = d.address
        self.lastName = d.lastName
        self.gender = d.gender
        self.age = d.age
        self.dob = d.dob
        self.dateOfDeceased = d.dateOfDeceased
        self.accountToID = d.accountToID
        self.account = d.account
        self.phone = d.phone

    def predict(self):
        self.p_c = []
        for i in self.address:
            if len(self.address[i]) > 1:
                IDs= list(set(self.address[i]))
                #print(adds)
                self.relation(i, IDs)

    def relation(self, adds, ids):
        num = len(ids)
        for i in range(num-1):
            if ids[i] not in self.gender:
                continue
            for j in range(i+1, num):
                id1 = ids[i]
                id2 = ids[j]
                if id2 not in self.gender:
                    continue
                #print(num, ids, id1, id2)
                for year_range_id1 in self.data[id1][adds]:
                    for year_range_id2 in self.data[id2][adds]:
                        y1 = year_range_id1[0]
                        y2 = year_range_id1[1]
                        y3 = year_range_id2[0]
                        y4 = year_range_id2[1]
                        if y1 =='':
                            y1 = 0
                        else:
                            y1 = int(y1)
                        if y2 =='':
                            y2 = datetime.datetime.now().year
                        else:
                            y2 = int(y2)
                        if y3 == '':
                            y3 = 0
                        else:
                            y3 = int(y3)
                        if y4 == '':
                            y4 = datetime.datetime.now().year
                        else:
                            y4 = int(y4)
                        a = range(y1, y2+1)
                        b = range(y3, y4+1)
                        if self.age[id1] == '' or self.age[id2] == '':
                            break
                        if len(set(a).intersection(set(b)))>=3:
                            names1 = list(self.lastName[id1].keys())
                            names2 = list(self.lastName[id2].keys())
                            intername = list(set(names1).intersection(set(names2)))
                            if len(intername) == 0:
                                break
                            else:
                                nameOverlap = False
                                for na in intername:
                                    for period_name_id1 in self.lastName[id1][na]:
                                        for period_name_id2 in self.lastName[id2][na]:
                                            newy1 = period_name_id1[0]
                                            newy2 = period_name_id1[1]
                                            newy3 = period_name_id2[0]
                                            newy4 = period_name_id2[1]
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
                                                    nameOverlap = True
                                                    break
                                        else:
                                            continue
                                    else:
                                        continue
                                    break
                                if nameOverlap:
                                    if 18<=abs(int(self.dob[id1])-int(self.dob[id2])) and abs(int(self.dob[id1])-int(self.dob[id2]))<=45:
                                        # make sure parent's deceased date is later than child's date of birth
                                        if int(self.dob[id1]) < int(self.dob[id2]):
                                            elderOne = id1
                                            youngerOne = id2
                                        else:
                                            elderOne = id2
                                            youngerOne = id1
                                        if elderOne in self.dateOfDeceased:
                                            if int(self.dateOfDeceased[elderOne]) < int(self.dob[youngerOne]):
                                                break
                                        flagAcc = False
                                        flagPhone = False
                                        if id1 in self.account and id2 in self.account:
                                            acc1 = list(self.account[id1].keys())
                                            acc2 = list(self.account[id2].keys())
                                            interacc = list(set(acc1).intersection(set(acc2)))
                                            if len(interacc) == 0:
                                                pass
                                            else:
                                                for acc in interacc:
                                                    for period_acc_id1 in self.account[id1][acc]:
                                                        for period_acc_id2 in self.account[id2][acc]:
                                                            newy1 = period_acc_id1[0]
                                                            newy2 = period_acc_id1[1]
                                                            newy3 = period_acc_id2[0]
                                                            newy4 = period_acc_id2[1]
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
                                        else:
                                            if int(self.dob[id1])<int(self.dob[id2]):
                                                if id1 in self.dateOfDeceased:
                                                    if int(self.dateOfDeceased[id1])>int(self.dob[id2]):
                                                        pair = (id1, id2)
                                                        self.p_c.append(pair)
                                                else:
                                                    pair = (id1, id2)
                                                    self.p_c.append(pair)
                                            else:
                                                if id2 in self.dateOfDeceased:
                                                    if int(self.dateOfDeceased[id2])>int(self.dob[id1]):
                                                        pair = (id2, id1)
                                                        self.p_c.append(pair)
                                                else:
                                                    pair = (id2, id1)
                                                    self.p_c.append(pair)
                                        if id1 in self.phone and id2 in self.phone:
                                            phone1 = list(self.phone[id1].keys())
                                            phone2 = list(self.phone[id2].keys())
                                            interpho = list(set(phone1).intersection(set(phone2)))
                                            if len(interpho) == 0:
                                                pass
                                            else:
                                                for ph in interpho:
                                                    for period_phone_id1 in self.phone[id1][ph]:
                                                        for period_phone_id2 in self.phone[id2][ph]:
                                                            newy1 = period_phone_id1[0]
                                                            newy2 = period_phone_id1[1]
                                                            newy3 = period_phone_id2[0]
                                                            newy4 = period_phone_id2[1]
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
                                        else:
                                            if int(self.dob[id1])<int(self.dob[id2]):
                                                if id1 in self.dateOfDeceased:
                                                    if int(self.dateOfDeceased[id1])>int(self.dob[id2]):
                                                        pair = (id1, id2)
                                                        self.p_c.append(pair)
                                                else:
                                                    pair = (id1, id2)
                                                    self.p_c.append(pair)
                                            else:
                                                if id2 in self.dateOfDeceased:
                                                    if int(self.dateOfDeceased[id2])>int(self.dob[id1]):
                                                        pair = (id2, id1)
                                                        self.p_c.append(pair)
                                                else:
                                                    pair = (id2, id1)
                                                    self.p_c.append(pair)
                                        if flagAcc or flagPhone:
                                            if int(self.dob[id1])<int(self.dob[id2]):
                                                if id1 in self.dateOfDeceased:
                                                    if int(self.dateOfDeceased[id1])>int(self.dob[id2]):
                                                        pair = (id1, id2)
                                                        self.p_c.append(pair)
                                                else:
                                                    pair =   (id1, id2)
                                                    self.p_c.append(pair)
                                            else:
                                                if id2 in self.dateOfDeceased:
                                                    if int(self.dateOfDeceased[id2])>int(self.dob[id1]):
                                                        pair = (id2, id1)
                                                        self.p_c.append(pair)
                                                else:
                                                    pair = (id2, id1)
                                                    self.p_c.append(pair)
                                    if 0<=abs(int(self.dob[id1])-int(self.dob[id2])) and abs(int(self.dob[id1])-int(self.dob[id2]))<=16:
                                        #add to sibling relationship
                                        flagAcc = False
                                        flagPhone = False
                                        if id1 in self.account and id2 in self.account:
                                            acc1 = list(self.account[id1].keys())
                                            acc2 = list(self.account[id2].keys())
                                            interacc = list(set(acc1).intersection(set(acc2)))
                                            if len(interacc) == 0:
                                                pass
                                            else:
                                                for acc in interacc:
                                                    for period_acc_id1 in self.account[id1][acc]:
                                                        for period_acc_id2 in self.account[id2][acc]:
                                                            newy1 = period_acc_id1[0]
                                                            newy2 = period_acc_id1[1]
                                                            newy3 = period_acc_id2[0]
                                                            newy4 = period_acc_id2[1]
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
                                        else:
                                            if int(self.dob[id1])<int(self.dob[id2]):
                                                if id1 in self.dateOfDeceased:
                                                    if int(self.dateOfDeceased[id1])>int(self.dob[id2]):
                                                        pair = (id1, id2)
                                                        #self.p_c.append(pair)
                                                else:
                                                    pair = (id1, id2)
                                                    #self.p_c.append(pair)
                                            else:
                                                if id2 in self.dateOfDeceased:
                                                    if int(self.dateOfDeceased[id2])>int(self.dob[id1]):
                                                        pair = (id2, id1)
                                                        #self.p_c.append(pair)
                                                else:
                                                    pair = (id2, id1)
                                                    #self.p_c.append(pair)
                                        if id1 in self.phone and id2 in self.phone:
                                            phone1 = list(self.phone[id1].keys())
                                            phone2 = list(self.phone[id2].keys())
                                            interpho = list(set(phone1).intersection(set(phone2)))
                                            if len(interpho) == 0:
                                                pass
                                            else:
                                                for ph in interpho:
                                                    for period_phone_id1 in self.phone[id1][ph]:
                                                        for period_phone_id2 in self.phone[id2][ph]:
                                                            newy1 = period_phone_id1[0]
                                                            newy2 = period_phone_id1[1]
                                                            newy3 = period_phone_id2[0]
                                                            newy4 = period_phone_id2[1]
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
                                        else:
                                            if int(self.dob[id1])<int(self.dob[id2]):
                                                if id1 in self.dateOfDeceased:
                                                    if int(self.dateOfDeceased[id1])>int(self.dob[id2]):
                                                        pair = (id1, id2)
                                                        #self.p_c.append(pair)
                                                else:
                                                    pair = (id1, id2)
                                                    #self.p_c.append(pair)
                                            else:
                                                if id2 in self.dateOfDeceased:
                                                    if int(self.dateOfDeceased[id2])>int(self.dob[id1]):
                                                        pair = (id2, id1)
                                                        #self.p_c.append(pair)
                                                else:
                                                    pair = (id2, id1)
                                                    #self.p_c.append(pair)
                                        if flagAcc or flagPhone:
                                            if int(self.dob[id1])<int(self.dob[id2]):
                                                if id1 in self.dateOfDeceased:
                                                    if int(self.dateOfDeceased[id1])>int(self.dob[id2]):
                                                        pair = (id1, id2)
                                                        #self.p_c.append(pair)
                                                else:
                                                    pair = (id1, id2)
                                                    #self.p_c.append(pair)
                                            else:
                                                if id2 in self.dateOfDeceased:
                                                    if int(self.dateOfDeceased[id2])>int(self.dob[id1]):
                                                        pair = (id2, id1)
                                                        #self.p_c.append(pair)
                                                else:
                                                    pair = (id2, id1)
                                                    #self.p_c.append(pair)
                                else:
                                    if 18<=abs(int(self.dob[id1])-int(self.dob[id2])) and abs(int(self.dob[id1])-int(self.dob[id2]))<=45 and min(int(self.age[id1]), int(self.age[id2]))<3:
                                        '''
                                            here the condition was hard coded to 2014 since the most recent birth year recorded in the file was 2014
                                            set the min age of one pair of individuals blow 3 years old
                                        '''
                                        if int(self.dob[id1]) < int(self.dob[id2]):
                                            elderOne = id1
                                            youngerOne = id2
                                        else:
                                            elderOne = id2
                                            youngerOne = id1
                                        if elderOne in self.dateOfDeceased:
                                            if int(self.dateOfDeceased[elderOne]) < int(self.dob[youngerOne]):
                                                break
                                        flagAcc = False
                                        flagPhone = False
                                        if id1 in self.account and id2 in self.account:
                                            acc1 = list(self.account[id1].keys())
                                            acc2 = list(self.account[id2].keys())
                                            interacc = list(set(acc1).intersection(set(acc2)))
                                            if len(interacc) == 0:
                                                pass
                                            else:
                                                for acc in interacc:
                                                    for period_acc_id1 in self.account[id1][acc]:
                                                        for period_acc_id2 in self.account[id2][acc]:
                                                            newy1 = period_acc_id1[0]
                                                            newy2 = period_acc_id1[1]
                                                            newy3 = period_acc_id2[0]
                                                            newy4 = period_acc_id2[1]
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
                                        else:
                                            if int(self.dob[id1])<int(self.dob[id2]):
                                                if id1 in self.dateOfDeceased:
                                                    if int(self.dateOfDeceased[id1])>int(self.dob[id2]):
                                                        pair = (id1, id2)
                                                        self.p_c.append(pair)
                                                else:
                                                    pair = (id1, id2)
                                                    self.p_c.append(pair)
                                            else:
                                                if id2 in self.dateOfDeceased:
                                                    if int(self.dateOfDeceased[id2])>int(self.dob[id1]):
                                                        pair = (id2, id1)
                                                        self.p_c.append(pair)
                                                else:
                                                    pair = (id2, id1)
                                                    self.p_c.append(pair)
                                        if id1 in self.phone and id2 in self.phone:
                                            phone1 = list(self.phone[id1].keys())
                                            phone2 = list(self.phone[id2].keys())
                                            interpho = list(set(phone1).intersection(set(phone2)))
                                            if len(interpho) == 0:
                                                pass
                                            else:
                                                for ph in interpho:
                                                    for period_phone_id1 in self.phone[id1][ph]:
                                                        for period_phone_id2 in self.phone[id2][ph]:
                                                            newy1 = period_phone_id1[0]
                                                            newy2 = period_phone_id1[1]
                                                            newy3 = period_phone_id2[0]
                                                            newy4 = period_phone_id2[1]
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
                                        else:
                                            if int(self.dob[id1])<int(self.dob[id2]):
                                                if id1 in self.dateOfDeceased:
                                                    if int(self.dateOfDeceased[id1])>int(self.dob[id2]):
                                                        pair = (id1, id2)
                                                        self.p_c.append(pair)
                                                else:
                                                    pair = (id1, id2)
                                                    self.p_c.append(pair)
                                            else:
                                                if id2 in self.dateOfDeceased:
                                                    if int(self.dateOfDeceased[id2])>int(self.dob[id1]):
                                                        pair = (id2, id1)
                                                        self.p_c.append(pair)
                                                else:
                                                    pair = (id2, id1)
                                                    self.p_c.append(pair)
                                        if flagAcc or flagPhone:
                                            if int(self.dob[id1])<int(self.dob[id2]):
                                                if id1 in self.dateOfDeceased:
                                                    if int(self.dateOfDeceased[id1])>int(self.dob[id2]):
                                                        pair = (id1, id2)
                                                        self.p_c.append(pair)
                                                else:
                                                    pair = (id1, id2)
                                                    self.p_c.append(pair)
                                            else:
                                                if id2 in self.dateOfDeceased:
                                                    if int(self.dateOfDeceased[id2])>int(self.dob[id1]):
                                                        pair = (id2, id1)
                                                        self.p_c.append(pair)
                                                else:
                                                    pair = (id2, id1)
                                                    self.p_c.append(pair)
                        else:
                            # check if the child younger than three years old
                            pass
                    else:
                        continue
                    break
    def writeToFile(self, outputFile):
        fileOut = open(outputFile, 'w')
        for i in self.p_c:
            fileOut.write(i[0])
            fileOut.write('\t')
            fileOut.write(i[1])
            fileOut.write('\n')
        fileOut.flush()
        fileOut.close()
