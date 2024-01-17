import requests
payload = {
    "source": "universal",
    "url": "https://www.imdb.com",
    "parse": True,
    "parsing_instructions": {
        "title": {
            "_fns": [
                        {
                            "_fn": "xpath_one",
                            "_args": [
                                "//title/text()"
                                ]
                        }
                    ]
                }
    },
}

response = requests.post(
    url="https://realtime.oxylabs.io/v1/queries",
    json=payload,
    auth=('username', 'password'),
)

print(response.json()['results'][0]['content'])
