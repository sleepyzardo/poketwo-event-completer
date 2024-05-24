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
    def check(ingredient_dict):
        butter_quantity = ingredient_dict.get("Butter", 0)

        for ingredient, quantity in ingredient_dict.items():
            if ingredient == "Butter":
                continue
            if int(quantity) <= int(butter_quantity):
                return False, butter_quantity

        return True, butter_quantity
    @staticmethod
    def checkb(order):
        if 'butter' in order.description.lower():
            return 999,999,999
        else:
            ingredients = ' '.join(item.split()[1] for item in order.description.split(', '))
            value = order.value
            return 0, ingredients, value
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
