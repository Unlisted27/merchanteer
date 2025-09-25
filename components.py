import os, time, random

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu(name:str,list_options:list,return_option=False,horizontal_sign="_",vertical_sign="|",return_tuple:bool=False):
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
    options = []
    items = []
    if return_option:
        options.append("Go back")
    for each in list_options:
        options.append(each)
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
                if return_option:
                    if int(answer) == 1:
                        return ("Go back","Go back")
                    return (int(answer)-1,selected)
                return (int(answer),selected)
            else:
                if return_option:
                    if int(answer) == 1:
                        return "Go back"
                    return int(answer)-1
                return int(answer)
        except Exception as e:
            #print(e) #Uncomment this line to show error message when the user enters an invalid option
            print("Invalid selection, try again")

#This whole thing was AI generated. Im not making logic like ts
def gen_contract(good_list: list, max_cargo_weight: float = 50):
    """
    Generates a contract with random goods and a reward proportional to value,
    ensuring the total weight is under max_cargo_weight.
    """

    # pick a random good to deliver
    good = random.choice(good_list)

    # calculate max amount that fits under weight limit
    max_amount = int(max_cargo_weight / good.weight)
    if max_amount < 1:
        max_amount = 1

    # choose a random amount up to max
    amount = random.randint(1, max_amount)

    # pick a reward good (can be the same or different)
    reward_type = random.choice(good_list)

    # calculate reward proportional to total value of delivered goods
    total_value = good.value * amount
    reward_amount = max(1, int(total_value * random.uniform(0.8, 1.2)))  # ±20% variability

    # pick a deadline (arbitrary units, e.g., hours)
    deadline = random.randint(1, 5) * 24  # 1–5 days

    # create the contract
    contract = Contract(
        reward_type=reward_type,
        reward_amount=reward_amount,
        deadline=deadline,
        goods=good,
        amount=amount
    )

    return contract


class Good:
    def __init__(self,name:str,description:str,value:int,weight:int):
        self.name = name
        self.description = description
        self.value = value
        self.weight = weight

class Storage:
    def __init__(self, name: str, cargo_max_weight: int = 1000, cargo: dict | None = None):
        if cargo is None:
            cargo = {}        # create a fresh dict for this instance
        self.cargo = cargo
        self.name = name
        self.cargo_max_weight = cargo_max_weight
        self.cargo_weight = 0

    def calc_cargo(self):
        self.cargo_weight = 0
        for good,amount in self.cargo.items():
            self.cargo_weight += self.get_crate_weight(good,amount)
    def get_crate_weight(self,good:Good,amount:int):
        return good.weight*amount
    def show_invent(self):
        self.calc_cargo()
        print(f"|{self.name} inventory | {self.cargo_weight}lbs/{self.cargo_max_weight}lbs |")
        for i, (good, amount) in enumerate(self.cargo.items(), start=1):
            print(
            f"[{i}] | Crate of {good.name} | "
            f"Amount: {amount} | "
            f"Value: ${good.value * amount} | "
            f"Weight: {self.get_crate_weight(good, amount)}lbs |"
            )
    def add_to_cargo(self,new_good:Good,amount:int=1):
        self.calc_cargo()
        if self.cargo_weight + self.get_crate_weight(new_good,amount) <= self.cargo_max_weight:
            for good in self.cargo:
                if good.name == new_good.name:        # find existing by name
                    self.cargo[good] += amount
                    break
            else:                               # not found -> create
                self.cargo[new_good] = amount
            self.calc_cargo()
            return True
        else:
            return False
    def remove_cargo(self, good_to_remove: Good, amount: int=1):
        for good in list(self.cargo):              # loop over keys safely
            if good.name == good_to_remove.name:   # match by name
                if self.cargo[good] >= amount:     # enough to remove?
                    self.cargo[good] -= amount     # just subtract
                    if self.cargo[good] <= 0:      # remove empty crates
                        del self.cargo[good]
                else:
                    return False           # Not enough to remove
                self.calc_cargo()
                return True
        return False  # not found
        
    def select_from_invent(self):
        self.calc_cargo()
        self.show_invent()
        print(f"[{len(self.cargo)+1}] | Go back")
        while True:
            try:
                answer = int(input(f"|:"))
                if answer <= (len(self.cargo)+1) and answer > 0:
                    return int(answer)
            except Exception as e:
                #print(e) #Uncomment this line to show error message when the user enters an invalid option
                print("Invalid selection, try again")

