import components

gold = components.good("gold","shiny",1,0.1)
gold_chest = components.crate(gold,100)
theSliver = components.ship("the Sliver",cargo=[gold_chest])
theSplinter = components.ship("the Splinter",cargo=[gold_chest])
portGrandure = components.port("port Grandure",[theSliver,theSplinter])

day = 0

#Game loop
while True:
    components.clear_terminal()
    print(f"Day {day}")
    answer = components.menu("Main Menu",["Manage goods at port","Quit game"])
    match answer:                           # <─ use match instead of “case answer:”
        case 1:                              # option 1
            portGrandure.manageGoods()
        case 2:                              # option 3
            print("Thanks for playing!")
            break                             # assuming this is inside a loop
    day += 1
