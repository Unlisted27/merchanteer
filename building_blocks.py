import components,random

#Locations
grandure = components.Location("Grandure","A bustling trade city with a large port.")
clammer = components.Location("Clammer","A small fishing village known for its seafood.")
old_cove = components.Location("Old Cove","One of the first foreign settlements, old cove has survived through it all.")

#world things
game_time = components.GameTime()
world = components.World([grandure,clammer,old_cove])

#Currency goods
gold = components.Good("gold","shiny",1,0.1)
silver = components.Good("silver","shiny",0.5,0.1)
#Other goods
bread = components.Good("bread","staple food",0.1,0.05)
fish = components.Good("fish","protein food",0.3,1)
wood = components.Good("wood","building material",0.5,2)
cloth = components.Good("cloth","fabric material",0.3,0.1)
rice = components.Good("rice","staple food",0.2,1)

#Events
event_list = []

class BadWind(components.ShipEvent):
    def __init__(self):
        super().__init__("Bad Wind")
    
    def run_event(self,ship:components.Ship):
        ship.daily_wind.current_value = random.randint(0,40) #Bad wind reduces the daily wind value, slowing the ship down
        #input(f"Bad wind event occured on {ship.name}")
event_list.append(BadWind())

class GoodWind(components.ShipEvent):
    def __init__(self):
        super().__init__("Good Wind")
    
    def run_event(self,ship:components.Ship):
        ship.daily_wind.current_value = random.randint(60,100) #Good wind increases the daily wind value, speeding the ship up
        #input(f"Good wind event occured on {ship.name}")
event_list.append(GoodWind())

class Storm(components.ShipEvent):
    def __init__(self):
        super().__init__("Storm")
    
    def run_event(self,ship:components.Ship):
        ship.daily_storm_value.current_value = random.randint(1,100) #Storms increase the daily storm value, which can cause damage to the ship and crew
        #input(f"Storm event occured on {ship.name}")
event_list.append(Storm())

#Crew roles
buckaneer = components.CrewRole("Buckaneer","A regular sailor, well equiped in all areas but not excelling in any.")

# Crew

#Ship types
ketch = components.ShipType("Ketch")
#ships
theSliver = components.Ship("the Sliver",ketch,event_list,crew=[components.gen_crewmate([buckaneer]),components.gen_crewmate([buckaneer])])
game_time.register(theSliver) #Register ship to game time so it can track travel time
theSplinter = components.Ship("the Splinter",ketch,event_list,crew=[components.gen_crewmate([buckaneer]),components.gen_crewmate([buckaneer])])
game_time.register(theSplinter) #Register ship to game time so it can track travel time
player_fleet = components.Fleet([theSliver,theSplinter])

#Warehouses
theHold = components.Warehouse("the Hold")
clammer_warehouse = components.Warehouse("Clammer Warehouse")
old_cove_warehouse = components.Warehouse("Old Cove Warehouse")

#lists
all_goods = [gold,silver,bread,fish,wood,cloth,rice,gold,silver]
trade_goods = [bread,fish,wood,cloth,rice]
currency_goods = [gold,silver]

#Other
player = components.Player(components.Storage("Player Inventory",100),0,fleet=player_fleet,warehouses=[theHold])

#Port creation
portClammer = components.Port("port Clammer",clammer,world,game_time,player,warehouses=[clammer_warehouse])
portGrandure = components.Port("port Grandure",grandure,world,game_time,player,[theSliver,theSplinter],[theHold])
portOldCove = components.Port("Old Cove Port",old_cove,world,game_time,player,warehouses=[old_cove_warehouse])

# Taverns
fishHeadTavern = components.Tavern("Fish Head Tavern",clammer,[buckaneer],player)

#Exchanges
#theFishermansWharf = components.Exchange("the Fisherman's Wharf",clammer,game_time, world,good_list=all_goods,reward_list=currency_goods)
theBargainHouse = components.Exchange("the Bargain House",grandure,game_time, world,good_list=trade_goods,reward_list=currency_goods)
#game_time.register(theFishermansWharf)
game_time.register(theBargainHouse)
