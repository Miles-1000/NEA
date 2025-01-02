from dotenv import load_dotenv
import os

load_dotenv(override=True)

class config(object):
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    api_key = os.getenv("API_KEY")
    acc_type = os.getenv("ACC_TYPE")
    acc_number = os.getenv("ACC_NUMBER")
