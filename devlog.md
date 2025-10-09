# Versioning scheme  
  0    .    0    .    0    -    s
MAJOR     MINOR     PATCH    SPECIAL

## Special legend


# up to 0.0.1 Contracts rework #1 and locations
-Created the following objects:  
    1. GameTime  
        -Tracks time, and updates different objects based on the current day  
        -Add a time trigger with GameTime.register(object,day)  
        -The object being registered MUST have a on_day_passed function, as this is what GameTime will trigger  
    2. World  
        -Holds locations  
        -Should be initialised after all Location objects are initialised so that it can store them  
        -Must be passed into different functions/objects that require knowledge of the available locations    
    3. Good  
        -Basic "item" style object  
        -Standard item stats   
        -Does not include amount  
    4. Storage  
        -Anything that wants to store anything needs a storage object  
        -Used to ensure that storage in different places works the same (such as boats and warehouses)  
    5. Ship  
        -Not very developed at the moment, but has a storage that can be interacted with  
        -Will have more functionality (such as sailing) in future updates  
    6. Warehouse  
        -Just like a ship in terms of storage (thanks Storage object)  
        -Bound to a port  
    7. Port  
        -Where you manage physical goods (not just contracts) and storage  
        -Provides CLI interaction for transfering goods between storage places  
        -Will handle dispatch of ships once I add that  
    8. Fleet  
        -Barely developed, might be discontinued  
        -Plan was to basically just be a list of all of the player's ships  
        -Maybe i'll add convoys, so you can dispatch an entire fleet?  
    9. Contract  
        -Holds the required goods, their destination, and expiry date  
        -When selected via Exchange, the exchange will GameTime.register them so they can track expiration date  
        -Also checks every day if the contract has been completed  
    10. Player  
        -Mostly just CLI for inspecting your stats  
        -Technicaly has a Storage, might remove this  
    11. Exchange  
        -Handles everything to do with contracts  
        -GameTime.register contracts that are accepted  
        -Lots of CLI  
    12. Location  
        -Contains list of location bound objects (ports and exchanges)  
        -Items put themselves on that list, so locations can be defined before the ports that are in them  
  
# 0.0.2 The sailing update
## Added features  
-Added game title art  
-Contracts will now deposite their goods in a player chosen warehouse  
-Ships can now sail to other ports, where they will automatically deposite all goods  
-Added event system, events will randomly occur and change the travel time of the ship
-Added ships log, you can now see why your lazy crew took so long

## Player notes  
-Contract rewards have yet to be implemented, so you don't get a payout on completion
  
## Bug fixes
-Fixed bug where the wrong contract is added once selected  
  
## Dev notes  
-Added warehouses list to player objects  
-Exchanges will now place contract goods into one of the player's owned warehouses (selected by the player)  
-Exchanges will now only put items into a warehouse if there is space  
-Added back button to warehouse selection  
-Changed Go Back option return type of menu function from str"Go back" to None, and tuple option: (None,"Go back)  
-Added coordinates to Location objects, now we can use math that I learned in school (for the first time ever) to get the distance between these points  
-Changed manageGoods function to manage_ships because it is now basically the main function of the port  
-World object is now a requirement of port objects  
-Ships now have a dispatched property (bool) and other properties for determining their target for depositing goods and travel time  
-Added some other things to contracts and ships to build shipping system  
-Sailded FIRST FUNCTIONING VOYAGE! The silver (should have been Sliver, but whatever) left port Grandure carrying silver, sailed 2 days to port Clammer, deposited it's silver, and returned to port Grandure within 4 days of it's departure!  
-Ships cannot be accesed while sailing  
-Ships will become available uppon return to port  
-ShipEvent class created  
-To make a ShipEvent, create a class that inherits it  
-All ShipEvent classes must have a run_event() function, and must initialise the parent: super().__init__("Event Name")  
-Ship events occur randomly when a ship is dispatched  
-Added ship log, just a list.  
-All events are shown in the ship log  

# 0.0.3  
## Added features 
 - Mail system, basically a delay on contract completion   
## Player notes  
- Contracts now take between 2 and 5 days from their completion for the exchange to recieve notice of their completion  
## Bug fixes
- Fixed the bug where ships would often not return to port, the issue was that we were storing time from 0 instead of from the current day :facepalm
## Dev notes  
- Contracts now check for completion BEFORE checking for expiry
- Port objects now require GameTime on creation