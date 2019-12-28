# Ideas stolen from jeffjeffjeffrey

from collections import defaultdict
from math import ceil
from queue import Queue


def read_input(file):
    with open(file, 'r') as f:
       text = f.read()
    recipe_texts = text.splitlines(False)
    recipes = {}
    for recipe_text in recipe_texts:
        recipe = Recipe(recipe_text)
        recipes[recipe.product.name] = recipe
    return recipes


class Recipe:

    def __init__(self, recipe_text):
        self.ingredients = []
        self.parse_inputs(recipe_text)

    def parse_inputs(self, text):
        ingredients, products = text.split(' => ')
        ingredients = ingredients.split(', ')
        for reactant in ingredients:
            self.ingredients.append(Ingredient(*reactant.split(' ')))
        self.product = Ingredient(*products.split(' '))


class Ingredient:
    def __init__(self, quantity, name):
        self.quantity = int(quantity)
        self.name = name


class Nanofactory:

    def __init__(self, recipes):
        self.recipes = recipes
        self.orders = Queue()
        self.supply = defaultdict(int)

    def make_fuel(self, amount):
        self.orders.put(Ingredient(amount, "FUEL"))
        ore_needed = 0
        while not self.orders.empty():
            order = self.orders.get()
            if order.name == "ORE":
                ore_needed += order.quantity
            elif order.quantity <= self.supply[order.name]:
                self.supply[order.name] -= order.quantity
            else:
                amount_needed = order.quantity - self.supply[order.name]
                recipe = self.recipes[order.name]
                batches = ceil(amount_needed / recipe.product.quantity)
                for ingredient in recipe.ingredients:
                    self.orders.put(Ingredient(ingredient.quantity * batches, ingredient.name))
                    leftover_amount = batches * recipe.product.quantity - amount_needed
                    self.supply[order.name] = leftover_amount
        return ore_needed


if __name__ == "__main__":
    reactions = read_input('input.txt')
    nanofactory = Nanofactory(reactions)
    required = nanofactory.make_fuel(1)
    print(required)
