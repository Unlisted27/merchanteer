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
