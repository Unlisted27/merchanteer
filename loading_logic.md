
# Intro
The save load system works by  breaking down every object into its properties and storing them in a JSON. An obvious problem arrises when we try to do this simply by storing each property as some properties are custom objects, and thus cannot be stored in a JSON file, thus the ID system.

# ID system:
On every load, each object that is registered with the master Game object (which is every object) is given a unique ID at the time of `__init__()`, this is done via the Game.register() function call. 

## ID - saving
If a property of an object is another object, it stores the unique ID of said object rather than the object itself.
During
## ID - loading
During the load phase, properties that themselves are objects are then searched by their IDs up from a list of already-loaded objects. This means that loading order is critical, as an object must be already loaded for it to be searched up. Linking a property to an already-loaded object is done by the function Game.scan_loaded_objects(item_type,item_id). This function will return an object, or None on fail. It will also print an error on fail that can be cought by adding an input() line before the first menu is called.
Every object should have an ID argument in it's `__init__()` if it wishes to be tracked.

# Saving
Saving the game state is fairly simple. Any object that needs to be saved must have a save() function that returns a dict. In order for an object to be loaded properly, it's ID must be saved.

When `Game.save_to_file(file_name)` is called, it will call the save function of every object in it's `self.observers`, and store the data recieved.
## Example save function:
```
def save(self) -> dict:
    save = {
        "name":self.name,
        "role":self.role.ID,
        "ID":self.ID
    }
    return save
```
Notice how self.role.ID was stored instead of self.role as self.role is of type CrewRole, which is not JSON serializable

# Loading
Loading is a little more complicated...
Loading happens in 3 important stages

 - ### Initial load
    The purpose of the initial_load is to only create the base class, and not populate any value that is not imediately required. This is done to allow for more flexibility in the load order.
    Any object that will be loaded must have a @classmethod function (this means it able to create an instance of itself with the cls argument) named init_load(cls,save,context). context provides the game object and some other external data (only ship_events as of 0.1.0a).
    Every init_load starts by getting the Game object from context (context.game). It then creates an instance of the object being loaded, and populates only the necessary fields (with a few exepsions such as storage, as many objects will create their own storage if none is provided on `__init__`).

    Example:
    ```
    def init_load(cls,save:dict,context:LoadContext):
        game = context.game
        instance = cls(
            game,
            save["name"],
            ID = save["ID"]
        )
        instance._save_data = save #<- This line is necessary for phase two
        return instance
    ```
    (Notice how role is not yet loaded, because ONLY IN OUR EXAMPLE, it is not required for the instantiation of this object)

    cls() creates a new instance of that object and thus calls the `__init__` function of said instance. It is the responsibility of the `__init__` to game.register() itself, adding it to the game.observers.

 - ### Object field population
    Once the initial loading phase is complete, certain objects will still have empy fields that must be populated with other objects. Now that those objects that are to fill those fields exist (they were loaded in the first phase), they can be referenced.
    The second phase of loading is to tie objects to eachother, and thats done by looking through the list of already loaded objects (game.observers) and finding specific objects by their unique ID (done with game.scan_loaded_objects)

    Note: The save in phase two is whatever data was stored in an object's `_save_data` at the end of phase 1.
    Example:
    ```
    def secondary_load(self,save,context:LoadContext):
        game = context.game
        self.role = game.scan_loaded_objects(CrewRole,save["role"])
    ```
    (Remember, we saved save["role"] as self.role.ID)

 - ### Delete temporary save data
    Finally, all of the temporary save data (anything stored in `_save_data` of an object) must be wiped

    This stage is done automatically by Game, it goes through each observer, and for any observer with a `_save_data` property, it deletes that property.

# Order of loading from a save:
Game object is created, day value is loaded 
game object tracks loaded objects via its observers list
Location
World
Goods
Storage
Warehouses
Ports
Contracts
Crew roles
Crew
Ship Type
Ships
Fleets
Player
Taverns
Exchanges
MessengerPigeon