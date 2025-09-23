def menu(name:str,options:list,horizontal_sign="_",vertical_sign="|",return_tuple:bool=False):
    '''Displays a menu of the paramater options.
    -
    Selected option returned as string
    -
    ex: menu("Choose",["a","b","c"]) 
    --> choice (say the player chose [1] (a), 1 (integer) would be returned)
    
    -horizontal_sign and vertical_sign are characters that will make up the border of the menu
    -return_tuple if set to True will return the string selected as well as it's number
        ex: in the previous example, (1,"a") would be returned'''
    length = 1
    i=1
    items = []
    for item in options:
        if type(item) != str:
            raise TypeError("Items in list must be type str")
        else:
            items.append(f"{vertical_sign}[{i}]{item}")
            i+=1
    for thing in items:
        if len(thing) > length:
            length = len(thing)
    print(horizontal_sign*length)
    print(name + " "*(length - 1 - len(name)))
    #print(f"|\033[4m{name + " "*(length - 1 - len(name))}\033[0m")#The funny characters are the underlined escape sequence in python
    for thing in items:
        print(thing)
    while True:
        try:
            answer = input(f"{vertical_sign}:")
            selected = options[int(answer)-1]
            if answer == "0":
                raise Exception
            if return_tuple:
                return (int(answer),selected)
            else:
                return int(answer)
        except Exception as e:
            #print(e) #Uncomment this line to show error message when the user enters an invalid option
            print("Invalid selection, try again")

class good():
    def __init__(self,name:str,description:str,value:int,weight:int):
        self.name = name
        self.description = description
        self.value = value
        self.weight = weight

class crate():
    def __init__(self,good:good,amount:int):
        self.amount = amount
        self.good = good
        self.weight = good.weight*amount

class ship():
    def __init__(self,name:str,health_current:int = 100,health_max:int = 100,cargo_max_weight:int = 1000,cargo:list[crate] = []):
        self.name = name
        self.health_current = health_current
        self.health_max = health_max
        self.cargo_max_weight = cargo_max_weight
        self.cargo = cargo
        self.cargo_weight = 0
    def calc_cargo(self):
        for crate in self.cargo:
            self.cargo_weight += crate.weight
    def show_invent(self):
        self.calc_cargo()
        print(f"|{self.name} inventory | {self.cargo_weight}lbs/{self.cargo_max_weight}lbs |")
        i=1
        for crate in self.cargo:
            print(f"[{i}] | Crate of {crate.good.name} | Amount: {crate.amount} | Value: ${crate.good.value*crate.amount} | Weight: {crate.weight}")
            i+=1
    def add_to_cargo(self,new_crate:crate):
        self.calc_cargo
        if self.cargo_weight + new_crate.weight <= self.cargo_max_weight:
            self.cargo.append(new_crate)
            return #f"Added {new_crate.good.name}!"
        else:
            return "Sorry, that couldnt be added"
    def remove_cargo(self,crate_to_remove:crate):
        try:
            self.cargo.remove(crate_to_remove)
            return
        except Exception:
            return "That couldn't be removed"
    def select_from_invent(self):
        self.show_invent()
        print(f"[{len(self.cargo)+1}] | Go back")
        while True:
            try:
                answer = int(input(f"|:"))
                if answer <= (len(self.cargo)+1) & answer > 0:
                    return int(answer)
            except Exception as e:
                #print(e) #Uncomment this line to show error message when the user enters an invalid option
                print("Invalid selection, try again")
class port():
    def __init__(self,name:str,ships:list[ship]):
        self.ships = ships
        self.name = name
        self.ship_names = []
        for ship in ships:
            self.ship_names.append(ship.name)
    def manageGoods(self):
        print(f"Welcome to port {self.name}")
        selected_ship:ship = self.ships[menu("Owned ships",self.ship_names) -1]
        print(f"|{selected_ship.name}|")
        action = menu("Actions",["Load","Unload","Change name","Go back"])
        #Loading logic
        if action == 1:
            selected_ship_from:ship = self.ships[menu("Load from",self.ship_names) -1] #Get the ship we are moving from
            while True:
                try:
                    moving_cargo = selected_ship_from.cargo[selected_ship_from.select_from_invent() -1] #Select the cargo that will be moved
                except Exception:
                    break
                if selected_ship_from.remove_cargo(moving_cargo): #Attempt to remove cargo from the FROM ship
                    print("There was a problem moving that cargo") #On failure, do nothing
                else: 
                    if selected_ship.add_to_cargo(moving_cargo): #Attempt to add cargo to current ship
                        selected_ship_from.add_to_cargo(moving_cargo) #On failure, return removed cargo
                        print("There was a problem moving that cargo")
                    else:
                        print("Cargo moved!")
        #Unloading logic:
        elif action == 2:
            pass
        #Change name logic
        elif action == 3:
            pass


class fleet():
    def __init__(self,ships:list[ship]):
        self.ships = ships

class player():
    def __init__(self,gold:int,reputation:int,fleet:fleet):
        self.gold = gold
        self.reputation = reputation
        self.fleet = fleet

class exchange():
    def __init__(self,name):
        self.name = name
    def start_exchange(self,player:player):
        print(f"Welcome to the {self.name} exchange!")