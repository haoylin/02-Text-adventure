#!/usr/bin/env python3
import sys, os, json
# Check to make sure we are running the correct version of Python
assert sys.version_info >= (3,7), "This script requires at least Python 3.7"

# The game and item description files (in the same folder as this script)
game_file = 'games.json'
item_file = 'items.json'
inventory =[] 





def load_files():
    try:
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(__location__, game_file)) as json_file: game = json.load(json_file)
        with open(os.path.join(__location__, item_file)) as json_file: items = json.load(json_file)
        return (game,items)
    except:
        print("There was a problem reading either the game or item file.")
        os._exit(1)


def Check_inventory(item):
    for i in inventory:
        if i == item:
            return True
    return False

def calculate_points(items):
    points = 0
    for i in inventory:
        if i in items:
            points += items[i]["points"]
        return points


def render(game,items,current,moves,points):
    c = game[current]
    print("\n\n{} Moves\t\t\t\t{} Points".format(moves, points))
    print("\nyou are at the" + c["name"])
    print(c["desc"])

    for item in c["items"]:
        if not Check_inventory(item["item"]):
            print(item["desc"])
    
    
    for i in inventory:
        if i in items:
            if current in items[i]["exits"]:
                print(items[i]["exits"][current])

    print("\nAvailable exits:")
    for e in c["exits"]:
        print(e["exit"].lower())


def get_input():
    response = input("\nwhat would you like to do? ")
    response = response.upper().strip()
    return response

def update(game,items,current,response):
    if response == "INVENTORY":
        print("you are carrying:")
        if len(inventory) == 0:
            print("Nothing")
        else:
            for i in inventory:
                print(i.lower())
        return current

    c = game[current]
    for e in c["exits"]:
        if response == e["exit"]:
            return e["target"]

    for item in c["items"]:
        if response =="GET" + item["item"] and not Check_inventory(item["items"]):
            print(item["take"])
            inventory .append(item["item"])
            return current
    
    for i in inventory:
        if i in items:
            for action in (items[i]["actions"][action]):
                if response == action + "" + i:
                    return current
    
    if response[0:3] == "GET":
        print("you can't take that")
    elif response in ["NORTH","SOUTH","EAST","WEST"]:
        print("you can't go that way")
    else:
        print("I don't understand what you are trying to do")

    return current


    
def main():
    current = 'School'  # The starting location
    end_game = ['Rooftop']  # Any of the end-game location
    moves = 0
    points = 0
    
    (game,items) = load_files()

    
    while True:
        render(game,items,current,moves,points)
        if current in end_game:
            break

        response = get_input()

        if response == "QUIT":
            break

        current = update(game,items,current,response)
        moves += 1
        points = calculate_points(items)    

    print("Thanks for playing!")
    print("You scored{} points in {} moves".format(points,moves))


    




# run the main function
if __name__ == '__main__':
	main()