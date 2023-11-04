from telethon.sync import TelegramClient
from datetime import datetime, timedelta

class StolenCommunity:
    def __init__(self, config) -> None:
        """ Connect to telethon API.
        """
        api_id = config['api_id']
        api_hash = config['api_hash']
        phone_number = config['phone_number']
        
        self.client = TelegramClient(config['username'], api_id, api_hash)
        self.stolen_meme_id = config['group_id']
        
        self.client.connect()
        if not self.client.is_user_authorized():
            self.client.send_code_request(phone_number)
            self.client.sign_in(phone_number, input('Enter the code: '))
    
    async def retrieve_best_memer(self, last_days, how_many_best_memer) -> list:
        """ Method that retrieve best memers.
        Args:
            last_days (int): from the last X day
            how_many_best_memer (int): first best memer
        Return:
            best_memers (list(dict)): list of {how_many_best_memer} best memer.
        """
        month = datetime.now() - timedelta(days=last_days)
        best_memers = []
        async for message in self.client.iter_messages(self.stolen_meme_id, offset_date=month, reverse=True):
            if message.media and message.sender.username is not None: # Impossible de mettre un filtre
                user = message.sender.username
                for best_memer in best_memers:
                    if user in best_memer.get("user"):
                        best_memer["post_count"] += 1
                        break
                else:
                    best_memers.append(
                        {
                            "user": user,
                            "post_count": 1
                        }
                    ) 
        return sorted(best_memers, key=lambda d: d['post_count'], reverse=True)[0:how_many_best_memer]
