from dotenv import load_dotenv
import os
from urllib.parse import quote_plus
load_dotenv('../data/.env')
schema = 'lianes_library'
host = '127.0.0.1'
user = 'root'
pass_word = os.getenv('SQL_PASSWORD')
port = 3306
def connection_str():
    return f'mysql+pymysql://{user}:{quote_plus(pass_word)}@{host}:{port}/{schema}'

print(type(pass_word))
print(pass_word is None)
