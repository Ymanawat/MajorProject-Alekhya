import requests, json
import os
import re

def save_images(query: str, data: list):
    # Clean up the query string
    clean_query = re.sub(r'[^\w\s]', '', query)
    
    # Create directory if it doesn't exist
    directory = f"assets/videos"
    os.makedirs(directory, exist_ok=True)
    
    # Iterate through the data and save images
    for index, item in enumerate(data):
        image_url = item['image_url']
        response = requests.get(image_url)
        if response.status_code == 200:
            # Extract filename from URL
            filename = re.sub(r'[^a-zA-Z0-9_.-]', '', os.path.basename(image_url))  # Remove special characters from filename
            filepath = os.path.join(directory, f"{query}_{index}.{filename.split('.')[-1]}")
            try:
                # Save the image
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                print(f"Image {index+1}/{len(data)} saved as {filename}")
            except:
                print(f"Error saving image {query}_{index}")
        else:
            print(f"Failed to download image {index+1}")

def image_search(query: str): # Change this line

    print ("search image : ", query)
    # Check if query is valid
    if not query:
        return {"error": "Please provide a query parameter"}
    
    # Construct GET request to Custom Search JSON API
    url = "https://www.googleapis.com/customsearch/v1/"
    # url = "https://cse.google.com/cse?cx=60e8c83068bc84aeb"
    
    params = {
        "key" : "AIzaSyBk1hnUgyo4mvymxCoOGh0OKB0Nbsh9I-4",
        "cx": "a11f34733f1f44863",
        "q": query, # Query parameter from user
        "searchType": "image",
        "num": 2
    }

    # params = {
    #     "key" : "AIzaSyCsWAb0PSkUA_hdU8BHwcw_RwxtrBPo2tY",
    #     # "key": "AIzaSyCsWAb0PSkUA_hdU8BHwcw_RwxtrBPo2tY",
    #     "cx": "60e8c83068bc84aeb",
    #     "q": query, # Query parameter from user
    #     "searchType": "image",
    #     "num": 2
    # }
    response = requests.get(url, params=params)
    # Check if response is valid
    if response.status_code != 200:
        return {"error": response.json().get("error")}
    # Parse JSON response and extract relevant information
    data = response.json()
    items = data.get("items", [])
    print(items)
    results = []
    for item in items:
        result = {
            "image_url": item.get("link"),
            "title": item.get("title"),
        }
        results.append(result)
        
    # Create a JSON output file from the results
    with open("results.json", "w") as outfile:
        json.dump(results, outfile)

    # Save images to directory
    save_images(query, results)
    print("google image result",results)
    
    # Return results as JSON object
    return {"results": results}

# image_search("lion")