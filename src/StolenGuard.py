import json
import StolenCommunity
import StolenHandler

class StolenGuard:
    def __init__(self):
        self.config_file = 'ressources/config.json'
        config = self.get_config()
        
        stolen_community = StolenCommunity.StolenCommunity(config['telethon'])
        stolen_guardhandler = StolenHandler.StolenGuardHandler(stolen_community, config['python_telegram_bot'])

    def get_config(self):
        with open(self.config_file, 'r') as f:
            return json.load(f)

if __name__ == "__main__":
    StolenGuard()