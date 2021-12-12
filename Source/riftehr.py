'''

@author: xiayuanhuang

'''

import csv
import matchECtoDemog
import riftehr_new_ped

def riftehr(patientFile, ecFile, familyTreeOutput):
    reader_p = csv.reader(open(patientFile, 'r'), delimiter = ',')
    h_p = next(reader_p)
    exp_header_p = ['PatientID', 'FirstName', 'LastName', 'Sex', 'PhoneNumber', 'Zipcode', 'birth_year', 'deceased_year']
    if not h_p == exp_header_p:
        raise Exception("Patient data file (%s) doesn't have the header expected: %s" % (patientFile, exp_header_p))

    reader_ec = csv.reader(open(ecFile, 'r'), delimiter = ',')
    h_ec = next(reader_ec)
    exp_header_ec = ['PatientID', 'EC_FirstName', 'EC_LastName', 'EC_PhoneNumber', 'EC_Zipcode', 'EC_Relationship']
    if not h_ec == exp_header_ec:
        raise Exception("Emergency contact data file (%s) doesn't have the header expected: %s" % (ecFile, exp_header_ec))
    
    '''
    args = input("Enter up to four different variables used for comparison (separated by space):")
    if args != '':
        line = args.strip().split(' ')
        if len(line) <=4:
            var = set(['fn', 'ln', 'phone', 'zip'])
            v_r = []
            for v in line:
                v_r.append(v.lower())
            print(v_r)
            if set(v_r).issubset(var):
                print('hi')
                mt = matchECtoDemog.matches(patientFile, ecFile, familyTreeOutput, v_r)
            else:
                raise Exception("Enter correct variables, such as ['fn', 'ln', 'phone', 'zip']")
        else:
            raise Exception("Enter less than five variables")

    else:
        raise Exception("Null arguments")
    '''

    args = input("Enter one PED file if any:")
    if args != '':
        ped = args.strip().split(' ')[0]
        reader_ped = csv.reader(open(ped, 'r'), delimiter = ',')
        h_ped = next(reader_ped)
        exp_header_ped = ['familyID', 'family_member', 'study_ID', 'StudyID_MATERNAL', 'StudyID_PATERNAL', 'Sex']
        if not h_ped == exp_header_ped:
            raise Exception("PED data file (%s) doesn't have the header expected: %s" % (ped, exp_header_ped))

        mt = matchECtoDemog.matches(patientFile, ecFile)

        ### merge new PED file
        merge = riftehr_new_ped.matches(mt.qc_matches, mt.sex, familyTreeOutput)
        
    else:
        mt = matchECtoDemog.matches(patientFile, ecFile)
        mt.assignFamily(familyTreeOutput)

    

    