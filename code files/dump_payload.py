import json

payload = {
    "source": "universal",
    "url": "https://www.imdb.com/chart/top/?ref_=nv_mv_250",
    "parse": True,
    "parsing_instructions": {
        "movies": {
            "_fns": [
                {
                    "_fn": "xpath",
                    "_args": [
                        "//li[contains(@class,'ipc-metadata-list-summary-item')]"
                    ]
                }
            ],
            "_items": {
                "movie_name": {
                    "_fns": [
                        {
                            "_fn": "xpath_one",
                            "_args": [
                                ".//h3/text()"
                            ]
                        }
                    ]
                },
                "year":{
                    "_fns": [
                        {
                            "_fn": "xpath_one",
                            "_args": [
                                ".//*[contains(@class,'cli-title-metadata-item')]/text()"
                            ]
                        }
                    ]
                },
                "rating": {
                    "_fns": [
                        {
                            "_fn": "xpath_one",
                            "_args": [
                                ".//*[contains(@aria-label,'IMDb rating')]/text()"
                            ]
                        }
                    ]
                }
            }
        }
    }
}

with open("top_250_payload.json", 'w') as f:
    json.dump(payload, f, indent=4)
