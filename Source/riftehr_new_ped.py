'''

@author: xiayuanhuang

'''

import csv
import sys
import copy
import networkx as nx

class matches(object):
    def __init__(self, ped, matches, sex, famTree):
        self.pedFile = ped
        self.qc_matches = matches
        self.sex = sex
        self.familyTree = famTree

        self.readPed()
        self.infer()
        self.pedigree(self.familyTree)

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

    ### infer new relationships and break conflicts
    ### here assume new PED is reliable
    ### later improvements can be done if new PED is not relable
    
    def infer(self):
        self.rifter_mo = {}
        self.rifter_fa = {}
        self.edges = []

        for i in self.qc_matches:
            for j in self.qc_matches[i]:
                self.edges.append((i, j))
                if self.qc_matches[i][j] == 'mother':
                    self.rifter_mo[i] = j
                if self.qc_matches[i][j] == 'father':
                    self.rifter_fa[i] = j
        
        new_ped_mo_copy = copy.deepcopy(self.new_ped_mo)
        for i in new_ped_mo_copy:
            if i in self.rifter_mo:
                if new_ped_mo_copy[i] != self.rifter_mo[i]:
                    del self.new_ped_mo[i]

        new_ped_fa_copy = copy.deepcopy(self.new_ped_fa)
        for i in new_ped_fa_copy:
            if i in self.rifter_fa:
                if new_ped_fa_copy[i] != self.new_ped_fa[i]:
                    del self.new_ped_fa[i]

        for i in self.new_ped_mo:
            self.edges.append((i, self.new_ped_mo[i]))
        for i in self.new_ped_fa:
            self.edges.append((i, self.new_ped_fa[i]))


    def pedigree(self, out):
        G = nx.Graph()
        G.add_edges_from(self.edges)

        comp = sorted(nx.connected_components(G), key = len, reverse=True)

        outfh = open(out, 'w')
        writer = csv.writer(outfh)
        writer.writerow(['familyID', 'family_member', 'study_ID', 'StudyID_MATERNAL', 'StudyID_PATERNAL', 'Sex'])

        for family_id in range(len(comp)):
            for individual_id in comp[family_id]:
                member_num = len(comp[family_id])
                if individual_id in self.rifter_mo:
                    mo = self.rifter_mo[individual_id]
                else:
                    if individual_id in self.new_ped_mo:
                        mo = self.new_ped_mo[individual_id]
                    else:
                        mo = ''
                
                if individual_id in self.rifter_fa:
                    fa = self.rifter_fa[individual_id]
                else:
                    if individual_id in self.new_ped_fa:
                        fa = self.new_ped_fa[individual_id]
                    else:
                        fa = ''
                
                if individual_id in self.sex:
                    sex = self.sex[individual_id]
                elif individual_id in self.new_ped_sex:
                    sex = self.new_ped_sex[individual_id]
                else:
                    sex = ''

                writer.writerow([family_id+1, member_num, individual_id, mo, fa, sex]) 
        outfh.close()