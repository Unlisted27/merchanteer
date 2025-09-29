import components,random

#Locations
grandure = components.Location("Grandure","A bustling trade city with a large port.")
clammer = components.Location("Clammer","A small fishing village known for its seafood.")

#world things
game_time = components.GameTime()
world = components.World([grandure,clammer])

#Currency goods
gold = components.Good("gold","shiny",1,0.1)
silver = components.Good("silver","shiny",0.5,0.1)
#Other goods
bread = components.Good("bread","staple food",0.1,0.05)
fish = components.Good("fish","protein food",0.3,1)
wood = components.Good("wood","building material",0.5,2)
cloth = components.Good("cloth","fabric material",0.3,0.1)
rice = components.Good("rice","staple food",0.2,1)

#ships and warehouses
theSilver = components.Ship("the Silver")
game_time.register(theSilver) #Register ship to game time so it can track travel time
theSilver.storage.add_to_cargo(gold,100)
theSplinter = components.Ship("the Splinter")
theSplinter.storage.add_to_cargo(gold,100)
game_time.register(theSplinter) #Register ship to game time so it can track travel time
theHold = components.Warehouse("the Hold")
clammer_warehouse = components.Warehouse("Clammer Warehouse")

#lists
all_goods = [gold,silver,bread,fish,wood,cloth,rice]
trade_goods = [bread,fish,wood,cloth,rice]
currency_goods = [gold,silver]

#Other
player = components.Player(components.Storage("Player Inventory",100),0,warehouses=[theHold])
print(theHold.storage.show_invent())

#Port creation
portClammer = components.Port("port Clammer",clammer,world,warehouses=[clammer_warehouse])
portGrandure = components.Port("port Grandure",grandure,world,[theSilver,theSplinter],[theHold])

#Clammer
theFishermansWharf = components.Exchange("the Fisherman's Wharf",clammer,game_time, world,good_list=all_goods,reward_list=currency_goods)
#Grandure
theBargainHouse = components.Exchange("the Bargan House",grandure,game_time, world,good_list=all_goods,reward_list=currency_goods)



print(random.choice(clammer.ports).name)
