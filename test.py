import json

with open('fresh_baked_access_token.json') as f:
    bearer = json.load(f)

print(bearer)