import components

gold = components.Good("gold","shiny",1,0.1)
theSliver = components.Ship("the Sliver")
theSliver.storage.add_to_cargo(gold,100)
theSplinter = components.Ship("the Splinter")
theSplinter.storage.add_to_cargo(gold,100)
theHold = components.Warehouse("the Hold")
theHold.storage.add_to_cargo(gold,100)
theHold.storage.remove_cargo(gold,10)
theHold.storage.show_invent()


portGrandure = components.Port("port Grandure",[theSliver,theSplinter],[theHold])