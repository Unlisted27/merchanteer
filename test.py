import components,building_blocks

player = components.Player(components.Storage("Player Inventory",100),0)

data = {
    "Item 1": {"property 1": 0, "property 2": 0},
    "Item 2": {"property 1": 0, "property 2": 0},
}

print(components.get_table(data))