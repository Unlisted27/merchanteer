import style

book_data = {
    "title":"Merchanteer's Handbook",
    "pages":[
        {
            "title":f"{style.BOLD}{style.UNDERLINE}Intro{style.RESET}",
            "content":f"Welcome to Merchanteer! This is a game about ancient sea trade, attempting to simulate the difficulty of not having any mode of communication faster than a boat or horse. This book contains everything you need to get started. Use the chapters menu to find specific information, or keep reading for the begginers guide.",
            "chapter_marker":True
        },
        {
            "title":f"{style.BOLD}{style.UNDERLINE}Begginers guide{style.RESET}",
            "content":f"This chapter will explain the basic game loop, and everything you need to get started. If you want specific information about the game, return to the cover and navigate the chapters from there.",
            "chapter_marker":True
        },
        {
            "title":f"{style.UNDERLINE}Day progression{style.RESET}",
            "content":f"Merchanteer is turn based, with each turn representing a day. The player can choose to progress to the next day at any time from the game menu (the menu that presents the save and quit option). Progressing time allows for anything the player set in motion during the day to progress (dispatching {style.CYAN}ships{style.RESET}), etc).\n"
            f"At the start of a new day, the player will recieve a breakdown made up of {style.YELLOW}notices{style.RESET}, of what happened during the time progression, such as if any {style.BROWN}contracts{style.RESET} were completed. {style.YELLOW}Notices{style.RESET} can be seen in {style.YELLOW}Game menu -> General actions -> View notices{style.RESET}.\n"
        },
        {
            "title":f"{style.UNDERLINE}Game loop{style.RESET}",
            "content":f"The basic game loop runs like this:\n"
            f"1. Go to the {style.MAGENTA}Bargain House{style.RESET} and accept a {style.BROWN}contract{style.RESET}.\n"
            f"2. Go to the {style.BLUE}port{style.RESET} and select a {style.CYAN}ship{style.RESET}.\n"
            f"3. Select {style.YELLOW}Load{style.RESET} to begin loading {style.GREEN}goods{style.RESET} from your warehouse.\n"
            f"4. Select {style.YELLOW}Plan voyage{style.RESET} and the {style.BROWN}contract{style.RESET} coresponding with the {style.GREEN}goods{style.RESET} you loaded. Then add the corresponding {style.LIGHT_BLUE}destination{style.RESET}.\n"
            f"5. Go back to the {style.YELLOW}Route planning{style.RESET} menu and select {style.YELLOW}Dispatch{style.RESET} to send the {style.CYAN}ship{style.RESET} on its way.\n"
            f"6. You can do steps 1 through 5 as many times as you like with multiple {style.CYAN}ships{style.RESET}. You can also dispatch {style.CYAN}ships{style.RESET} to multiple destinations with multiple {style.BROWN}contracts{style.RESET}.\n"
            "(This continues on the next page...)"
        },
        {
            "title":f"{style.UNDERLINE}Game loop continued...{style.RESET}",
            "content":
            f"7. Progress to the next day from the main menu until you receive a notice that your {style.BROWN}contract(s){style.RESET} can be redeemed.\n"
            f"8. Go to the {style.MAGENTA}Bargain House{style.RESET} and redeem your {style.BROWN}contract(s){style.RESET}. The {style.GREEN}reward{style.RESET} will be deposited in a warehouse of your choosing\n\n"
            "This concludes the Begginers guide. At the time this was written, you can't really do anything with your currency goods, but purchasing ships, crew contracts, and more ways to expand you merchant empire are coming soon."
        },
        {
            "title":f"{style.BOLD}{style.UNDERLINE}The world{style.RESET}",
            "content":f"The world of Merchanteer is made up of {style.LIGHT_BLUE}Locations{style.RESET}. Each {style.LIGHT_BLUE}location{style.RESET} contains {style.BLUE}ports{style.RESET} that you can dispatch {style.CYAN}ships{style.RESET} to. Despite multiple {style.BLUE}ports{style.RESET} existing, only one is accessible directly by you, as that is the {style.BLUE}port{style.RESET} you are currently 'at'. The world is randomly generated at the start of each new game, so travel time between different {style.LIGHT_BLUE}locations{style.RESET} varies each playthrough.",
            "chapter_marker":True
        },
        {
            "title":f"{style.GREEN}{style.BOLD}{style.UNDERLINE}Currency and goods{style.RESET}",
            "content":f"All {style.GREEN}goods{style.RESET} in merchanteer have a base value stat, however money itself in Merchanteer is itself a {style.GREEN}good{style.RESET} (typically a precious metal like {style.GREEN}gold{style.RESET} or {style.GREEN}silver{style.RESET}).\n"
            f"These 'money' {style.GREEN}goods{style.RESET} are known as {style.GREEN}currency goods{style.RESET}, and can be used to purchase other {style.GREEN}goods{style.RESET}, {style.CYAN}ships{style.RESET}, or services.",
            "chapter_marker":True

        },
        {
            "title":f"{style.BROWN}{style.BOLD}{style.UNDERLINE}Contracts{style.RESET}",
            "content":f"{style.BROWN}Contracts{style.RESET} are the primary money maker in Merchanteer.\n"
            f"A {style.BROWN}contract{style.RESET} consists of the following {style.YELLOW}important properties{style.RESET}:\n"
            f"{style.BOLD}{style.YELLOW}Name{style.RESET}: A randomly generated name useful for tracking purposes\n"
            f"{style.BOLD}{style.YELLOW}Weight{style.RESET}: The weight in Kg, useful to know if a {style.CYAN}ship{style.RESET} can carry those {style.GREEN}goods{style.RESET}\n"
            f"{style.BOLD}{style.YELLOW}Good{style.RESET}: The {style.GREEN}good{style.RESET} that is being transported\n"
            f"{style.BOLD}{style.YELLOW}Reward{style.RESET}: The amount and type of {style.GREEN}currency good{style.RESET} that will be rewarded uppon completion.\n"
            f"{style.BOLD}{style.LIGHT_BLUE}Destination{style.RESET}: The destination for the {style.BROWN}contract{style.RESET} {style.GREEN}goods{style.RESET} to be delivered to.\n"
            f"{style.BOLD}{style.YELLOW}Status{style.RESET}: The current status of the {style.BROWN}contract{style.RESET}, indicating a due date, completed, or expired.\n",
            "chapter_marker":True
        },
        {
            "title":f"{style.BROWN}{style.UNDERLINE}Contracts{style.RESET}{style.UNDERLINE} continued...{style.RESET}",
            "content":f"{style.BROWN}Contracts{style.RESET} can be found in the {style.MAGENTA}Bargain House{style.RESET}. Once a {style.BROWN}contract{style.RESET} is accepted, the {style.GREEN}goods{style.RESET} required to be delivered will be transported to a warehouse of your choosing. The {style.GREEN}goods{style.RESET} can then be loaded onto a {style.CYAN}ship{style.RESET}, and transported to their destination. The {style.GREEN}reward{style.RESET} for the {style.BROWN}contract{style.RESET} will not be deposited instantly, but rather you will have to wait a small amount of time for a carrier pigeon to fly from the {style.BLUE}destination port{style.RESET} to deliver the news that the {style.GREEN}goods{style.RESET} were delivered successfully. Once a {style.BROWN}contract{style.RESET} is ready to be redeemed, a notice will appear at the start of a new day and you can go to the {style.MAGENTA}Bargain House{style.RESET} to redeem it."
        },
        {
            "title":f"{style.BOLD}{style.UNDERLINE}Index{style.RESET}",
            "content":
            f"{style.GREEN}Goods{style.RESET} are in {style.GREEN}Green{style.RESET}\n"
            f"{style.BROWN}Contracts{style.RESET} are in {style.BROWN}Brown{style.RESET}\n"
            f"{style.ORANGE}Crew{style.RESET} and related are in {style.ORANGE}Orange{style.RESET}\n"
            f"{style.LIGHT_BLUE}Locations{style.RESET} are in {style.LIGHT_BLUE}Light Blue{style.RESET}\n"
            f"{style.BLUE}Ports{style.RESET} are in {style.BLUE}Blue{style.RESET}\n"
            f"{style.MAGENTA}Exchanges{style.RESET} are in {style.MAGENTA}Magenta{style.RESET}\n"
            f"{style.CYAN}Ships{style.RESET} are in {style.CYAN}Cyan{style.RESET}\n"
            f"{style.YELLOW}Highlighted information{style.RESET} is in {style.YELLOW}Yellow{style.RESET}\n"
            f"{style.RED}Hazards{style.RESET} and {style.RED}Errors{style.RESET} are in {style.RED}Red{style.RESET}\n",
            "chapter_marker":True
        }
    ]
}