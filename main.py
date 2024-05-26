import discord
import random
import re
import string
import asyncio
import requests as r
import coloredlogs
import threading
import logging
from utility import Utils
coloredlogs.install(level="INFO")
logger = logging.getLogger(__name__)

TOKENS = [
    {'token': '', 'channel': ''},
]

DELAY = 2
EVENTS = {'Applin', 'Falinks', 'Bellibolt', 'Gulpin', 'Spheals', 'Clamacaron', 'Goomy', 'Tangela', 'Alopix', 'Doublade'}
DEBUG = False

class BotClient(discord.Client):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.available_ingredients = {}

    async def on_ready(self):
        logger.info(f'Successfully Logged into {self.user}.')
        logger.warning(f'PLEASE MAKE SURE YOUR CURRENT ORDERS ARE FINISHED!')
        if self.config['channel'] == '':
            logger.critical('Please set a ChannelId and restart the program...')
            exit()
        if DELAY <= 1:
            logger.warning('Delay is set to less than or equal to 1, This can cause rate-limit issues...')
        if not DEBUG:
            Utils.send('<@716390085896962058> ev inv', self.config['token'], self.config['channel'])
            self.event_mons = 0
            self.pc = 0
            self.shards = 0
            self.redeems = 0
        else:
            channel = self.get_channel(int(self.config['channel']))
            message = await channel.fetch_message(12354)
            print(message.embeds[0].to_dict())
            input()

    async def on_message(self, message):
        if message.author.id == 716390085896962058 and message.channel.id == int(self.config['channel']):
            if len(message.embeds) > 0 and message.embeds[0].title == 'Welcome to Poké2Café!':
                easy = message.components[0].children[0]
                if len(message.components) > 1:
                    custom_id = easy.custom_id
                    guild_id = str(message.guild.id)
                    type = 3
                    channel_id = str(message.channel.id)
                    application_id = str(message.author.id)
                    option = easy.options[0]
                    idx, ind, v, self.available_ingredients = Utils.checkb(easy.options, available_ingredients=self.available_ingredients)
                    if idx != 999:
                        session_id = Utils.generate_session_id()
                        logger.warning(f'SessionId: {session_id}')
                        logger.info(f'Button Request Result (200/204/202 is good): {Utils.click_button(self.config["token"], message.id, custom_id, channel_id, guild_id, application_id, session_id, type, v)}')
                        await message.channel.send(f'<@716390085896962058> ev use {ind}')
                        await asyncio.sleep(DELAY)
                        logger.info('Starting another round...')
                        await message.channel.send(f'<@716390085896962058> ev')
                    else:
                        logger.info('Finished all Recipes/Ran out of materials for the current order...')
                        logger.info(f'Pokecoins: {self.pc}')
                        logger.info(f'Shards: {self.shards}')
                        logger.info(f'Redeems: {self.redeems}')
                        logger.info(f'Events: {self.event_mons}')
                else:
                    logger.info('Finished all Recipes/Ran out of materials for the current order...')
                    logger.info(f'Pokecoins: {self.pc}')
                    logger.info(f'Shards: {self.shards}')
                    logger.info(f'Redeems: {self.redeems}')
                    logger.info(f'Events: {self.event_mons}')

            if "You've completed the order" in message.content:
                logger.info(f'Successfully Completed Order for {Utils.extract_dish_name(message.content)}...')
                if len(message.embeds) > 0:
                    embed = message.embeds[0]
                    embed_desc = embed.description
                    for i in EVENTS:
                        if i in embed_desc:
                            self.event_mons += 1
                            break
                    if 'Shards' in embed_desc or 'Pokécoins' in embed_desc:
                        pattern = r"<:\w+:\d+>\s*([\d,]+)\s*(\w+)"
                        match = re.search(pattern, embed_desc)
                        if match:
                            amount = match.group(1).replace(',', '') 
                            type_ = match.group(2)
                            if type_ == 'Shards':
                                self.shards += int(amount)
                            elif type_ == 'Pokécoins':
                                self.pc += int(amount)
                    if 'Redeem' in embed_desc:
                        pattern = r"([\d,]+)\s+(\w+)"
                        match = re.search(pattern, embed_desc)
                        if match:
                            amount = match.group(1).replace(',', '')
                            self.redeems += int(amount)

            if len(message.embeds) > 0 and 'You donate your ingredients' in message.embeds[0].title:
                raw = message.embeds[0].description.splitlines()
                for i in raw:
                    for j in EVENTS:
                        if j in i:
                            self.event_mons += 1
                            continue
                    if 'Shards' in i or 'Pokécoins' in i:
                        pattern = r"<:\w+:\d+>\s*([\d,]+)\s*(\w+)"
                        match = re.search(pattern, i)
                        if match:
                            amount = match.group(1).replace(',', '')
                            type_ = match.group(2)
                            if type_ == 'Shards':
                                self.shards += int(amount)
                            elif type_ == 'Pokécoins':
                                self.pc += int(amount)
                    if 'Redeem' in i:
                        pattern = r"([\d,]+)\s+(\w+)"
                        match = re.search(pattern, i)
                        if match:
                            amount = match.group(1).replace(',', '')
                            self.redeems += int(amount)
            
            if len(message.embeds) > 0 and 'Poké2Café Ingredients Inventory' in message.embeds[0].title:
                text = message.embeds[0].fields[0].value
                ingredient_dict = {}
                ingredient_values = re.findall(r"`([^`]+)`\s+`([^`]+)`", text)
                for ingredient, quantity in ingredient_values:
                    ingredient_dict[ingredient.strip()] = quantity.strip()
                min_quantity = Utils.check_min_quantity(ingredient_dict)
                if min_quantity > 0:
                    total_quantity = min_quantity
                    while total_quantity > 0:
                        # Limit the donation quantity to a maximum of 15 or the available quantity, whichever is smaller
                        donation_quantity = min(total_quantity, 15)
                        Utils.send(f'<@716390085896962058> ev donate {donation_quantity}', self.config['token'], self.config['channel'])
                        logger.warning('Sleeping for 6 seconds..')
                        await asyncio.sleep(6)
                        
                        total_quantity -= donation_quantity
                    # Maintain a dictionary of available ingredients after donation
                    self.available_ingredients = {ingredient: int(quantity) - min_quantity for ingredient, quantity in ingredient_dict.items()}
                    self.available_ingredients = {ingredient: quantity for ingredient, quantity in self.available_ingredients.items() if str(quantity) != '0'}
                    Utils.send('<@716390085896962058> ev', self.config['token'], self.config['channel'])
                else:
                    self.available_ingredients = ingredient_dict
                    self.available_ingredients = {ingredient: quantity for ingredient, quantity in self.available_ingredients.items() if str(quantity) != '0'}
                    logger.warning('Ingredients are over. Proceeding to recipes..')
                    Utils.send('<@716390085896962058> ev', self.config['token'], self.config['channel'])
            if 'Are you sure you want to donate' in  message.content:
                easy = message.components[0].children[0]
                custom_id = easy.custom_id
                guild_id = str(message.guild.id)
                session_id = Utils.generate_session_id()
                type = 2
                channel_id = str(message.channel.id)
                application_id = str(message.author.id)
                logger.info(f'Button Request Result (200/204/202 is good): {Utils.click_button(self.config["token"], message.id, custom_id, channel_id, guild_id, application_id, session_id, type)}.')


def start_bot(config):
    client = BotClient(config)
    client.run(config['token'])

if __name__ == "__main__":
    threads = []
    for config in TOKENS:
        thread = threading.Thread(target=start_bot, args=(config,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

