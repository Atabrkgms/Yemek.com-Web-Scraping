import requests
import pandas as pd
import firebase_admin
from firebase_admin import credentials , firestore

cred = credentials.Certificate("your_firebase_json_key")
app = firebase_admin.initialize_app(cred)
db = firestore.client()

url = "https://zagorapi.yemek.com/search/recipe" #API URL

res = []

for x in range(10,100):#Page numbers for the recipes

    querystring = {"Start":f"{x}","Rows":"100"}

    headers = {
    "cookie": "__cf_bm=J4CepJ1U.cj3eivpAmUi5eIgI.tfN8cKPLCSUHK9C0A-1699453039-0-AVODtiOe4a%2F4pQ6QXld7wPaWJrzNdttwjZDzRdsdwvfqkpLYQmYqQuzAc5tfSZHawBoDcEFH2drbnGD%2FaIJbwv4%3D",
    "authority": "zagorapi.yemek.com",
    "accept": "application/json, text/plain, */*",
    "accept-language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7,fr;q=0.6",
    "origin": "https://yemek.com",
    "referer": "https://yemek.com/",
    "sec-ch-ua": "Google Chrome;v=119, Chromium;v=119, Not?A_Brand;v=24",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "macOS",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    data = response.json()

    for p in data['Data']['Posts']:
        res.append(p)

titles = []
recipe_ingredient = []
recipe_instruction = []


for p in res:
    title_customized = p.get('TitleCustomized')
    recipe_order_time = p.get('RecipeOrderTimeText')
    recipe_ingredient = p.get('RecipeIngredient')
    recipe_instruction = p.get('RecipeInstruction')
    label = p.get('Label')
    recipe_category = p.get('RecipeCategory')
    image_orj = p.get('FeaturedImage.MediaData.ymk-original.Path')

    data = {
        "title": title_customized,
        "orderTime": recipe_order_time,
        "ingredient": recipe_ingredient,
        "instruction": recipe_instruction,
        "label": label,
        "category": recipe_category,
        "imageUrl": image_orj,
        }
    
    collection_ref = db.collection("Recipes")
    #Adding to firebase collection
    collection_ref.add(data)
    




#Export to csv
df = pd.json_normalize(res)
df.to_csv('firstResults.csv')



