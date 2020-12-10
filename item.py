# Import external libraries.
import json
import config
import utilities

# The object model for locations on the map.
class Item:
	# These values are default placeholders.

	# The unique identifier for this item. All lowercase, no spaces.
	id = ""

	# The type of item it is; Whether it's a general purpose item, a piece of food, or something else.
	type = ""

	# The nice, proper name for this place. May contain uppercase letters, and spaces.
	name = ""

	# The description provided when inspecting it. TODO: Add inspecting.
	description = ""
	
	# The price of this item if it is sold at a vendor. 
	value = None

	# The vendor this item is sold at.
	vendor = None

	# The amount hunger restored if this item is eaten.
	satiation = None

	# The amount of times the item can be used before breaking.
	durability = None

	# The destination of a GrubHub order.
	destination = None

	def __init__(
		self,
		id,
		type,
		name,
		description,
		value = None,
		vendor = None,
		satiation = None,
		durability = None,
		destination = None,
	):
		self.id = id
		self.type = type
		self.name = name
		self.description = description
		self.value = value
		self.vendor = vendor
		self.satiation = satiation
		self.durability = durability
		self.destination = destination

# The object model for the player's inventory.
class Inventory:
    # These values are default placeholders. They will be overwritten when the player's data can be retrieved.

    # The dictionary containing all items and their values.
    dictionary = {}

    # Create the scene object.
    def __init__(self):
        try: # Open up the save file.
            with open('save.json', 'r') as save_file:
                # Turn the JSON object into a Python list containing dictionaries.
                data = json.load(save_file)

                # Retrieves the item data from the save file.
                self.dictionary = data['items']

                # Safely close the file.
                save_file.close()
        except: # If there is no save file in the game's directory.
            utilities.new_game()

    # Save the data from this player object to the save file.
    def persist(self):
        # Open up the save file again to store the data as a local dictionary for ease of use.
        with open('save.json', 'r') as save_file:
            # Turn the JSON object into a Python list containing dictionaries.
            save_data = json.load(save_file)
            # Safely close the file.
            save_file.close()

        # Update the save file.
        with open('save.json', 'w') as save_file:
            # Overwrite the save file with the data from this object.
            save_data['items'] = self.dictionary

            # Convert the dictionary into a JSON object and save it in a save file.
            json.dump(save_data, save_file, indent=2)

            # Safely close the file.
            save_file.close()

def get_inventory():
	with open('save.json') as save_file:
		# Load the player's save file and retrieve their inventory data.
		return Inventory()

def create_item(desired_item):
	with open('save.json') as save_file:
		# Load the player's save file and retrieve their inventory data.
		inventory = Inventory()

		used_id_strings = inventory.dictionary.keys()
		used_id_integers = [int(id) for id in used_id_strings]

		index = int(max(used_id_integers)) + 1 if inventory.dictionary != {} else 1

		new_item = {
			index: {
				"id": desired_item.id,
				"type": desired_item.type,
				"name": desired_item.name,
				"description": desired_item.description,
			}
		}

		if desired_item.value != None:
			new_item[index]["value"] = desired_item.value
		
		if desired_item.vendor != None:
			new_item[index]["vendor"] = desired_item.vendor
		
		if desired_item.satiation != None:
			new_item[index]["satiation"] = desired_item.satiation
		
		if desired_item.durability != None:
			new_item[index]["durability"] = desired_item.durability
		
		if desired_item.destination != None:
			new_item[index]["destination"] = desired_item.destination

		inventory.dictionary.update(new_item)
		inventory.persist()

def search_for_item(sought_item):
	with open('save.json') as save_file:
		# Load the player's save file and retrieve their inventory data.
		inventory = Inventory()

		for item in inventory.dictionary:
			if inventory.dictionary[item]['id'] == sought_item:
				item_object = Item(
								id = inventory.dictionary[item]['id'],
								type = inventory.dictionary[item]['type'],
								name = inventory.dictionary[item]['name'],
								description = inventory.dictionary[item]['description'],
							)
				
				if "value" in inventory.dictionary[item].keys():
					item_object.value = inventory.dictionary[item]["value"]
				
				if "vendor" in inventory.dictionary[item].keys():
					item_object.vendor = inventory.dictionary[item]["vendor"]
				
				if "satiation" in inventory.dictionary[item].keys():
					item_object.satiation = inventory.dictionary[item]["satiation"]
				
				if "durability" in inventory.dictionary[item].keys():
					item_object.durability = inventory.dictionary[item]["durability"]
				
				if "destination" in inventory.dictionary[item].keys():
					item_object.destination = inventory.dictionary[item]["destination"]

				return item_object


def delete_item(sought_item):
	with open('save.json') as save_file:
		# Load the player's save file and retrieve their inventory data.
		inventory = Inventory()

		for item in inventory.dictionary:
			if inventory.dictionary[item]['id'] == sought_item:
				del inventory.dictionary[item]
				inventory.persist()
				break

def edit_item(sought_item, property, new_value):
	with open('save.json') as save_file:
		# Load the player's save file and retrieve their inventory data.
		inventory = Inventory()

		for item in inventory.dictionary:
			if inventory.dictionary[item]['id'] == sought_item:
				inventory.dictionary[item][property] = new_value
				inventory.persist()
				break