import os
from os import environ

id_pattern = re.compile(r'^.\d+$')

AUTH_CHANNEL = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('AUTH_CHANNEL', '-1002245813234').split()] 
# give channel id with separate space. Ex: ('-10073828 -102782829 -1007282828')


API_HASH = os.getenv("API_HASH", "f668c20d77d1a8feee31afdc810f8ac4")
API_ID = int(os.getenv("API_ID", "27148454"))
BOT_TOKEN = os.getenv("BOT_TOKEN", "7482878132:AAHD6Hse2QZl2C8tXfhpvoy2uoSaGmN17wg")
UPDATE_CHANNEL = os.getenv("UPDATE_CHANNEL", "Prime_Botz")
BOT_OWNER = int(os.getenv("BOT_OWNER", "5926160191"))
DATABASE_URL = os.getenv("DATABASE_URL", "mongodb+srv://cokas14279:yXIpH2JZnYfMHGHD@cluster0.dhfes.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
