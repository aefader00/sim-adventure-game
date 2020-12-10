# Import other parts of our code.
from map import Location
from item import Item

game_name = "Untitled Text Adventure Featuring Slime and Capitalism As Gameplay Mechanics"
game_version = "1"

# Commands.
command_help = 'help'
command_debug = 'debug'
command_exit = 'exit'
command_mine = 'mine'
command_data = 'data'
command_move = 'move'
command_look = 'look'
command_order = 'order'
command_eat = 'eat'
command_deposit = 'deposit'
command_menu = 'menu'
command_inventory = 'inventory'
command_talk = 'talk'
command_craps = 'craps'
command_slots = 'slots'
command_sell = 'sell'

# Variables for the player's debt.
initial_debt = 1000000

# Variables for scenes.
scene_id_newgame = "Introduction"

# Generic responses.
text_invalid_location = "You must be in {location_name} to use this command."

# Generic inputs in the affirmative.
accept_inputs = [
	"yes",
	"okay",
	"accept",
]

# Generic inputs in the negative.
decline_inputs = [
	"no",
	"nah",
	"decline"
]

# Variables for the locations in the game.
location_id_downtown = "downtown"
location_id_uptown = "uptown"
location_id_south_end = "southend"
location_id_outskirts = "outskirts"

location_id_mines = "mines"
location_id_loan_agency = "loanagency"
location_id_casino = "casino"
location_id_grocer = "grocer"
location_id_soup_kitchen = "soupkitchen"
location_id_bus_stop = "busstop"
location_id_dicks = "dickssportinggoods"
location_id_canada = "canada"

# A list of every location in the game as Location objects.
location_list = [
	Location(
		id=location_id_downtown,
		alias=[
			"dt",
		],
		name="Downtown",
		description="This is Downtown. Skyscrappers, crowds of people walking every which way, all that sort of stuff. You know the deal.",
		neighbors=[
			location_id_uptown,
			location_id_south_end,
			location_id_loan_agency,
			location_id_bus_stop,
			location_id_dicks,
		],
	),
	Location(
		id=location_id_uptown,
		alias=[
			"ut",
		],
		name="Uptown",
		description="This is Uptown. Yuppies all around you. You barf.",
		neighbors={
			location_id_downtown,
			location_id_grocer,
		},
	),
	Location(
		id=location_id_south_end,
		alias=[
			"se",
		],
		name="South End",
		description="This is the South End. Rough and tumble hard knock life stuff Bruce Willis is your dad.",
		neighbors=[
			location_id_downtown,
			location_id_outskirts,
			location_id_soup_kitchen,
			location_id_casino,
		],
	),
	Location(
		id=location_id_outskirts,
		alias=[
			"o",
		],
		name="The Outskirts",
		description="This is the Outskirts. The wind's blowing all like *woooooowowwwoooooooooo*, y'know? Shut up.",
		neighbors=[
			location_id_south_end,
			location_id_mines,
		],
	),
	Location(
		id=location_id_mines,
		alias=[
			"mines",
			"m"
		],
		name="the Mines",
		description="This is the Mines. SLIME AS FAR AS THE EYES CAN SEE!!!! BASED BASED BASED BASED. There's also a fucking mountain of rusty pickaxes on the ground.",
		neighbors=[
			location_id_outskirts,
		],
	),
	Location(
		id=location_id_casino,
		alias=[
			"l",
		],
		name="Casino",
		description="This is the Casino. Lights and shit are blinking everywhere and it's loud and it's totally like MOOOM why did you even bring me here I can't even gamble I'm like 13 please let me just sit in the car I want to beat Kirby Super Start Ultra PLEEEASE WAHHHHHHHHHHHHHH. You know how it is.",
		neighbors=[
			location_id_south_end,
		],
	),
	Location(
		id=location_id_loan_agency,
		alias=[
			"loan",
			"la"
		],
		name="the Loan Agency",
		description="This is the Loan Agency. Fuck this place.",
		neighbors=[
			location_id_downtown,
		],
	),
	Location(
		id=location_id_grocer,
		alias=[
			"g",
		],
		name="a Grocer",
		description="This is some Whole Food shit, it's disgusting. You peel off every 'non-gmo' sticker you can find.",
		neighbors=[
			location_id_uptown,
		],
	),
	Location(
		id=location_id_soup_kitchen,
		alias=[
			"sk",
		],
		name="a Soup Kitchen",
		description="This is a Soup Kitchen. It's really sad in here.",
		neighbors=[
			location_id_south_end,
		],
	),
	Location(
		id=location_id_bus_stop,
		alias=[
			"bs",
		],
		name="a Bus Stop",
		description="This is a bus stop. There's a man you can <b>talk</b> to here.",
		neighbors=[
			location_id_downtown,
		],
	),
	Location(
		id=location_id_canada,
		alias=[
			"mapleleaf",
		],
		name="Canada",
		description="Welcome to Canada! ...Man, it's cold here.",
	),
	Location(
		id=location_id_dicks,
		alias=[
			"d",
			"dsg"
		],
		name="Dick's Sporting Goods",
		description="Y'know like that place with the hockey sticks and stuff. Y'know. You've probably bought cleets here once. No? No cleats? Huh. Well, I've bought cleats here. AND LET ME TELL YOU. They were alright. Sell your poudrins here, also, by the way.",
		neighbors=[
			location_id_downtown,
		],
	),
]

# A dictionary mapping every location identifier to their corresponding locations as Location objects.
id_to_location = {}

for location in location_list:
	# Populate the dictionary.
	id_to_location[location.id] = location

	# Connect the aliases of each location to their corresponding Location objects too.
	for alias in location.alias:
		id_to_location[alias] = location

# Variables for the items in the game.
type_general = "general"
type_food = "food"

# A list of every item in the game as Item objects.
item_list = [
	Item(
		id = "rustypickaxe",
		type = type_general,
		name = "Rusty Pickaxe",
		description = "It's rusty, but it works.",
		durability = 50,
	),
	Item(
		id = "pickaxe",
		type = type_general,
		name = "Pickaxe",
		description = "It's rusty, but it works.",
		durability = 100,
		value = 5000,
		vendor = location_id_dicks,
	),
	Item(
		id = "superpickaxe",
		type = type_general,
		name = "Super Pickaxe",
		description = "It's rusty, but it works.",
		durability = 200,
		value = 20000,
		vendor = location_id_dicks,
	),
	Item(
		id = "poudrin",
		type = type_general,
		name = "Slime Poudrin",
		value = 1000,
		description = "A dense, crystalized chunk of precious slime.",
	),
	Item(
		id = "apple",
		type = type_food,
		name = "Red Apple",
		description = "Juicy and delicious...",
		value = 500,
		vendor = location_id_grocer,
		satiation = 10,
	),
	Item(
		id = "pizza",
		type = type_food,
		name = "pizza",
		description = "Pepperoni, mushroom, onion, and green pepper. Extra cheese. Obliterated with red pepper flakes.",
		value = 2000,
		vendor = location_id_grocer,
		satiation = 100,
	),
		Item(
		id = "gruel",
		type = type_food,
		name = "Gruel",
		description = "Well, it's better than nothing, I guess...",
		value = 10,
		vendor = location_id_soup_kitchen,
		satiation = 5,
	),
]

# A dictionary mapping every item identifier to their corresponding items as Items objects.
item_map = {}

# Populate item map.
for item in item_list:
	item_map[item.id] = item