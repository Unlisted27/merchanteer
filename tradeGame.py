import components

gold = components.Good("gold","shiny",1,0.1)
lead = components.Good("lead","dull",0.5,10)
lead_brick = components.Crate(lead,100)
gold_chest = components.Crate(gold,100)
theSliver = components.Ship("the Sliver")
theSliver.storage.add_to_cargo(gold_chest)
theSplinter = components.Ship("the Splinter")
theSplinter.storage.add_to_cargo(gold_chest)
theHold = components.Warehouse("the Hold")
theHold.storage.add_to_cargo(lead_brick)
portGrandure = components.Port("port Grandure",[theSliver,theSplinter],[theHold])

day = 0

#Game loop
while True:
    components.clear_terminal()
    print(f"Day {day}")
    answer = components.menu("Main Menu",["Manage goods at port","Next day","Quit game"]) 
    match answer:                           # <─ use match instead of “case answer:”
        case 1:                              # option 1
            portGrandure.manageGoods()
        case 2:                              # option 2
            print("A new day begins...")
            day += 1
        case 3:                              # option 3
            print("Thanks for playing!")
            break                             # assuming this is inside a loop