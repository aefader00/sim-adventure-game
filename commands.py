# Import external libraries.
import random
import time
import pygame

# Import other parts of our code.
import utilities
import player
import config
import map
import item
from item import get_inventory

move_counter = 0

# Class to send general data about an interaction to a command.
class Command:
	command = ""
	tokens = []
	tokens_count = 0
	message = None

	def __init__(
		self,
		tokens=[],
		message=None,
	):
		self.tokens = tokens
		self.message = message

		if len(tokens) >= 1:
			self.tokens_count = len(tokens)
			self.command = tokens[0]


def debug(cmd):
	response = "Hello!"

	return response

# Gives a brief overview of information about the game.
def help(cmd):
	response = "You whip out your smartphone and navigate to Slimepedia, your goto source for all of your slime-based needs.<br> <br><b>Welcome to Untitled Text Adventure Featuring Slime and Capitalism As Gameplay Mechanics!</b> Your goal is to get enough <b>slime</b> to pay off your debts. You can check how much slime you have and how much of your debt you still have to pay off with the <b>data</b> command. Your best bet for getting slime early on is to use the <b>mine</b> command, while you’re in <b>the Mines</b>, of course. You’ll have to use these sorts of text commands a lot, so get used to it. Most of the time commands can be used by just typing them out, like with <b>data</b> and <b>mine</b>. Others will require additional text to accompany the command itself, like <b>slots</b> and <b>order</b>. So, just input the command, followed by a space, and then whatever additional information you need to specify. Below is a list of basic commands, and when relevant, whatever else you’ll need to type. Don’t worry, you’ll get used to it.<br><br> <br> LIST OF BASIC COMMANDS:<br><b>help</b> - This command!<br><b>data</b> - Shows you your slime and the amount of debt you still have to pay off.<br><b>deposit [amount of slime you wish to deposit] </b> - Pay off some of your debt. Only usable in the Loan Shark’s Office.<br><b>move [neighboring location]</b> - Move to a new location.<br><b>look</b> - Shows you a brief description of the location you’re in and the neighboring locations you can move to from your current one.<br><b>inventory</b> - Shows you all of the items in your inventory.<br><b>menu</b> - Shows you all the items you can buy at your current location. Most of the time you won’t be able to buy any, but some locations have shops.<br><b>order [the item you want to buy]</b> - Order an item from whatever shop you’re at.<br><b>eat [the item you want to eat]</b> - Eat an item that’s in your inventory if you get hungry.<br><b>mine</b> - Mine slime. Only usable in the mines.<br><b>craps [amount of slime you want to bet]</b> - Gamble slime when you’re at the casino. <br><b>slots [amount of slime you want to bet]</b> - Gamble slime when you’re at the casino.<br>"

	return response

