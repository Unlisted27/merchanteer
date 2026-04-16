import components, building_blocks, game_art, style,pathlib

#Art
title = game_art.title

import pathlib

def get_saves_folder() -> pathlib.Path:
    current_dir = pathlib.Path(__file__).parent
    saves_dir = current_dir.parent / "m_saves"
    saves_dir.mkdir(parents=True, exist_ok=True)
    return saves_dir

def select_save_file():
    saves_dir = get_saves_folder()
    files = [file.name.removesuffix(".json") for file in list(saves_dir.iterdir())]

    selected_index = components.menu("Select a save",files,True)
    if selected_index is None:
        return None
    selected_index -=1
    selected_file = saves_dir / (files[selected_index]+".json")
    return selected_file

def create_new_game():
    while True:
        components.clear_terminal()
        print("~ A new adventure begins ~")
        world_name = input("Enter world name: ")+".json"
        saves_dir = get_saves_folder()
        existing_files = [file.name for file in list(saves_dir.iterdir())]
        if world_name in existing_files:
            input("This save name already exists!")
            continue
        save_file = saves_dir / world_name
        game = building_blocks.gen_world()
        break
    run_game(game,save_file)

def run_game(game:components.Game,save_path:pathlib.Path):
    for observer in game.observers:
        if type(observer) == components.Port:
            if observer.name == "port Grandure":
                portGrandure = observer
            elif observer.name == "port Clammer":
                portClammer = observer
            elif observer.name == "Old Cove Port":
                portOldCove = observer
        if type(observer) == components.Player:
            player = observer
        if type(observer) == components.Tavern:
            if observer.name == "Fish Head Tavern":
                fishHeadTavern = observer
        if type(observer) == components.Exchange:
            if observer.name == "the Bargain House":
                theBargainHouse = observer
    while True:
        try:
            answer = components.menu(f"Game menu | Day:{game.day}",["General actions","Bargain house","Port","Tavern","Next day","Save and quit"],art = game_art.title) 
            match answer: 
                #General actions
                case 1:      
                    while True:
                        answer = components.menu("General Actions",["View notices","Player actions"],True)                        # option 1
                        match answer:
                            case 1:
                                components.clear_terminal()
                                if len(game.notices) > 0:
                                    for notice in game.notices:
                                        print(notice)
                                else:
                                    print("No notices yet")
                                input("Press enter to continue")
                            case 2:
                                player.player_actions()
                            case _:
                                break
                #Exchange
                case 2: 
                    theBargainHouse.start_exchange(player)
                case 3:
                    portGrandure.manage_ships(player)
                case 4:
                    fishHeadTavern.select_crew()
                case 5:   
                    game.advance()
                case 6:                             
                    print("Saving game...")
                    game.save_to_file(save_path)
                    print("Game saved successfully!")
                    print("Thanks for playing!")
                    break
        except KeyboardInterrupt:
            input(f"{style.RED}Woah there, make sure you save before you exit!{style.RESET}")

def __main__():
    components.clear_terminal()
    print(title)
    input("Press Enter to begin...")
    while True:
        answer = components.menu("Main Menu",["Start new game","Load save","Settings","Credits","Quit game"])
        match answer:
            case 1:
                create_new_game()
            case 2:
                file = select_save_file()
                if file is None:
                    continue
                else:
                    print("Loading...")
                    game = components.Game()
                    context = components.LoadContext(game,building_blocks.event_list)
                    new_game = components.Game.load_from_file(file,context)
                    run_game(new_game,file)
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
                input()
            case 5:
                print("Thanks for playing!")
                break

__main__()


def _new_temp_game():
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
    contract_1 = components.Contract(game,gold,10,5,bread,5,port_away,dest_storage,home)

    buckaneer = components.CrewRole("Buckaneer","A regular sailor, well equiped in all areas but not excelling in any.",game)

    crew_roles = [buckaneer]
    crewMate1 = components.gen_crewmate(crew_roles,game)
    crewMate2 = components.gen_crewmate(crew_roles,game)

    sloop = components.ShipType(game,"Sloop")

    theSliver = components.Ship("The Sliver",sloop,building_blocks.event_list,game,[crewMate1,crewMate2])
    
    player_fleet = components.Fleet([theSliver],game)
    
    player_storage = components.Storage("Player storage",game)
    player_1 = components.Player(game,player_storage,1,player_fleet,[contract_1],[home_warehouse1])
    
    theFishHeadTavern = components.Tavern("Fish Head's Tavern",game,home,crew_roles,player_1)
    
    theBargainHouse = components.Exchange("The Bargain House",home,game,world,[bread],[gold])
    
    pigeon = components.MessengerPigeon(game,"Test msg",away.coordinates,home.coordinates)
    return game

def _test_save_load():
    print("Creating new test game")
    game = _new_temp_game()
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

    print("Unique tests")
    for observer in new_game.observers:
        if type(observer) == components.Ship:
            print(f"{style.GREEN}Found a ship!{style.RESET}")
            print(f"Ship name: {observer.name}")
            print(f"Ship crew: {[crew.name for crew in observer.crew]}")
        if type(observer) == components.Fleet:
            print(f"{style.GREEN}Found a fleet!{style.RESET}")
            print("Ships in the fleet:")
            print([ship.name for ship in observer.ships]) 
        if type(observer) == components.Player:
            print(f"{style.GREEN}Found a player!{style.RESET}")
            print("Player warehouses:")
            print([house.name for house in observer.warehouses]) 
        if type(observer) == components.Tavern:
            tavern = observer

    print("Unique tests complete")
    input("Press enter to run exchange!")
    #tavern.select_crew()
    print("Saving game...")
    game.save_to_file("save1")
