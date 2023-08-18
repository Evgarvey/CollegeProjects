import random

# CIS 400 Assignment 1 - Evan Garvey
# This is a simple game about a smith that makes weapons.

rarities = ["Common", "Uncommon", "Unique", "Exquisite", "Legendary"]
damages = [1, 1.5, 2, 2.5, 3.5]
rDict = {(t, v) for t, v in zip(rarities, damages)}

types = ["Broken", "Fractured", "Chipped", "Normal", "Fine", "Sharpened", "Honed"]
vals = [0.5, 0.75, 0.875, 1, 1.125, 1.25, 1.5]
tDict = {(t, v) for t, v in zip(types, vals)}


# The Smith class is the player. They have a level, and XP, but a limited inventory of 10 items.
class Smith:

    def __init__(self):
        self.level = 1
        self.xp = 0
        self.inventory = []

    # addXp and levelUp work hand in hand, they essentially just add XP to the pool of obtained XP

    def addXp(self, xp):
        while xp > 0:
            if (50 * self.level) - self.xp <= xp:
                xp -= (100 * self.level) - self.xp
                self.level += 1
                self.xp = 0
                self.levelUp()
            else:
                self.xp += xp
                xp = 0

    def levelUp(self):
        print("Level up! You are now level " + str(self.level))

    # Build is what builds us a weapon. All weapon stats are randomized and a final damage float is given to estimate
    # price.

    def build(self):
        if len(self.inventory) < 10:
            weapon = Weapon(self.level)
            print("You have built a weapon!")
            weapon.printStats()
            self.addXp(int(weapon.damage * 10))
            self.inventory.append(weapon)
        else:
            print("Too many weapons! sell one.")

    # Sell takes a weapon and the seller's preferences, and compares the two. XP is given based on the comparison

    def sell(self, customer, weapon):
        targetDamage = customer.getTargetDamage()
        levelOffset = self.level / customer.level
        damageOffset = weapon.damage / targetDamage
        totalSum = int((levelOffset * damageOffset) * self.level)
        print("Sold!! you sold your level " + str(weapon.level) + " " + weapon.type + " " + weapon.rarity + " sword.")
        print("You earned " + str(totalSum) + " xp.")
        self.inventory.remove(weapon)


# The customer class is essentially the face of the marketplace, it gives preferences to sell your weapons to

class Customer:

    def __init__(self, playerLevel):
        if playerLevel < 5:
            self.level = random.randrange(1, playerLevel + 5)
        else:
            self.level = random.randrange(playerLevel - 5, playerLevel + 5)
        self.rarity, self.type = self.setStandards()

    # setStandards and getTargetDamage are for checking their preferences and comparing them to yours respectively

    def setStandards(self):
        rarityTemp = random.random()
        typeTemp = random.random()
        rarityStandard = rarities[0]
        typeStandard = types[0]
        for i in range(1, 6):
            if rarityTemp > (i - 0.5) / 5:
                rarityStandard = rarities[i - 1]
        for i in range(1, 8):
            if typeTemp > (i - 0.5) / 7:
                typeStandard = types[i - 1]
        return rarityStandard, typeStandard

    def getTargetDamage(self):
        targetRarity = rarities.index(self.rarity)
        targetType = types.index(self.type)
        return damages[targetRarity] * vals[targetType] * (self.level / 2)

    # printCustomer is what prints customer info in the marketplace

    def printCustomer(self):
        print("Level " + str(self.level) + " customer")
        print("Prefers " + self.type + " minimum quality and " + self.rarity + " minimum rarity")


# the weapon class holds the info related to the weapons you're building and eventually selling

class Weapon:

    def __init__(self, level):
        self.level = level
        self.rarity = self.setRarity()
        self.type = self.setType()
        self.damage = self.setDamage(self.rarity, self.type)

    # setRarity and setType use randomizers to check what stats your weapon has

    def setRarity(self):
        temp = random.random()
        val = 0.6
        for i in range(5):
            if val > temp:
                return rarities[i]
            val += 0.1
        return rarities[4]

    def setType(self):
        temp = random.random()
        val = 1.0 / 6.5
        for i in range(6):
            if val > temp:
                return types[i]
            val += 1.0 / 7.0
        return types[6]

    # setDamage takes the information from your weapon and puts it all together into one float value (for comparison)

    def setDamage(self, rarity, type):
        for (t, x) in rDict:
            if t == rarity:
                for (v, y) in tDict:
                    if v == type:
                        return x * y * (self.level / 2)

    # printStats is what's used when first making a weapon and selling it in the marketplace

    def printStats(self):
        print("Level " + str(self.level) + " " + str(self.type) + " " + str(self.rarity) + " sword")
        print("Damage = " + str(self.damage))


# Main runs in an infinite loop, I could implement a save / exit feature but that's far beyond the scope of this project

if __name__ == "__main__":
    player = Smith()
    print("Welcome young smith!\nYou have been given this forge to build strong armaments.")
    print("type commands to perform actions.\n(build) a sword, or (sell) your inventory.")
    while 1 < 2:

        order = input()
        if order.lower() == "build":

            player.build()

        elif order.lower() == "sell" and len(player.inventory) == 0:

            print("You have no weapons! returning to menu...")

        elif order.lower() == "sell":

            print("\n\nWelcome to the marketplace!")
            print("Which customer would you like to sell to? selling under level or quality gives a debuff,")
            print("while selling above this grants bonuses! input 1 through 5 for customers, and")
            print("choose 1 through " + str(len(player.inventory)) + " for weapons. Seperate entries with a space\n")
            customers = []
            for i in range(5):
                print("---Customer " + str(i + 1) + "---")
                customers.append(Customer(player.level))
                customers[i].printCustomer()

            print("\n")

            for j in range(len(player.inventory)):

                if j + 1 < 10:
                    print("---Weapon " + str(j + 1) + "---")

                else:
                    print("---Weapon " + str(j + 1) + "--")

                player.inventory[j].printStats()
            print("\n")
            sellStats = input()
            try:
                sellTo, sellWeapon = sellStats.split(" ")

            except:
                print("Improper inputs used! returning ...")

            else:
                if 0 < int(sellTo) <= 5 and 0 < int(sellWeapon) <= len(player.inventory):
                    player.sell(customers[int(sellTo) - 1], player.inventory[int(sellWeapon) - 1])
                else:
                    print("Improper inputs used! returning...")
        else:
            print("Improper inputs used! returning...")
