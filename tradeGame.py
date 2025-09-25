import components

gold = components.Good("gold","shiny",1,0.1)
silver = components.Good("silver","shiny",0.5,0.1)

theSliver = components.Ship("the Sliver")
theSliver.storage.add_to_cargo(gold,100)
theSplinter = components.Ship("the Splinter")
theSplinter.storage.add_to_cargo(gold,100)
theHold = components.Warehouse("the Hold")
theHold.storage.add_to_cargo(gold,10000)
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