# Mine for slime in The Mines!
def mine(cmd):
	# Get the player's data.
	player_data = player.Player()

	# Checks to see if the player is in the right location.
	if player_data.location == config.location_id_mines:
		
		search_for_rusty_pickaxe = item.search_for_item(sought_item="rustypickaxe")
		search_for_pickaxe = item.search_for_item(sought_item="pickaxe")
		search_for_super_pickaxe = item.search_for_item(sought_item="superpickaxe")

		has_pickaxe = None
		has_super_pickaxe = None
		found_poudrin = None

		if search_for_rusty_pickaxe is None and search_for_pickaxe is None and search_for_super_pickaxe is None:
			rusty_pickaxe_object = config.item_map.get("rustypickaxe")
			item.create_item(rusty_pickaxe_object)
			response = "But, alas, you have no pickaxe! Luckily, there's a rusty on the floor. You pick it up, and can now mine. Once you've gotten more slime, you should head into town to look for a better pickaxe instead of relying on hand-me-downs."
			return response
		
		else:
			if search_for_rusty_pickaxe is not None:
				pickaxe = search_for_rusty_pickaxe
			if search_for_pickaxe is not None:
				pickaxe = search_for_pickaxe
				has_pickaxe = True
			if search_for_super_pickaxe is not None:
				pickaxe = search_for_super_pickaxe
				has_super_pickaxe = True

		if player_data.hunger < 100:
			pickaxe.durability -= 1

			pickaxe_broken = False
			if pickaxe.durability <= 0:
				pickaxe_broken = True
				item.delete_item(pickaxe.id)
			else:
				item.edit_item(sought_item=pickaxe.id,
							   property="durability", new_value=pickaxe.durability)
			
			if has_pickaxe or has_super_pickaxe is True:
				if has_super_pickaxe:
					poudrin_chance = 10
					extra_slime_chance = 20
					yield_celling = 300
					extra_celling = 3
				else:
					poudrin_chance = 5
					extra_slime_chance = 10
					yield_celling = 200
					extra_celling = 2

				if random.randint(1, 100) < poudrin_chance:
					poudrin_object = config.item_map.get("poudrin")
					item.create_item(poudrin_object)
					found_poudrin = True
			else:
				yield_celling = 100
				extra_slime_chance = 5
				extra_celling = 1
		
			# Select a random number from 1 to 100 to provide the user with.
			mine_yield = random.randint(1, yield_celling)

			# Add the slime to the player's slimes.
			player_data.slimes += mine_yield
			player_data.hunger += random.randint(1, 5)
			player_data.persist()

			response = "You mined {mine_yield} slime!".format(
				mine_yield=mine_yield)
			
			if random.randint(1, 100) < extra_slime_chance:
				extra_yield = (random.randint(1, yield_celling) * random.randint(1, extra_celling))
				player_data.slimes += extra_yield
				player_data.persist()
				response += "<br><b>Lucky!</b> You hit an extra big vein of slime, you got {} extra slime!".format(extra_yield)

			if found_poudrin:
				response += "<br>You found a <b>slime poudrin</b>! You could probably sell this bad boy for a FORTUNE!" 

			if pickaxe_broken:
				response += "<br>Oh no! Your pickaxe broke!"

			mine_sound = pygame.mixer.Sound("media/sounds/mine.wav")
			pygame.mixer.Sound.play(mine_sound)
		else:
			response = "You're too hungry to mine any more slime! You'll have to eat something..."

	else:
		required_location = config.id_to_location.get(
			config.location_id_mines)
		response = config.text_invalid_location.format(
			location_name=required_location.name)

	return response

# Returns all of the data from your save file.
def data(cmd):
	# Get the player's data.
	player_data = player.Player()

	response = "You name is {name}. ".format(name=player_data.name)

	# Match the current location identifier found in the player's data to a Location object using the id_to_location array in the config file, then store it here.
	current_location = config.id_to_location.get(player_data.location)
	response += "You stand in {location}. ".format(
		location=current_location.name)

	response += "You currently have {slimes} slimes. ".format(
		slimes=player_data.slimes)

	return response

# Look around at your surroundings.
def look(cmd):
	# Get the player's data.
	player_data = player.Player()

	# Match the current location identifier found in the player's data to a Location object using the id_to_location array in the config file, then store it here.
	location = config.id_to_location.get(player_data.location)

	response = "You stand in {location_name}.<br>{location_description}".format(
		location_name=location.name, location_description=location.description)

	if location.neighbors is not None and len(location.neighbors) != 0:
		response += "<br><br>{location_name} is connected to:".format(
			location_name=location.name)
		for neighbor in location.neighbors:
			neighbor_location = config.id_to_location.get(neighbor)
			response += "<br>{neighbor_name}".format(
				neighbor_name=neighbor_location.name)

	return response

