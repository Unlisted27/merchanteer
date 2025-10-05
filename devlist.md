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
    d. Contract payouts  
        i. Contracts can only get cashed once word of the completion has reached the home port  
        COMPLETE ii. This means adding a mail system...  
4. Mail system
    REWORKED a. Mail of contract payouts takes a short time to reach home, usually half the time it takes a ship  
    COMPLETE |-> a. REWORK: Mail takes between 2 to 5 days to arrive at the home port.
    b. Once the exchange gets the mail, they will allow you to deposite completed contract payouts

5. Bugs to fix
    Bug discovered, something to do with ships not getting back to port. To reproduce, send a ship out twice, try different cargo loads as well.