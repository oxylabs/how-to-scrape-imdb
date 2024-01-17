import requests
import json
import pandas as pd

payload = {}
def get_reviews():
    with open("reviews_payload.json") as f:
        payload = json.load(f)

    response = requests.post(
        url="https://realtime.oxylabs.io/v1/queries",
        json=payload,
        auth=('username', 'password'),
    )

    print(response.status_code)

    return response.json()
def save(data):
    with open("results_reviews.json", "w") as f:
        json.dump(data, f, indent=4)
    df = pd.DataFrame(data['results'][0]['content']['reviews'])
    df.to_csv('reviews.csv', index=False)



if __name__ == '__main__':
    data = get_reviews()
    save(data)