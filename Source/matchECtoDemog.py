'''

@author: xiayuanhuang

'''
import os
import sys
import csv
import copy

from numpy.core import machar
from tqdm import tqdm
from collections import defaultdict
import networkx as nx

class matches(object):
    def __init__(self, patientFile, ecFile):
        self.readPtFile(patientFile)
        self.readEcFile(ecFile)
        self.find_matches()
        self.clean()
        self.infer_matches()
        self.test()
        #self.assignFamily(result)
    
    def readPtFile(self, patientFile):
        self.pt_data = list()
        ### map patientID to birth_year
        self.age = {}
        self.sex = {}
        reader = csv.reader(open(patientFile, 'rU'), delimiter=',')
        #exp_header = ['MRN', 'FirstName', 'LastName', 'PhoneNumber', 'Zipcode']
        exp_header = ['PatientID', 'FirstName', 'LastName', 'Sex', 'PhoneNumber', 'Zipcode', 'birth_year', 'deceased_year']
        h = next(reader)
        if not h == exp_header:
            raise Exception("Patient demographic data file (%s) doesn't have the header expected:%s" % (patientFile, exp_header))
        try:
            for i, (mrn, fn, ln, sex, phone, zipcode, dob, dod) in enumerate(reader):
                #print(i)
                fn = fn.strip().lower()
                ln = ln.strip().lower()
            
                first_names = [fn]
                if fn.replace('-', ' ').find(' ') != -1:
                    first_names += fn.replace('-',' ').split(' ')
            
                last_names = [ln]
                if ln.replace('-', ' ').find(' ') != -1:
                    last_names += ln.replace('-',' ').split(' ')
            
                for fn_comp in first_names:
                    for ln_comp in last_names:
                        self.pt_data.append([mrn, fn_comp, ln_comp, phone, zipcode])
                self.age[mrn] = dob
                self.sex[mrn] = sex
        except Exception as e:
            #print >> sys.stderr, "Failed with error: %s" % csv.Error
            print(sys.stderr, "Failed in %s at line: %d with error: %s" % (patientFile, i+2, e))
            sys.exit(20)

    def readEcFile(self, ecFile):
        reader = csv.reader(open(ecFile, 'rU'), delimiter=',')
        h = next(reader)
        exp_header = ['PatientID', 'EC_FirstName', 'EC_LastName', 'EC_PhoneNumber', 'EC_Zipcode', 'EC_Relationship']
        if not h == exp_header:
            raise Exception("Emergency contact data file (%s) doesn't have the header expected: %s" % (ecFile, exp_header))
        self.ec_data = list()
        for mrn, fn, ln, phone, zipcode, rel in reader:
            fn = fn.strip().lower()
            ln = ln.strip().lower()
            
            first_names = [fn]
            if fn.replace('-', ' ').find(' ') != -1:
                first_names += fn.replace('-',' ').split(' ')
            
            last_names = [ln]
            if ln.replace('-', ' ').find(' ') != -1:
                last_names += ln.replace('-', ' ').split(' ')
                    
            for fn_comp in first_names:
                for ln_comp in last_names:
                    self.ec_data.append([mrn, fn_comp, ln_comp, phone, zipcode, rel])

    def find_matches(self):
        print(sys.stderr, "Building hash libraries...")
        first_hash = defaultdict(list)
        last_hash = defaultdict(list)
        phone_hash = defaultdict(list)
        zip_hash = defaultdict(list)

        num_char = 13
        print(sys.stderr, "\thashing num = %d" % num_char)
        for pt in self.pt_data:
            mrn, fn, ln, phone, zipcode = pt
            if fn[:num_char] != '':
                first_hash[fn[:num_char]].append( pt )
            if ln[:num_char] != '':
                last_hash[ln[:num_char]].append( pt )
            if phone[:num_char] != '':
                phone_hash[phone[:num_char]].append( pt )
            if zipcode[:num_char] != '':
                zip_hash[zipcode[:num_char]].append( pt )

        ofh = open('relations.csv', 'w')
        #delim = '\t' if result.endswith('txt') else ','
        writer = csv.writer(ofh, delimiter=',')

        ###create a set of matching relationship tuples (pt, relationship, ec)
        self.matching_tuples = set()
        
        for pt_mrn, ec_first, ec_last, ec_phone, ec_zip, relationship in tqdm(self.ec_data):
            first_matches = set([pt[0] for pt in first_hash[ec_first[:num_char]] if pt[1] == ec_first])
            last_matches = set([pt[0] for pt in last_hash[ec_last[:num_char]] if pt[2] == ec_last])
            phone_matches = set([pt[0] for pt in phone_hash[ec_phone[:num_char]] if pt[3] == ec_phone])
            zip_matches = set([pt[0] for pt in zip_hash[ec_zip[:num_char]] if pt[4] == ec_zip])

            matching_mrns = list()
            if len(first_matches) == 1:
                matching_mrns.extend([(mrn, 'first') for mrn in first_matches])
            if len(last_matches) == 1:
                matching_mrns.extend([(mrn, 'last') for mrn in last_matches])
            if len(phone_matches) == 1:
                matching_mrns.extend([(mrn, 'phone') for mrn in phone_matches])
            if len(zip_matches) == 1:
                matching_mrns.extend([(mrn, 'zip') for mrn in zip_matches])

            if len(first_matches & last_matches) == 1:
                matching_mrns.extend([(mrn, 'first,last') for mrn in (first_matches & last_matches)])
            if len(first_matches & phone_matches) == 1:
                matching_mrns.extend([(mrn, 'first,phone') for mrn in (first_matches & phone_matches)])
            if len(first_matches & zip_matches) == 1:
                matching_mrns.extend([(mrn, 'first,zip') for mrn in (first_matches & zip_matches)])
            if len(last_matches & phone_matches) == 1:
                matching_mrns.extend([(mrn, 'last,phone') for mrn in (last_matches & phone_matches)])
            if len(last_matches & zip_matches) == 1:
                matching_mrns.extend([(mrn, 'last,zip') for mrn in (last_matches & zip_matches)])
            if len(phone_matches & zip_matches) == 1:
                matching_mrns.extend([(mrn, 'phone,zip') for mrn in (phone_matches & zip_matches)])

            if len(first_matches & last_matches & phone_matches) == 1:
                matching_mrns.extend([(mrn, 'first,last,phone') for mrn in (first_matches & last_matches & phone_matches)])
            if len(first_matches & last_matches & zip_matches) == 1:
                matching_mrns.extend([(mrn, 'first,last,zip') for mrn in (first_matches & last_matches & zip_matches)])
            if len(first_matches & phone_matches & zip_matches) == 1:
                matching_mrns.extend([(mrn, 'first,phone,zip') for mrn in (first_matches & phone_matches & zip_matches)])
            if len(last_matches & phone_matches & zip_matches) == 1:
                matching_mrns.extend([(mrn, 'last,phone,zip') for mrn in (last_matches & phone_matches & zip_matches)])

            if len(first_matches & last_matches & phone_matches & zip_matches) == 1:
                matching_mrns.extend([(mrn, 'first,last,phone,zip') for mrn in (first_matches & last_matches & phone_matches & zip_matches)])
                
            for matched_mrn, path in matching_mrns:
                self.matching_tuples.add((pt_mrn, relationship, matched_mrn))
                writer.writerow([pt_mrn, relationship, matched_mrn, path])
        
        ofh.close()
    
        ### quality control of matches
    def clean(self):
        remove_re = set()
        for i in self.matching_tuples:
            if i[1].lower() == 'spouse' or i[1].lower() == 'friend':
                remove_re.add(i)
            if i[1].lower() == 'mother' or i[1].lower() == 'father':
                if int(self.age[i[0]]) - int(self.age[i[2]]) <= 10:
                    remove_re.add(i)
            if i[1].lower() == 'child':
                if int(self.age[i[2]]) - int(self.age[i[0]]) <= 10:
                    remove_re.add(i)
            if i[1].lower() == 'grandmother' or i[1].lower() == 'grandfather':
                if int(self.age[i[0]]) - int(self.age[i[2]]) <= 20:
                    remove_re.add(i)
            if i[1].lower() == 'grandchild':
                if int(self.age[i[2]]) - int(self.age[i[0]]) <=20:
                    remove_re.add(i)
        self.matching_tuples = self.matching_tuples.difference(remove_re)

        ### remove patient that matches to 20 or more distinct emergency contact
        matching_dict = {}
        for i in self.matching_tuples:
            if i[0] in matching_dict:
                matching_dict[i[0]].append((i[1], i[2]))
            else:
                rel = []
                rel.append((i[1], i[2]))
                matching_dict[i[0]] = rel
        matching_dict_copy = copy.deepcopy(matching_dict)
        for k, v in matching_dict_copy.items():
            if len(v) >= 20:
                del matching_dict[k]
        self.qc_matches = {}
        ### This algorithm assumes ec relationship is unique and TRUE for the same pair
        ### self.qc_matches: {k:{{},{}.{}},k:{{}.{}}}
        for k in matching_dict:
            v = matching_dict[k]
            a = {}
            for j in v:
                a[j[1]] = j[0]
                self.qc_matches[k] = a
        ### create opposite relationships
        qc_matches_copy = copy.deepcopy(self.qc_matches)
        for k1, v in qc_matches_copy.items():
            for k2 in v:
                r = v[k2]
                if k2 in qc_matches_copy:
                    if k1 in qc_matches_copy[k2]:
                        continue
                    else:
                        if r.lower() == 'mother' or r.lower() == 'father':
                            self.qc_matches[k2][k1] = 'child'
                        if r.lower() == 'child':
                            if self.sex[k1].lower() == 'f':
                                self.qc_matches[k2][k1] = 'mother'
                            if self.sex[k1].lower() == 'm':
                                self.qc_matches[k2][k1] = 'father'
                        if r.lower() == 'sibling':
                            self.qc_matches[k2][k1] = 'sibling'
                        if r.lower() == 'aunt' or r.lower() == 'uncle':
                            if self.sex[k1].lower() == 'f':
                                self.qc_matches[k2][k1] = 'niece'
                            if self.sex[k1].lower() == 'm':
                                self.qc_matches[k2][k1] = 'nephew'
                        if r.lower() == 'grandchild':
                            if self.sex[k1].lower() == 'f':
                                self.qc_matches[k2][k1] = 'grandmother'
                            if self.sex[k1].lower() == 'm':
                                self.qc_matches[k2][k1] = 'grandfather'
                        if r.lower() == 'grandmother' or r.lower() == 'grandfather':
                            self.qc_matches[k2][k1] = 'grandchild'
                        if r.lower() == 'niece' or r.lower() == 'nephew':
                            if self.sex[k1].lower() == 'f':
                                self.qc_matches[k2][k1] = 'aunt'
                            if self.sex[k1].lower() == 'm':
                                self.qc_matches[k2][k1] = 'uncle'
                else:
                    if r.lower() == 'mother' or r.lower() == 'father':
                        opp_rel = {}
                        opp_rel[k1] = 'child'
                        self.qc_matches[k2] = opp_rel
                    if r.lower() == 'child':
                        if self.sex[k1].lower() == 'f':
                            opp_rel = {}
                            opp_rel[k1] = 'mother'
                            self.qc_matches[k2] = opp_rel
                        if self.sex[k1].lower() == 'm':
                            opp_rel = {}
                            opp_rel[k1] = 'father'
                            self.qc_matches[k2] = opp_rel
                    if r.lower() == 'sibling':
                        opp_rel = {}
                        opp_rel[k1] = 'sibling'
                        self.qc_matches[k2] = opp_rel
                    if r.lower() == 'aunt' or r.lower() == 'uncle':
                        if self.sex[k1].lower() == 'f':
                            opp_rel = {}
                            opp_rel[k1] = 'niece'
                            self.qc_matches[k2] = opp_rel
                        if self.sex[k1].lower() == 'm':
                            opp_rel = {}
                            opp_rel[k1] = 'nephew'
                            self.qc_matches[k2] = opp_rel
                    if r.lower() == 'grandchild':
                        if self.sex[k1].lower() == 'f':
                            opp_rel = {}
                            opp_rel[k1] = 'grandmother'
                            self.qc_matches[k2] = opp_rel
                        if self.sex[k1].lower() == 'm':
                            opp_rel = {}
                            opp_rel[k1] = 'grandfather'
                            self.qc_matches[k2] = opp_rel
                    if r.lower() == 'grandmother' or r.lower() == 'grandfather':
                        opp_rel = {}
                        opp_rel[k1] = 'grandchild'
                        self.qc_matches[k2] = opp_rel
                    if r.lower() == 'niece' or r.lower() == 'nephew':
                        if self.sex[k1].lower() == 'f':
                            opp_rel = {}
                            opp_rel[k1] = 'aunt'
                            self.qc_matches[k2] = opp_rel
                        if self.sex[k1].lower() == 'm':
                            opp_rel = {}
                            opp_rel[k1] = 'uncle'
                            self.qc_matches[k2] = opp_rel

    ### infer familial relationships
    def infer_matches(self):
        qc_matches_copy = copy.deepcopy(self.qc_matches)
        for k1, v in qc_matches_copy.items():
            for k2, r1 in v.items():
                for k3, r2 in qc_matches_copy[k2].items():
                    if k3 not in qc_matches_copy[k1] and k3 != k1:
                        if r1.lower() == 'mother' or r1.lower() == 'father':
                            if r2.lower() == 'aunt':
                                self.qc_matches[k1][k3] = 'grandaunt'
                            elif r2.lower() == 'uncle':
                                self.qc_matches[k1][k3] = 'granduncle'
                            elif r2.lower() == 'child':
                                self.qc_matches[k1][k3] = 'sibling'
                            elif r2.lower() == 'grandmother':
                                self.qc_matches[k1][k3] = 'great-grandparent'
                            elif r2.lower() == 'grandfather':
                                self.qc_matches[k1][k3] = 'great-grandparent'
                            elif r2.lower() == 'nephew' or r2.lower() == 'niece':
                                self.qc_matches[k1][k3] = 'cousin'
                            elif r2.lower() == 'mother' or r2.lower() == 'father':
                                if self.sex[k3].lower() == 'f':
                                    self.qc_matches[k1][k3] = 'grandmother'
                                elif self.sex[k3].lower() == 'm':
                                    self.qc_matches[k1][k3] = 'grandfather'
                            elif r2.lower() == 'sibling':
                                if self.sex[k3].lower() == 'f':
                                    self.qc_matches[k1][k3] = 'aunt'
                                elif self.sex[k3].lower() == 'm':
                                    self.qc_matches[k1][k3] = 'uncle'
                        elif r1.lower() == 'child':
                            if r2.lower() == 'child':
                                self.qc_matches[k1][k3] = 'grandchild'
                            elif r2.lower() == 'grandchild':
                                self.qc_matches[k1][k3] = 'great-grandchild'
                            elif r2.lower() == 'mother' or r2.lower() == 'father':
                                self.qc_matches[k1][k3] = 'spouse'
                            elif r2.lower() == 'sibling':
                                self.qc_matches[k1][k3] = 'child'
                        elif r1.lower() == 'sibling':
                            if r2.lower() == 'aunt':
                                self.qc_matches[k1][k3] = 'aunt'
                            elif r2.lower() == 'uncle':
                                self.qc_matches[k1][k3] = 'uncle'
                            elif r2.lower() == 'grandmother':
                                self.qc_matches[k1][k3] = 'grandmother'
                            elif r2.lower() == 'grandfather':
                                self.qc_matches[k1][k3] = 'grandfather'
                            elif r2.lower() == 'mother':
                                self.qc_matches[k1][k3] = 'mother'
                            elif r2.lower() == 'father':
                                self.qc_matches[k1][k3] = 'father'
                            elif r2.lower() == 'sibling':
                                self.qc_matches[k1][k3] = 'sibling'
                        elif r1.lower() == 'aunt' or r1.lower() == 'uncle':
                            if r2.lower() == 'child':
                                self.qc_matches[k1][k3] = 'cousin'
                        elif r1.lower() == 'grandchild':
                            if r2.lower() == 'child':
                                self.qc_matches[k1][k3] = 'great-grandchild'
                            elif r2.lower() == 'grandchild':
                                self.qc_matches[k1][k3] = 'great-great-grandchild'
                            elif r2.lower() == 'grandmother' or r2.lower() == 'grandfather':
                                self.qc_matches[k1][k3] = 'spouse'
                            elif r2.lower() == 'sibling':
                                self.qc_matches[k1][k3] = 'grandchild'
                        elif r1.lower() == 'grandmother' or r1.lower() == 'grandfather':
                            if r2.lower() == 'mother' or r2.lower() == 'father':
                                self.qc_matches[k1][k3] = 'great-grandparent'
                            elif r2.lower() == 'sibling':
                                if self.sex[k3].lower() == 'f':
                                    self.qc_matches[k1][k3] = 'grandaunt'
                                elif self.sex[k3].lower() == 'm':
                                    self.qc_matches[k1][k3] = 'granduncle'
    
    def assignFamily(self, result):
        G = nx.Graph()
        edges = []
        for i in self.qc_matches:
            for j in self.qc_matches[i]:
                edges.append((i, j))
        G.add_edges_from(edges)
        #graph = list(nx.connected_component_subgraphs(G))
        comp = sorted(nx.connected_components(G), key = len, reverse=True)

        outfh = open(result, 'w')
        writer = csv.writer(outfh)
        writer.writerow(['family_id', 'individual_id'])
                            
        for family_id in range(len(comp)):
            for individual_id in comp[family_id]:
                writer.writerow([family_id+1, individual_id]) 
        outfh.close()
    
    def test(self):
        outfh = open('relationship_for_each.csv', 'w')
        writer = csv.writer(outfh)
        writer.writerow(['patient_ID1', 'patient_ID2', 'relationship'])
        for i in self.qc_matches:
            for j in self.qc_matches[i]:
                print(i, self.qc_matches[i])
                writer.writerow([i, j, self.qc_matches[i][j]])