## The Tyranny of the Rocket Equation

with open("input.txt", 'r') as f:
    components = f.readlines()
components = [int(c) for c in components]
print(components)

required_fuel = [c//3-2 for c in components]
total_fuel = sum(required_fuel)

print(total_fuel)

##  need to account for weight of fuel

fuel = []
for component in components:
    fuel_requirement = component // 3 - 2
    completed = False
    additional_fuel = []
    extra_fuel = fuel_requirement
    while not completed:
        extra_fuel = extra_fuel // 3 - 2
        if extra_fuel > 0:
            additional_fuel.append(extra_fuel)
        else:
            completed = True
    fuel.append(fuel_requirement + sum(additional_fuel))

print(sum(fuel))