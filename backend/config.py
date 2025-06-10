import os
from dotenv import load_dotenv

load_dotenv()

SEC_API_KEY= os.getenv("SEC_API_KEY")
STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")