# Move around the world.
def move(cmd):
	# Define this variable as the first token the player input after the command itself.
	target = utilities.flatten_tokens(cmd.tokens[1:])

	# If the player didn't input anything after the command.
	if target == None or len(target) == 0:
		response = "Where do you want to go to?"
		return response

	# Get the player's data.
	player_data = player.Player()

	# Match the current location identifier found in the player's data to a Location object using the id_to_location array in the config file, then store it here.
	current_location = config.id_to_location.get(player_data.location)
	# Do the same thing for the "target" variable, which we will assume is a location.
	target_location = config.id_to_location.get(target)

	# If the target location identifier can't be matched to a Location object in the id_to_location array.
	if target_location == None:
		response = "That is not a valid location."
		return response

	# If you are already in your target location.
	if target_location.id == player_data.location:
		response = "You are already there."
		return response

	# If your current location has no neighbors, or if your target location has no neighbors, or if your target location is not a neighborhood of your current location.
	if len(current_location.neighbors) == 0 or len(target_location.neighbors) == 0 or target_location.id not in current_location.neighbors:
		response = "You don't know how to get there from here."
		return response

	else:
		# Change the player's current location to their target location.
		player_data.location = target_location.id
		player_data.persist()

		response = "You enter {current_location}.".format(
			current_location=target_location.name)
		return response

# Order an item.
def menu(cmd):
	player_data = player.Player()

	current_location = config.id_to_location.get(player_data.location)

	list_of_items_for_sale = []

	for item in config.item_list:
		if item.vendor == current_location.id:
			item_listing = "<b>{}</b>: {} slimes<br>".format(
				item.name, item.value)
			list_of_items_for_sale.append(item_listing)
		else:
			pass

	if len(list_of_items_for_sale) == 0:
		response = "There are no items for sale here."
		return response
	else:
		nice_list_of_items_for_sale = utilities.format_nice_list(
			list_of_items_for_sale)

		response = "There are the following items for sale:<br>{}".format(
			nice_list_of_items_for_sale)
		return response



# Order an item.
def order(cmd):
	# Whatever the player inputs after the move command itself.
	target = utilities.flatten_tokens(cmd.tokens[1:])

	# If the player doesn't input anything after the order command.
	if target == None or len(target) == 0:
		response = "What do you want to order?"
		return response

	# Match the desired order to an Item object using the item_map array in the config file, then store it here.
	desired_order = config.item_map.get(target)

	# If the desired order identifier can't be matched to an Item object in the item_map array.
	if desired_order == None:
		response = "That is not a valid item."
		return response
	else:
		# Check to see if the player can buy the found item.
		if desired_order.value is not None and desired_order.vendor is not None:
			# Get the player's data.
			player_data = player.Player()

			# If the player is in the location of the vendor selling the item.
			if desired_order.vendor != player_data.location:
				response = "You cannot buy that item here."
				return response

			# If the player does not have enough slime to buy the desired order.
			if desired_order.value > player_data.slimes:
				response = "You do not have enough slime to order this item! A {order} costs {price}, and you only have {slimes}!".format(
					order=desired_order.name, price=desired_order.value, slimes=player_data.slimes)
				return response
			else:
				# Spend the slime necessary to buy the item.
				player_data.slimes -= desired_order.value
				player_data.persist()

				# Actually create the item.
				item.create_item(desired_order)

				response = "You order a {item}!".format(
					item=desired_order.name, description=desired_order.description)
				return response

def inventory(cmd):
	inventory = get_inventory()

	if inventory.dictionary == None or len(inventory.dictionary) == 0:
		response = "You aren't holding any items."
		return response

	response = "You are holding the following items:<br>"

	for item in inventory.dictionary:
		response += "{}<br>".format(inventory.dictionary[item]['name'])

	return response

# Eat something.
def eat(cmd):
	# Whatever the player inputs after the move command itself.
	target = utilities.flatten_tokens(cmd.tokens[1:])

	# If the player doesn't input anything after the eat command.
	if target == None or len(target) == 0:
		response = "What do you want to eat?"
		return response

	# Search through the player's inventory for the sought item.
	sought_item = item.search_for_item(target)

	# If we don't find the item in the player's inventory.
	if sought_item == None:
		response = "You don't have one of those."
		return response

	# If the player can eat the item.
	if sought_item.satiation == None:
		response = "You can't eat that!"
		return response
	else:
		# Get the player's data.
		player_data = player.Player()
		player_data.hunger -= sought_item.satiation
		if player_data.hunger < 0:
			player_data.hunger = 0
		player_data.persist()

		# Eat the item.
		item.delete_item(target)
		response = "You chomp into the {item}! {description}".format(
			item=sought_item.name, description=sought_item.description)
		if player_data.hunger == 0:
			response = " You're stuffed!"
		return response

