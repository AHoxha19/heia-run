import json
class GameManager:

      world_number = 0
      has_loaded = False
      reset = False
      number_of_lifes = 3
      next_level = False
      mute = False

      data = {
          "world_number": 0
      }
      
      @staticmethod
      def load_game():
          with open("save.json", "r") as read_file:
            GameManager.data = json.load(read_file)
            GameManager.world_number = GameManager.data['world_number']

      @staticmethod
      def save_game():
          GameManager.data['world_number'] = GameManager.world_number
          with open("save.json", "w") as write_file:
              json.dump(GameManager.data, write_file)



