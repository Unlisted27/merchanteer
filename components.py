import os, time, random, math
from abc import ABC, abstractmethod

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
                        return (None,"Go back")
                    return (int(answer)-1,selected)
                return (int(answer),selected)
            else:
                if return_option:
                    if int(answer) == 1:
                        return None
                    return int(answer)-1
                return int(answer)
        except Exception as e:
            #print(e) #Uncomment this line to show error message when the user enters an invalid option
            print("Invalid selection, try again")

#AI generated table printing function
def print_table(headers: list[str], rows: list[list], sep: str = "  "):
    """
    Print a text table with columns sized to fit their contents.

    headers : list of column titles
    rows    : list of lists; each inner list is a row of values
    sep     : spacing string between columns (default: two spaces)
    """
    # Convert everything to string for measuring
    str_rows = [[str(c) for c in row] for row in rows]
    str_headers = [str(h) for h in headers]

    # Find max width of each column
    widths = [
        max(len(h), max(len(row[i]) for row in str_rows) if str_rows else 0)
        for i, h in enumerate(str_headers)
    ]

    # Format pattern
    pattern = sep.join("{:<" + str(w) + "}" for w in widths)

    # Print header
    print(pattern.format(*str_headers))
    print(sep.join("-" * w for w in widths))

    # Print rows
    for row in str_rows:
        print(pattern.format(*row))


#This whole thing was AI generated and tweaked by me. Im not making logic like ts
def gen_contract(good_list: list,reward_list:list, current_day, current_location, world, max_cargo_weight: int = 1000):
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
    amount = random.randint(int(max_amount/8), max_amount)

    # pick a reward good (can be the same or different)
    reward_type = random.choice(reward_list)

    # calculate reward proportional to total value of delivered goods
    total_value = good.value * amount
    reward_amount = max(1, int(total_value * random.uniform(0.8, 1.2)))  # ±20% variability

    # pick a deadline (arbitrary units, e.g., hours)
    deadline = current_day + random.randint(10, 20)  # 10-20 days from now

    possible_destinations = []
    for location in world.locations:
        if location != current_location:
            possible_destinations.append(location)
    destination_location = random.choice(possible_destinations) if len(possible_destinations) > 0 else None
    #print(f"Possible destinations: {[loc.name for loc in possible_destinations]}")
    #print(f"Chosen destination: {destination_location.name if destination_location else 'None'}")
    #print(f"destination_location ports: {[port.name for port in destination_location.ports] if destination_location else 'N/A'}")
    #input()
    destination_port=random.choice(destination_location.ports) if len(destination_location.ports) > 0 else input("Found an error here") #This logic needs to be fixed to allow for multiple ports per location
    if destination_port and len(destination_port.warehouses) > 0:
        destination_storage = destination_port.warehouses[0].storage#random.choice(destination_port.warehouses).storage 
    else:
        return  #no valid destination found
    # create the contract
    contract = Contract(
        reward_type=reward_type,
        reward_amount=reward_amount,
        deadline=deadline,
        good=good,
        amount=amount,
        destination_port=destination_port,
        destination_storage=destination_storage
    )

    return contract

class GameTime:
    def __init__(self):
        self.day = 0
        self.observers = []   # anything that needs to react to time passing

    def register(self, obj):
        """Register an object that has an `on_day_passed(days:int)` method."""
        self.observers.append(obj)

    def advance(self, days=1):
        """Advance the global clock and notify observers."""
        self.day += days
        for o in self.observers:
            o.on_day_passed(self.day)

class World:
    def __init__(self,locations:list[object]):
        self.locations = locations

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

#This class is abstract, meaning it cannot be instantiated without being inherited from, and any class that inherits from it must implement run_event
class ShipEvent(ABC):
    def __init__(self,name:str):
        self.name = name

    @abstractmethod
    def run_event(self,ship:"Ship"):
        pass

