import components,building_blocks,gc,inspect

# Save format:
# {
# "Property1":value,
# "Property2":value
# }

# Order of build
# 1. Game
# 2. Locations
# 3. World
# 4. Goods
# 5. Events - Does not need to be saved as events are constant
# 6. Crew roles
# 7. Crew - None created on first build as crew created during runtime
# 8. Ship types - Not need to be saved as its a constant
# 9. Ships
# 10. Fleets
# 11. Warehouses
# 12. Player
# 13. Ports
# 14. Taverns
# 15. Exchanges

# Order of loading from a save:
# 1. Game /
# 2. Location /
# 3. World /
# 4. Goods /
# 5. Crew roles /
# 6. Crew
# 7. Ships
# 8. Fleets
# 9. Warehouses
# 10. Player
# 11. Ports
# 12. Taverns
# 13. Exchanges

# NEED TO IMPLEMENT loaded_objects FOR OBJECTS THAT REQUIRE OTHER OBJECTS ON INIT
# LEFT OFF ON LINE 1356


# NO NEED FOR A SECOND PASS, OBJECTS THAT BECOME CHILDREN SHOULD AUTOMATICALLY ADD THEMSELVES TO THEIR PARENTS
# Example: Port objects automatically add themselves to their parent location objects
game = building_blocks.game
print(building_blocks.grandure.coordinates)
save_data = building_blocks.grandure.save()
print(save_data)
loaded_location = components.Location.load(save_data,game)
print(loaded_location.coordinates)

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