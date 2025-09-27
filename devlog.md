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