class Ship:
    def __init__(self,name:str,health_current:int = 100,health_max:int = 100,cargo_max_weight:int = 1000,event_list=list[ShipEvent]):
        self.name = name
        self.health_current = health_current
        self.health_max = health_max
        self.cargo_max_weight = cargo_max_weight
        self.cargo_weight = 0
        self.event_list = list(event_list) if event_list is not None else []
        self.ships_log = []
        #Affectable ship properties
        self.storage = Storage(f"{name} Cargo", cargo_max_weight)
        self.is_dispatched = False
        self.day_of_arrival = 0
        self.day_of_return = 0
        self.target_warehouse:Warehouse = None
        self.returning_port:Port = None
    def on_day_passed(self, days):
        #Remember, this function runs every new day
        if days == self.day_of_arrival:
                #Empty cargo into target warehouse
                for good, amount in list(self.storage.cargo.items()):  # <-- iterate over a copy
                    self.target_warehouse.storage.add_to_cargo(good, amount)
                    self.storage.remove_cargo(good, amount)
        #Check for return to home port
        if days == self.day_of_return:
            self.is_dispatched = False
            self.day_of_arrival = 0
            self.day_of_return = 0
            self.target_warehouse = None
            self.returning_port.ships.append(self) #Return the ship to the port
            print(f"{self.name} has returned from its journey!")
            input("Press enter to continue")
        #Daily checks when dispatched
        if self.is_dispatched:
            #Event logic
            event_roll = random.randint(1,4) #Decide if an event happens today
            if event_roll == 1 and len(self.event_list) > 0: #If an event is to happen, and there are events to happen
                event:ShipEvent = random.choice(self.event_list) #Select a random event from the list
                event.run_event(self) #Run the event, passing in the ship as a parameter
                self.ships_log.append(f"Day {days}: {event.name} event occurred.")
            #Check for arrival at foreign port
            

class Warehouse:
    def __init__(self,name:str,max_weight:int = 10000):
        self.name = name
        self.max_weight = max_weight
        self.storage = Storage(f"{name} Warehouse",self.max_weight)

class Port:
    def __init__(self, name: str, location:object,world:World,game_time:GameTime,ships: list[Ship] | None = None, warehouses: list[Warehouse] | None = None):
        self.name = name
        self.location:Location = location
        self.world = world
        self.game_time = game_time
        self.ships = list(ships) if ships is not None else []
        self.ship_names = []
        self.warehouses = list(warehouses) if warehouses is not None else []
        if self.location is not None:
            self.location.add_port(self)

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
    def manage_ships(self):
        while True:
            self.ship_names = []
            self.warehouse_names = []
            for warehouse in self.warehouses:
                self.warehouse_names.append(warehouse.name)
            for ship in self.ships:
                self.ship_names.append(ship.name)
            clear_terminal()
            try:
                selected_ship:Ship = self.ships[menu("Owned ships",self.ship_names,return_option=True) -1] #Select a ship to manage\
            except Exception:
                break
            while True:
                clear_terminal()
                print(f"|{selected_ship.name}|")
                action = menu("Actions",["Load","view inventory","Dispatch ship","Change name","View event log"],True)
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
                    #Show invent
                    case 2:
                        clear_terminal()
                        selected_ship.storage.show_invent()
                        input("Press enter to go back")
                    #Dispatch ship
                    case 3:
                        clear_terminal()
                        location_names = []
                        available_locations = []
                        for location in self.world.locations:
                            if location != self.location:
                                available_locations.append(location)
                                location_names.append(location.name)
                        try:
                            answer = (menu("Select destination",location_names,True)-1)
                        except Exception:
                            break
                        destination:Location = available_locations[answer]
                        try:
                            selected_ship.target_warehouse = destination.ports[0].warehouses[0] #Select the first warehouse in the location
                        except Exception:
                            print("That location has no warehouses, cannot dispatch there")
                            input("Press enter to continue")
                            break
                        travel_time = round(math.sqrt((self.location.coordinates[0] - destination.coordinates[0])**2 + (self.location.coordinates[1] - destination.coordinates[1])**2) / 100) #The formula I learned in school, forgot, and then searched up when I needed it. Thanks grade 10 advanced math, you helped, a little, kinda, thanks, a little. Thanks google.
                        selected_ship.is_dispatched = True
                        selected_ship.day_of_arrival = self.game_time.day + travel_time
                        selected_ship.day_of_return = self.game_time.day + travel_time*2
                        selected_ship.returning_port = self
                        selected_ship.ships_log.append(f"-----Dispatched to {destination.name}-----")
                        self.ships.remove(selected_ship) #Remove the ship from the port while it is dispatched
                        print(f"{selected_ship.name} has been dispatched to {destination.name}!")
                        print(f"It will take aproximately {travel_time} days to get there.")
                        print(f"It will return in aproximately {travel_time*2} days.")
                        input("Press enter to continue")
                        break
                    #Rename ship
                    case 4:
                        new_name = input("Enter new name:")
                        selected_ship.name = new_name
                        selected_ship.storage.name = f"{new_name} Cargo"
                        print("Name changed!")
                    case 5:
                        clear_terminal()
                        print(f"Event log for {selected_ship.name} ({len(selected_ship.ships_log)}):")
                        for log_entry in selected_ship.ships_log:
                            print(log_entry)
                        input("Press enter to go back")
                    case _:
                        break