# Sell a poudrin.
def sell(cmd):
	player_data = player.Player()

	if player_data.location == config.location_id_dicks:

		# Whatever the player inputs after the move command itself.
		target = utilities.flatten_tokens(cmd.tokens[1:])

		# If the player doesn't input anything after the eat command.
		if target == None or len(target) == 0:
			response = "What do you want to sell?"
			return response

		# Search through the player's inventory for the sought item.
		sought_item = item.search_for_item(target)

		# If we don't find the item in the player's inventory.
		if sought_item == None:
			response = "You don't have one of those."
			return response

		# If the player can eat the item.
		if sought_item.id != "poudrin":
			response = "You can't sell that!"
			return response
		else:
			# Get the player's data.
			slime_yield = random.randint(500, 5000)
			player_data.slimes += slime_yield
			player_data.persist()

			# Eat the item.
			item.delete_item(target)
			response = "You pass over the {} to the cashier! You get {:,} slime!".format(sought_item.name, slime_yield)
			
	else:
		required_location = config.id_to_location.get(
			config.location_id_dicks)
		response = config.text_invalid_location.format(
			location_name=required_location.name)
	
	return response

# Deposit some slime into your loan shark's bank account.
def deposit(cmd):
	# Get the player's data.
	player_data = player.Player()

	if player_data.location != config.location_id_loan_agency:
		required_location = config.id_to_location.get(
			config.location_id_loan_agency)

		response = config.text_invalid_location.format(
			location_name=required_location.name)
		return response

	# Define this variable as the first token the player input after the command itself.
	try:
		amount = int(utilities.flatten_tokens(cmd.tokens[1:]))
	except:
		amount = None

	# If the player didn't input anything after the command.
	if amount == None or amount == 0:
		response = "How much slime do you want to deposit?"
		return response

	# Get the player's data.
	player_data = player.Player()

	# If the player tries to deposit more slimes than they have.
	if amount > player_data.slimes:
		response = "You can't deposit that much slime, you only have {:,}.".format(
			player_data.slimes)
		return response

	else:
		# Deposit the slime.
		player_data.slimes -= amount
		player_data.debt -= amount
		player_data.persist()

		response = "You dump {:,} slime into the ATM.".format(amount)

		if player_data.debt <= 0:
			response += "<br>Good job, you've paid off all your debts!<br> <br> ...What? Did you expect something more rewarding? All you’ve done is reset things to zero. You’re still poor, and you’ll have to keep mining slime if you want to keep the lights on. Then, when the mines dry up, you’ll need another loan. Rinse and repeat. There’s no happy ending here. But, you did beat the game. That’s pretty cool, huh?"
			response += "<br> <br><b>YOU WIN!!</b><br> <br>This project was created by the SIM Technology Group.<br>In no paticular order, here are the people who helped make this game possible:"
			response += "<br>- Nick Thompson<br>- Dominic Milton<br>- Ryan Davies<br>- Sonnae Peterson<br>- Anthony Fader<br>- Aidan Collins<br>- Dana Moser"
		return response

# Talk to the man at the bus stop.
def talk(cmd):
	# Get the player's data.
	player_data = player.Player()

	# Checks to see if the player is in the right location.
	if player_data.location == config.location_id_bus_stop:
		bribe = item.search_for_item(sought_item="pizza")

		if bribe is not None:
			player_data.location = config.location_id_canada
			player_data.persist()

			response = "Is that a pizza? Please, give it to me! I'll give you this bus ticket in return..."
			response += "You give the pizza to the man and in exchange you get the ticket. You wait patiently and board the next bus."
			response += "As you board, a wave of relief washes over you. You've escaped America, and your debts along with it!"
			response += "<br>You wonder if there's slime in Canada..."
			response += "<br> <br><b>YOU WIN!!</b><br> <br>This project was created by the SIM Technology Group.<br>In no paticular order, here are the people who helped make this game possible:"
			response += "<br>- Nick Thompson<br>- Dominic Milton<br>- Ryan Davies<br>- Sonnae Peterson<br>- Anthony Fader<br>- Aidan Collins<br>- Dana Moser"
			return response

		else:
			response = "You approach the man and strike up a casual conversation."
			response += "<br><br>'Guhhh... I'm so hungry... If someone were to give me an piece of pizza right now, I'd be so happy, I'd totally just straight up give them my bus ticket which could totally be, like, their opportunity to escape their debts and illegal immigrate to Canada, and stuff... *Sigh* Like, that'll ever happen...'"
			return response

	else:
		required_location = config.id_to_location.get(
			config.location_id_bus_stop)
		response = config.text_invalid_location.format(
			location_name=required_location.name)

	return response

