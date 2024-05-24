import discord, random, re, string, asyncio
from utility import Util
import requests as r
import coloredlogs
import json
import logging
TOKEN = 'ur account token'
CHANNEL_ID = 'channel id'
DELAY = 2
client = discord.Client()
coloredlogs.install(level="INFO")
logger = logging.getLogger(__name__)

@client.event
async def on_ready():
    logger.info(f'Successfully Logged into {client.user}.')
    logger.warning(f'PLEASE MAKE SURE YOUR CURRENT ORDERS ARE FINISHED!')
    if CHANNEL_ID == '':
        logger.critical('Please set a ChannelId and restart the program...')
        exit()
    if DELAY <= 1:
        logger.warning('Delay is set to less than or equal to 1, This can cause rate-limit issues...')
    Utils.send('<@716390085896962058> ev inv', TOKEN, CHANNEL_ID)
@client.event
async def on_message(message):
    if message.author.id == 716390085896962058 and message.channel.id == int(CHANNEL_ID):
        if len(message.embeds) > 0 and message.embeds[0].title == 'Welcome to Poké2Café!':
            easy = message.components[0].children[0]
            if len(message.components) > 1:
                custom_id = easy.custom_id
                guild_id = str(message.guild.id)
                type = 3
                channel_id = str(message.channel.id)
                application_id = str(message.author.id)
                option = easy.options[0]
                idx, ind, v = Utils.checkb(option)
                if idx != 999:
                    session_id = Utils.generate_session_id()
                    logger.warning(f'SessionId: {session_id}')
                    logger.info(f'Button Request Result (200/204/202 is good): {Utils.click_button(TOKEN, message.id, custom_id, channel_id, guild_id, application_id, session_id, type, v)}')
                    await message.channel.send(f'<@716390085896962058> ev use {ind}')
                    await asyncio.sleep(DELAY)
                    logger.info('Staring another round...')
                    await message.channel.send(f'<@716390085896962058> ev')
            else:
                logger.info('Finished all Recipes/Ran out of materials for current order...')
        if "You've completed the order" in message.content:
            logger.info(f'Successfully Completed Order for {Utils.extract_dish_name(message.content)}...')
            logger.warning(f'Sleeping for {DELAY} seconds...')
        if len(message.embeds) > 0 and 'Poké2Café Ingredients Inventory' in message.embeds[0].title:
            text = message.embeds[0].fields[0].value
            ingredient_dict = {}
            ingredient_values = re.findall(r"`([^`]+)`\s+`([^`]+)`", text)
            for ingredient, quantity in ingredient_values:
                ingredient_dict[ingredient.strip()] = quantity.strip()
            res, bq = Utils.check(ingredient_dict)
            if res:
                if int(bq) > 0:
                    total_quantity = int(bq)
                    while total_quantity > 0:
                        donation_quantity = min(total_quantity, 15)
                        Utils.send(f'<@716390085896962058> ev donate {donation_quantity}', TOKEN, CHANNEL_ID)
                        total_quantity -= donation_quantity
                else:
                    logger.warning('Butter is over. Proceeding to recipes..')
                    Utils.send('<@716390085896962058> ev', TOKEN, CHANNEL_ID)
            else:
                logger.warning('Passing Donating as the values for ingredients is less than Butter...')
                Utils.send('<@716390085896962058> ev', TOKEN, CHANNEL_ID)
        if 'Are you sure you want to donate' in  message.content:
            easy = message.components[0].children[0]
            custom_id = easy.custom_id
            guild_id = str(message.guild.id)
            session_id = Utils.generate_session_id()
            type = 2
            channel_id = str(message.channel.id)
            application_id = str(message.author.id)
            logger.info(f'Button Request Result (200/204/202 is good): {Utils.click_button(TOKEN, message.id, custom_id, channel_id, guild_id, application_id, session_id, type)}.')
            Utils.send('<@716390085896962058> ev', TOKEN, CHANNEL_ID)

       


client.run(TOKEN, log_handler=None)