class Fleet:
    def __init__(self,ships:list[Ship]):
        self.ships = ships

class Contract:
    def __init__(self,reward_type:Good,reward_amount:int,deadline:int,good:Good,amount:int,destination_port:Port,destination_storage:Storage):
        self.reward_type = reward_type
        self.reward_amount = reward_amount
        self.deadline = deadline
        self.good = good
        self.amount = amount
        self.destination_port = destination_port
        self.destination_storage = destination_storage
        self.expired = False
        self.complete = False
        self.complete_notice = False
    def check_completion(self):
        if self.destination_storage.cargo.get(self.good,0) >= self.amount:
            return True
    def on_day_passed(self, day):
        contract_travel_time = None
        if self.check_completion(): #Check if contract is complete
            if not self.complete: #Check if it was already complete
                contract_travel_time = day + random.randint(2,5) #Random travel time for reward delivery
                self.complete = True
        if day == contract_travel_time and self.complete is True and self.complete_notice is False:
            self.complete_notice = True
        if self.deadline < day and self.complete is False:
            self.expired = True

class Player:
    def __init__(self, storage: Storage, reputation: int, fleet: Fleet | None = None, contracts: list[Contract] | None = None, warehouses: list[Warehouse] | None = None):
        self.storage = storage
        self.reputation = reputation
        self.fleet = fleet
        self.contracts = list(contracts) if contracts is not None else []
        self.warehouses = list(warehouses) if warehouses is not None else []
        #self.location = ""
    def view_stats(self):
        print(f"Reputation: {self.reputation}")
        print(f"Fleet size: {len(self.fleet.ships) if self.fleet else 0}")
        self.storage.show_invent()
    def view_contracts(self):
        headers = ["ID", "Amount", "Goods", "Reward", "Status"]
        rows = []
        for i, c in enumerate(self.contracts, start=1):
            status = "Expired" if c.expired else f"Due day {c.deadline}"
            reward = f"{c.reward_amount} {c.reward_type.name}"
            rows.append([i, c.amount, c.good.name, reward, status])
        print_table(headers, rows)
    def player_actions(self):
        answer = menu("Actions",["View stats","View contracts"],True)
        match answer:
            case 1:
                clear_terminal()
                self.view_stats()
                input("Press enter to go back")
            case 2:
                clear_terminal()
                self.view_contracts()
                input("Press enter to go back")
            case _:
                pass

