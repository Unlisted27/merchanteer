# Code by Unlisted_dev
# This is the back end, really complicated stuff so be ware. 
# If you want to mod the game, or understand how this is all implemented, check out building_blocks.py
import os, time, random, math, shutil, game_art, style
from abc import ABC, abstractmethod

def distance(point1:tuple[int],point2:tuple[int]):
    return round(math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2) / 100)

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu(
    name: str,
    list_options: list,
    return_option=False,
    art: str | game_art.Art | None = None,
    horizontal_sign="_",
    vertical_sign="|",
    return_tuple: bool = False,
    table:dict | None = None
):
    """Displays a menu with optional ASCII art beside it."""
    if art is not None:
        if isinstance(art, str):
            art = art
        elif isinstance(art, game_art.Art):
            art = art.__str__()
        else:
            raise TypeError("Art must be a string or an Art object")
    options = []
    if return_option:
        options.append("Go back")
    options.extend(list_options)

    # Build menu items
    items = []
    for i, item in enumerate(options, start=1):
        if not isinstance(item, str):
            raise TypeError("Items in list must be type str")
        items.append(f"{vertical_sign}[{i}] {item}")

    length = max(len(name) + 1, *(len(i) for i in items)) #Calculate menu width based on longest line

    # Build menu block
    menu_lines = []
    menu_lines.append(horizontal_sign * length)
    menu_lines.append(name + " " * (length - len(name)))
    for thing in items:
        menu_lines.append(thing)

    # Prepare art block
    art_lines = []
    if art:
        art_lines = art.splitlines()

    table_lines = []
    if table:
        table_lines = get_table(table).splitlines()
    # Determine total height
    total_height = max(len(menu_lines), len(art_lines),len(table_lines))

    # Pad blocks
    while len(menu_lines) < total_height:
        menu_lines.append("")

    while len(art_lines) < total_height:
        art_lines.append("")

    while len(table_lines) < total_height:
        table_lines.append("")
    
    while True:
        clear_terminal()
        # Print side-by-side
        gap = "  |  "
        for m, a, t in zip(menu_lines, art_lines, table_lines):
            line = m.ljust(length)
            if a:
                line += gap + a
            if t:
                line += gap + t
            if not a and not t:
                line += gap
            print(line)

        # User input box
        print(("_"*(length+2))+"|") #Top border
        print("|:"+ " " * (length) + "|")
        print("‾"*(length+2)) #Bottom border
        print("\033[2A\033[3C", end="", flush=True)
        # Input loop
        
        try:
            answer = input()
            selected = options[int(answer) - 1]

            if answer == "0":
                raise Exception

            if return_tuple:
                if return_option:
                    if int(answer) == 1:
                        return (None, "Go back")
                    return (int(answer) - 1, selected)
                return (int(answer), selected)
            else:
                if return_option:
                    if int(answer) == 1:
                        return None
                    return int(answer) - 1
                return int(answer)

        except Exception:
            print(f"\033[1A{style.RED}XXXXXXXXXXXXXXXXXXXXXXXX{style.RESET}")
            time.sleep(0.2)

#AI generated table printing function
def get_table(data:dict|list, sep: str = "  "):
    """
    get_table(data, sep="  "): str
    ---
    Print a text table with columns sized to fit their contents. 
    \n
    data:
        Pass list for single column table (list)  
        Pass dict{str:dict} for multi column table (dict)  
    \n
    sep: spacing string between columns (default: two spaces)
    """
    rows:list = []
    headers:list = []
    if isinstance(data, list):
        if len(data) <= 1:
            if len(data) <= 1:
                header = data[0] if data else ""
                return f"{header}\n{'-'*len(str(header))}\nNo data to display"
        headers = data[0]
        rows = data[1:]

        str_headers = [data[0]]
        str_rows = [row for row in rows]
    elif isinstance(data, dict):
        if len(data) > 0:
            headers:list = ["Item"] + list(next(iter(data.values())).keys())
            for item, properties in data.items():
                row = [item] + list(properties.values())
                rows.append(row)
            # Convert everything to string for measuring
            str_rows = [[str(c) for c in row] for row in rows]
            str_headers = [str(h) for h in headers]
        else: return "No data to display"
    else:
        raise TypeError("Data must be a list of str or a dictionary")

    # Find max width of each column
    widths = [
        max(len(h), max(len(row[i]) for row in str_rows) if str_rows else 0)
        for i, h in enumerate(str_headers)
    ]

    # Format pattern
    pattern = sep.join("{:<" + str(w) + "}" for w in widths)

    # make headers
    block = """"""
    block += pattern.format(*str_headers) + "\n"
    block += sep.join("-" * w for w in widths) + "\n"

    # make rows
    for row in str_rows:
        if isinstance(row, str):        # single-column case
            row = [row]                 # wrap in list
        block += pattern.format(*row) + "\n"

    return block

