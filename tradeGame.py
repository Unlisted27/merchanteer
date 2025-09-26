import components,building_blocks


player = components.Player(components.Storage("Player Inventory",100),0,None)
theBarganHouse = components.Exchange("the Bargan House",good_list=building_blocks.all_goods,reward_list=building_blocks.currency_goods,game_time=building_blocks.game_time)
portGrandure = components.Port("port Grandure",[building_blocks.theSilver,building_blocks.theSplinter],[building_blocks.theHold])

def start_exchange(exchange:components.Exchange,player:components.Player):
    components.clear_terminal()
    while True:
        components.clear_terminal()
        print(f"Welcome to {exchange.name}, here you can take contracts to earn money.")
        answer = components.menu("Exchange Menu",["View available contracts"],True) 
        match answer:                           # <─ use match instead of “case answer:”
            case 1:                              # option 1
                components.clear_terminal()
                contract = exchange.select_contract()
                if type(contract) is components.Contract:
                    building_blocks.game_time.register(contract)
                    player.contracts.append(contract)
            case _:                              # option 2
                break                             # assuming this is inside a loop


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
            start_exchange(theBarganHouse,player)
        case 3:
            components.clear_terminal()
            portGrandure.manageGoods()
        case 4:   
            components.clear_terminal()                           
            print("A new day begins...")
            building_blocks.game_time.advance()
        case 5:                             
            print("Thanks for playing!")
            break                             # assuming this is inside a loop