class Exchange:
    def __init__(self, name: str, location, game_time: GameTime, world: World,
                 contracts: list[Contract] | None = None, good_list: list[Good] | None = None,
                 reward_list: list[Good] | None = None, max_cargo_weight: int = 1000):
        self.name = name
        self.location = location
        self.game_time = game_time
        self.world = world
        # defensive copies: new list for each instance
        self.contracts = list(contracts) if contracts is not None else []
        self.good_list = list(good_list) if good_list is not None else []
        self.reward_list = list(reward_list) if reward_list is not None else []
        self.max_cargo_weight = max_cargo_weight
        if self.location is not None:
            self.location.add_exchange(self)
        if not self.contracts:   # safer check for empty list
            self.gen_daily_contracts()

    def gen_daily_contracts(self):
        if len(self.good_list) == 0 or len(self.reward_list) == 0 or self.game_time is None:
            raise ValueError("If no contracts are provided, good_list, reward_list, and GameTime must be provided. Also, make sure the day value is accurate.")
        for i in range(random.randint(3,5)):
            self.contracts.append(gen_contract(self.good_list,self.reward_list,self.game_time.day,self.location,self.world,self.max_cargo_weight)) #We can GameTime.register contracts that are selected, dont need to do it when they are generated
    def show_contracts(self):
        #input(self.contracts)
        headers = ["ID", "Amount", "Good", "Reward", "Destination", "Status"]
        rows = []
        for i, c in enumerate(self.contracts, start=1):
            status = "Expired" if c.expired else f"Due day {c.deadline}"
            reward = f"{c.reward_amount} {c.reward_type.name}"
            rows.append([i, c.amount, c.good.name, reward, c.destination_port.location.name, status])
        print_table(headers, rows)
    def select_contract(self,player:Player):
        while True:
            clear_terminal()
            self.show_contracts()
            print("(Enter 0 to go back)")
            try:
                answer = int(input(f"|:"))
            except Exception:# as e:
                print("Invalid selection, try again")
            if answer <= (len(self.contracts)+1):
                if answer != 0:
                    chosen_contract = self.contracts[answer-1] 
                    while True:
                        clear_terminal()
                        warehouse_names = []
                        for warehouse in player.warehouses:
                            warehouse_names.append(warehouse.name)
                        try:
                            answer = int(menu("Where would you like to store these goods?",warehouse_names,True))-1
                        except Exception:
                            break
                        selected_warehouse:Warehouse = player.warehouses[answer] 
                        if selected_warehouse.storage.add_to_cargo(chosen_contract.good,chosen_contract.amount):
                            input("Contract accepted! (press enter to continue)")
                            return chosen_contract
                        else:
                            input("That warehouse cannot hold that much cargo, choose another (press enter to continue)")
                else:
                    return None
            #except Exception as e:
                #print(e) #Uncomment this line to show error message when the user enters an invalid option
                #print("Invalid selection, try again")
    def cashout_contracts(self,player:Player):
        while True:
            clear_terminal()
            player.view_contracts()
            print("(Enter 0 to go back)")
            try:
                answer = int(input(f"|:"))
                if answer == 0:
                    break
                chosen_contract:Contract = player.contracts[answer-1] 
                if chosen_contract.complete_notice:
                    warehouse_names = []
                    for warehouse in player.warehouses:
                        warehouse_names.append(warehouse.name)
                    try:
                        answer = int(menu("Where would you like to store these goods?",warehouse_names,True))-1
                    except Exception:
                        break
                    selected_warehouse:Warehouse = player.warehouses[answer] 
                    if selected_warehouse.storage.add_to_cargo(chosen_contract.reward_type,chosen_contract.reward_amount):
                        input("Contract cashed out! (press enter to continue)")
                        player.contracts.remove(chosen_contract)
                        del chosen_contract
                    else:
                        input("That warehouse cannot hold that much cargo, choose another (press enter to continue)")
                else:
                    input("This contract is not yet ready to be cashed out. (press enter to continue)")
            except Exception:# as e:
                #print(e) #Uncomment this line to show error message when the user enters an invalid option
                print("Invalid selection, try again")

class Location:
    def __init__(self,name:str,description:str | None = None,coordinates:tuple[int,int] | None = None, ports:list[Port] | None = None,exchanges:list[Exchange] | None = None):
        self.name = name
        self.coordinates = coordinates
        self.description = description
        self.ports = ports if ports is not None else []
        self.exchanges = exchanges if exchanges is not None else []
        self.randomise_coordinates()
    def randomise_coordinates(self,x_range:tuple[int,int]=(0,1000),y_range:tuple[int,int]=(0,1000)):
        self.coordinates = (random.randint(x_range[0],x_range[1]),random.randint(y_range[0],y_range[1]))
    def add_port(self, port):
        if port not in self.ports:
            self.ports.append(port)
    def add_exchange(self, exchange):
        if exchange not in self.exchanges:
            self.exchanges.append(exchange)
