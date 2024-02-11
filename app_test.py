import streamlit as st

# st.set_page_config(layout='wide')
# st.title('test')
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the value of OPEN_API_KEY
open_api_key = os.getenv('OPENAI_API_KEY')
print(open_api_key)
print('HI')