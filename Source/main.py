'''
Run family pedigree prediction algorithm.

@author: xiayuanhuang

USAGE
1. Select one algorithm OR both to run family pedigree prediction by typing:
[FPPA] -- "Family Pedigree Prediction Algorithm"
[RIFTEHR] -- "Relationship Inference from the Electronic Health Records"
[BOTH] -- Run both algorithms in parallel, and combine predicted family pedigree results from
        two algorithms

2. Enter input files for your option to run:
FPPA    -- 6 arguments: 
            addressFile:        address_deid.csv
            nameFile:           name_deid.csv
            demoFile:           demo_deid.csv
            accountFile:        account_deid.csv
            relationFile:       an intermediate output txt file for predicted parent-child relationship and input file 
                                for familiy_tree construction.
                                e.g. p_c.txt  (child, parent)
            famPedigree:        an output csv file of predicted families
                                e.g. family_tree.csv

        ['address_deid.csv', 'name_deid.csv', 'demo_deid.csv', 'account_deid.csv', 'p_c.txt', 'family_tree.csv']

RIFTEHR -- 3 arguments:
           patientsFile:        patients.csv
           emergencyContact:    emergencyContact.csv
           famPedigree:         output csv file of predicted families
        
        []

BOTH    --  8 arguments:
            addressFile:        address_deid.csv
            nameFile:           name_deid.csv
            demoFile:           demo_deid.csv
            accountFile:        account_deid.csv
            relationFile:       an intermediate output txt file for predicted parent-child relationship and input file 
                                for familiy_tree construction.
                                e.g. p_c.txt  (child, parent)
            patientsFile:        patients.csv
            emergencyContact:    emergencyContact.csv
            famPedigree:        an output csv file of predicted families
                                e.g. family_tree.csv
        
        []
'''

import sys
import fppa
import riftehr
import combine

def main(option):
    if option.upper() == "FPPA":
        args = input("Enter your input files for FPPA:")
        if args != '':
            line = args.strip().split(' ')
            if len(line) == 6:
                f = fppa.fppa(line[0], line[1], line[2],
                            line[3], line[4], line[5])
            else:
                raise Exception("Follow the correct argument format for input")
        else:
            raise Exception("Null arguments")
            
    if option.upper() == "RIFTEHR":
        args = input("Enter your input files for RIFTEHR:")
        if args != '':
            line = args.strip().split(' ')
            if len(line) == 3:
                r = riftehr.riftehr(line[0], line[1], line[2])
            else:
                raise Exception("Follow the correct argument format for input")
        else:
            raise Exception("Null arguments")
    if option.upper() == "BOTH":
        args = input("Enter your input files for BOTH:")
        if args != '':
            line = args.strip().split(' ')
            if len(line) == 8:
                b = combine.combine(line[0], line[1], line[2],line[3], line[4],
                                    line[5], line[6], line[7])
            else:
                raise Exception("Follow the correct argument format for input")
        else:
            raise Exception("Null arguments")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise Exception("Choose one option to run by typing [FPPA], [RIFTEHR] or [BOTH]")

    main(sys.argv[1])