#This whole thing was AI generated and tweaked by me. Im not making logic like ts
def gen_contract(good_list: list,reward_list:list, current_day, current_location:'Location', world:'World', max_cargo_weight: int = 1000):
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
    possible_destinations = [loc for loc in world.locations if loc != current_location]
    destination_location = random.choice(possible_destinations) if possible_destinations else None
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
        destination_storage=destination_storage,
        home_port = current_location
    )

    return contract

class Stat():
    def __init__(self,max_value:int,min_value:int = 0,current_value:int = None):
        self.max_value = max_value
        self.min_value = min_value
        self.current_value = current_value if current_value else max_value
    def __str__(self):
        return f"[{self.current_value}/{self.max_value}]"

class GameTime:
    def __init__(self):
        self.day = 0
        self.observers = []   # anything that needs to react to time passing

    def register(self, obj):
        """Register an object that has an `on_day_passed(days:int)` method."""
        self.observers.append(obj)

    def advance(self, days=1):
        notices = []
        """Advance the global clock and notify observers."""
        self.day += days
        for o in self.observers:
            msg = o.on_day_passed(self.day)
            if msg:
                notices.append(msg)
        print(f"--Day [{self.day}] notices--")
        for notice in notices:
            print(notice)
        input("Press enter to continue")

class World:
    def __init__(self,locations:list['Location']):
        self.locations = locations

class Good:
    def __init__(self,name:str,description:str,value:int,weight:int):
        self.name = name
        self.description = description
        self.value = value
        self.weight = weight

class Storage:
    def __init__(self, name: str, cargo_weight: int = 1000, cargo: dict | None = None):
        if cargo is None:
            cargo: dict[Good, int] = {}        # create a fresh dict for this instance
        self.cargo = cargo
        self.name = name
        self.cargo_weight = Stat(cargo_weight)

    def calc_cargo(self):
        self.cargo_weight.current_value = 0
        for good,amount in self.cargo.items():
            self.cargo_weight.current_value += self.get_crate_weight(good,amount)
    def get_crate_weight(self,good:Good,amount:int):
        return good.weight*amount
    def get_invent(self,starting_index = 1):
        self.calc_cargo()
        to_return = ""
        for i, (good, amount) in enumerate(self.cargo.items(), start=starting_index):
            to_return += (
            f"[{i}] | Crate of {good.name} | "
            f"Amount: {amount} | "
            f"Value: ${round(good.value * amount, 2)} | "
            f"Weight: {round(self.get_crate_weight(good, amount), 2)}lbs |\n"
            )
        return to_return
    def show_invent(self,back_option=False):
        print(f"|{self.name} | {self.cargo_weight.__str__()}lbs|")
        if back_option: print("[1] | Go back")
        print(self.get_invent(2 if back_option else 1))
    def add_to_cargo(self,new_good:Good,amount:int=1):
        self.calc_cargo()
        if self.cargo_weight.current_value + self.get_crate_weight(new_good,amount) <= self.cargo_weight.max_value:
            for good in self.cargo:
                if good.name == new_good.name:        # find existing by name
                    self.cargo[good] += amount
                    break
            else:   # not found -> create DO NOT INDENT THIS ELSE BLOCK, ITS A ```for else``` LOOP
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
        
    def select_from_invent(self) -> int | None:
        """Displays the inventory in a menu format and allows the user to select an item by number.\n
        returns the list index of the selected item (1st item = 0)"""
        self.show_invent(back_option=True)
        while True:
            try:
                answer = int(input(f"|:"))
                if answer == 1:
                    return None
                if answer <= (len(self.cargo)+1) and answer > 0:
                    return int(answer)-2
            except Exception as e:
                #print(e) #Uncomment this line to show error message when the user enters an invalid option
                print("Invalid selection, try again")

