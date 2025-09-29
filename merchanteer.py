import components,building_blocks,art

#Art
title = art.title

#Objects
player = building_blocks.player
theBargainHouse = building_blocks.theBargainHouse
portGrandure = building_blocks.portGrandure


def start_exchange(exchange:components.Exchange,player:components.Player):
    components.clear_terminal()
    while True:
        components.clear_terminal()
        print(f"Welcome to {exchange.name}, here you can take contracts to earn money.")
        answer = components.menu("Exchange Menu",["View available contracts"],True) 
        match answer:                           # <─ use match instead of “case answer:”
            case 1:                              # option 1
                components.clear_terminal()
                contract = exchange.select_contract(player)
                if type(contract) is components.Contract:
                    building_blocks.game_time.register(contract)
                    player.contracts.append(contract)
            case _:                              # option 2
                break                             # assuming this is inside a loop
components.clear_terminal()
print(title)
input("Press Enter to begin...")
while True:
    components.clear_terminal()
    print(f"Day {building_blocks.game_time.day}")
    answer = components.menu("Main Menu",["Player actions","Bargain house","Port","Next day","Quit game"]) 
    match answer:                           # <─ use match instead of “case answer:”
        case 1:      
            components.clear_terminal()                        # option 1
            player.player_actions()
        case 2: 
            components.clear_terminal()
            start_exchange(theBargainHouse,player)
        case 3:
            components.clear_terminal()
            portGrandure.manage_ships()
        case 4:   
            components.clear_terminal()                           
            print("A new day begins...")
            building_blocks.game_time.advance()
        case 5:                             
            print("Thanks for playing!")
            break