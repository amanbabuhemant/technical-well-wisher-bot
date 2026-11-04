import os

from dotenv import load_dotenv


load_dotenv()


APPLICATION_ID     = os.getenv("APPLICATION_ID")
PUBLIC_KEY         = os.getenv("PUBLIC_KEY")
TOKEN              = os.getenv("TOKEN")
PERMISSION_INTEGER = os.getenv("PERMISSION_INTEGER")