#This class is abstract, meaning it cannot be instantiated without being inherited from, and any class that inherits from it must implement run_event
class ShipEvent(ABC):
    def __init__(self,name:str):
        self.name = name

    @abstractmethod
    def run_event(self,ship:"Ship"):
        pass #This function is meant to be overridden by child classes, it will run the event's effects on the ship that is passed in as a parameter

class ShipType:
    def __init__(self,name:str,health:int=100,cargo_capacity:int=48000,crew_capacity:int=10,sailing_efficiency:int=160,toughness:int=350):
        self.name = name
        self.health = health
        self.cargo_capacity = cargo_capacity #This is in kg
        self.crew_capacity = crew_capacity
        self.sailing_efficiency = sailing_efficiency #This is the max amount of sailing efficiency (sum of all crew sailing skill) for this ship to perform at its best
        self.toughness = toughness

class Ship:
    def __init__(self,name:str,ship_type:ShipType,event_list:list[ShipEvent]):
        #SHIP STATS
        self.health = Stat(ship_type.health)
        self.sailing_efficiency = Stat(ship_type.sailing_efficiency,current_value=0) # This determines the max a ship can perform (so a rowboat's max performance will be less than a proper ship). The actual ship performace (the current value of this stat) is determined by the sum of all crew sailing_ability
        self.toughness = Stat(ship_type.toughness) # This is the max ship toughness, this may degrade during travels        
        #Internal properties (only to be adjsuted within the declaration of the class)
        self.name = name
        self.cargo_weight = Stat(ship_type.cargo_capacity)
        self.event_list = list(event_list) if event_list is not None else []
        self.ships_log = []
        self.crew_capacity = Stat(ship_type.crew_capacity)
        self.crew:list[CrewMate] = []
        #Affectable ship properties (to be adjusted by outside factors)
        self.storage = Storage(f"{name} Cargo", self.cargo_weight)
        self.is_dispatched = False
        self.day_of_arrival = 0
        self.destinations:list[Location] = []
        self.current_destination:Location = None
        self.contracts:list[Contract] = []
        self.current_port:Port = None
    def primary_dispatch(self, destinations:'Location', game_time:GameTime):
        '''Call this function to dispatch a ship (DO NOT USE dispatch())\n
        This function will handle all the backend for proper ship dispatch that dispatch() will not'''
        self.destinations = destinations
        self.destinations.append(self.current_port.location) #Add the current location as the final destination so the ship returns home after its route is complete
        self.dispatch(self.destinations[0],game_time)
    def dispatch(self, destination:'Location', game_time:GameTime):
        '''This is an internal function, should not regularily be called outside of the class \n
        Use primary_dispatch() instead\n
        This function is the action of sending a ship off, but will not handle things like multiple destinations, or returning the ship to its home port'''
        travel_time = distance((self.current_port.location.coordinates[0],self.current_port.location.coordinates[1]),(destination.coordinates[0],destination.coordinates[1]))
        #travel_time = round(math.sqrt((self.current_port.location.coordinates[0] - destination.coordinates[0])**2 + (self.current_port.location.coordinates[1] - destination.coordinates[1])**2) / 100) #The formula I learned in school, forgot, and then searched up when I needed it. Thanks grade 10 advanced math, you helped, a little, kinda, thanks, a little. Thanks google.
        self.day_of_arrival = game_time.day + travel_time
        self.ships_log.append(f"-----Dispatched to {destination.name}-----")
        self.current_destination = destination
        self.destinations.remove(destination) #Remove the current destination from the ship's list of possible destinations (this only removes the first instance of that destination)
        self.current_port.ships.remove(self) #Remove the ship from the port while it is dispatched
        self.current_port = None
        self.is_dispatched = True
    def check_arrival(self, days:int):
        # check_arrival() logic breakdown:
        # First step is checking if the ship is dispatched, we dispatch to next destination if it isnt
        # Check for arrival at a port
        # If we arrived at a port, we need to empty cargo acording to any contracts assosiated with that port
        # Then we dispatch to the next desitnation if there is one
        if self.is_dispatched:
            # Check for arrival at a port
            if days == self.day_of_arrival:
                self.current_port = self.current_destination.ports[0] #This logic needs to be fixed to allow for multiple ports per location
                self.current_port.add_ship(self) #Add the ship to the port's list of ships
                self.ships_log.append(f"Arrived at {self.current_port.name} on day {days}!") #Log arrival at port
                #Empty cargo into target storage
                for contract in self.contracts:
                    if contract.destination_port.location == self.current_destination: #Check if this contract is for the port we just arrived at
                        if contract.good in self.storage.cargo: #Check if we have any of the contracted good in storage
                            amount_to_deposite = min(contract.amount, self.storage.cargo.get(contract.good, 0)) #Calculate how much of the contracted good we can actually deposite based on how much we have in storage and how much the contract requires
                            contract.destination_storage.add_to_cargo(contract.good,amount_to_deposite) #Add the goods for this contract to the destination storage
                            self.storage.remove_cargo(contract.good,amount_to_deposite) #Remove the goods for this contract from the ship's storage
                        if contract.check_completion():
                            self.ships_log.append(f"Contract for {contract.amount} {contract.good.name} completed!")
                        else:
                            self.ships_log.append(f"Contract for {contract.amount} {contract.good.name} was NOT completed!")
                        self.contracts.remove(contract) #Remove the contract from the ship's list of contracts, even if it wasnt completed cause the ship is out of that Good anyways
                if len(self.destinations) > 0:
                    self.dispatch(self.destinations[0],self.current_port.game_time) #Dispatch to the next destination in the list (this only dispatches to the first instance of that destination)
                else:
                    self.is_dispatched = False
                    self.current_destination = None
                    self.day_of_arrival = None #Make this None so it throws errors if anything tries to interact with it, helps with pinpointing lost ship bugs
                    self.ships_log.append(f"No more destinations, {self.name} is now idle.")
                    return f"{self.name} has arrived at {self.current_port.name} and has no more destinations, it is now idle."
        return None
    def run_events(self,days:int):
        #Event logic
        if self.is_dispatched:
            event_roll = random.randint(1,4) #Decide if an event happens today
            if event_roll == 1 and len(self.event_list) > 0: #If an event is to happen, and there are events to happen
                event:ShipEvent = random.choice(self.event_list) #Select a random event from the list
                event.run_event(self) #Run the event, passing in the ship as a parameter
                self.ships_log.append(f"Day {days}: {event.name} event occurred.")
    def on_day_passed(self, days:int):
        #Daily checks when dispatched
        msg = None
        msg = self.check_arrival(days)
        if msg is None:
            self.run_events(days)
            msg = self.check_arrival(days)
        return msg
            
