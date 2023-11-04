from abc import ABC
import re
from telegram import Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler
import StolenCommunity

class StolenGuardHandler:
    def __init__(self, stolen_community: StolenCommunity, config) -> None:
        """ Init method for Telegram class.
        """
        self.TIMER_TEMPORARY_MESSAGE = 15        
        self.application = ApplicationBuilder().token(config['token']).build()
        self.stolen_community = stolen_community
        self.init_handler()

    def init_handler(self) -> None:
        """ Method that init and add every handler.
        """
        URL = ForbidenURL()

        handler_url = MessageHandler(filters.Entity('url') & (URL), self.sentence_url)
        handler_text_link = MessageHandler(filters.Entity("text_link"), self.sentence_text_link)
        handler_bestmemer = CommandHandler("bestmemers", self.response_bestmemer)
        
        self.application.add_handler(handler_url)
        self.application.add_handler(handler_text_link)
        self.application.add_handler(handler_bestmemer)

        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

    async def sentence_url(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """ Method to handle sentence if a user send a link that is not allowed.
        """
        await self.delete_alert_inform(update, context, BotResponse.link)

    async def sentence_text_link(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """ Method to handle sentence if a user send text link.
        """
        await self.delete_alert_inform(update, context, BotResponse.text_link)

    async def response_bestmemer(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """ Method to handle bestmemer command.
        """
        await self.inform_best_memer(update, context)

    """ ---------- Method ---------- """

    async def inform_best_memer(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """ Fonction that :
            1. Send temporary msg, saying that the function is processing
            2. Send the best memer list
        """
        chat_id = update.effective_chat.id
        last_days = 30
        
        temporary_message = await context.bot.send_message(
            chat_id=chat_id,
            disable_notification=True,
            text=BotResponse.wait()
        )
        best_memers = await self.stolen_community.retrieve_best_memer(
            last_days=last_days, 
            how_many_best_memer=5
        )
        await context.bot.delete_message(chat_id=chat_id, message_id=temporary_message.id) # Ptetre moyen d'ajouter la suppresion en job_queue
        await context.bot.send_message(
            chat_id=chat_id,
            disable_notification=True,
            text=BotResponse.best_memers(best_memers=best_memers, last_days=last_days)
        )
        
    async def delete_alert_inform(self, update: Update, context: ContextTypes.DEFAULT_TYPE, alert_message_method) -> None:
        """ Method that execute the following sentence :
            1. Delete the message.
            2. Send a temporary message that will alert the user.

        Args:
            alert_message_method (_type_): method of class BotResponse.
        """
        from_user = update.message.from_user['username']
        chat_id = update.effective_chat.id
        
        await update.message.delete()
        msg = await context.bot.send_message(
            chat_id=chat_id, 
            disable_notification=True, 
            text=alert_message_method(from_user)
        )
        context.job_queue.run_once(
            callback=self.delete_message, 
            when=self.TIMER_TEMPORARY_MESSAGE, 
            data=msg['message_id'], 
            chat_id=str(chat_id)
        )

    async def delete_message(self, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send the alarm message."""
        await context.bot.delete_message(
            chat_id=context.job.chat_id, 
            message_id=context.job.data
        )

class BotResponse(ABC):
    """ Abstract bot response class.
    """
    def text_link(from_user: str) -> str:
        return f'No text link allowed here @{from_user}'
    
    def link(from_user: str) -> str:
        return f'No such link allowed here @{from_user}'

    def wait():
        return f'Command proceded. Pliz wait a bit :)'
    
    def best_memers(best_memers, last_days):
        final_str = f'🗿 Best memer of the last {last_days} days are : \n'
        for best_memer in best_memers:
            final_str = f'{final_str} @{best_memer.get("user")} with {best_memer.get("post_count")} posted memes \n'
        return final_str

class ForbidenURL(filters.MessageFilter):
    """ Extended class of filters.MessageFilter.
    """
    def filter(self, message: filters.Message) -> bool:
        """ Filter method.
        Parameters :
            message (filters.Message) : Message object
        Return :
            bool : true if yes. false if no.
        """
        forbiden_site = {
            't.me'
        }

        for site in forbiden_site:
            if re.search(site, message.text, re.IGNORECASE):
                return True
        return False

