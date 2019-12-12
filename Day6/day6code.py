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
        grandparents = []
        parent = self.parent
        at_root = False
        while not at_root:
            parent = parent.parent
            grandparents.append(parent.id)
            if parent.id == 'COM':
                at_root = True
        return grandparents

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

print([o.id for o in objects.values()])

orbits = 0
for object in objects.values():
    print(object.id)
    if object.id == 'COM':
        continue
    at_root = False
    while not at_root:
        parent = object.parent
        orbits += 1
        object = parent
        if parent.id == 'COM':
            at_root = True

print(orbits)


my_gp = objects['YOU'].grandparents()
santa_gp = objects['SAN'].grandparents()

def first_common_grandparent(gp1, gp2):
    for gp_a in gp1:
        for gp_b in gp2:
            if gp_a == gp_b:
                return gp_a

common = first_common_grandparent(my_gp, santa_gp)
print('Common: ', common)

dist1 = my_gp.index(common)
dist2 = santa_gp.index(common)

print(dist1 + dist2)