class Warehouse:
    def __init__(self,name:str,max_weight:int = 10000):
        self.name = name
        self.storage = Storage(f"{name} Warehouse",max_weight)

class Port:
    def __init__(self, name: str, location:object,world:World,game_time:GameTime,player:'Player',ships: list[Ship] | None = None, warehouses: list[Warehouse] | None = None):
        self.name = name
        self.location:Location = location
        self.world = world
        self.game_time = game_time
        self.ships = list(ships) if ships is not None else []
        self.ship_names = []
        self.warehouses = list(warehouses) if warehouses is not None else []
        self.player = player
        if self.location is not None:
            self.location.add_port(self)
        if self.ships is not None:
            for ship in self.ships:
                ship.current_port = self
        self.planned_destinations:list[Location] = []
    def add_ship(self, ship: Ship):
        self.ships.append(ship)
        ship.current_port = self
    def transfer_goods(self,from_storage:Storage,to_storage:Storage):
        while True:
            try:
                clear_terminal()
                index = from_storage.select_from_invent()
                goods_list = list(from_storage.cargo.keys())
                moving_cargo: Good = goods_list[index]    # the Good object selected
            except Exception:
                break
            while True:
                try:
                    print(f"Enter amount of {moving_cargo.name} to move (Enter 'all' to move everything)")
                    amount = input("|:")
                    if amount.lower().strip() == "all":
                        amount = from_storage.cargo[moving_cargo]  # move all available, this logic works because its getting the value of the key 'Good', which is the amount fo that good in the inventory
                    else:
                        amount = int(amount)
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

    # ===== Player interacting functions =====
    # ==SUB FUNCTIONS==
    def dispatch_menu(self,selected_ship:Ship):
        while True:
            clear_terminal()
            answer = menu("Route planning",["Add contracts","Add destinations","Dispatch"],True)
            match answer:
                # Dispatch with contract logic
                case 1:
                    clear_terminal()
                    contract_names = []
                    for contract in self.player.contracts:
                        contract_names.append(f"{contract.amount} {contract.good.name} to {contract.destination_port.name}")
                    contract_names.append("clear all")
                    selected_contract_names = ["Selected Contracts"] + [f"{contract.amount} {contract.good.name} to {contract.destination_port.name}" for contract in selected_ship.contracts]
                    while True:
                        try:
                            answer = menu("Select contracts to add (order does not matter)",contract_names,True,table=selected_contract_names)
                            if answer == len(contract_names): #Clear all option
                                selected_contract_names = ["Selected Contracts"]
                                for contract in self.player.contracts:
                                    if contract in selected_ship.contracts:
                                        selected_ship.contracts.remove(contract) #Remove the contract from the ship if its currently selected
                                continue
                            selected_contract_names.append(contract_names[answer-1])
                        except Exception:
                            #input("BREAKED" + e)
                            break
                        selected_contract:Contract = self.player.contracts[answer-1]
                        
                        try:
                            selected_ship.contracts.append(selected_contract) #Add the contract to the ship's list of contracts
                        except Exception as e:
                            print("There was an error selecting contract")
                            ans = input("Press enter to continue (e for error details) ")
                            if ans.lower() == "e": input(e)
                            break
                    
                case 2:
                    clear_terminal()
                    location_names = []
                    available_locations = []
                    for location in self.world.locations:
                        if location != self.location:
                            available_locations.append(location)
                            location_names.append(location.name)
                    location_names.append("Clear all")
                    selected_destination_names = ["Selected Destinations"] + [loc.name for loc in self.planned_destinations] # Gets the name of destinations that may already be set prior to opening the menu
                    while True:
                        try:
                            answer = menu("Select destinations (Order matters!)",location_names,True,table=selected_destination_names)
                            if answer == len(location_names): #Clear all option
                                self.planned_destinations = []
                                selected_destination_names = ["Selected Destinations"]
                                continue
                            self.planned_destinations.append(available_locations[answer-1])
                            selected_destination_names.append(available_locations[answer-1].name)
                        except Exception:
                            break
                case 3:
                    if len(self.planned_destinations) >= 1:
                        selected_ship.primary_dispatch(self.planned_destinations,self.game_time)
                        print(f"{selected_ship.name} has been dispatched!")
                        input("Press enter to continue")
                        break
                    else:
                        input("You must add at least one destination before dispatching (Press enter to continue)")
                case _:
                    break
    
    def load_ship_menu(self,selected_ship:Ship):
        clear_terminal()
        answer = menu("Load from",["Warehouse","Another ship"],True)
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
            case _:
                return

    def change_ship_name_menu(self,selected_ship:Ship):
        new_name = input("Enter new name (press [ENTER] to cancel): ")
        if new_name.strip() == "":
            print("Name change cancelled.")
            input("Press enter to continue")
            return
        selected_ship.name = new_name
        selected_ship.storage.name = f"{new_name} Cargo"
        print("Name changed!")

    # ==MAIN FUNCTIONS==
    def manage_ships(self):
        while True:
            # Initial ship selection menu
            self.ship_names = []
            self.warehouse_names = []
            self.planned_destinations:list[Location] = []
            for warehouse in self.warehouses:
                self.warehouse_names.append(warehouse.name)
            for ship in self.ships:
                self.ship_names.append(ship.name)
            clear_terminal()
            try:
                selected_ship:Ship = self.ships[menu(f"Port {self.name}",self.ship_names,return_option=True,art=game_art.port_birds_eye) -1] #Select a ship to manage\
            except Exception:
                break
            # Ship management menu
            while True:
                clear_terminal()
                print(f"|{selected_ship.name}|")
                action = menu("Ship actions",["Load","view inventory","Plan voyage","Change name","View event log"],True,art=game_art.ship_1)
                match action:
                    case 1:
                        #Load ship
                        self.load_ship_menu(selected_ship)
                    case 2:
                        #Show invent
                        clear_terminal()
                        selected_ship.storage.show_invent()
                        input("Press enter to go back")
                    case 3:
                        #Dispatch ship
                        self.dispatch_menu(selected_ship)
                    case 4:
                        #Rename ship
                        self.change_ship_name_menu(selected_ship)
                    case 5:
                        #View ships log
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
    def __init__(self,reward_type:Good,reward_amount:int,deadline:int,good:Good,amount:int,destination_port:Port,destination_storage:Storage,home_port:Port=None):
        self.reward_type = reward_type
        self.reward_amount = reward_amount
        self.deadline = deadline
        self.good = good
        self.amount = amount
        self.destination_port = destination_port
        self.destination_storage = destination_storage
        self.home_port = home_port
        self.expired = False
        self.complete = False
        self.complete_notice = False
        self.contract_travel_time = None
    def check_completion(self):
        if self.destination_storage.cargo.get(self.good,0) >= self.amount:
            return True
        return False
    def on_day_passed(self, day):
        if self.check_completion(): #Check if contract is complete
            if not self.complete: #Check if it was already complete
                self.contract_travel_time = day + random.randint(2,5) #Random travel time for reward delivery
                self.complete = True
        if day == self.contract_travel_time and self.complete is True and self.complete_notice is False and self.expired is False: #Check if reward should be delivered
            self.complete_notice = True
            return f"Contract for {self.amount} {self.good.name} is ready to be cashed out!"
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
        table_data = {}

        for i, c in enumerate(self.contracts, start=1):
            status = "Expired" if c.expired else f"Due day {c.deadline}"
            reward = f"{c.reward_amount} {c.reward_type.name}"

            # Use i as the key for each contract
            table_data[i] = {
                "ID": i,
                "Amount": c.amount,
                "Good": c.good.name,
                "Reward": reward,
                "Destination": c.destination_port.location.name,
                "Status": status
            }
        print(get_table(table_data))
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
    def __init__(self, name: str, location:'Location', game_time: GameTime, world: World,
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
        if self.location is not None and type(self.location) is Location:
            self.location.add_exchange(self)
        else:
            raise ValueError("Exchange must have a valid Location")
        if not self.contracts:   # safer check for empty list
            self.gen_daily_contracts()
    
    def gen_daily_contracts(self):
        if len(self.good_list) == 0 or len(self.reward_list) == 0 or self.game_time is None:
            raise ValueError("If no contracts are provided, good_list, reward_list, and GameTime must be provided. Also, make sure the day value is accurate.")
        for i in range(random.randint(3,5)):
            self.contracts.append(gen_contract(self.good_list,self.reward_list,self.game_time.day,self.location,self.world,self.max_cargo_weight)) #We can GameTime.register contracts that are selected, dont need to do it when they are generated
    
    def on_day_passed(self, days):
        self.contracts = []
        self.gen_daily_contracts()

    def show_contracts(self):
        table_data = {}

        for i, c in enumerate(self.contracts, start=1):
            status = "Expired" if c.expired else f"Due day {c.deadline}"
            reward = f"{c.reward_amount} {c.reward_type.name}"

            # Use i as the key for each contract
            table_data[i] = {
                "ID": i,
                "Amount": c.amount,
                "Good": c.good.name,
                "Reward": reward,
                "Destination": c.destination_port.location.name,
                "Status": status
            }
        print(get_table(table_data))
    def select_contract(self,player:Player):
        while True:
            clear_terminal()
            self.show_contracts()
            print("(Enter 0 to go back)")
            try:
                answer = int(input(f"|:"))
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
                            except Exception as e:
                                input("An error occured!\n"+e)
                            selected_warehouse:Warehouse = player.warehouses[answer]
                            #input(selected_warehouse.name) 
                            if selected_warehouse.storage.add_to_cargo(chosen_contract.good,chosen_contract.amount):
                                input("Contract accepted! (press enter to continue)")
                                self.contracts.remove(chosen_contract) #Remove the contract from the exchange's list of contracts
                                return chosen_contract
                            else:
                                input("That warehouse cannot hold that much cargo, choose another (press enter to continue)")
                    else:
                        return None
            except Exception:# as e:
                print("Invalid selection, try again")
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
                        answer = int(menu("Where would you like to store the reward?",warehouse_names,True))-1
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

class CrewRole():
    def __init__(self):
        pass

class Human():
    def __init__(self,max_health,strength,name):
        self.max_health = max_health
        self.strength = strength
        self.name = name

        self.current_health = max_health

class CrewMate(Human):
    def __init__(self,crew_role):
        super().__init__()