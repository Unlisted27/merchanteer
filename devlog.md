# Versioning scheme  
```
  0    .    0    .    0    -    s
MAJOR     MINOR     PATCH    SPECIAL
```
### Special legend
a - Alpha (internal testing)  
b - Beta  (external testing)  
p - pre-release (available for download but not most stable final verion)
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

# 0.0.4a The sailing rework, art, and UI update
## Added features
### Major added features
- voyage planning has replaced simply dispatching a ship. The player must now add destinations and contracts before dispatching a ship
    a. This means that ships can now travel to multiple locations
        i. Once dispatched, a ship will travel to all assigned locations in order of assignment before returning to its port of origin
    b. Ships now deposite goods based on the contracts assigned to that ship
        i. When arriving at a new port, the ship will check if any of its assigned contracts are set to deposite there
        ii. If one is, it will deposite no more than the contract's required amount of that good at that port (it will deposite as much as possible if it doesent have enough)
        iii. You can check the ships log when it is at the same port as you to see success or failure of contract completion.
- Art can now be found in some menus
### Minor added features
- Main menu
- Credits sequence
- Menu function changed to display a row of Xs on incorrect input
- Menu function now has a box to enter text in
- contracts now calculate their time to return to their port of origin rather than selecting a random time to be redeemed
## Player notes
- Exchanges now refresh contracts daily
- When dispatching a ship, you can now choose whether to send that ship with a contract or not. Sending a ship with a contract will automatically grab the correct destination
## Bug fixes
- Fixed back option displaying above inventory header while loading a ship
- Fixed crash with type hint pointing to a class that hadnt been declared (Exchange pointing at Location)
- Fixed ships returning from journey not being displayed in daily log
- Fixed fatal error with Location being referenced in ship before being defined
- Fixed menu skipping when going back from adding contracts in route planning
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
- player in building_blocks.py now initialises with a Fleet object, this doesent change anything and I might remove fleet in the future, or keep it, depending on the existence of non-player-owned ships
- menus can now accept art as one of their arguments and will display the art alongside the menu
- art.py renamed to game_art.py
- Added and later removed Curses as a requirement
- Added style.py to store ANSI escape codes for formatting text
- reformated the switch case statements under components.Port into functions rather than nested statements for readability.
- Added distance() function to get the distance between two points, then divide that by 100
## Other notes

# 0.0.5a More menu info
## Added features
### Major added features
- Data tables can now be found in some menus
- Data tables allow for it to be more obvious that the player has selected something if returning to the same menu once the selection is complete
### Minor added features
- New location Old Cove has been added
## Player notes
- Some menus have been updated with more information on side tables (ex: ship destination and contract selection menu now displays selected contracts and destinations)
## Bug fixes
- Bug that would cause contracts to be announced as being able to be cashed out even if they had already expired has been patched
- Fixed ships often not announcing their return, this was caused by check_arrival() being called twice even if the first one succeeded, resulting in the second returning None instead of the returned notification
- Fixed bug when planning ship travel where the table would only display destinations selected during the time that the player was on that menu, and re-opening the menu would whipe the table. Now the table is pre populated with the planned destinations of a ship.
## Dev notes
- Added __main__() method in merchanteer.py
- Added table:dict | list    to menu() function. This wil allow a table to be displayed with the other content
- print_table() has now been replaced with get_table()
- get_table() can now take a dict for full table displays, or a list[str] for single column tables (lists)
## Other notes

# 0.0.6a The Crew and ship needs Update (Ship travel overhaul)
## Added features
### Major added features
- Ship stats:
    - Ships have a variety of stats, some of these stats are checked every day and if they cannot be met, there may be consequences
    - Base stats:
        - health
        - cargo_weight (switching to kg)
        - sailing_efficiency
        - toughness
        - crew_capacity
- Crew
    - Sailing ability affects the amount a ship can travel daily. 
    - Each crew member's sailing ability is the number of kms they can contribute to the ship's travel.
    - The daily travel distance is the total sailing ability of all crew members combined plus some random variation, and adjusted based on the ship's daily wind value
    - Crew can be selected and moved between ships or terminated
- Storms
    - If the daily storm value (affected by events) is greater than the ships tougness, it will take damage equal to the difference (storm_value - toughness)
- Tavern
    - You can now go to the tavern to hire crew
