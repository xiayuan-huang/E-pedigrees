'''

@author: xiayuanhuang

'''

import csv
import decisionTreeV7
import family_treeV4
import fppa_new_ped


def fppa(addressFile, nameFile, demoFile, accountFile, outputFile, familyTreeOutput):
    reader_add = csv.reader(open(addressFile, 'r'), delimiter = ',')
    h_add = next(reader_add)
    exp_header_add = ['study_id', 'street_1', 'street_2', 'city', 'state', 'zip', 'from_year', 'thru_year']
    if not h_add == exp_header_add: 
        raise Exception("Address file (%s) doesn't have the header expected: %s" % (addressFile, exp_header_add))
    
    reader_name = csv.reader(open(nameFile, 'r'), delimiter = ',')
    h_name = next(reader_name)
    exp_header_name = ['study_id', 'last_name_id', 'first_name_id', 'middle_name_id', 'from_year', 'thru_year']
    if not h_name == exp_header_name:
        raise Exception("Name file (%s) doesn't have the header expected: %s" % (nameFile, exp_header_name))
    
    reader_demo = csv.reader(open(demoFile, 'r'), delimiter = ',')
    h_demo = next(reader_demo)
    exp_header_demo = ['study_id', 'GENDER_CODE', 'birth_year', 'deceased_year', 'PHONE_NUM_id', 'from_year', 'thru_year']
    if not h_demo == exp_header_demo:
        raise Exception("Demographic data file (%s) doesn't have the header expected: %s" % (demoFile, exp_header_demo))

    reader_acc = csv.reader(open(accountFile, 'r'), delimiter = ',')
    h_acc = next(reader_acc)
    exp_header_acc = ['study_id', 'ACCT_NUM_id', 'from_year', 'thru_year']
    if not h_acc == exp_header_acc:
        raise Exception("Account file (%s) doesn't have the header expected: %s" % (accountFile, exp_header_acc))

    '''
    additional PED file
    '''
    args = input("Enter one PED file if any:")
    if args != '':
        ped = args.strip().split(' ')[0]
        reader_ped = csv.reader(open(ped, 'r'), delimiter = ',')
        h_ped = next(reader_ped)
        print(h_ped)
        exp_header_ped = ['familyID', 'family_member', 'study_ID', 'StudyID_MATERNAL', 'StudyID_PATERNAL', 'Sex']
        if not h_ped == exp_header_ped:
            raise Exception("PED data file (%s) doesn't have the header expected: %s" % (ped, exp_header_ped))

        newDT = decisionTreeV7.DT(addressFile, nameFile, demoFile, accountFile)
        newDT.predict()
        newDT.writeToFile(outputFile)

        newFamilyTree = family_treeV4.familyTree(newDT)
        #newFamilyTree = family_treeV4.familyTree(addressFile, nameFile, demoFile, accountFile)
        newFamilyTree.filter(outputFile)
        newFamilyTree.buildTree()
        #newFamilyTree.connected(familyTreeOutput)

        merge = fppa_new_ped.matches(ped, newFamilyTree.edges, newFamilyTree.gender, familyTreeOutput)

        
    else:
        newDT = decisionTreeV7.DT(addressFile, nameFile, demoFile, accountFile)
        newDT.predict()
        newDT.writeToFile(outputFile)

        newFamilyTree = family_treeV4.familyTree(newDT)
        #newFamilyTree = family_treeV4.familyTree(addressFile, nameFile, demoFile, accountFile)
        newFamilyTree.filter(outputFile)
        newFamilyTree.buildTree()
        newFamilyTree.connected(familyTreeOutput)


'''
    if args != '':
        ped = args.strip().split(' ')[0]
        print(ped)
    else:
        ped = False

    newDT = decisionTreeV7.DT(addressFile, nameFile, demoFile, accountFile)
    newDT.predict()
    newDT.writeToFile(outputFile)

    newFamilyTree = family_treeV4.familyTree(newDT)
    #newFamilyTree = family_treeV4.familyTree(addressFile, nameFile, demoFile, accountFile)
    newFamilyTree.filter(outputFile)
    newFamilyTree.buildTree()
    newFamilyTree.connected(familyTreeOutput)

'''