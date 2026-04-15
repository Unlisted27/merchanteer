import components, building_blocks, game_art

#Art
title = game_art.title

#Objects
player = building_blocks.player
theBargainHouse = building_blocks.theBargainHouse
portGrandure = building_blocks.portGrandure

def new_temp_game():
    game = components.Game()
    gold = components.Good("Gold","Shiny",1,0.1,game)
    bread = components.Good("Bread","Staple food",0.1,0.2,game)
    home = components.Location("Home",game)
    away = components.Location("Away",game)
    world = components.World([home,away],game)
    home_warehouse1 = components.Warehouse("Home warehouse 1",game)
    home_warehouse2 = components.Warehouse("Home Warehouse 2",game)
    dest_warehouse1 = components.Warehouse("Dest warehouse",game)
    port_home = components.Port("Port Home",home,world,game,[gold],warehouses=[home_warehouse1,home_warehouse2])
    port_away = components.Port("Port Away",away,world,game,[gold],warehouses=[dest_warehouse1])
    dest_storage = dest_warehouse1.storage
    contract_1 = components.Contract(game,gold,10,5,bread,5,port_away,dest_storage,port_home)

    buckaneer = components.CrewRole("Buckaneer","A regular sailor, well equiped in all areas but not excelling in any.",game)

    crew_roles = [buckaneer]
    crewMate1 = components.gen_crewmate(crew_roles,game)
    crewMate2 = components.gen_crewmate(crew_roles,game)

    return game

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
                    building_blocks.game.register(contract)
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
                print(f"Day {building_blocks.game.day}")
                answer = components.menu("Game menu",["General actions","Bargain house","Port","Tavern","Next day","Save and quit"],art = game_art.title) 
                match answer:                           # <─ use match instead of “case answer:”
                    case 1:      
                        while True:
                            answer = components.menu("General Actions",["View notices","Player actions"],True)                        # option 1
                            match answer:
                                case 1:
                                    components.clear_terminal()
                                    if len(building_blocks.game.notices) > 0:
                                        for notice in building_blocks.game.notices:
                                            print(notice)
                                    else:
                                        print("No notices yet")
                                    input("Press enter to continue")
                                case 2:
                                    player.player_actions()
                                case _:
                                    break
                    case 2: 
                        components.clear_terminal()
                        start_exchange(theBargainHouse,player)
                    case 3:
                        components.clear_terminal()
                        portGrandure.manage_ships(player)
                    case 4:
                        components.clear_terminal()
                        building_blocks.fishHeadTavern.select_crew()
                    case 5:   
                        components.clear_terminal()                           
                        building_blocks.game.advance()
                        print("A new day begins...")
                    case 6:                             
                        #print("Saving game...")
                        #save_load.show_building_blocks_objects()
                        input("=====DONE=====")
                        #print("Game saved successfully!")
                        #print("Thanks for playing!")
                        #break
        case 2:
            print("Loading...")
            game = components.Game()
            context = components.LoadContext(game)
            new_game = components.Game.load_from_file("save1",context)
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

print("Creating new test game")
game = new_temp_game()
print("Success!")

input("Press enter to run game save")
game.save_to_file("save1")

input("Press enter to load")
print("Loading...")
game = components.Game()
context = components.LoadContext(game,building_blocks.event_list)
new_game = components.Game.load_from_file("save1",context)

print("Here are the observers...")
for observer in new_game.observers:
    print(f"{observer} | {observer.ID}")