- Ship needs
    - While at sea, ships have needs
    - Needs are met by having crew with the required skill to meet those needs
    - Ex: Daily maintenance is maintained by the sum of all crew member's maintenance stats
    - If needs are not met while dispatched, a ship's stats will degrade
- Messenger Pigeons now carry messages back from your ships to notify you of things like losing a ship.
- Ships can now sink
- Ship repairs:
    - If a ship takes damage, it can be repaired at a port by paying a fee. It will take a few days for most repairs.
### Minor added features
- Changed all weight values from Lbs to Kg (scaling didnt change, just units. Ballancing coming soon)
- General actions added to main Game Menu. It contains:
    - Player actions
        - Player actions menu (moved from Game Menu)
    - View notices
        - Allows viewing of past notices that the player might have missed
## Player notes
- Ship health can now be affected by storms
- Crew have been added!
- Ships have a default crew, but to get the most out of your ships, hire more crew from the tavern
- All weights are now in Kg, and distances in Km
- Ships now have daily needs while at sea. See the needs in the ship menu in the port. Ensure your crew have the skill to meet those needs or else the ship could degrade stats while at sea. (Not having enough maintenance degrades toughness)
- Watch out for notes from messenger pigeons on your daily notices!
- Ships can now be repaired at port
- The go back option will now CONSISTANTLY be 1
- Menus now look nicer and are easier to align with items in their tables
## Bug fixes
- Fixed 0.0.5a ship travel planning bug but for contracts rather than destinations
- Fixed "Port" being displayed before port names in the port menu title that would lead to things like "Port port Grandure"
- Fixed menu returning to the ship menu after dispatching a ship
## Dev notes
- Added Stat class that holds a min, max and current value
- Removed unecessary property max_weight from warehouses as the warehouse's storage was the only thing that used this property
- added __iadd__ and __isub__ to Stat class. Now stats CURRENT VALUE can be changed with Stat += int/float. Stat will automatically clamp the value so it does not exceed the max or go below the min
- Removed ID from the available contracts menu
- Added ShipNeed class. This holds tie-ins for all the values it needs to effect, brining together crew abilities and ship daily needs.
- Removed the need for ships to be registered withe game_time.register, they now take game time on initialisation and register themselves
- Added MessengerPigeon class for sending messages back to the player home port. Basically, to semi-simulate ancient times, this class simulates information delay before it reaches the player on their daily notices screen.
- Added error handling for menus created with no items, return_option=False and text_input = False. If this happens, a ValueError will be raised
- Reworked the transfering of goods system to be more up to date with the modern table format of menus. The go back option will now CONSISTANTLY be 1
## Other notes
- Made the discord link in the README work and added a little blurb for devs regarding code structure

# 0.1.0a Save load
## Added features
### Major added features
Save/load system (I've been waiting so long to write that, more info in loading_logic.md)
### Minor added features
 - Art for the tavern has now been added
 - In the main menu, there is a table displaying all active contracts
## Player notes
You can now save and load your game!
## Bug fixes
A lot went unlogged NGL
 - Fixed bug where exchanges would not populate with contracts on first load
 - Fixed bug where accepted contracts wouldnt load causing fatal crash (due to mis-aligned arguments in the contract's init_load method)
 - Fixed outdated logic in selecting a warehouse to store contract goods that caused a-typical menu behaviour.
 - Fixed notices not saving
 - Fixed Contracts and Crew members persisting in game.observers even after being removed from their Exchange/Tavern. Patched my first RAM leak (:
## Dev notes
- All objects that need to be tracked via save/load now have an ID value. This value is set when the object runs ```game.register(self)``` in ```__init__```
- GameTime changed to Game, and all references changed accordingly.
    - This was done as Game now acts as the register tracking all objects that need to be saved, as well as the central clock. Game is a more fitting name for this new role.
- Exchange objects now GameTime.register themselves
    - The old system of running GameTime.register on everything that needs to be time tracked is now fully deprecated as all objects that accept a GameTime arg now register themselves
 - Contracts now have an active status and can only complete when it is True. This avoids contracts that were not yet accepted being completed due to their required resources ending up in the required warehouse because of a different contract
 - Also to prevent contracts being completed from the goods of another cotnract, contracts now remove their required completion items from their target warehouse upon completion.
## Other notes
A lot has changed, see notes on the save/load system in loading_logic.md