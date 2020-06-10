import json

lookup = 'airportlookup.json'

with open(lookup, "r") as read_file:
    data = json.load(read_file)

print(data)