import components,building_blocks,gc,inspect

# Save format:
# {
# "Property1":value,
# "Property2":value
# }

# Note: An object is static if it is created once and none of its properties should ever change
# Ex: CrewRole is static as it holds specific values that do not change during runtime
# Ex: Port is not static as it holds ships that can change

# Order of build
# 1. Game
# 2. Locations - Static
# 3. World - Static
# 4. Goods - Static
# 5. Events - Static
# 6. Crew roles - Static
# 7. Crew - None created on first build as crew created during runtime
# 8. Ship types - Static
# 9. Ships
# 10. Fleets
# 11. Warehouses
# 12. Player
# 13. Ports
# 14. Taverns
# 15. Exchanges

# Order of loading from a save:
# . Game object is created, day value is loaded in. game object tracks loaded objects via its observers list
# . Location /
# . World /
# . Warehouses
# . Ports
# . Goods /
# . Contracts /
# . Crew roles /
# . Crew /
# . Ship Type
# . Ships
# . Fleets
# . Player
# . Taverns
# . Exchanges
# . MessengerPigeon

# NO NEED FOR A SECOND PASS, OBJECTS THAT BECOME CHILDREN SHOULD AUTOMATICALLY ADD THEMSELVES TO THEIR PARENTS
# Example: Port objects automatically add themselves to their parent location objects
game = building_blocks.game
#print(building_blocks.grandure.coordinates)
#save_data = building_blocks.grandure.save()
#print(save_data)
#loaded_location = components.Location.load(save_data,game)
#print(loaded_location.coordinates)

#crewRole1 = components.CrewRole("ROLE 1","A ROLE",game)
#crew1 = components.gen_crewmate([crewRole1],game)
#print(f"{crew1.name} {crew1.crew_role.name}")
#save_data = crew1.save()
#print(save_data)
#loaded_crew = components.CrewMate.load(save_data,game)
#print(f"{loaded_crew.name} {loaded_crew.crew_role.name}")
game.save_to_file("save1")
input("Press enter to load data")
game.load_from_file("save1")
print(game.observers[0].name)
#Save load template:
#
#def save(self) -> dict:
#        save = {
#            "name":self.name,
#            "coordinates":self.coordinates,
#            "description":self.description
#        }
#        return save
#    
#    @classmethod
#    def load(cls, save: dict,game:Game):
#        instance = cls(
#            save["name"],
#            game=game,
#            coordinates = save["coordinates"],
#            description = save["description"]
#        )
#        return instance