class Ship:
    def __init__(self,name:str,health_current:int = 100,health_max:int = 100,cargo_max_weight:int = 1000):
        self.name = name
        self.health_current = health_current
        self.health_max = health_max
        self.cargo_max_weight = cargo_max_weight
        self.cargo_weight = 0
        self.storage = Storage(f"{name} Cargo", cargo_max_weight)

class Warehouse:
    def __init__(self,name:str,max_weight:int = 10000):
        self.name = name
        self.max_weight = max_weight
        self.storage = Storage(f"{name} Warehouse",self.max_weight)

class Port:
    def __init__(self,name:str,ships:list[Ship],warehouses:list[Warehouse]=[]):
        self.ships = ships
        self.name = name
        self.ship_names = []
        self.warehouses = warehouses
    def transfer_goods(self,from_storage:Storage,to_storage:Storage):
        while True:
            try:
                clear_terminal()
                index = from_storage.select_from_invent() - 1
                goods_list = list(from_storage.cargo.keys())
                moving_cargo: Good = goods_list[index]    # the Good object selected
            except Exception:
                break
            while True:
                try:
                    print(f"How much {moving_cargo.name} would you like to move?")
                    amount = int(input("|:"))
                    break
                except Exception:
                    print("Invalid amount, try again")
            if not from_storage.remove_cargo(moving_cargo,amount):
                print("There was a problem moving that cargo")
                time.sleep(1)
            else:
                if not to_storage.add_to_cargo(moving_cargo,amount):
                    # add failed -> return the goods back
                    from_storage.add_to_cargo(moving_cargo,amount)
                    print("There was a problem moving that cargo")
                    time.sleep(1)
                else:
                    print("Cargo moved!")
                    time.sleep(1)
    def manageGoods(self):
        while True:
            self.ship_names = []
            self.warehouse_names = []
            for warehouse in self.warehouses:
                self.warehouse_names.append(warehouse.name)
            for ship in self.ships:
                self.ship_names.append(ship.name)
            clear_terminal()
            print(f"Welcome to {self.name}")
            try:
                selected_ship:Ship = self.ships[menu("Owned ships",self.ship_names,return_option=True) -1] #Select a ship to manage\
            except Exception:
                break
            while True:
                clear_terminal()
                print(f"|{selected_ship.name}|")
                action = menu("Actions",["Load","Unload","view inventory","Change name"],True)
                #Loading logic
                match action:
                    case 1:
                        clear_terminal()
                        answer = menu("Load from",["Warehouse","Another ship"])
                        match answer:
                            #Warehouse loading logic
                            case 1:
                                clear_terminal()
                                from_storage:Storage = self.warehouses[menu("Load from",self.warehouse_names) -1].storage #Get the warehouse we are moving from
                                self.transfer_goods(from_storage,selected_ship.storage)
                            #Another ship loading logic
                            case 2:
                                clear_terminal()
                                from_storage:Storage = self.ships[menu("Load from",self.ship_names) -1].storage #Get the ship we are moving from
                                self.transfer_goods(from_storage,selected_ship.storage)
                    case 2:
                        pass
                    case 3:
                        clear_terminal()
                        selected_ship.storage.show_invent()
                        input("Press enter to go back")
                    case 4:
                        new_name = input("Enter new name:")
                        selected_ship.name = new_name
                        print("Name changed!")
                    case _:
                        break

class Fleet:
    def __init__(self,ships:list[Ship]):
        self.ships = ships

class Player:
    def __init__(self,storage:Storage,reputation:int,fleet:Fleet):
        self.storage = storage
        self.reputation = reputation
        self.fleet = fleet
    def view_stats(self):
        print(f"Reputation: {self.reputation}")
        print(f"Fleet size: {len(self.fleet.ships)}")
        self.storage.show_invent()

class Contract:
    def __init__(self,reward_type:Good,reward_amount:int,deadline:int,goods:Good,amount:int):
        self.reward_type = reward_type
        self.reward_amount = reward_amount
        self.deadline = deadline
        self.goods = goods
        self.amount = amount

class Exchange:
    def __init__(self,name:str,contracts:list[Contract]=[]):
        self.name = name
    def start_exchange(self,player:Player):
        print(f"Welcome to the {self.name} exchange!")
        print("Here are the available contracts")
        
