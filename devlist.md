# !!!NOTICE!!!
This file is NOT for accurate tracking of the development timeline, this is simpyl a task list so not every change is recoreded.  

For proper timeline and versionning, go to devlog.md
# before 0.0.3a
1. Add location system  
    COMPLETE a. Every building (port, exchange) is tied to a location  
2. Add ship travel  
    COMPLETE a. Ships can be dispatched to a destination port.
    COMPLETE b. Dispatches will be handled by Port objects, which will be tied to the World object, which will contain all of the ports in the world
    COMPLETE c. exchanges will handle placing items into warehouses
    COMPLETE d. PRIORITY Locations have coordinates, randomly generated, determine their distances from eachother (finaly I use the math I learned in school lol)
    COMPLETE e. Travel time variation
        COMPLETE i. Travel events
        COMPLETE ii. Events cause time changes
        COMPLETE iii. Events have an effect on the ship properties
3. Contract stuff  
    COMPLETE a. Contracts have a destination  
    COMPLETE b. Contracts simply check the destination warehouse storage every day to see if the goods have been delivered.    
    COMPLETE c. Player has a list of owned warehouses
    COMPLETE d. Contract payouts  
        COMPLETE i. Contracts can only get cashed once word of the completion has reached the home port  
        COMPLETE ii. This means adding a mail system...  
4. Mail system
    REWORKED a. Mail of contract payouts takes a short time to reach home, usually half the time it takes a ship  
    COMPLETE |-> a. REWORK: Mail takes between 2 to 5 days to arrive at the home port.
    COMPLETE b. Once the exchange gets the mail, they will allow you to deposite completed contract payouts

5. Bugs to fix
    FIXED - Bug discovered, something to do with ships not getting back to port. To reproduce, send a ship out twice, try different cargo loads as well.
    FIX: it is possible for events to occur on the day the ship returns, and since the return logic checks if the ship return day is the current day, and event that makes the return day lower than the current day will cause the ship to never be registered as returning. The fix was to check for return to port before running events.
    
    UNKOWN? - Bug discovered, contracts not being recorded as complete
    info: Bug has not re-apeared in a long time, possibly fixed and undocumented?
    

# 0.0.4a
COMPLETE 1. Make contracts in the exchange restock daily
COMPLETE 2. Add orders system to allow ships to go to multiple ports and deposite set numbers of resources.
 COMPLETE a. Tie contract to a ship, then when the ship reaches its destination it deposites the contract amount of resources into the contract target storage
COMPLETE 3. Reformat switch cases to avoid nested statements and implement higher levels of functionalisation.

# 0.0.5a the UI Update
 - COMPLETE Patch fatal bug when redeeming contracts
# 0.0.6a The ship overhaul
 - Ship constants (new and old):
    - health_max (old)
    - cargo_max_weight (old) (weight appears to be currently in lbs)
    - 
 - Ship types
    - Small ship : Ketch
    - medium ship : 
 - Ship stats:
    Ships have a variety of stats, some of these stats are checked every day and if they cannot be met, there may be consequences
 - Ship needs:
    While at sea, ships will have needs that must be met in order to perform optimally. Some needs are tied to stats, if those needs cannot be met, the stat decreases
 - Crew system
    - Roles on a ship
        - Different sized ships require more roles, and have different number of crew slots
    - Human object
    - Crew object
        - Crew best role
        - Crew skill
        - (crew can perform any role, but they specialise in one area)