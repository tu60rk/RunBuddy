def get_user_lang(message):
    return message.from_user.language_code or "en"