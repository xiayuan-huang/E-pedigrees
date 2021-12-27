'''

@author: xiayuanhuang
'''

'''

infer family relationships by combining FPPA and RIFTEHR
'''

import csv
import networkx as nx
import copy

class matches(object):
    def __init__(self, riftehr_relation_pair, sex, fppa_relation_pair, gender, familyTreeOutput):
        ### gender of patient from fppa
        self.p_c_gender = gender
        ### parent child relationship pairs from fppa
        self.p_c = fppa_relation_pair
        ### relationship pairs from emergency contact (RIFTEHR)
        self.ec = riftehr_relation_pair
        ### sex of patient from riftehr
        self.sex = sex
        ### output family pedigree
        self.famOut = familyTreeOutput

        self.updateFPPA_relation()
        #self.assignFamilies()

    def updateFPPA_relation(self):
        self.fppa_pair = {}
        self.famIDChanged = set()
        for i in self.p_c:
            c = i[0]
            p = i[1]
            if c in self.fppa_pair:
                if self.p_c_gender[p].lower() == 'f':
                    self.fppa_pair[c][p] = 'mother'
                elif self.p_c_gender[p].lower() == 'm':
                    self.fppa_pair[c][p] = 'father'
            else:
                rel = {}
                if self.p_c_gender[p].lower() == 'f':
                    rel[p] = 'mother'
                elif self.p_c_gender[p].lower() == 'm':
                    rel[p] = 'father'
                self.fppa_pair[c] = rel
        ### delete variable
        del self.p_c

        ### delete conflicted parent_child pairs with 
        qc_matches_copy = copy.deepcopy(self.fppa_pair)
        for k1, v in qc_matches_copy.items():
            if k1 in self.ec:
                for k2, r1 in v.items():
                    if k2 in self.ec and k2 in self.ec[k1]:
                        if r1.lower() != self.ec[k1][k2]:
                            del self.fppa_pair[k1][k2]
                            self.famIDChanged.add(k1)
                    else:
                        for i in self.ec[k1]:
                            if r1 == self.ec[k1][i] and i != k2:
                                del self.fppa_pair[k1][k2]
                                self.famIDChanged.add(k1)
        ### k1 not in ec, parents of k1 in ec
            else:
                for k2 in v:
                    pa = []
                    if k2 in self.ec:
                        pa.append(k2)
                if len(pa) == 2:
                    if self.ec == 'spouse':
                        pass
                    else:
                        del self.fppa_pair[k1][k2]
                        self.famIDChanged.add(k1)
        ### delete variable
        del qc_matches_copy

        ### create opposite relationship
        fppa_pair_copy = copy.deepcopy(self.fppa_pair)
        for i in fppa_pair_copy:
            for j in fppa_pair_copy[i]:
                if j in self.fppa_pair:
                    self.fppa_pair[j][i] = 'child'
                else:
                    rel = {}
                    rel[i] = 'child'
                    self.fppa_pair[j] = rel
        ### delete variable
        del fppa_pair_copy
        
        ### infer additional relationships, first degree
        qc_matches_copy = copy.deepcopy(self.fppa_pair)
        for k1, v in qc_matches_copy.items():
            for k2, r1 in v.items():
                for k3, r2 in qc_matches_copy[k2].items():
                    if k3 not in qc_matches_copy[k1] and k3 != k1:
                        if r1.lower() == 'mother' or r1.lower() == 'father':
                            if r2.lower() == 'mother':
                                self.fppa_pair[k1][k3] = 'grandmother'
                            elif r2.lower() == 'father':
                                self.fppa_pair[k1][k3] = 'grandfather'
                            elif r2.lower() == 'child':
                                self.fppa_pair[k1][k3] = 'sibling'
                        elif r1.lower() == 'child':
                            if r2.lower() == 'mother' or r2.lower() == 'father':
                                self.fppa_pair[k1][k3] = 'spouse'
                            elif r2.lower() == 'child':
                                self.fppa_pair[k1][k3] = 'grandchild'
        ### delete variable
        del qc_matches_copy
        
        qc_matches_copy = copy.deepcopy(self.fppa_pair)
        for k1, v in qc_matches_copy.items():
            for k2, r1 in v.items():
                for k3, r2 in qc_matches_copy[k2].items():
                    if k3 not in qc_matches_copy[k1] and k3 != k1:
                        if r1.lower() == 'mother' or r1.lower() == 'father':
                            if r2.lower() == 'mother':
                                self.fppa_pair[k1][k3] = 'grandmother'
                            elif r2.lower() == 'father':
                                self.fppa_pair[k1][k3] = 'grandfather'
                            elif r2.lower() == 'child':
                                self.fppa_pair[k1][k3] = 'sibling'
                            elif r2.lower() == 'grandmother' or r2.lower() == 'grandfather':
                                self.fppa_pair[k1][k3] = 'great-grandparent'
                            elif r2.lower() == 'sibling':
                                if self.p_c_gender[k3].lower() == 'f':
                                    self.fppa_pair[k1][k3] = 'aunt'
                                elif self.p_c_gender[k3].lower() == 'm':
                                    self.fppa_pair[k1][k3] = 'uncle'
                        elif r1.lower() == 'child':
                            if r2.lower() == 'child':
                                self.fppa_pair[k1][k3] = 'grandchild'
                            elif r2.lower() == 'grandchild':
                                self.fppa_pair[k1][k3] = 'great-grandchild'
                            elif r2.lower() == 'mother' or r2.lower() == 'father':
                                self.fppa_pair[k1][k3] = 'spouse'
                            elif r2.lower() == 'sibling':
                                self.fppa_pair[k1][k3] = 'child'
                        elif r1.lower() == 'sibling':
                            if r2.lower() == 'aunt':
                                self.fppa_pair[k1][k3] = 'aunt'
                            elif r2.lower() == 'uncle':
                                self.fppa_pair[k1][k3] = 'uncle'
                            elif r2.lower() == 'child':
                                if self.p_c_gender[k3] == 'f':
                                    self.fppa_pair[k1][k3] = 'niece'
                                elif self.p_c_gender[k3] == 'm':
                                    self.fppa_pair[k1][k3] = 'nephew'
                            elif r2.lower() == 'grandchild':
                                if self.p_c_gender[k3] == 'f':
                                    self.fppa_pair[k1][k3] = 'grandniece'
                                elif self.p_c_gender[k3] == 'm':
                                    self.fppa_pair[k1][k3] = 'grandnephew'
                            elif r2.lower() == 'grandmother':
                                self.fppa_pair[k1][k3] = 'grandmother'
                            elif r2.lower() == 'grandfather':
                                self.fppa_pair[k1][k3] = 'grandfather'
                            elif r2.lower() == 'mother':
                                self.fppa_pair[k1][k3] = 'mother'
                            elif r2.lower() == 'father':
                                self.fppa_pair[k1][k3] = 'father'
                            elif r2.lower() == 'sibling':
                                self.fppa_pair[k1][k3] = 'sibling'
                        elif r1.lower() == 'grandchild':
                            if r2.lower() == 'child':
                                self.fppa_pair[k1][k3] = 'great-grandchild'
                            elif r2.lower() == 'grandchild':
                                self.fppa_pair[k1][k3] = 'great-great-grandchild'
                            elif r2.lower() == 'grandmother' or r2.lower() == 'grandfather':
                                self.fppa_pair[k1][k3] = 'spouse'
                            elif r2.lower() == 'sibling':
                                self.fppa_pair[k1][k3] = 'grandchild'
                        elif r1.lower() == 'grandmother' or r1.lower() == 'grandfather':
                            if r2.lower() == 'aunt':
                                self.fppa_pair[k1][k3] = 'great-grandaunt'
                            elif r2.lower() == 'uncle':
                                self.fppa_pair[k1][k3] = 'great-granduncle'
                            elif r2.lower() == 'grandmother':
                                self.fppa_pair[k1][k3] = 'great-great-grandparent'
                            elif r2.lower() == 'grandfather':
                                self.fppa_pair[k1][k3] = 'great-great-grandparent'
                            elif r2.lower() == 'mother' or r2.lower() == 'father':
                                self.fppa_pair[k1][k3] = 'great-grandparent'
                            elif r2.lower() == 'sibling':
                                if self.p_c_gender[k3] == 'f':
                                    self.fppa_pair[k1][k3] = 'grandaunt'
                                elif self.p_c_gender[k3] == 'm':
                                    self.fppa_pair[k1][k3] = 'granduncle'
        ### delete variable
        del qc_matches_copy
        
        qc_matches_copy = copy.deepcopy(self.fppa_pair)
        for k1, v in qc_matches_copy.items():
            for k2, r1 in v.items():
                for k3, r2 in qc_matches_copy[k2].items():
                    if k3 not in qc_matches_copy[k1] and k3 != k1:
                        if r1.lower() == 'mother' or r1.lower() == 'father':
                            if  r2.lower() == 'aunt':
                                self.fppa_pair[k1][k3] = 'grandaunt'
                            elif r2.lower() == 'uncle':
                                self.fppa_pair[k1][k3] = 'granduncle'
                            elif r2.lower() == 'niece' or r2.lower() == 'nephew':
                                self.fppa_pair[k1][k3] = 'cousin'
                            elif r2.lower() == 'sibling':
                                if self.p_c_gender[k3] == 'f':
                                    self.fppa_pair[k1][k3] = 'aunt'
                                elif self.p_c_gender[k3] == 'm':
                                    self.fppa_pair[k1][k3] = 'uncle'
                        elif r1.lower() == 'sibling':
                            if r2.lower() == 'aunt':
                                self.fppa_pair[k1][k3] = 'aunt'
                            elif r2.lower() == 'uncle':
                                self.fppa_pair[k1][k3] = 'uncle'
                            elif r2.lower() == 'child':
                                if self.p_c_gender[k3] == 'f':
                                    self.fppa_pair[k1][k3] = 'niece'
                                elif self.p_c_gender[k3] == 'm':
                                    self.fppa_pair[k1][k3] = 'nephew'
                        elif r1.lower() == 'aunt' or r1.lower() == 'uncle':
                            if r2.lower() == 'child':
                                self.fppa_pair[k1][k3] = 'cousin'
                        elif r1.lower() == 'niece':
                            if r2.lower() == 'child':
                                self.fppa_pair[k1][k3] = 'grandniece'
                            elif r2.lower() == 'grandchild':
                                self.fppa_pair[k1][k3] = 'great-grandniece'
                        elif r1.lower() == 'nephew':
                            if r2.lower() == 'child':
                                self.fppa_pair[k1][k3] = 'grandnephew'
                            elif r2.lower() == 'grandchild':
                                self.fppa_pair[k1][k3] = 'great-grandnephew'
        ### delete variable
        del qc_matches_copy

        ### break conflicts, pay attention here
        break_pairs = copy.deepcopy(self.fppa_pair)
        for k1, v in break_pairs.items():
            if k1 not in self.ec or k1 not in self.fppa_pair:
                continue
            for k2, r1 in v.items():
                if k2 in self.ec[k1]:
                    if r1.lower() != self.ec[k1][k2].lower():
                        #del self.fppa_pair[k1][k2]
                        if r1.lower() == 'sibling':
                            if self.ec[k1][k2].lower() == 'spouse':
                                for pa in break_pairs[k1]:
                                    if pa in self.fppa_pair[k1]:
                                        if self.fppa_pair[k1][pa].lower() == 'mother' or self.fppa_pair[k1][pa].lower() == 'father':
                                            if k2 in self.fppa_pair and pa in self.fppa_pair[k2]:
                                                del self.fppa_pair[k1][pa]
                                                del self.fppa_pair[k2][pa]
                                                self.famIDChanged.add(k1)
                                                if pa in self.fppa_pair:
                                                    if k1 in self.fppa_pair[pa]:
                                                        del self.fppa_pair[pa][k1]
                                                    if k2 in self.fppa_pair[pa]:
                                                        del self.fppa_pair[pa][k2]
                            #elif self.ec[k1][k2] == 'child' or self.ec[k2][k1] == 'child':
                            elif self.ec[k1][k2].lower() == 'child' or self.ec[k1][k2].lower() == 'mother' or self.ec[k1][k2].lower() == 'father':
                                if k2 in self.fppa_pair[k1]:
                                    del self.fppa_pair[k1][k2]
                                    self.famIDChanged.add(k1)
                                for mem in break_pairs[k1]:
                                    if k2 in self.fppa_pair:
                                        if mem in self.fppa_pair[k2]:
                                            del self.fppa_pair[k2][mem]
                                            if mem in self.fppa_pair[k1]:
                                                del self.fppa_pair[k1][mem]
                                            if mem in self.fppa_pair:
                                                if k1 in self.fppa_pair[mem]:
                                                    del self.fppa_pair[mem][k1]
                                                if k2 in self.fppa_pair[mem]:
                                                    del self.fppa_pair[mem][k2]
                            #elif self.ec[k1][k2] == 'niece' or self.ec[k1][k2] == 'nephew' or self.ec[k2][k1] == 'niece' or self.ec[k2][k1] == 'nephew':
                            elif self.ec[k1][k2].lower() == 'niece' or self.ec[k1][k2].lower() == 'nephew':
                                for pa in break_pairs[k1]:
                                    if break_pairs[k1][pa].lower() == 'mother' or break_pairs[k1][pa].lower() == 'father':
                                        if k2 in self.fppa_pair:
                                            if pa in self.fppa_pair[k2]:
                                                del self.fppa_pair[k2][pa]
                                                self.famIDChanged.add(k2)
                                                if pa in self.fppa_pair[k1]:
                                                    del self.fppa_pair[k1][pa]
                                                if pa in self.fppa_pair:
                                                    if k1 in self.fppa_pair[pa]:
                                                        del self.fppa_pair[pa][k1]
                                                    if k2 in self.fppa_pair[pa]:
                                                        del self.fppa_pair[pa][k2]
                        elif r1.lower() == 'mother' or r1.lower() == 'father':
                            if k2 in self.fppa_pair[k1]:
                                del self.fppa_pair[k1][k2]
                                self.famIDChanged.add(k1)
                if r1.lower() == 'mother':
                    for mem in self.ec[k1]:
                        if self.ec[k1][mem].lower() == 'mother':
                            if mem != k2:
                                if k1 in self.fppa_pair and k2 in self.fppa_pair[k1]:
                                    del self.fppa_pair[k1][k2]
                                    self.famIDChanged.add(k1)
                if r1.lower() == 'father':
                    for mem in self.ec[k1]:
                        if self.ec[k1][mem].lower() == 'father':
                            if mem != k2:
                                if k1 in self.fppa_pair and k2 in self.fppa_pair[k1]:
                                    del self.fppa_pair[k1][k2]
                                    self.famIDChanged.add(k1)


        ### delete variable
        del break_pairs

        # delete empty relationship dictionary
        fppa_pair_copy = copy.deepcopy(self.fppa_pair)
        for i in fppa_pair_copy:
            if i in self.fppa_pair:
                if not bool(self.fppa_pair[i]):
                    del self.fppa_pair[i]
            
        ### unsolved conflits
        self.conflit_id_pool = set()
        for i in self.fppa_pair:
            if i in self.ec:
                for j in self.fppa_pair[i]:
                    if j in self.ec[i]:
                        if self.fppa_pair[i][j] != self.ec[i][j]:
                            self.conflit_id_pool.add(i)
                            self.conflit_id_pool.add(j)

    def assignFamilies(self):
        self.edges = []
        child_mother = {}
        child_father = {}
        ec_child_mother = {}
        ec_child_father = {}

        ec_relationship_reference = set()

        for i in self.fppa_pair:
            for j in self.fppa_pair[i]:
                if self.fppa_pair[i][j].lower() == 'mother':
                    self.edges.append((i, j))
                    child_mother[i] = j
                if self.fppa_pair[i][j].lower() == 'father':
                    self.edges.append((i, j))
                    child_father[i] = j
        for i in self.ec:
            for j in self.ec[i]:
                self.edges.append((i, j))
                if self.ec[i][j].lower() == 'mother':
                    ec_child_mother[i] = j
                if self.ec[i][j].lower() == 'father':
                    ec_child_father[i] = j
                if i in self.fppa_pair and j not in self.fppa_pair:
                    ec_relationship_reference.add((i, j, self.ec[i][j]))
                if i not in self.fppa_pair and j in self.fppa_pair:
                    ec_relationship_reference.add((j, i, self.ec[j][i]))
        G = nx.Graph()
        G.add_edges_from(self.edges)

        comp = sorted(nx.connected_components(G), key = len, reverse=True)

        outfh = open(self.famOut, 'w')
        writer = csv.writer(outfh)
        writer.writerow(['family_id', 'family_member', 'individual_id', 'Maternal', 'Paternal', 'Sex'])

        outConflict = open('conflit_family.csv', 'w')
        writer_conflict = csv.writer(outConflict)
        writer_conflict.writerow(['family_id_conflict'])

        ec_refer = open('ec_relationship_reference.csv', 'w')
        writer_reference = csv.writer(ec_refer)
        writer_reference.writerow(['study_id1', 'study_id2', 'relationship'])

        outChangedFamily = open('changed_family.csv', 'w')
        writer_changed = csv.writer(outChangedFamily)
        writer_changed.writerow(['FamilyID'])

        conflict_family_id = set()
        changed_family_id = set()

        for family_id in range(len(comp)):
            flag = False
            flag_changed = False
            for individual_id in comp[family_id]:
                member_num = len(comp[family_id])
                if flag == False and individual_id in self.conflit_id_pool:
                    flag = True
                if individual_id in child_mother:
                    mo = child_mother[individual_id]
                else:
                    mo = ''
                if individual_id in child_father:
                    fa = child_father[individual_id]
                else:
                    fa = ''
                if individual_id in self.p_c_gender:
                    sex = self.p_c_gender[individual_id]
                elif individual_id in self.sex:
                    sex = self.sex[individual_id]
                else:
                    sex = ''
                writer.writerow([family_id+1, member_num, individual_id, mo, fa, sex])
                if flag_changed ==False and individual_id in self.famIDChanged:
                    flag_changed = True
            if flag_changed:
                changed_family_id.add(family_id+1)
                writer_changed.writerow(family_id+1)
            if flag:
                conflict_family_id.add(family_id+1)
                writer_conflict.writerow([family_id+1])
        
        for i in ec_relationship_reference:
            writer_reference.writerow([i[0], i[1], i[2]])

        outfh.close()
        outConflict.close()
        ec_refer.close()
        outChangedFamily.close()
