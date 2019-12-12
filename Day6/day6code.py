# Universal Orbit Map

# Whenever A orbits B and B orbits C, then A INDIRECTLY ORBITS C

with open('input.txt', 'r') as f:
    test_input = f.read()
test_input = test_input.split('\n')[:-1]

class orbiter:
    def __init__(self, id, parent):
        self.id = id
        self.parent = parent

    def grandparents(self):
        if self.parent.id == 'COM':
            return []
        grandparents = []
        parent = self.parent
        at_root = False
        while not at_root:
            parent = parent.parent
            grandparents.append(parent.id)
            if parent.id == 'COM':
                at_root = True
        return grandparents

    def parents(self):
        if self.parent == None:
            return []
        else:
            return [self.parent] + self.grandparents()

objects = {}
for relationship in test_input:
    parent, child = relationship.split(')')
    if parent not in objects.keys():
        objects[parent] = orbiter(parent, None)
    if child not in objects.keys():
        objects[child] = orbiter(child, objects[parent])
    else:
        if objects[child].parent == None:
            objects[child].parent = objects[parent]


print('Total orbits: ', sum([len(o.parents()) for o in objects.values()]))

my_gp = objects['YOU'].parents()
santa_gp = objects['SAN'].parents()

def first_common_parent(gp1, gp2):
    for gp_a in gp1:
        for gp_b in gp2:
            if gp_a == gp_b:
                return gp_a

common = first_common_parent(my_gp, santa_gp)

dist1 = my_gp.index(common)
dist2 = santa_gp.index(common)

print('Number of transfers: ', dist1 + dist2)

