import vk_api
from dotenv import load_dotenv
import os

load_dotenv()
session = vk_api.VkApi(token=os.getenv("TOEKN"))


