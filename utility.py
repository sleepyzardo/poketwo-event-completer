import random, re, string
import requests as r

class Utils:
    @staticmethod
    def click_button(token, message_id, custom_id, channel_id, guild_id, application_id, session_id, type, values=None):
        url = 'https://discord.com/api/v9/interactions'
        headers = {'Authorization': token}
        payload = {
            "type": 3,
            "guild_id": guild_id,
            "channel_id": channel_id,
            "message_id": message_id,
            "application_id": application_id,
            "session_id": session_id,
            "data": {
                "component_type": type,
                "custom_id": custom_id,
                "type": 3
            }
        }
        if values is not None:
            payload['data']['values'] = [values]
        res = r.post(url, headers=headers, json=payload)
        return res.status_code

    @staticmethod
    def send(content, token, channel_id):
        url = f'https://discord.com/api/v9/channels/{channel_id}/messages'
        headers = {'Authorization': token}
        payload = {'content': content}
        r.post(url, headers=headers, json=payload)

    @staticmethod
    def check_min_quantity(ingredient_dict):
        min_quantity = float('inf')  # Initialize with infinity to find the minimum quantity

        # Find the minimum quantity among all ingredients
        for quantity in ingredient_dict.values():
            if int(quantity) < min_quantity:
                min_quantity = int(quantity)

        return min_quantity

    @staticmethod
    def checkb(orders, available_ingredients):
        for order in orders:
            order_ingredients = order.description.lower().split(', ')
            all_ingredients_available = True
            temp_ingredients = available_ingredients.copy()  # Create a temporary copy to deduct from

            for ingredient_info in order_ingredients:
                quantity, ingredient = ingredient_info.split('x ')
                ingredient = ingredient.strip().title()
                quantity = int(quantity.strip())
                
                if ingredient in temp_ingredients and quantity <= int(temp_ingredients[ingredient]):
                    temp_ingredients[ingredient] = int(temp_ingredients[ingredient]) - quantity
                else:
                    all_ingredients_available = False
                    break

            if all_ingredients_available:
                return 0, ' '.join(item.split()[1] for item in order.description.split(', ')), order.value, temp_ingredients

        return 999, 999, 999, available_ingredients

    @staticmethod
    def generate_session_id():
        return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(32))

    @staticmethod
    def extract_dish_name(text):
        dish_name_pattern = r"\*\*(.*?)\*\*"
        
        dish_name_match = re.search(dish_name_pattern, text)
        
        if dish_name_match:
            dish_name = dish_name_match.group(1)
            return dish_name
        else:
            return None
