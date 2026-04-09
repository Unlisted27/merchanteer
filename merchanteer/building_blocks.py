import components, random

# Remember, anything that needs to be saved MUST Game.register

#Initial setup
game = components.Game()

#Locations
grandure = components.Location("Grandure",game,"A bustling trade city with a large port.")
clammer = components.Location("Clammer",game,"A small fishing village known for its seafood.")
old_cove = components.Location("Old Cove",game,"One of the first foreign settlements, old cove has survived through it all.")

#world things
world = components.World([grandure,clammer,old_cove],game)

#Currency goods
gold = components.Good("gold","shiny",1,0.1,game)
silver = components.Good("silver","less-shiny",0.5,0.1,game)
#Other goods
bread = components.Good("bread","staple food",0.1,0.05,game)
fish = components.Good("fish","protein food",0.3,1,game)
wood = components.Good("wood","building material",0.5,2,game)
cloth = components.Good("cloth","fabric material",0.3,0.1,game)
rice = components.Good("rice","staple food",0.2,1,game)

#goods lists
all_goods = [gold,silver,bread,fish,wood,cloth,rice,gold,silver]
trade_goods = [bread,fish,wood,cloth,rice]
currency_goods = [gold,silver]

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
buckaneer = components.CrewRole("Buckaneer","A regular sailor, well equiped in all areas but not excelling in any.",game)

# Crew

#Ship types
ketch = components.ShipType("Ketch")
#ships
theSliver = components.Ship("the Sliver",ketch,event_list,game,crew=[components.gen_crewmate([buckaneer],game),components.gen_crewmate([buckaneer],game)])
theSplinter = components.Ship("the Splinter",ketch,event_list,game,crew=[components.gen_crewmate([buckaneer],game),components.gen_crewmate([buckaneer],game)])
#Fleet
player_fleet = components.Fleet([theSliver,theSplinter],game)

#Warehouses
theHold = components.Warehouse("the Hold",game)
clammer_warehouse = components.Warehouse("Clammer Warehouse",game)
old_cove_warehouse = components.Warehouse("Old Cove Warehouse",game)

#Player
player = components.Player(game,components.Storage("Player Inventory",game,100),0,fleet=player_fleet,warehouses=[theHold])

#Port creation
portClammer = components.Port("port Clammer",clammer,world,game,player,currency_goods,warehouses=[clammer_warehouse])
portGrandure = components.Port("port Grandure",grandure,world,game,player,currency_goods,ships=[theSliver,theSplinter],warehouses=[theHold])
portOldCove = components.Port("Old Cove Port",old_cove,world,game,player,currency_goods,warehouses=[old_cove_warehouse])

# Taverns
fishHeadTavern = components.Tavern("Fish Head Tavern",game,clammer,[buckaneer],player)

#Exchange
theBargainHouse = components.Exchange("the Bargain House",grandure,game, world,good_list=trade_goods,reward_list=currency_goods)