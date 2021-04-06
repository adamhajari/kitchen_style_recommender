import pandas as pd
import sqlite3
from collections import defaultdict

from app import database_file

def get_db_connection():
    return sqlite3.connect(database_file)

def get_kitchen_attributes():
    kitchens_from_sql = pd.read_sql_query('select * from image_attributes', get_db_connection())
    kitchen_dict = defaultdict(list)
    for i, row in kitchens_from_sql.iterrows():
        kitchen_dict[row['image_id']].append(row['attribute'])
    return kitchen_dict


def get_user_feedback(user_id):
    query = f'select * from user_image_feedback where user_id={str(user_id)}'
    return pd.read_sql_query(query, get_db_connection())
    

def get_user_style_profile(user_id):
    user_feedback_df = get_user_feedback(user_id)
    kitchen_attributes = get_kitchen_attributes()
    user_dict = defaultdict(int)

    image_count = 0  # keep track of how many images the user has given feedback to
    for i, row in user_feedback_df.iterrows():
        image_id = row['image_id']
        attributes = kitchen_attributes[image_id]
        for attribute in attributes:
            user_dict[attribute] += row['feedback']
            image_count += 1
    return user_dict, image_count
