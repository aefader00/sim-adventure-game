import player
import utilities
import config
import json

# The object model for the scripted sequences in the game.
class Scene:
    # These values are default placeholders. They will be overwritten when the player's data can be retrieved.

    # The progress the player has made through the scene.
    progress = 0

    # Create the scene object.
    def __init__(self, scene):
        try: # Open up the save file.
            with open('save.json', 'r') as save_file:
                # Turn the JSON object into a Python list containing dictionaries.
                data = json.load(save_file)

                # Retrieves the the relevant data from the save file.
                scene_data = data['quest_progress']

                # Loads the data into the player object.
                self.progress = scene_data[scene]

                # Safely close the file.
                save_file.close()
        except: # If there is no save file in the game's directory.
            utilities.new_game()

    # Save the data from this player object to the save file.
    def persist(self, scene):
        # Open up the save file again to store the data as a local dictionary for ease of use.
        with open('save.json', 'r') as save_file:
            # Turn the JSON object into a Python list containing dictionaries.
            save_data = json.load(save_file)
            # Safely close the file.
            save_file.close()

        # Update the save file.
        with open('save.json', 'w') as save_file:
            # Overwrite the save file with the data from this object.
            save_data['quest_progress'][scene] = self.progress

            # Convert the dictionary into a JSON object and save it in a save file.
            json.dump(save_data, save_file, indent=2)

            # Safely close the file.
            save_file.close()

def Introduction(message):
    scene = Scene(config.scene_id_newgame)

    if scene.progress == 0:
        scene.progress = 1
        scene.persist(config.scene_id_newgame)

        response = "You are in dire straits.<br><br>After being laid off unexpectedly last month, you have been trying to find new work to no avail. In your desperation, you turned to one of the city's notorious loan sharks for help. Your family was fed for a few months, but.. now you're {:,} slimes in debt and still without a job. In order to pay off your loan, you'll have to mine some slime in one of the quarries in the outskirts of the city. It might be illegal, and it might be horribly demeaning, but you don't have any other choice.".format(
            config.initial_debt)
        response += "<br><br>But, first things firsts. What's your name?"
    
    elif scene.progress == 1:
        scene.progress = 2
        scene.persist(config.scene_id_newgame)

        player_data = player.Player()
        player_data.name = message
        player_data.scene = None
        player_data.persist()
        response = "Understood. So, {player_name}, what will you do now?".format(
            player_name=player_data.name)
    
    return response
