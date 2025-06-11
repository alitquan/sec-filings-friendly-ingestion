import os
from dotenv import load_dotenv

# define file called .env at same level with the 
# appropriate keys 
load_dotenv()

SEC_API_KEY= os.getenv("SEC_API_KEY")
GENERATION_DIRECTORY="pdf-filings"
