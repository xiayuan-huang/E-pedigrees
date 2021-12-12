'''

@author: xiayuanhuang

'''

import sys
import csv
import copy
import networkx as nx

from fppa import fppa

class matches(object):
    def __init__(self, ped, ec, sex, p_c, gender, familyOut):
        self.pedFile = ped
        self.ec = ec
        self.sex = sex
        self.fppa_pair = p_c
        self.gender = gender
        self.familyTree = familyOut

        self.readPed()
        self.infer()
        self.pedigree()

    def readPed(self):
        self.new_ped_mo = {}
        self.new_ped_fa = {}
        self.new_ped_sex = {}

        reader = csv.reader(open(self.pedFile, 'rU'), delimiter=',')
        #exp_header = ['MRN', 'FirstName', 'LastName', 'PhoneNumber', 'Zipcode']
        exp_header = ['familyID', 'family_member', 'study_ID', 'StudyID_MATERNAL', 'StudyID_PATERNAL', 'Sex']
        h = next(reader)
        if not h == exp_header:
            raise Exception("Patient demographic data file (%s) doesn't have the header expected:%s" % (self.pedFile, exp_header))
        
        try:
            for i, (fam_id, mem_num, p_id, mother_id, father_id, sex) in enumerate(reader):
                if mother_id != '':
                    self.new_ped_mo[p_id] = mother_id
                if fam_id != '':
                    self.new_ped_fa[p_id] = father_id
                self.new_ped_sex[p_id] = sex
        except Exception as e:
            #print >> sys.stderr, "Failed with error: %s" % csv.Error
            print(sys.stderr, "Failed in %s at line: %d with error: %s" % (self.pedFile, i+2, e))
            sys.exit(20)

    def infer(self):
        self.fppa_mo = {}
        self.fppa_fa = {}
        self.edges = []
        self.ec_mo = {}
        self.ec_fa = {}

        for i in self.fppa_pair:
            for j in self.fppa_pair[i]:
                if self.fppa_pair[i][j].lower() == 'mother':
                    self.fppa_mo[i] = j
                if self.fppa_pair[i][j].lower() == 'father':
                    self.fppa_fa[i] = j

        ### break conflicted parent child relationships of fppa and new PED

        fppa_mo_copy = copy.deepcopy(self.fppa_mo)
        for i in fppa_mo_copy:
            if i in self.new_ped_mo:
                if fppa_mo_copy[i] != self.new_ped_mo[i]:
                    del self.fppa_mo[i]

        fppa_fa_copy = copy.deepcopy(self.fppa_fa)
        for i in fppa_fa_copy:
            if i in self.new_ped_fa:
                if fppa_fa_copy[i] != self.new_ped_fa[i]:
                    del self.fppa_fa[i]

        ### break conflicted parent child relationships from PED and RIFTEHR
        for i in self.ec:
            for j in self.ec[i]:
                self.edges.append((i, j))
                if self.ec[i][j].lower() == 'mother':
                    self.ec_mo[i] = j
                if self.ec[i][j].lower() == 'father':
                    self.ec_fa[i] = j

        new_ped_mo_copy = copy.deepcopy(self.new_ped_mo)
        for i in new_ped_mo_copy:
            if i in self.ec_mo:
                if new_ped_mo_copy[i] != self.ec_mo[i]:
                    del self.new_ped_mo[i]
        new_ped_fa_copy = copy.deepcopy(self.new_ped_fa)
        for i in new_ped_fa_copy:
            if i in self.ec_fa:
                if new_ped_fa_copy[i] != self.ec_fa[i]:
                    del self.new_ped_fa[i]

        ### add the rest of edges

        for i in self.fppa_mo:
            self.edges.append((i, self.fppa_mo[i]))
        for i in self.fppa_fa:
            self.edges.append((i, self.fppa_fa[i]))
        for i in self.new_ped_mo:
            self.edges.append((i, self.new_ped_mo[i]))
        for i in self.new_ped_fa:
            self.edges.append((i, self.new_ped_fa[i]))


    def pedigree(self):
        G = nx.Graph()
        G.add_edges_from(self.edges)

        comp = sorted(nx.connected_components(G), key = len, reverse=True)

        outfh = open(out, 'w')
        writer = csv.writer(outfh)
        writer.writerow(['familyID', 'family_member', 'study_ID', 'StudyID_MATERNAL', 'StudyID_PATERNAL', 'Sex'])

        for family_id in range(len(comp)):
            for individual_id in comp[family_id]:
                member_num = len(comp[family_id])

                if individual_id in self.fppa_mo:
                    mo = self.fppa_mo[individual_id]
                elif individual_id in self.new_ped_mo:
                    mo = self.new_ped_mo[individual_id]
                elif individual_id in self.ec_mo:
                    mo = self.ec_mo[individual_id]
                else:
                    mo = ''

                if individual_id in self.fppa_fa:
                    fa = self.fppa_fa[individual_id]
                elif individual_id in self.new_ped_fa:
                    fa = self.new_ped_fa[individual_id]
                elif individual_id in  self.ec_fa:
                    fa = self.ec_fa[individual_id]
                else:
                    fa = ''

                if individual_id in self.sex:
                    sex = self.sex[individual_id]
                elif individual_id in self.gender:
                    sex = self.gender[individual_id]
                elif individual_id in self.new_ped_sex:
                    sex = self.new_ped_sex[individual_id]
                else:
                    sex = ''
                
                writer.writerow([family_id+1, member_num, individual_id, mo, fa, sex])
        outfh.close()

