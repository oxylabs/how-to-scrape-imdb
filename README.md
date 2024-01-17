# How to Scrape IMDb Data: Step-by-Step Guide
Learn how to easily scrape public IMDb data for your projects using Python and Oxylabs [IMDb Scraper API](https://oxylabs.io/products/scraper-api/web/imdb). Get your **1-week free trial** by registering on the [dashboard](https://dashboard.oxylabs.io/en/) and code your way to success.

See the complete [blog post](https://oxylabs.io/blog/how-to-scrape-imdb) for an in-depth tutorial with images.

- [1. Setting up for scraping IMDb](#1-setting-up-for-scraping-imdb)
  * [Creating a virtual environment](#creating-a-virtual-environment)
  * [Activating the virtual environment](#activating-the-virtual-environment)
  * [Installing required libraries](#installing-required-libraries)
- [2. Overview of IMDb Scraper API](#2-overview-of-imdb-scraper-api)
  * [Scraping a title](#scraping-a-title)
- [3. Scraping movie info from a list](#3-scraping-movie-info-from-a-list)
- [4. Scraping movie reviews](#4-scraping-movie-reviews)
- [5. Exporting to JSON and CSV](#5-exporting-to-json-and-csv)

## 1. Setting up for scraping IMDb
As you’ll be writing a Python script, make sure you have [Python](https://www.python.org/downloads/) 3.8 or newer installed on your machine.

### Creating a virtual environment
```bash
python -m venv imdb_env #Windows
python3 -m venv imdb_env #Mac and Linux
```
Replace `imdb_env` with the name you'd like to give to your virtual environment.

### Activating the virtual environment
```bash
.\imdb_env\Scripts\Activate #Windows
source imdb_env/bin/activate #Mac and Linux
```

### Installing required libraries
We'll use the `requests` library for this project to make HTTP requests. Install it by running the following command:

```bash
$ pip install requests pandas
```

## 2. Overview of IMDb Scraper API

Oxylabs' [IMDb Scraper API](https://oxylabs.io/products/scraper-api/web/imdb) allows you to extract data from many complex websites easily. Claim your **1-week free trial** by registering on the [Oxylabs dashboard](https://dashboard.oxylabs.io/en/) and follow along. Below you can see a basic example that shows how Scraper API works:

```python
# scraper_api_demo.py
import requests

USERNAME = "username"
PASSWORD = "password"

payload = {
    "source": "universal",
    "url": "https://www.imdb.com"
}

response = requests.post(
    url="https://realtime.oxylabs.io/v1/queries",
    json=payload,
    auth=(USERNAME,PASSWORD),
)

print(response.json())
```

### Scraping a title
The following code prints the title of the IMDb page:

```python
# imdb_title.py
import requests

USERNAME = "username"
PASSWORD = "password"

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
    auth=(USERNAME,PASSWORD),
)


print(response.json()['results'][0]['content'])
```

Learn more about the Custom Parser feature [here](https://developers.oxylabs.io/scraper-apis/custom-parser).

## 3. Scraping movie info from a list
Before scraping a page, we need to examine the page structure. See the steps on our [blog post](https://oxylabs.io/blog/how-to-scrape-imdb#3.-scraping-movie-info-from-a-list). We'll target this [IMDb top 250](https://www.imdb.com/chart/top/?ref_=nv_mv_250) listing page:
```python
# dump_payload.py
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
```
A good way to organize your code is to save the payload as a separator JSON file. It will allow you to keep your Python file short:

```python
# parse_top_250.py
import requests
import json

USERNAME = "username"
PASSWORD = "password"

payload = {}
with open("top_250_payload.json") as f:
    payload = json.load(f)


response = requests.post(
    url="https://realtime.oxylabs.io/v1/queries",
    json=payload,
    auth=(USERNAME, PASSWORD),
)


print(response.status_code)


with open("result.json", "w") as f:
    json.dump(response.json(),f, indent=4)
```
## 4. Scraping movie reviews
Let's scrape [movie reviews](https://www.imdb.com/title/tt0111161/reviews?ref_=tt_urv) of Shawshank Redemption:

```json
{
    "source": "universal",
    "url": "https://www.imdb.com/title/tt0111161/reviews?ref_=tt_urv",
    "parse": true,
    "parsing_instructions": {
        "movie_name": {
            "_fns": [
                {
                    "_fn": "css_one",
                    "_args": [
                        ".parent a"
                    ]
                },
                {
                    "_fn": "element_text"
                }
            ]
        },
        "reviews": {
            "_fns": [
                {
                    "_fn": "css",
                    "_args": [
                        ".imdb-user-review"
                    ]
                }
            ],
            "_items": {
                "review_title": {
                    "_fns": [
                        {
                            "_fn": "css_one",
                            "_args": [
                                ".title"
                            ]
                        },
                        {
                            "_fn": "element_text"
                        }
                    ]
                },
                "review-body": {
                    "_fns": [
                        {
                            "_fn": "css_one",
                            "_args": [
                                ".content>.show-more__control"
                            ]
                        },
                        {
                            "_fn": "element_text"
                        }
                    ]
                },
                "rating": {
                    "_fns": [
                        {
                            "_fn": "css_one",
                            "_args": [
                                ".rating-other-user-rating"
                            ]
                        },
                        {
                            "_fn": "element_text"
                        }
                    ]
                },
                "name": {
                    "_fns": [
                        {
                            "_fn": "css_one",
                            "_args": [
                                ".display-name-link a"
                            ]
                        },
                        {
                            "_fn": "element_text"
                        }
                    ]
                },
                "review_date": {
                    "_fns": [
                        {
                            "_fn": "css_one",
                            "_args": [
                                ".review-date"
                            ]
                        },
                        {
                            "_fn": "element_text"
                        }
                    ]
                }
            }
        }
    }
}
```
Once your payload file is ready, you can use the same Python code file shown in the previous section, point to this payload, and run the code to get the results.

## 5. Exporting to JSON and CSV

```python
# parse_reviews.py
# save results into a variable data
# save the data as a json file
with open("results_reviews.json", "w") as f:
json.dump(data, f, indent=4)
# save the reviews in a CSV file
df = pd.DataFrame(data['results'][0]['content']['reviews'])
df.to_csv('reviews.csv', index=False)
```
You might also be interested in reading up about scraping other targets such as [YouTube](https://oxylabs.io/blog/how-to-scrape-youtube), [Google News](https://oxylabs.io/blog/how-to-scrape-google-news), or [Netflix](https://oxylabs.io/products/scraper-api/web/netflix).