def craps(cmd):
	player_data = player.Player()

	if player_data.location == config.location_id_casino:
		# Define this variable as the first token the player input after the command itself.
		try:
			amount = int(utilities.flatten_tokens(cmd.tokens[1:]))
		except:
			amount = None
		# If the player didn't input anything after the command.
		if amount == None or amount <= 0:
			response = "How much slime do you want to bet?"
			return response

		# If the player tries to deposit more slimes than they have.
		if amount > player_data.slimes:
			response = "You can't deposit that much slime, you only have {:,}.".format(player_data.slimes)
			return response

		else:
			roll_1 = random.randint(1,6)
			roll_2 = random.randint(1,6)

			if (roll_1 + roll_2) == 7:
				winnings = 5 * amount
				player_data.slimes += winnings
				player_data.persist()
				response = "You rolled a 7!! Amazing! You got {}!".format(winnings)
			else:
				player_data.slimes -= amount
				player_data.persist()
				response = "You didn't roll a 7! You lost your slime."
	else:
		required_location = config.id_to_location.get(
			config.location_id_casino)
		response = config.text_invalid_location.format(
			location_name=required_location.name)
	
	return response

def slots(cmd):
	player_data = player.Player()

	if player_data.location == config.location_id_casino:
		# Define this variable as the first token the player input after the command itself.
		try:
			amount = int(utilities.flatten_tokens(cmd.tokens[1:]))
		except:
			amount = None
		# If the player didn't input anything after the command.
		if amount == None or amount <= 0:
			response = "How much slime do you want to bet?"
			return response

		# If the player tries to deposit more slimes than they have.
		if amount > player_data.slimes:
			response = "You can't deposit that much slime, you only have {:,}.".format(player_data.slimes)
			return response

		else:	
			possible_slots = [
				"7",
				"Lemon",
				"Orange",
				"Apple",
				"Lime"
			]
			possible_slots_len = len(possible_slots)

			# Determine the final state.
			slot_1 = possible_slots[random.randrange(0, possible_slots_len)]
			slot_2 = possible_slots[random.randrange(0, possible_slots_len)]
			slot_3 = possible_slots[random.randrange(0, possible_slots_len)]

			# Determine winnings.
			if slot_1 == slot_2 and slot_1 == slot_3:
				if slot_1 == "7" and slot_2 == "7" and slot_3 == "7":
					winnings = 777 * amount
					response = "You got: <b>{}</b> <b>{}</b> <b>{}</b>".format(slot_1, slot_2, slot_3)
					response += "<br><b>SUPER JACKPOT YOU ARE A MOVIESTAR!!!!</b> The machine spits out {:,} slime.**".format(winnings)
				else:
					winnings = 50 * amount
					response = "You got: <b>{}</b> <b>{}</b> <b>{}</b>".format(slot_1, slot_2, slot_3)
					response += "<br><b>JACKPOT!!</b> The machine spits out {:,} slime.**".format(winnings)
				
				player_data.slimes += winnings
				player_data.persist()
			else:
				response = "You got: <b>{}</b> <b>{}</b> <b>{}</b>".format(slot_1, slot_2, slot_3)
				response += "<br>*Nothing happens...*"
				player_data.slimes -= amount
				player_data.persist()
	else:
		required_location = config.id_to_location.get(
			config.location_id_casino)
		response = config.text_invalid_location.format(
			location_name=required_location.name)
		
	return response