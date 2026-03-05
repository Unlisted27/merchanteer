# Versioning scheme  
```
  0    .    0    .    0    -    s
MAJOR     MINOR     PATCH    SPECIAL
```
### Special legend
a - Alpha (internal testing)  
b - Beta  (external testing)  
p - pre-release (available for download but not most stable verion)
d - in-development version, not meant to be played, likely very unstable

# up to 0.0.1a Contracts rework #1 and locations
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
  
# 0.0.2a The sailing update
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

# 0.0.3a Contracts rework #2
## Added features 
### Major added features
 - Mail system, basically a delay on contract completion 
 - Notices system, every new day will present the player with certain event notices  
### Minor added features
 - Added ability to cancel name change when changing ship name
 - Currencies no longer listed as transportable items in the bargain house
 - Back button when selecting from inventory is now 1 rather than the final option
## Player notes  
- Contracts now take between 2 and 5 days from their completion for the exchange to recieve notice of their completion  
- At the start of a new day you will get a list of events that have occured (ships returning to port, contracts completed, etc)
- You can now enter "all" when moving cargo to move all of the selected good
## Bug fixes
- Fixed the bug where ships would often not return to port, the issue was that we were storing time from 0 instead of from the current day :facepalm
- Fixed bug when going trhough available contracts in the Bargain house, entering no value will now just redo the prompt, rather than crashing the app.
- Fixed ship not returning bug (AGAIN). Had to check for the ship's return before and after event roll, incase the event pushed the return date to the currect date.
- Fixed contracts remaining in the exchange even after being selected and loaded to a ship
- Fixed inventories displaying as "inventory inventory" by removing the code that appended "inventory" to storage names
- Fixed rounding bug in the warehouse, numbers will no longer have incredibly long decimal values
## Dev notes  
- Contracts now check for completion BEFORE checking for expiry
- Port objects now require GameTime on creation
- on_day_passed function of objects registered with game time can now return a string that will be added to the daily notices
- Storage.get_invent(self, starting_index) function added. This returns the inventory in nicely formatted text
- Storage.select_from_invent() now returns the list index of the item selected
## Other notes
- Removed artist tag on ASCII art (per their request), will be added back when credits added
- More art added to the art.py file, but not yet implemented in the game

# 0.0.4a 
## Added features
### Major added features
- voyage planning has replaced simply dispatching a ship. The player must now add destinations and contracts before dispatching a ship
    a. This means that ships can now travel to multiple locations
        i. Once dispatched, a ship will travel to all assigned locations in order of assignment before returning to its port of origin
    b. Ships now deposite goods based on the contracts assigned to that ship
        i. When arriving at a new port, the ship will check if any of its assigned contracts are set to deposite there
        ii. If one is, it will deposite no more than the contract's required amount of that good at that port (it will deposite as much as possible if it doesent have enough)
        iii. You can check the ships log when it is at the same port as you to see success or failure of contract completion.
### Minor added features
## Player notes
- Exchanges now refresh contracts daily
- When dispatching a ship, you can now choose whether to send that ship with a contract or not. Sending a ship with a contract will automatically grab the correct destination
## Bug fixes
- Fixed back option displaying above inventory header while loading a ship
- Fixed crash with type hint pointing to a class that hadnt been declared (Exchange pointing at Location)
- Fixed ships returning from journey not being displayed in daily log
## Dev notes
- Added some type hints in Exchange
- Added error handling for the case where an Exchange is created without a valid Location
- Added on_day_passed() function to Exchange
- Exchange must now be registerd with GameTime (GameTime.register(Exchange))
- Storage.show_invent(self,back_option=False) now has a back option and removed the starting index option
- Port now requires Player on creation
- Ship objects now have target_storage rather than target_warehouse
- Ship objects now have a current_port value that is set when a port object is initialised with ships assigned, or when Port.add_ship() is run.
- All ships being added to ports should be added with the Port.add_ship() method to correctly make the ship's current_port correct
## Other notes