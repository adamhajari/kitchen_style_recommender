import pandas as pd
import requests
# run this script once while the flask app is running after running create_db.py

BASE_URL = 'http://127.0.0.1:5000'

# read kitchen / style data from tsv
kitchens = pd.read_csv('sample_data/kitchen_style_kitchens.tsv', sep='\t').set_index('kitchen')

# convert to "long" format for storing in db
kitchens_long = kitchens.melt(var_name='attribute', ignore_index=False)

# write only "1"s to db
url = f'{BASE_URL}/attributes'
for i, row in kitchens_long.loc[kitchens_long['value']==1].iterrows():
    data = {'image_id': i, 'attribute': row['attribute']}
    r = requests.post(url, data)


# read kitchen / image preference data from tsv
users = pd.read_csv('sample_data/kitchen_style_users.tsv', sep='\t').set_index('user')

# convert to "long" format for storing in db
users_long = users.melt(var_name='image_id', value_name='feedback', ignore_index=False)

# write only "1"s to db
url = f'{BASE_URL}/feedback'
for i, row in users_long.loc[users_long['feedback']==1].iterrows():
    data = {'user_id': i, 'image_id': row['image_id'], 'feedback': row['feedback']}
    r = requests.post(url, data)
