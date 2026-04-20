# Code by Unlisted_dev
# This is the back end, really complicated stuff so be ware. 
# If you want to mod the game, or understand how this is all implemented, check out building_blocks.py
from __future__ import annotations
from collections import defaultdict #IDK what this does
import os, time, random, math, json, game_art, style, uuid
from abc import ABC, abstractmethod

def distance(point1:tuple[int],point2:tuple[int]):
    '''Returns the distance between two points. For ballancing and standard reasons, distances are in NM'''
    return round(math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2) / 100)

def point_along_vector(start: tuple[float, float],
                       end: tuple[float, float],
                       distance: float) -> tuple[float, float]:
    x1, y1 = start
    x2, y2 = end

    dx = x2 - x1
    dy = y2 - y1

    length = (dx**2 + dy**2) ** 0.5

    if length == 0:
        raise ValueError("Start and end points cannot be the same")

    # Normalize direction vector
    unit_dx = dx / length
    unit_dy = dy / length

    # Scale by desired distance
    new_x = x1 + unit_dx * distance
    new_y = y1 + unit_dy * distance

    return (new_x, new_y)

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu(
    name: str,
    list_options: list,
    return_option=False,
    art: str | game_art.Art | None = None,
    horizontal_sign="-",
    vertical_sign="|",
    return_tuple: bool = False,
    table:dict | None = None,
    sub_table:dict | None = None,
    text_input: bool = False
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

    if len(items) == 0 and not text_input:
        raise ValueError("Menu must have at least one option, return option, or be a text input")
    length = max(len(name) + 1, *(len(i) for i in items)) #Calculate menu width based on longest line

    # Build menu block
    menu_lines = []
    #menu_lines.append(name + " " * (length - len(name)))
    for thing in items:
        if return_option and thing == f"{vertical_sign}[1] Go back":
            menu_lines.append(style.YELLOW + thing + style.RESET + " " * (length - len(f"{vertical_sign}[1] Go back")))
            menu_lines.append(horizontal_sign * length)
        else:
            menu_lines.append(thing)

    # Prepare art block
    art_lines = []
    if art:
        art_lines = art.splitlines()

    table_lines = []
    if table:
        table_lines = get_table(table).splitlines()
    table_width = max((len(t) for t in table_lines), default=0)

    sub_table_lines = []
    if sub_table:
        sub_table_lines = get_table(sub_table).splitlines()

    # Combine table + sub_table vertically
    if table_lines and sub_table_lines:
        table_lines = table_lines + [""] + sub_table_lines
    elif sub_table_lines:
        table_lines = sub_table_lines

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
        print(f"~ {name} ~")
        gap = "  |  "

        for m, a, t in zip(menu_lines, art_lines, table_lines):
            m = m.ljust(length)
            a = a.ljust(max(len(x) for x in art_lines)) if art_lines else ""
            t = t.ljust(table_width)

            line = m + gap + a + gap + t
            print(line)

        # User input box
        print(("_"*(length+2))+"|") #Top border
        print("|:"+ " " * (length) + "|")
        print("‾"*(length+2)) #Bottom border
        print("\033[2A\033[3C", end="", flush=True)
        # Input loop
        
        try:
            answer = input()
            if text_input:
                return answer
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
            headers:list = list(next(iter(data.values())).keys())
            for item, properties in data.items():
                row = list(properties.values())
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

# Generators

#This whole thing was AI generated and tweaked by me. Im not making logic like ts
def gen_contract(game:'Game',good_list: list,reward_list:list, current_day, current_location:'Location', world:'World', max_cargo_weight: int = 1000):
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
    reward_good = random.choice(reward_list)

    # calculate reward proportional to total value of delivered goods
    total_value = good.value * amount
    reward_amount = max(1, int(total_value * random.uniform(0.8, 1.2)))  # ±20% variability

    # pick a deadline (arbitrary units, e.g., hours)
    deadline = current_day + random.randint(10, 20)  # 10-20 days from now
    possible_destinations = [loc for loc in world.locations if loc != current_location]
    destination_location = random.choice(possible_destinations) if possible_destinations else None
    #input(destination_location.name)
    if destination_location is None:
        raise ValueError("Failed to create contract, no possible destinations found!")
    #print(f"Possible destinations: {[loc.name for loc in possible_destinations]}")
    #print(f"Chosen destination: {destination_location.name if destination_location else 'None'}")
    #print(f"destination_location ports: {[port.name for port in destination_location.ports] if destination_location else 'N/A'}")
    #input()
    destination_port=random.choice(destination_location.ports) if len(destination_location.ports) > 0 else input("Found an error here")
    #input(destination_port.warehouses)
    if destination_port and len(destination_port.warehouses) > 0:
        destination_storage = destination_port.warehouses[0].storage#random.choice(destination_port.warehouses).storage 
    else:
        raise ValueError("Could not create contract, no valid destination warehouses found!")
    # create the contract
    contract = Contract(
        game,
        name=genname(),
        reward_good=reward_good,
        reward_amount=reward_amount,
        deadline=deadline,
        good=good,
        amount=amount,
        destination_port=destination_port,
        destination_storage=destination_storage,
        home_location = current_location
    )

    return contract

class name_parts:
    start_sounds = [
    'Ada', 'Adel', 'Adri', 'Agn', 'Alf', 'Ale', 'Ali', 'Alma', 'Alo', 'Alv', 'Ama', 'Amb', 'Ana', 'And', 'Ang', 'Ann', 
    'Ans', 'Ant', 'Arn', 'Art', 'Aug', 'Aur', 'Bar', 'Bel', 'Ben', 'Ber', 'Bert', 'Bess', 'Bla', 'Blan', 'Bor', 'Bry', 
    'Cal', 'Cam', 'Car', 'Carl', 'Cas', 'Cat', 'Cha', 'Che', 'Chr', 'Clar', 'Cla', 'Cle', 'Clif', 'Cly', 'Con', 'Cor', 
    'Cyr', 'Dan', 'Dar', 'Dav', 'Deb', 'Del', 'Den', 'Dia', 'Dol', 'Dom', 'Dor', 'Dot', 'Edg', 'Edm', 'Edn', 'Edu', 
    'Edw', 'Ela', 'Ele', 'Eli', 'Eliz', 'Ell', 'Emi', 'Emm', 'Eph', 'Est', 'Ethel', 'Eug', 'Eva', 'Eve', 'Evi', 'Flo', 
    'Flora', 'Fran', 'Fre', 'Fred', 'Gab', 'Geo', 'Ger', 'Gil', 'Glad', 'Gor', 'Gra', 'Gre', 'Gus', 'Gwe', 'Har', 'Hen', 
    'Her', 'Hes', 'Hor', 'How', 'Hub', 'Hugh', 'Ina', 'Ire', 'Isa', 'Iva', 'Ivy', 'Jac', 'Jam', 'Jan', 'Jas', 'Jen', 
    'Jes', 'Jim', 'Joh', 'Jon', 'Jos', 'Jud', 'Jul', 'Jus', 'Kat', 'Ken', 'Kev', 'Kim', 'Lan', 'Lar', 'Leo', 'Les', 'Lil', 
    'Lin', 'Liz', 'Lou', 'Luc', 'Lud', 'Lut', 'Lyd', 'Lyn', 'Mar', 'Marv', 'Mat', 'Maud', 'Max', 'Meg', 'Mel', 'Mic', 
    'Mil', 'Min', 'Mit', 'Mor', 'Myr', 'Nan', 'Nel', 'Nell', 'Nev', 'Nia', 'Nor', 'Norv', 'Oli', 'Oma', 'Oph', 'Ora', 
    'Osc', 'Ott', 'Pat', 'Paul', 'Peg', 'Pet', 'Phil', 'Pru', 'Quin', 'Rad', 'Ray', 'Reb', 'Reg', 'Ren', 'Ric', 'Rob', 
    'Rod', 'Rog', 'Ron', 'Ros', 'Row', 'Roy', 'Ruf', 'Ruth', 'Sam', 'Sar', 'Sid', 'Sim', 'Sol', 'Ste', 'Stu', 'Sue', 
    'Syl', 'Ted', 'The', 'Tho', 'Tim', 'Tom', 'Ton', 'Urs', 'Vic', 'Vir', 'Viv', 'Wal', 'War', 'Wil', 'Wilf', 'Win', 
    'Wor', 'Wyn', 'Zac', 'Abel', 'Abr', 'Ach', 'Adal', 'Adolf', 'Aeth', 'Alar', 'Ald', 'Alv', 'Ambr', 'Arch', 'Arl', 'Arth', 
    'Atha', 'Audr', 'Bald', 'Beau', 'Beli', 'Bern', 'Blan', 'Brun', 'Cad', 'Cael', 'Cai', 'Cel', 'Cen', 'Chr', 'Cid', 'Cleof', 
    'Conr', 'Cons', 'Cyri', 'Dag', 'Diet', 'Diot', 'Ead', 'Eald', 'Ebra', 'Eber', 'Egbert', 'Eld', 'Elea', 'Elfr', 'Elys', 'Emm', 
    'Ermin', 'Ern', 'Eth', 'Faust', 'Fitz', 'Flav', 'Fran', 'Frem', 'Gabr', 'Gai', 'Gar', 'Geof', 'Gerar', 'Gilb', 'Godr', 'Gott', 
    'Guill', 'Gund', 'Gwen', 'Hadr', 'Hawk', 'Helo', 'Herv', 'Hild', 'Hilg', 'Holm', 'Ida', 'Inga', 'Irmi', 'Jarl', 'Jero', 'Joan', 
    'Joaq', 'Josc', 'Josia', 'Judith', 'Klem', 'Lam', 'Lamb', 'Lau', 'Leif', 'Leod', 'Leom', 'Leop', 'Loth', 'Luc', 'Ludo', 
    'Lup', 'Magn', 'Marce', 'Mart', 'Maur', 'Maxi', 'Melv', 'Mica', 'Milv', 'Nor', 'Odil', 'Odon', 'Off', 'Osm', 'Otth', 'Owin', 
    'Pasc', 'Perci', 'Petron', 'Phine', 'Piers', 'Plac', 'Rein', 'Reym', 'Richm', 'Rinal', 'Roder', 'Roel', 'Rowl', 'Sigm', 
    'Sixt', 'Stam', 'Tancr', 'Thib', 'Thorf', 'Thorv', 'Tryg', 'Ulr', 'Ursm', 'Valt', 'Vikt', 'Wald', 'Walther', 'Wit', 'Wolf', 
    'Wulf', 'Ysm', 'Zeb', 'Zim'
    ]
    middle_sounds = [
        'bel', 'bert', 'beth', 'bald', 'dred', 'drik', 'fred', 'gald', 'gar', 'gard', 'ger', 'hard', 'helm', 'lian', 'lina', 
        'lind', 'lisa', 'man', 'mar', 'met', 'mir', 'mund', 'nad', 'nard', 'nath', 'neer', 'nel', 'nor', 'phin', 'rad', 'rick', 
        'rold', 'rud', 'ryn', 'san', 'sandra', 'son', 'ston', 'thel', 'ther', 'trid', 'vald', 'ven', 'ver', 'vin', 'wald', 
        'ward', 'win', 'wyn', 'yell', 'bel', 'belle', 'claud', 'den', 'din', 'dora', 'dyn', 'eline', 'ene', 'fan', 'gene', 
        'hilde', 'la', 'lene', 'lene', 'leth', 'lie', 'lien', 'liev', 'line', 'lisa', 'lith', 'mand', 'maria', 'mine', 'mira', 
        'mona', 'mund', 'nath', 'nelle', 'nor', 'pat', 'quin', 'rene', 'reth', 'ric', 'rin', 'rine', 'ryn', 'seb', 'sey', 
        'stan', 'ston', 'tin', 'ton', 'uel', 'vin', 'vor', 'wen', 'ylen', 'zel', 'zia', 'zor', 'ang', 'ant', 'bra', 'cia', 'con', 
        'dar', 'del', 'dor', 'dre', 'ein', 'eis', 'eus', 'fan', 'fer', 'fran', 'fri', 'gie', 'gio', 'gis', 'gie', 'han', 'hel', 
        'hin', 'jan', 'jes', 'jin', 'kar', 'kie', 'laf', 'let', 'lin', 'lis', 'lud', 'mat', 'mir', 'mor', 'nat', 'nor', 'ral', 
        'ram', 'ric', 'sie', 'sta', 'sue', 'tan', 'tor', 'tri', 'vic', 'von', 'vin', 'wyn'
    ]
    end_sounds = [
        'a', 'ah', 'an', 'ard', 'ard', 'as', 'bel', 'bert', 'beth', 'dine', 'dine', 'dith', 'don', 'dor', 'dra', 'dred', 
        'dyn', 'e', 'el', 'el', 'en', 'er', 'et', 'eth', 'eus', 'ey', 'fred', 'ga', 'gar', 'go', 'goth', 'gus', 'ham', 'hard', 
        'helm', 'ia', 'ian', 'ias', 'ic', 'ice', 'ie', 'iel', 'ien', 'ier', 'if', 'in', 'ine', 'io', 'ion', 'is', 'isa', 'ius', 
        'la', 'line', 'lis', 'lith', 'lon', 'ma', 'mar', 'mer', 'mir', 'mond', 'mund', 'na', 'nard', 'ne', 'nel', 'neth', 
        'ney', 'ni', 'no', 'nor', 'on', 'or', 'os', 'que', 'ra', 'rad', 'ran', 'red', 'ric', 'rick', 'rid', 'ro', 'ron', 'ros', 
        'sa', 'san', 'sel', 'son', 'ston', 'ta', 'tan', 'tha', 'ther', 'thia', 'tia', 'tin', 'ton', 'uel', 'us', 'va', 'ver', 
        'vin', 'ward', 'wen', 'win', 'wyn', 'ya', 'yah', 'zar', 'zo'
    ]

def genname():
    length = random.randint(2,3)
    if length == 2:
        name = name_parts.start_sounds[random.randint(0,len(name_parts.start_sounds)-1)] + name_parts.end_sounds[random.randint(0,len(name_parts.end_sounds)-1)]
    if length == 3:
        name = name_parts.start_sounds[random.randint(0,len(name_parts.start_sounds)-1)] + name_parts.middle_sounds[random.randint(0,len(name_parts.middle_sounds)-1)] + name_parts.end_sounds[random.randint(0,len(name_parts.end_sounds)-1)]
    return(name)

def gen_crewmate(crew_roles:list['CrewRole'],game:'Game'):
    name = genname()
    if len(crew_roles) > 0:  
        crew_role = random.choice(crew_roles) 
    else:
        raise ValueError("Crew roles list cannot be empty")
    return CrewMate(crew_role,game,name=name)

# Core components

class Stat:
    def __init__(self, max_value: int, min_value: int = 0, current_value: int | None = None):
        self.max_value = max_value
        self.min_value = min_value
        self.current_value = current_value if current_value is not None else max_value
    def _clamp(self):
        self.current_value = max(
            self.min_value,
            min(self.current_value, self.max_value)
        )
    def full(self) -> bool:
        # This function returns true if the stats current value is equal to its max
        return self.max_value == self.current_value
    def __str__(self):
        return f"[{self.current_value}/{self.max_value}]"
    #iadd and isub allow for a += b (the value of a is now changed) whereas __add__ would be for a + b where a is not changed
    def __iadd__(self, other):
        if isinstance(other, (int, float)):
            self.current_value += other
            self._clamp()
            return self
        return NotImplemented

    def __isub__(self, other):
        if isinstance(other, (int, float)):
            self.current_value -= other
            self._clamp()
            return self
        return NotImplemented

    def __int__(self):
        return self.current_value
    
    # This function is mainly used in the save process to convert to a JSON friendly type
    def as_tuple(self):
        """Returns tuple(max,min,current)"""
        #input("STAT AS TUPLE")
        new_tup = tuple([self.max_value,self.min_value,self.current_value])
        return new_tup

    @classmethod
    def from_tuple(cls,tuple):
        #input(f"LOADING TUPLE: {tuple[0]} / {tuple[1]} / {tuple[2]}")
        instance = cls(tuple[0],tuple[1],tuple[2])
        return instance

class LoadContext:
    def __init__(self, game:'Game', event_list:list['ShipEvent']):
        self.game = game
        self.event_list = event_list or []

class Game:
    def __init__(self):
        self.day = 0
        self.observers = []
        self.to_remove = []
        self.notices = []
        self.used_IDs = []

    def save(self) -> dict:
        save = {
            "day": self.day,
            "notices":self.notices,
            "game_items": []  # Will store all observer save data
        }
        
        # Iterate through each observer and call its save() method
        print("ALL CURRENT GAME OBSERVERS")
        for observer in self.observers:
            if hasattr(observer,"save"):
                observer_data = {
                    "type": type(observer).__name__,  # Store the class name (e.g., "CrewMate", "Ship")
                    "data": observer.save()  # Call the observer's save() method
                }
                print(f"{type(observer)} | {observer.ID}")
                save["game_items"].append(observer_data)
        
        return save
    
    def save_to_file(self, filename: str):
        """Save the entire game state to a JSON file."""
        save_data = self.save()
        print(save_data)
        with open(filename, 'w') as f:
            json.dump(save_data, f, indent=2)
        print(f"Game saved to {filename}")
    
    @classmethod
    def load_from_file(cls, filename: str,context:LoadContext):
        """Load the entire game state from a JSON file."""
        with open(filename, 'r') as f:
            save_data = json.load(f)
        
        # Create the Game instance
        # Step 1
        game = context.game
        game.day = save_data["day"]
        game.notices = save_data["notices"]

        grouped = defaultdict(list)

        for item in save_data["game_items"]:
            grouped[item["type"]].append(item["data"])
        
        LOAD_ORDER = [
            "Location",
            "World",
            "Good",
            "Storage",
            "Warehouse",
            "Port",
            "Contract",
            "CrewRole",
            "CrewMate",
            "ShipType",
            "Ship",
            "Fleet",
            "Player",
            "Tavern",
            "Exchange",
            "MessengerPigeon"
        ]

        CLASS_REGISTRY = {
            "World": World,
            "Location": Location,
            "Good": Good,
            "Storage": Storage,
            "Warehouse":Warehouse,
            "Port": Port,
            "Contract": Contract,
            "CrewRole": CrewRole,
            "CrewMate": CrewMate,
            "ShipType":ShipType,
            "Ship": Ship,
            "Fleet":Fleet,
            "Player":Player,
            "Tavern":Tavern,
            "Exchange":Exchange,
            "MessengerPigeon":MessengerPigeon
        }
        # Load phase 1: Instantiate all objects
        for item_type in LOAD_ORDER:
            for item_data in grouped[item_type]:
                print(f"Loading {item_type} | {item_data["ID"]}")
                obj = CLASS_REGISTRY[item_type].init_load(item_data, context)
                print(f"Got: {obj}")

        print("CURRENT OBSERVERS")
        print(f"{type(observer)} | {observer.ID}" for observer in game.observers)
        # Load phase 2: Populate object properties
        for item in game.observers:
            if hasattr(item,"secondary_load"):
                print(f"Secondary load: {type(item)} {item.ID}")
                item.secondary_load(item._save_data,context)
        
        # Load phase 3: Delete temporary save data in each object
        for item in game.observers:
            if hasattr(item, "_save_data"):
                del item._save_data

        return game
    
    def scan_loaded_objects(self,item_type,item_id,crash_on_fail=False):
        for item in self.observers:
            if type(item) == item_type:
                if hasattr(item,"ID"):
                    if item.ID == item_id:
                        return item
                else:
                    raise ValueError("Could not scan for loaded item as item provided has no 'ID' property! \nAborting load...")
        else:
            if crash_on_fail:
                raise ValueError(f"Could not find object {item_id} in loaded items! \nAborting load...")
            else:
                print(f"{style.RED}Could not find an object! Object:{style.YELLOW}{item_type}{style.RED} with ID: {style.YELLOW}{item_id}{style.RESET}")
                return None

    # Game methods
    def register(self, obj):
        """Register an object that has an `on_day_passed(days:int)` method."""
        self.observers.append(obj)
        if obj.ID is None:
            ID = str(uuid.uuid4())
            while ID in self.used_IDs:
                ID = str(uuid.uuid4())
            obj.ID = ID
            self.used_IDs.append(ID)

    def unregister(self, obj):
        self.to_remove.append(obj)

    def advance(self, days=1):
        daily_notices = []
        """Advance the global clock and notify observers."""
        self.day += days
        for o in self.observers:
            if hasattr(o,"on_day_passed"):
                msg = o.on_day_passed(self.day)
                if msg:
                    daily_notices.append(msg)
        for obj in self.to_remove:
            if obj in self.observers:
                self.observers.remove(obj)
        self.to_remove.clear()
        clear_terminal()
        print(f"--Day [{self.day}] notices--")
        for notice in daily_notices:
            self.notices.append(notice)
            print(notice)
        input("Press enter to continue")

class Location:
    def __init__(self,name:str,game:Game,description:str | None = None,coordinates:tuple[int,int] | None = None, ports:list['Port'] | None = None,exchanges:list['Exchange'] | None = None, ID:str | None = None):
        self.name = name # Saved
        self.game = game
        self.coordinates = coordinates # Saved
        self.description = description # Saved
        self.ports = ports if ports is not None else []
        self.exchanges = exchanges if exchanges is not None else []
        if self.coordinates is None:
            self.randomise_coordinates()
        self.ID = ID if ID is not None else None
        game.register(self)
    
    def save(self) -> dict:
        save = {
            "ID":self.ID,
            "name":self.name,
            "coordinates":self.coordinates,
            "description":self.description
        }
        return save
    
    @classmethod
    def init_load(cls, save: dict,context:LoadContext):
        game = context.game
        instance = cls(
            save["name"],
            game,
            coordinates = save["coordinates"],
            description = save["description"],
            ID=save["ID"]
        )
        return instance
    
    def randomise_coordinates(self,x_range:tuple[int,int]=(0,50000),y_range:tuple[int,int]=(0,50000)):
        self.coordinates = (random.randint(x_range[0],x_range[1]),random.randint(y_range[0],y_range[1]))
    def add_port(self, port):
        if port not in self.ports:
            self.ports.append(port)
    def add_exchange(self, exchange):
        if exchange not in self.exchanges:
            self.exchanges.append(exchange)

class World:
    def __init__(self,locations:list['Location'],game:Game, ID:str | None = None):
        self.locations = locations
        self.game = game
        self.ID = ID if ID is not None else None
        game.register(self)

    def save(self) -> dict:
        save = {
            "locations":[location.ID for location in self.locations],
            "ID":self.ID
        }
        return save
    
    @classmethod
    def init_load(cls, save: dict,context:LoadContext):
        game = context.game
        locations = [game.scan_loaded_objects(Location,locID) for locID in save["locations"]]
        instance = cls(
            locations=locations,
            game=game,
            ID=save["ID"]
        )
        return instance

class Good:
    def __init__(self,name:str,description:str,value:int,weight:int,game:Game, ID:str | None = None):
        self.name = name
        self.description = description
        self.value = value
        self.weight = weight
        self.ID = ID if ID is not None else None
        game.register(self)
    
    def save(self) -> dict:
        save = {
            "name":self.name,
            "description":self.description,
            "value":self.value,
            "weight":self.weight,
            "ID":self.ID
        }
        return save
    
    @classmethod
    def init_load(cls, save: dict,context:LoadContext):
        game = context.game
        instance = cls(
            save["name"],
            save["description"],
            save["value"],
            save["weight"],
            game,
            ID = save["ID"]
        )
        return instance 

class Storage:
    def __init__(self, name: str,game:Game, max_cargo_weight: int = 1000, cargo: dict | None = None, ID:str | None = None):
        if cargo is None:
            cargo: dict[Good, int] = {}        # create a fresh dict for this instance
        self.cargo = cargo
        self.name = name
        self.cargo_weight = Stat(max_cargo_weight,current_value=0)
        self.game = game
        self.ID = ID if ID is not None else None
        game.register(self)

    def calc_cargo(self):
        self.cargo_weight.current_value = 0
        for good,amount in self.cargo.items():
            self.cargo_weight.current_value += self.get_crate_weight(good,amount)
    def get_crate_weight(self,good:Good,amount:int):
        return good.weight*amount
    def get_invent_table(self):
        self.calc_cargo()
        table_data = {}
        for good, amount in self.cargo.items():
            table_data[good.name] = {
            "Good": good.name,
            "Amount": amount,
            "Value": round(good.value*amount,2),
            "Weight": f"{round(self.get_crate_weight(good,amount),2)}Kg"
        }
        return table_data
    def show_invent(self):
        menu(f"Inventory",[],return_option=True,table=self.get_invent_table())
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
        table_data = self.get_invent_table()
        return menu("Select an item",[f"{amount} | {good.name}" for good,amount in self.cargo.items()],return_option=True,table=table_data)-1
    
    def save(self):
        save_cargo = {}
        for good,amount in self.cargo.items():
            save_cargo[good.ID] = amount
        save = {
            "cargo":save_cargo,
            "name":self.name,
            "cargo_weight":self.cargo_weight.as_tuple(),
            "ID":self.ID
        }
        return save
    
    @classmethod
    def init_load(cls, save: dict,context:LoadContext):
        game = context.game
        instance = cls(
            save["name"],
            game,
            ID=save["ID"]
        )
        instance._save_data = save # THIS IS CRITICAL, IT STORES DATA FOR THE SECOND PHASE
        return instance
    
    def secondary_load(self,save,context:LoadContext):
        game = context.game
        self.cargo_weight=Stat.from_tuple(save["cargo_weight"])
        for good_id,amount in dict(save["cargo"]).items():
            self.cargo[game.scan_loaded_objects(Good,good_id)]=amount

class Contract:
    def __init__(self,game:Game,name:str,reward_good:Good,reward_amount:int,deadline:int,good:Good,amount:int,destination_port:'Port',destination_storage:Storage,home_location:Port,expired:bool=False,complete:bool=False,complete_notice:bool=False,contract_travel_time:int|None = None, active:bool=False,ID:str | None = None):
        self.name=name
        self.reward_good = reward_good
        self.reward_amount = reward_amount
        self.deadline = deadline
        self.good = good
        self.amount = amount
        self.destination_port = destination_port
        self.destination_storage = destination_storage
        self.home_location = home_location
        self.expired = expired
        self.complete = complete
        self.complete_notice = complete_notice
        self.contract_travel_time:int = contract_travel_time
        self.game = game
        self.active = active
        self.ID = ID if ID is not None else None
        game.register(self)


    def save(self):
        save = {
            "name":self.name,
            "reward_good":self.reward_good.ID,
            "reward_amount":self.reward_amount,
            "deadline":self.deadline,
            "good":self.good.ID,
            "amount":self.amount,
            "destination_port":self.destination_port.ID,
            "destination_storage":self.destination_storage.ID,
            "home_location":self.home_location.ID,
            "expired":self.expired,
            "complete":self.complete,
            "complete_notice":self.complete_notice,
            "contract_travel_time":self.contract_travel_time,
            "active":self.active,
            "ID":self.ID
        }
        return save

    @classmethod
    def init_load(cls,save:dict,context:LoadContext):
        game = context.game
        reward_good = game.scan_loaded_objects(Good,save["reward_good"])
        good = game.scan_loaded_objects(Good,save["good"])
        destination_port = game.scan_loaded_objects(Port,save["destination_port"])
        destination_storage = game.scan_loaded_objects(Storage,save["destination_storage"])
        home_location = game.scan_loaded_objects(Location,save["home_location"])
        instance = cls(
            game,
            save["name"],
            reward_good,
            save["reward_amount"],
            save["deadline"],
            good,
            save["amount"],
            destination_port,
            destination_storage,
            home_location,
            expired=save["expired"],
            complete=save["complete"],
            complete_notice=save["complete_notice"],
            contract_travel_time=save["contract_travel_time"],
            active=save["active"],
            ID=save["ID"]
        )
        return instance

    def simple_table(self) -> dict:
        table_data = {}
        status = f"{style.RED}Expired{style.RESET}" if self.expired else f"{style.YELLOW}Due day {self.deadline}{style.RESET}"
        status = f"{style.GREEN}Complete!{style.RESET}" if self.complete_notice else f"{style.YELLOW}Due day {self.deadline}{style.RESET}"
        table_data = {
            "Name": self.name,
            "Destination": self.destination_port.location.name,
            "Status": status
        }
        return table_data

    def complex_table(self) -> dict:
        table_data = {}
        status = f"{style.RED}Expired{style.RESET}" if self.expired else f"{style.YELLOW}Due day {self.deadline}{style.RESET}"
        status = f"{style.GREEN}Complete!{style.RESET}" if self.complete_notice else f"{style.YELLOW}Due day {self.deadline}{style.RESET}"
        reward = f"{self.reward_amount} {self.reward_good.name}"
        table_data = {
            "Amount": self.amount,
            "Good": self.good.name,
            "Reward": reward,
            "Destination": self.destination_port.location.name,
            "Status": status
        }
        return table_data

    def check_completion(self):
        if self.destination_storage.cargo.get(self.good,0) >= self.amount:
            self.destination_storage.remove_cargo(self.good,self.amount)
            return True
        return False
    def on_day_passed(self, day):
        if not self.complete and self.active:
            if self.check_completion(): #Check if contract is complete
             #Check if it was already complete
                self.contract_travel_time = day + random.randint(2,5) #Random travel time for reward delivery
                self.complete = True
        if day == self.contract_travel_time and self.complete is True and self.complete_notice is False and self.expired is False: #Check if reward should be delivered
            self.complete_notice = True
            return f"Contract for {self.amount} {self.good.name} is ready to be cashed out!"
        if self.deadline < day and self.complete is False:
            self.expired = True

class CrewRole:
    def __init__(self,name:str,description:str,game:Game,sailing_booster:int=0,maintenance_booster:int=0, ID:str | None=None):
        self.name = name
        self.description = description
        self.sailing_booster = sailing_booster
        self.maintenance_booster = maintenance_booster
        self.ID = ID if ID is not None else None
        game.register(self)
    
    def save(self) -> dict:
        save = {
            "name":self.name,
            "description":self.description,
            "sailing_booster":self.sailing_booster,
            "maintenance_booster":self.maintenance_booster,
            "ID":self.ID
            }
        return save
    
    @classmethod
    def init_load(cls, save: dict,context:LoadContext):
        game = context.game
        instance = cls(
            save["name"],
            save["description"],
            game,
            save["sailing_booster"],
            save["maintenance_booster"],
            ID=save["ID"]
        )
        return instance

class Human:
    def __init__(self,max_health:int=100,strength:int=5,name:str | None = None):
        self.health = Stat(max_health)
        self.strength = strength
        self.name = name if name is not None else genname()

class CrewMate(Human):
    def __init__(self,crew_role:CrewRole,game:Game,sailing_ability:int | None = None,maintenance_ability:int | None = None, name:str | None = None, ID:str | None = None):
        super().__init__(name=name)
        self.crew_role = crew_role
        self.sailing_ability = Stat(100,current_value=sailing_ability if sailing_ability is not None else random.randint(10,20)+crew_role.sailing_booster) #Base sailing ability is a random number between 10 and 20, plus any booster from their crew role
        self.maintenance_skill = Stat(100,current_value=maintenance_ability if maintenance_ability is not None else random.randint(10,20)+crew_role.maintenance_booster) #Base maintenance skill is a random number between 10 and 20, plus any booster from their crew role
        self.ID = ID if ID is not None else None
        game.register(self)
    
    def save(self) -> dict:
        save = {
            "crew_role":self.crew_role.ID,
            "sailing_ability":self.sailing_ability.current_value,
            "maintenance_skill":self.maintenance_skill.current_value,
            "name":self.name,
            "ID":self.ID
        }
        return save
    
    @classmethod
    def init_load(cls, save: dict,context:LoadContext):
        game = context.game
        role = game.scan_loaded_objects(CrewRole,save["crew_role"])
        instance = cls(
            role,
            game,
            save["sailing_ability"],
            save["maintenance_skill"],
            save["name"],
            ID=save["ID"]
        )
        return instance

#This class is abstract, meaning it cannot be instantiated without being inherited from, and any class that inherits from it must implement run_event
class ShipEvent(ABC):
    def __init__(self,name:str):
        self.name = name

    @abstractmethod
    def run_event(self,ship:"Ship"):
        pass #This function is meant to be overridden by child classes, it will run the event's effects on the ship that is passed in as a parameter

class ShipNeed:
    def __init__(self,parent_ship:'Ship',crew_skill_tie_in:str,ship_stat_tie_in:str,name:str,max_value:int):
        '''crew_skill_tie_in is the EXACT name of the skill that will contribute to this need (ex: "maintenance_skill").\n
        ship_stat_tie_in is the EXACT name of the ship stat that will be affected by this need (ex: "toughness")'''
        self.parent_ship = parent_ship
        self.crew_skill_tie_in = crew_skill_tie_in
        self.ship_stat_tie_in = ship_stat_tie_in
        self.name = name
        self.max_value = max_value
        self.need_value = Stat(max_value,0,0)
    def update_need_value(self):
        '''Checks if the need is being met'''
        #calculate the total contribution from the crew
        total_contribution = 0
        for crew_mate in self.parent_ship.crew:
            if hasattr(crew_mate, self.crew_skill_tie_in):
                total_contribution += getattr(crew_mate, self.crew_skill_tie_in).current_value
        self.need_value += total_contribution #Use += because Stat will auto handle clamping the value

    def run_need(self):
        '''Checks if the need is being met, and applies consequences if it isn't'''
        self.update_need_value()
        if not self.need_value.full():
            degradation = self.need_value.max_value - self.need_value.current_value
            if hasattr(self.parent_ship, self.ship_stat_tie_in):
                current_stat = getattr(self.parent_ship, self.ship_stat_tie_in)
                if isinstance(current_stat, Stat):
                    current_stat -= degradation
                    self.parent_ship.ships_log.append(f"{self.name} need not met! {self.ship_stat_tie_in} degraded by {degradation}. Current {self.ship_stat_tie_in}: {current_stat}")
                else:
                    raise TypeError(f"{self.ship_stat_tie_in} is not a Stat instance")
            else:
                raise AttributeError(f"Parent ship does not have attribute {self.ship_stat_tie_in}")

class ShipType:
    def __init__(self,game:Game,name:str,health:int=100,cargo_capacity:int=48000,crew_capacity:int=10,max_sailing_efficiency:int=50,toughness:int=35,daily_maintenance:int=10, ID:str | None = None):
        '''All default stats are for a sloop, the smallest/starter ship'''
        self.game = game
        self.name = name
        self.health = health
        self.cargo_capacity = cargo_capacity #This is in kg
        self.crew_capacity = crew_capacity
        self.sailing_efficiency = max_sailing_efficiency #This is the max amount of sailing efficiency (sum of all crew sailing skill) for this ship to perform at its best. Adding crew that boost sailing efficiency past this point will do nothing
        self.toughness = toughness
        self.ID = ID if ID is not None else None
        #Needs
        self.daily_maintenance = daily_maintenance #If this is not met, the ship's toughness will degrade
        game.register(self)
    def save(self) -> dict:
        save = {
            "name":self.name,
            "health":self.health,
            "cargo_capacity":self.cargo_capacity,
            "crew_capacity":self.crew_capacity,
            "sailing_efficiency":self.sailing_efficiency,
            "toughness":self.toughness,
            "daily_maintenance":self.daily_maintenance,
            "ID":self.ID
        }
        return save
    
    @classmethod
    def init_load(cls, save: dict,context:LoadContext):
        game = context.game
        instance = cls(
            game,
            save["name"],
            save["health"],
            save["cargo_capacity"],
            save["crew_capacity"],
            save["sailing_efficiency"],
            save["toughness"],
            save["daily_maintenance"],
            ID = save["ID"]
        )
        return instance

class Ship:
    def __init__(self,name:str,ship_type:ShipType,event_list:list[ShipEvent],game:Game,crew:list['CrewMate'] | None = None,coordinates:tuple | None = None, current_health:int | None = None, current_toughness:int | None = None, ships_log:list[str] | None = None, storage:Storage | None = None, is_dispatched:bool | None = None, travel_progress:Stat | None = None, destinations:list[Location] | None = None, current_destination:Location | None = None, contracts:list[Contract] | None = None, home_port:'Port' | None = None, current_port:'Port' | None = None, last_port:'Port'| None = None, is_under_repair:bool | None = None, daily_repair_amount:int | None = None, ID = None):
        self.ship_type = ship_type
        self.game = game
        self.coordinates = coordinates if coordinates is not None else (0,0)
        self.ID = ID if ID is not None else None
        self.game.register(self) #Register to game time so it can track daily needs and events
        #SHIP STATS
        self.health = Stat(ship_type.health,0,current_health if current_health is not None else ship_type.health)
        self.sailing_efficiency = Stat(ship_type.sailing_efficiency,current_value=0) # Does not need to be saved as it is calculated later is calculate_crew_amount(). This determines the max a ship can perform (so a rowboat's max performance will be less than a proper ship). The actual ship performace (the current value of this stat) is determined by the sum of all crew sailing_ability
        self.toughness = Stat(ship_type.toughness,0,current_toughness if current_toughness is not None else ship_type.toughness) # This is the max ship toughness, this may degrade during travels        
        #Internal properties (only to be adjsuted within the declaration of the class)
        self.name = name
        self.event_list = event_list # Not saved, gonna pass event_list into the load function
        self.ships_log = ships_log if ships_log is not None else []
        self.crew_amount = Stat(ship_type.crew_capacity,0,0) # Calculated later, does not need to be saved
        self.crew = crew if crew is not None else []
        #Affectable ship properties (to be adjusted by outside factors)
        self.storage = Storage(f"{name} Cargo",self.game, ship_type.cargo_capacity) if storage is None else storage
        self.is_dispatched = is_dispatched if is_dispatched is not None else False
        self.travel_progress = travel_progress if travel_progress is not None else Stat(0,0,0)
        self.destinations:list[Location] = destinations if destinations is not None else []
        self.current_destination:Location = current_destination if current_destination is not None else None
        self.contracts:list[Contract] = contracts if contracts is not None else []
        self.home_port:Port = home_port if home_port is not None else None
        self.current_port:Port = current_port if current_port is not None else None
        self.last_port:Port = last_port if last_port is not None else None
        
        #Ship needs
        self.daily_maintenance = ShipNeed(self,"maintenance_skill","toughness","Maintenance",ship_type.daily_maintenance)

        #Needs list
        self.needs = [self.daily_maintenance]

        self.calculate_crew_amount()

        # Properties for events to interact with
        self.daily_storm_value = Stat(100,0,0)
        self.daily_wind = Stat(100,0,0) #Average wind is 50

        #Repair values
        self.is_under_repair = is_under_repair if is_under_repair is not None else False
        self.daily_repair_amount = daily_repair_amount if daily_repair_amount is not None else 0

    def save(self) -> dict:
        save = {
            # All stat values are current value, as their max value is populated by ship type
            "ship_type":self.ship_type.ID,
            "coordinates":self.coordinates,
            "ID":self.ID,
            "current_health":self.health.current_value,
            #"sailing_efficiency":self.sailing_efficiency.current_value,
            "current_toughness":self.toughness.current_value,
            "name":self.name,
            "ships_log":self.ships_log,
            "crew":[crewMate.ID for crewMate in self.crew],
            "storage":self.storage.ID,
            "is_dispatched":self.is_dispatched,
            "travel_progress":self.travel_progress.as_tuple(),
            "destinations":[loc.ID for loc in self.destinations] if len(self.destinations) > 0 else None,
            "current_destination": self.current_destination.ID if self.current_destination else None,
            "contracts":[con.ID for con in self.contracts] if len(self.contracts) > 0 else None,
            "home_port":self.home_port.ID if self.home_port is not None else None,
            "current_port":self.current_port.ID if self.current_port is not None else None,
            "last_port":self.last_port.ID if self.last_port is not None else None,
            "is_under_repair":self.is_under_repair,
            "daily_repair_amount":self.daily_repair_amount
        }
        return save

    @classmethod
    def init_load(cls,save:dict,context:LoadContext):
        game=context.game
        event_list = context.event_list
        ship_type = game.scan_loaded_objects(ShipType,save["ship_type"])
        storage = game.scan_loaded_objects(Storage,save["storage"])
        instance = cls(
            save["name"],
            ship_type,
            event_list,
            game,
            storage = storage,
            ID=save["ID"]
        )
        instance._save_data = save  # 🔥 store for phase 2
        return instance
    
    def secondary_load(self,save:dict,context:LoadContext):
        game = context.game
        crew = [game.scan_loaded_objects(CrewMate,crewID) for crewID in save["crew"]] if save["crew"] else []
        destinations = [game.scan_loaded_objects(Location,destID) for destID in save["destinations"]] if save["destinations"] else []
        current_destination = game.scan_loaded_objects(Location,save["current_destination"]) if save["current_destination"] else None
        contracts = [game.scan_loaded_objects(Contract,conID) for conID in save["contracts"]] if save["contracts"] else []
        home_port = game.scan_loaded_objects(Port,save["home_port"]) if save["home_port"] else None
        current_port = game.scan_loaded_objects(Port,save["current_port"]) if save["current_port"] else None
        last_port = game.scan_loaded_objects(Port,save["last_port"]) if save["last_port"] else None
        self.crew=crew
        self.coordinates=save["coordinates"]
        self.health.current_value = save["current_health"]
        self.toughness.current_value = save["current_toughness"]
        self.ships_log=save["ships_log"]
        self.is_dispatched=save["is_dispatched"]
        self.travel_progress=Stat.from_tuple(save["travel_progress"])
        self.destinations=destinations
        self.current_destination=current_destination
        self.contracts=contracts
        self.home_port=home_port
        self.current_port=current_port
        self.last_port=last_port
        self.is_under_repair=save["is_under_repair"]
        self.daily_repair_amount=save["daily_repair_amount"]
    
    #NON-USER FRIENDLY FUNCTIONS (NO UI)
    def start_repairs(self,daily_repair_amount:int):
        '''Will repair the ship daily while the ship is in port, until the ship is fully repaired or leaves port'''
        self.is_under_repair = True
        self.daily_repair_amount = daily_repair_amount
    
    def _run_daily_repairs(self,daily_repair_amount:int):
        if self.is_under_repair:
            if self.current_port:
                self.health += daily_repair_amount
                self.ships_log.append(f"Ship repaired by {daily_repair_amount}. Current health: {self.health}")
            else:
                self.ships_log.append("Ship is not in port, terminating repairs")
                self.is_under_repair = False

    def calculate_crew_amount(self):
        self.crew_amount.current_value = 0
        for crew_mate in self.crew:
            if self.crew_amount.full():
                raise ValueError("Total crew cannot exceed crew capacity at __init__")
            self.crew_amount += 1
            self.sailing_efficiency += crew_mate.sailing_ability.current_value
    def update_ship_daily_needs(self):
        '''Updates all ship daily needs'''
        for need in self.needs:
            need.update_need_value()
    def run_ship_daily_needs(self,days:int):
        '''Checks all ship needs and runs consequences'''
        for need in self.needs:
            need.run_need()
    def calculate_ship_stats_daily_variation(self,days:int):
        '''All of the daily variation that the ship may encounter. This is where the events are run.'''
        self.daily_storm_value.current_value = 0
        self.daily_wind.current_value = 50
        self.sailing_efficiency.current_value = 0
        self.run_events(days)
        for crew_mate in self.crew:
            if self.crew_amount.full():
                raise ValueError("Total crew cannot exceed crew capacity at __init__")
            self.sailing_efficiency.current_value += crew_mate.sailing_ability.current_value + random.randint(-5,5) # random variation added to each crewmate's ability
        if self.daily_storm_value.current_value > self.toughness.current_value:
            damage = self.daily_storm_value.current_value - self.toughness.current_value
            self.health -= damage
            self.ships_log.append(f"Ship took {damage} damage from the storm! Current health: {self.health}")
        if self.health.current_value <= 0:
            DeathMessage = MessengerPigeon(self.game,f"The {self.name} has been destroyed at sea!",self.coordinates,self.home_port.location.coordinates) #The coordinates here are placeholders, as the pigeon system is not fully implemented yet
            self.game.unregister(self) #Unregister the ship from game time, makes no more references and pyhton cleans it up automatically
            #Handle ship destruction (this could be expanded to include things like losing cargo, or the crew being stranded at sea, but for now it just logs the destruction of the ship)

    def add_crew(self,new_crew:'CrewMate'):
        '''Returns True on success, false on failure'''
        if not self.crew_amount.full():
            self.crew.append(new_crew)
            self.sailing_efficiency += new_crew.sailing_ability.current_value
            self.crew_amount += 1
            return True
        else:
            return False
    
    def remove_crew(self,crew_mate:'CrewMate'):
        '''Returns True on success, false on failure'''
        if crew_mate in self.crew:
            self.crew.remove(crew_mate)
            self.sailing_efficiency -= crew_mate.sailing_ability.current_value
            self.crew_amount -= 1
            return True
        else:
            return False
    # INTERNAL FUNCTIONS

    def dispatch(self, destination:'Location', game:Game):
        '''This is an internal function, should not regularily be called outside of the class \n
        Use primary_dispatch() instead\n
        This function is the action of sending a ship off, but will not handle things like multiple destinations, or returning the ship to its home port'''
        travel_time = distance((self.current_port.location.coordinates[0],self.current_port.location.coordinates[1]),(destination.coordinates[0],destination.coordinates[1]))
        self.travel_progress.current_value = 0
        self.travel_progress.max_value = distance(self.current_port.location.coordinates,destination.coordinates)
        #travel_time = round(math.sqrt((self.current_port.location.coordinates[0] - destination.coordinates[0])**2 + (self.current_port.location.coordinates[1] - destination.coordinates[1])**2) / 100) #The formula I learned in school, forgot, and then searched up when I needed it. Thanks grade 10 advanced math, you helped, a little, kinda, thanks, a little. Thanks google.
        self.day_of_arrival = game.day + travel_time
        self.ships_log.append(f"-----Dispatched to {destination.name}-----")
        self.current_destination = destination
        self.destinations.remove(destination) #Remove the current destination from the ship's list of possible destinations (this only removes the first instance of that destination)
        self.current_port.ships.remove(self) #Remove the ship from the port while it is dispatched
        self.last_port = self.current_port
        self.current_port = None
        self.is_dispatched = True
    def run_events(self,days:int):
        #Event logic
        if self.is_dispatched:
            event_roll = random.randint(1,4) #Decide if an event happens today
            if event_roll == 1 and len(self.event_list) > 0: #If an event is to happen, and there are events to happen
                event:ShipEvent = random.choice(self.event_list) #Select a random event from the list
                event.run_event(self) #Run the event, passing in the ship as a parameter
                self.ships_log.append(f"Day {days}: {event.name} event occurred.")
    def daily_travel(self,days:int):
        if self.is_dispatched:
            # Run travel logic
            self.run_ship_daily_needs(days)
            self.calculate_ship_stats_daily_variation(days)
            self.travel_progress += self.sailing_efficiency.current_value * ((self.daily_wind.current_value/100)*2)  #The ship moves faster the higher its sailing efficiency and wind
            self.coordinates = point_along_vector(self.last_port.location.coordinates,self.current_destination.coordinates,self.travel_progress.current_value)
            #input(self.travel_progress)
            # Check for arrival at a port
            if self.travel_progress.full():
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
                    self.dispatch(self.destinations[0],self.current_port.game) #Dispatch to the next destination in the list (this only dispatches to the first instance of that destination)
                else:
                    self.is_dispatched = False
                    self.current_destination = None
                    self.day_of_arrival = None #Make this None so it throws errors if anything tries to interact with it, helps with pinpointing lost ship bugs
                    self.ships_log.append(f"No more destinations, {self.name} is now idle.")
                    return f"{self.name} has arrived at {self.current_port.name} and has no more destinations, it is now idle."
        return None
    
    #EXTERNAL FUNCTIONS
    def primary_dispatch(self, destinations:'Location', game:Game):
        '''Call this function to dispatch a ship (DO NOT USE dispatch())\n
        This function will handle all the backend for proper ship dispatch that dispatch() will not'''
        self.destinations = destinations
        self.home_port = self.current_port
        self.destinations.append(self.current_port.location) #Add the current location as the final destination so the ship returns home after its route is complete
        self.dispatch(self.destinations[0],game)

    def manage_crew(self,player:Player):
        while True:
            table_data = {}
            for crew_mate in self.crew:
                table_data[crew_mate.name] = {
                    "Name": crew_mate.name,
                    "Role": crew_mate.crew_role.name,
                    "Health": crew_mate.health,
                    "Sailing Ability": crew_mate.sailing_ability
                }
            selected_crew = menu(f"{self.name} crew", [crew_mate.name for crew_mate in self.crew], True, table = table_data)
            if selected_crew is not None:
                while True:
                    crew_mate = self.crew[selected_crew-1]
                    table_data = {
                        crew_mate.name: {
                            "Name": crew_mate.name,
                            "Role": crew_mate.crew_role.name,
                            "Health": crew_mate.health,
                            "Sailing Ability": crew_mate.sailing_ability
                        }
                    }
                    action = menu(f"{crew_mate.name} - {crew_mate.crew_role.name}", ["Transfer ship","Terminate contract"], return_option=True,table=table_data)
                    match action:
                        case 1:
                            while True:
                                selected_ship = menu("Select a ship to add this crew mate to", [ship.name for ship in player.fleet.ships], return_option=True)
                                if selected_ship is not None:
                                    selected_ship = player.fleet.ships[selected_ship-1]
                                    if selected_ship.add_crew(crew_mate):
                                        self.remove_crew(crew_mate)
                                        input(f"{crew_mate.name} has been transferred to {selected_ship.name}!")
                                        break
                                    else:
                                        input(f"{selected_ship.name} does not have enough crew capacity to add {crew_mate.name}, press enter to continue")
                                else:
                                    break
                        case 2:
                            if self.remove_crew(crew_mate):
                                input(f"{crew_mate.name} has been terminated, press enter to continue")
                            else:
                                input("There was an error terminating that crew mate, press enter to continue")
                        case _:
                            break
                    break
            else:
                break
    
    # Final thing

    def on_day_passed(self, days:int):
        #Daily checks
        self._run_daily_repairs(self.daily_repair_amount) #This checks if the ship is under repair too
        self.coordinates = (self.current_port.location.coordinates[0],self.current_port.location.coordinates[1]) if self.current_port is not None else self.coordinates
        msg = None
        msg = self.daily_travel(days)
        return msg

class Warehouse:
    def __init__(self,name:str,game:Game,storage:Storage | None = None,max_weight:int = 10000,ID:str | None = None):
        self.name = name
        self.storage = storage if storage is not None else Storage(f"{name} Warehouse",game,max_weight)
        self.ID = ID if ID is not None else None
        game.register(self)

    def save(self):
        save = {
            "name":self.name,
            "storage":self.storage.ID,
            "ID":self.ID
        }
        return save

    @classmethod
    def init_load(cls,save:dict,context:LoadContext):
        game = context.game
        storage = game.scan_loaded_objects(Storage,save["storage"])
        game = context.game
        instance = cls(
            save["name"],
            game,
            storage,
            ID = save["ID"]
        )
        return instance

class Port:
    def __init__(self, name: str, location:Location,world:World,game:Game,currency_goods:list[Good],ships: list[Ship] | None = None, warehouses: list[Warehouse] | None = None, ID:str | None = None):
        self.name = name
        self.location = location
        self.world = world
        self.game = game
        self.currency_goods = currency_goods
        self.ships = list(ships) if ships is not None else []
        self.ship_names = []
        self.warehouses = list(warehouses) if warehouses is not None else []
        self.location.add_port(self) # Since location is static and does not save its ports, ports need to re-add themselves to location on load
        if self.ships is not None:
            for ship in self.ships:
                ship.current_port = self
        self.planned_destinations:list[Location] = []
        
        self.ID = ID if ID is not None else None
        game.register(self)
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
                    input("Cargo moved! Press enter to continue")

    # ===== Player interacting functions =====
    # ==SUB FUNCTIONS==
    def repair_ship_menu(self,selected_ship:Ship,player:Player):
        while True:
            clear_terminal()
            days_to_repair = math.floor((selected_ship.health.max_value - selected_ship.health.current_value)/10)
            cost_to_repair = days_to_repair * 20
            table_data = {
                "Table Data": {
                    "Health": selected_ship.health,
                    "Days to Repair": days_to_repair
                }
            }
            sub_table_data = {
                "Cost to Repair":
                {good.name: math.ceil(cost_to_repair/good.value) for good in self.currency_goods}
            }
            answer = menu("Repair ship",[f"Pay with {good.name}" for good in self.currency_goods],True,table=table_data,sub_table=sub_table_data)
            if answer is not None:
                selected_good = self.currency_goods[answer-1]
                selected_warehouse:Warehouse = player.warehouses[menu("Select warehouse to pay from",[warehouse.name for warehouse in player.warehouses],True)-1]
                if selected_warehouse is not None:
                    if selected_good in selected_warehouse.storage.cargo and selected_warehouse.storage.cargo[selected_good]*selected_good.value >= cost_to_repair:
                        amount_to_remove = math.ceil(cost_to_repair/selected_good.value)
                        selected_warehouse.storage.remove_cargo(selected_good,amount_to_remove)
                        selected_ship.start_repairs(10)
                        input(f"{selected_ship.name} is now undergoing repairs! Press enter to continue")
                        break
                    else:
                        input("You do not have enough of that good to pay for repairs, press enter to continue")
            else:
                break
    def dispatch_menu(self,selected_ship:Ship,player:Player):
        while True:
            clear_terminal()
            answer = menu("Route planning",["Add contracts","Add destinations","Dispatch"],True)
            match answer:
                # Dispatch with contract logic
                case 1:
                    clear_terminal()
                    contract_names = []
                    for contract in player.contracts:
                        contract_names.append(f"{contract.amount} {contract.good.name} to {contract.destination_port.name}")
                    contract_names.append("clear all")
                    selected_contract_names = ["Selected Contracts"] + [f"{contract.amount} {contract.good.name} to {contract.destination_port.name}" for contract in selected_ship.contracts]
                    while True:
                        try:
                            answer = menu("Select contracts to add (order does not matter)",contract_names,True,table=selected_contract_names)
                            if answer == len(contract_names): #Clear all option
                                selected_contract_names = ["Selected Contracts"]
                                for contract in player.contracts:
                                    if contract in selected_ship.contracts:
                                        selected_ship.contracts.remove(contract) #Remove the contract from the ship if its currently selected
                                continue
                            selected_contract_names.append(contract_names[answer-1])
                        except Exception:
                            break
                        selected_contract:Contract = player.contracts[answer-1]
                        
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
                        selected_ship.calculate_crew_amount()
                        if selected_ship.crew_amount.current_value > 0:
                            selected_ship.primary_dispatch(self.planned_destinations,self.game)
                            print(f"{selected_ship.name} has been dispatched!")
                            input("Press enter to continue")
                            return True
                        else:
                            input("You cannot dispatch a ship with no crew, press enter to continue")
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
                from_storage:Storage = self.warehouses[menu("Load from",self.warehouse_names) -1].storage #Get the warehouse we are moving from
                self.transfer_goods(from_storage,selected_ship.storage)
            #Another ship loading logic
            case 2:
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
        input("Name changed! Press enter to continue")

    # ==MAIN FUNCTIONS==
    def manage_ships(self,player:Player):
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
                table_data = {
                    ship.name: {
                        "Name": ship.name,
                        "Type": ship.ship_type.name,
                        "Health": ship.health,
                        "In repair": f"{style.RED}Yes{style.RESET}" if ship.is_under_repair else f"{style.GREEN}No{style.RESET}",
                    } for ship in self.ships
                }
                selected_ship:Ship = self.ships[menu(self.name,self.ship_names,return_option=True,art=game_art.port_birds_eye,table=table_data) -1] #Select a ship to manage\
            except Exception:
                break
            # Ship management menu
            while True:
                clear_terminal()
                table_data = {
                        selected_ship.name: {
                            "Name": selected_ship.name,
                            "Type": selected_ship.ship_type.name,
                            "Health": selected_ship.health,
                            "Toughness": selected_ship.toughness,
                            "Sailing Efficiency": selected_ship.sailing_efficiency
                        }
                    }
                selected_ship.update_ship_daily_needs() #Check if the ship's needs are being met, and update the need values accordingly, this is done here to allow the player to see the current state of the ship's needs in the menu
                sub_table_data = {
                    "Daily upkeed": 
                            {need.name: need.need_value for need in selected_ship.needs}
                }
                action = menu(f"{selected_ship.name} actions",["Load","view inventory","Plan voyage","View crew","Change name","View event log","Repair ship"],return_option=True,art=game_art.ship_1,table=table_data,sub_table=sub_table_data)
                match action:
                    case 1:
                        #Load ship
                        self.load_ship_menu(selected_ship)
                    case 2:
                        #Show invent
                        clear_terminal()
                        selected_ship.storage.show_invent()
                    case 3:
                        #Dispatch ship
                        if self.dispatch_menu(selected_ship,player) == True:
                            break
                    case 4:
                        #View crew
                        selected_ship.manage_crew(player)
                    case 5:
                        #Rename ship
                        self.change_ship_name_menu(selected_ship)
                    case 6:
                        #View ships log
                        clear_terminal()
                        print(f"Event log for {selected_ship.name} ({len(selected_ship.ships_log)}):")
                        for log_entry in selected_ship.ships_log:
                            print(log_entry)
                        input("Press enter to go back")
                    case 7:
                        #Repair ship
                        self.repair_ship_menu(selected_ship,player)
                    case _:
                        break
    
    def save(self):
        save  = {
            "name":self.name,
            "location":self.location.ID,
            "world":self.world.ID,
            "currency_goods":[good.ID for good in self.currency_goods],
            "ships":[ship.ID for ship in self.ships],
            "warehouses":[warehouse.ID for warehouse in self.warehouses],
            "ID":self.ID
        }
        return save

    @classmethod
    def init_load(cls,save:dict,context:LoadContext):
        game = context.game
        location = game.scan_loaded_objects(Location,save["location"])
        world = game.scan_loaded_objects(World,save["world"])
        currency_goods = []
        for good_id in save["currency_goods"]:
            currency_goods.append(game.scan_loaded_objects(Good,good_id))
        instance = cls(
            save["name"],
            location,
            world,
            game,
            currency_goods,
            ID=save["ID"]
        )
        instance._save_data = save
        return instance

    def secondary_load(self,save,context:LoadContext):
        game = context.game
        ships = []
        warehouses = []
        for warehouse_id in save["warehouses"]:
            warehouses.append(game.scan_loaded_objects(Warehouse,warehouse_id))
        for ship_id in save["ships"]:
            ships.append(game.scan_loaded_objects(Ship,ship_id))
        self.ships = ships
        self.warehouses = warehouses

class Fleet:
    def __init__(self,ships:list[Ship],game:Game, ID:str | None = None):
        self.ships = ships
        self.ID = ID if ID is not None else None
        game.register(self)
    
    def save(self):
        save = {
            "ships":[ship.ID for ship in self.ships],
            "ID":self.ID
        }
        return save

    @classmethod
    def init_load(cls,save:dict,context:LoadContext):
        game = context.game
        ships = [game.scan_loaded_objects(Ship,shipID) for shipID in save["ships"]]
        instance = cls(
            ships,
            game,
            save["ID"]
        )
        return instance

class Player:
    def __init__(self, game:Game,storage: Storage, reputation: int, fleet: Fleet | None = None, contracts: list[Contract] | None = None, warehouses: list[Warehouse] | None = None, ID:str | None = None):
        self.storage = storage
        self.reputation = reputation
        self.fleet = fleet if fleet is not None else None
        self.contracts = list(contracts) if contracts is not None else []
        self.warehouses = list(warehouses) if warehouses is not None else []
        self.game = game
        self.ID = ID if ID is not None else None
        game.register(self)
    def view_stats(self):
        print(f"Reputation: {self.reputation}")
        print(f"Fleet size: {len(self.fleet.ships) if self.fleet else 0}")
        self.storage.show_invent()
    def view_contracts(self):
        table_data = {}
        for contract in self.contracts:
            table_data[contract.good.name] = contract.simple_table()
        ans = menu("Contracts", [f"{contract.name}" for contract in self.contracts], table=table_data, return_option=True)
        if ans is not None:
            selected_con = self.contracts[ans-1]
            menu(f"{selected_con.name}",[],True,table={"":selected_con.complex_table()})

    def select_contract(self):
        table_data = {}
        for contract in self.contracts:
            table_data[contract.good.name] = contract.simple_table()
        ans = menu("Contracts", [f"{contract.name}" for contract in self.contracts], table=table_data, return_option=True)
        if ans is not None:
            return self.contracts[ans-1]
        else:
            return None

    def player_actions(self):
        while True:
            answer = menu("Player actions",["View stats","View contracts"],True)
            match answer:
                case 1:
                    clear_terminal()
                    self.view_stats()
                case 2:
                    clear_terminal()
                    self.view_contracts()
                case _:
                    break
    
    def save(self):
        save = {
            "storage":self.storage.ID,
            "reputation":self.reputation,
            "fleet":self.fleet.ID if self.fleet is not None else None,
            "contracts":[con.ID for con in self.contracts],
            "warehouses":[house.ID for house in self.warehouses],
            "ID":self.ID
        }
        return save
    
    @classmethod
    def init_load(cls,save:dict,context:LoadContext):
        game = context.game
        storage = game.scan_loaded_objects(Storage,save["storage"])
        instance = cls(
            game,
            storage,
            save["reputation"],
            ID=save["ID"]
        )
        instance._save_data = save
        return instance
    
    def secondary_load(self,save:dict,context:LoadContext):
        game = context.game
        self.fleet = game.scan_loaded_objects(Fleet,save["fleet"])
        self.contracts = [game.scan_loaded_objects(Contract,conID) for conID in save["contracts"]]
        self.warehouses = [game.scan_loaded_objects(Warehouse,houseID) for houseID in save["warehouses"]]

class Exchange:
    def __init__(self, name: str, location:Location, game: Game, world: World,
                good_list: list[Good] | None = None,
                 reward_list: list[Good] | None = None, max_cargo_weight: int = 1000, ID:str | None = None):
        self.name = name
        self.location = location
        self.game = game
        self.world = world
        self.ID = ID if ID is not None else None
        game.register(self) #Register the exchange to game
        # defensive copies: new list for each instance
        #self.contracts = list(contracts) if contracts is not None else []
        self.contracts = []
        self.good_list = list(good_list) if good_list is not None else []
        self.reward_list = list(reward_list) if reward_list is not None else []
        self.max_cargo_weight = max_cargo_weight
        if self.location is not None and type(self.location) is Location:
            if self not in self.location.exchanges:
                self.location.add_exchange(self)
        else:
            raise ValueError("Exchange must have a valid Location")

    def save(self):
        save = {
            "name":self.name,
            "location":self.location.ID,
            "world":self.world.ID,
            "good_list":[good.ID for good in self.good_list] if len(self.good_list) > 0 else [],
            "reward_list":[reward.ID for reward in self.reward_list] if len(self.reward_list) > 0 else [],
            "max_cargo_weight":self.max_cargo_weight,
            "ID":self.ID
        }
        return save

    @classmethod
    def init_load(cls,save:dict,context:LoadContext):
        game = context.game
        location = game.scan_loaded_objects(Location,save["location"])
        world = game.scan_loaded_objects(World,save["world"])
        good_list = [game.scan_loaded_objects(Good,goodID) for goodID in save["good_list"]]
        reward_list = [game.scan_loaded_objects(Good,rewardID) for rewardID in save["reward_list"]]
        instance = cls(
            save["name"],
            location,
            game,
            world,
            good_list = good_list,
            reward_list = reward_list,
            max_cargo_weight = save["max_cargo_weight"],
            ID=save["ID"]
        )
        instance._save_data = save
        return instance

    def secondary_load(self,save,context):
        if not self.contracts:   # safer check for empty list
            self.gen_daily_contracts()

    def gen_daily_contracts(self):
        if len(self.good_list) == 0 or len(self.reward_list) == 0 or self.game is None:
            raise ValueError("If no contracts are provided, good_list, reward_list, and Game must be provided. Also, make sure the day value is accurate.")
        for i in range(random.randint(3,5)):
            self.contracts.append(gen_contract(self.game,self.good_list,self.reward_list,self.game.day,self.location,self.world,self.max_cargo_weight)) #We can Game.register contracts that are selected, dont need to do it when they are generated
    
    def on_day_passed(self, days):
        for contract in self.contracts:
            self.game.unregister(contract)
        self.contracts = []
        self.gen_daily_contracts()

    def show_contracts(self):
        if len(self.contracts) == 0:
            self.gen_daily_contracts()
        table_data = {}
        for i, c in enumerate(self.contracts, start=1):
            status = "Expired" if c.expired else f"Due day {c.deadline}"
            reward = f"{c.reward_amount} {c.reward_good.name}"

            # Use i as the key for each contract
            table_data[i] = {
                "Amount": c.amount,
                "Good": c.good.name,
                "Reward": reward,
                "Destination": c.destination_port.location.name,
                "Status": status
            }
        return menu("Available Contracts", [f"{contract.amount} {contract.good.name} to {contract.destination_port.name}" for contract in self.contracts], table=table_data, return_option=True)
    
    def select_contract(self,player:Player):
        while True:
            clear_terminal()
            answer = self.show_contracts()
            if answer is None:
                return None
            chosen_contract = self.contracts[answer-1] 
            while True:
                clear_terminal()
                warehouse_names = []
                for warehouse in player.warehouses:
                    warehouse_names.append(warehouse.name)
                
                answer = menu("Where would you like to store these goods?",warehouse_names,True)
                if answer == None:
                    break
                answer -= 1
                selected_warehouse:Warehouse = player.warehouses[answer]
                if selected_warehouse.storage.add_to_cargo(chosen_contract.good,chosen_contract.amount):
                    input("Contract accepted! (press enter to continue)")
                    self.contracts.remove(chosen_contract) #Remove the contract from the exchange's list of contracts
                    chosen_contract.active = True
                    return chosen_contract
                else:
                    input("That warehouse cannot hold that much cargo, choose another (press enter to continue)")
    
    def cashout_contracts(self,player:Player):
        while True:
            clear_terminal()
            chosen_contract = player.select_contract()
            if chosen_contract is None:
                return
            try:
                if chosen_contract.complete_notice:
                    warehouse_names = []
                    for warehouse in player.warehouses:
                        warehouse_names.append(warehouse.name)
                    try:
                        answer = int(menu("Where would you like to store the reward?",warehouse_names,True))-1
                    except Exception:
                        break
                    selected_warehouse:Warehouse = player.warehouses[answer] 
                    if selected_warehouse.storage.add_to_cargo(chosen_contract.reward_good,chosen_contract.reward_amount):
                        input("Contract cashed out! (press enter to continue)")
                        player.contracts.remove(chosen_contract)
                        del chosen_contract
                    else:
                        input("That warehouse cannot hold that much cargo, choose another (press enter to continue)")
                else:
                    input("This contract is not yet ready to be cashed out. (press enter to continue)")
            except Exception:# as e:
                #print(e) #Uncomment this line to show error message when the user enters an invalid option
                input("Invalid selection, try again")
    
    def start_exchange(self,player:Player):
        while True:
            answer = menu("Exchange Menu",["View available contracts","Cashout contracts"],True)
            match answer:
                case 1:
                    contract = self.select_contract(player)
                    if type(contract) is Contract:
                        player.contracts.append(contract)
                case 2:
                    self.cashout_contracts(player)
                case _:
                    break

class Tavern:
    def __init__(self,name:str,game:Game,location:Location,crew_roles:list[CrewRole],player:Player,crew:list[CrewMate] | None = None, ID:str | None = None):
        self.name = name
        self.game = game
        self.location = location
        self.crew_roles = crew_roles
        self.crew = crew if crew is not None else []
        self.player = player
        self.ID = ID if ID is not None else None
        game.register(self)
        self.populate_crew(10)

    def populate_crew(self,crew_count:int):
        for i in range(crew_count):
            new_crew = gen_crewmate(self.crew_roles,self.game)
            self.crew.append(new_crew)
    
    def select_crew(self):
        table_data = {}
        for crew_mate in self.crew:
            table_data[crew_mate.name] = {
                "Name": crew_mate.name,
                "Role": crew_mate.crew_role.name,
                "Sailing Ability": crew_mate.sailing_ability
            }
        selected_crew = menu(f"{self.name} crew",list(table_data.keys()),return_option=True, table = table_data,art=game_art.tavern)
        if selected_crew is not None:
            selected_ship = menu("Select a ship to add this crew mate to", [ship.name for ship in self.player.fleet.ships], return_option=True)
            if selected_ship is not None:
                if self.player.fleet.ships[selected_ship-1].add_crew(self.crew[selected_crew-1]):
                    input(f"{self.crew[selected_crew-1].name} has been added to {self.player.fleet.ships[selected_ship-1].name}! (press enter to continue)")
                    self.crew.pop(selected_crew-1) #Remove the crew mate from the tavern's list of crew
                else:
                    input("Cannot add crew, that ship is at crew capacity!")
        else:
            None

    def save(self):
        save = {
            "name":self.name,
            "location":self.location.ID,
            "crew_roles":[role.ID for role in self.crew_roles],
            "player":self.player.ID,
            "ID":self.ID
        }
        return save

    @classmethod
    def init_load(cls,save:dict,context:LoadContext):
        game = context.game
        location = game.scan_loaded_objects(Location,save["location"])
        crew_roles = [game.scan_loaded_objects(CrewRole,roleID) for roleID in save["crew_roles"]]
        player = game.scan_loaded_objects(Player,save["player"])
        instance = cls(
            save["name"],
            game,
            location,
            crew_roles,
            player,
            ID = save["ID"]
        )
        return instance

    def on_day_passed(self, days):
        for crewMate in self.crew:
            self.game.unregister(crewMate)
        self.crew = []
        self.populate_crew(10)

class MessengerPigeon:
    def __init__(self,game:Game,message:str,start_coordinates:tuple[int],destination_coordinates:tuple[int], travel_time:int | None = None,ID:str | None = None):
        self.game = game
        self.message = message
        self.start_coordinates = start_coordinates
        self.destination_coordinates = destination_coordinates
        self.travel_time = travel_time if travel_time is not None else distance(start_coordinates,destination_coordinates) #Calculate travel time based on distance
        self.ID = ID if ID is not None else None
        self.game.register(self) #Register to game time so it can track travel time
    def on_day_passed(self, current_day):
        if self.travel_time > 0:
            self.travel_time -= 1
            if self.travel_time <= 0:
                self.game.unregister(self) #Unregister from game time, makes no more references and pyhton cleans it up automatically
                return f"A messenger pigeon has delivered a message:\n {self.message}"
        return None

    def save(self):
        save = {
            "message":self.message,
            "start_coordinates":self.start_coordinates,
            "destination_coordinates":self.destination_coordinates,
            "travel_time":self.travel_time,
            "ID":self.ID
            }
        return save
    
    @classmethod
    def init_load(cls,save:dict,context:LoadContext):
        game = context.game
        instance = cls(
            game,
            save["message"],
            save["start_coordinates"],
            save["destination_coordinates"],
            save["travel_time"],
            save["ID"]
        )
        return instance