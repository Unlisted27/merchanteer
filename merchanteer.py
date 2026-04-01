import components,building_blocks,game_art

#Art
title = game_art.title

#Objects
player = building_blocks.player
theBargainHouse = building_blocks.theBargainHouse
portGrandure = building_blocks.portGrandure

def start_exchange(exchange:components.Exchange,player:components.Player):
    components.clear_terminal()
    while True:
        components.clear_terminal()
        print(f"Welcome to {exchange.name}, here you can take contracts to earn money.")
        answer = components.menu("Exchange Menu",["View available contracts","Cashout contracts"],True) 
        match answer:
            case 1:                              # option 1
                components.clear_terminal()
                contract = exchange.select_contract(player)
                if type(contract) is components.Contract:
                    building_blocks.game_time.register(contract)
                    player.contracts.append(contract)
            case 2:                              # option 2
                exchange.cashout_contracts(player)
            case _:                              # option 2
                break                             # assuming this is inside a loop

def __main__():
    components.clear_terminal()
    print(title)
    input("Press Enter to begin...")
    components.clear_terminal()
    answer = components.menu("Main Menu",["Start new game","Load save","Settings","Credits","Quit game"])
    match answer:
        case 1:
            while True:
                components.clear_terminal()
                print(f"Day {building_blocks.game_time.day}")
                answer = components.menu("Game menu",["Player actions","Bargain house","Port","Tavern","Next day","Quit game"],art = game_art.title) 
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
                        building_blocks.fishHeadTavern.select_crew()
                    case 5:   
                        components.clear_terminal()                           
                        building_blocks.game_time.advance()
                        print("A new day begins...")
                    case 6:                             
                        print("Thanks for playing!")
                        break
        case 2:
            print("Load save feature coming soon!")
        case 3:
            print("Settings menu coming soon!")
        case 4:
            components.clear_terminal()
            game_art.slow_print(game_art.super_center_block(game_art.title.art),0.3)
            game_art.slow_print(game_art.super_center_block("""
    ============CREDITS============
              Game design
              Unlisted_dev
                                
                  Code    
              Unlisted_dev

                  Art         
          DefinitelyNotAPickle

         Thank you for playing!
                               
               support us             
  https://buymeacoffee.com/unlisted_dev
     (30/70) Artist / main dev split     
      Unless specified otherwise (:
    """),0.3)
        case 5:
            print("Thanks for playing!")

__main__()