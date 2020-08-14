import ast
import requests
from datetime import datetime
from typing import List
import spotipy
import spotipy.util as util
from os import listdir
import pandas as pd

def get_token(user, 
              client_id,
              client_secret,
              redirect_uri,
              scope):
  
    token = util.prompt_for_user_token(username = user,scope=None,client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri)
    return token