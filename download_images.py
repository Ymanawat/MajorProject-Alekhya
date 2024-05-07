import requests
import os

UNSPLASH_ROOT = 'https://api.unsplash.com'

async def get_photos_by_query(query, per_page=2, download_dir='assets/videos'):
    url = f"{UNSPLASH_ROOT}/search/photos"
    params = {
        "query": query,
        "per_page": per_page,
        "client_id": 'FzXQznA_wzwaGrmyP75eGceTjTWqE1qSZJyMqjbcfJc'
    }
    response = await requests.get(url, params=params)

    print('download_image', response)
    data = response.json()

    print(data)

    for i, photo in enumerate(data["results"]):
        image_url = photo["urls"]["regular"]
        image_response = requests.get(image_url)
        image_data = image_response.content
        with open(os.path.join(download_dir, f"{query}_{i+1}.jpg"), "wb") as f:
            f.write(image_data)
            print(f"Downloaded image {i+1}")

    return data

# Example usage
query = "lion"
# data = get_photos_by_query(query)
# print(data)
