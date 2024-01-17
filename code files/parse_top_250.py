import requests
import json

payload = {}
with open("top_250_payload.json") as f:
    payload = json.load(f)

response = requests.post(
    url="https://realtime.oxylabs.io/v1/queries",
    json=payload,
    auth=('username', 'password'),
)

print(response.status_code)


with open("result.json", "w") as f:
    json.dump(response.json(),f, indent=4)
