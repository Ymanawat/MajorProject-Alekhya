import requests, json
import os

# Define function to save images
def save_images(query: str, data: list):
    # Create directory if it doesn't exist
    directory = f"assets/videos/{query}"
    os.makedirs(directory, exist_ok=True)
    
    # Iterate through the data and save images
    for index, item in enumerate(data):
        image_url = item['image_url']
        response = requests.get(image_url)
        if response.status_code == 200:
            # Get the file extension from the URL
            file_extension = image_url.split('.')[-1]
            # Generate filename
            filename = f"{query}_{index}.{file_extension}"
            filepath = os.path.join(directory, filename)
            # Save the image
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print(f"Image {index+1}/{len(data)} saved as {filename}")
        else:
            print(f"Failed to download image {index+1}")

def image_search(query: str): # Change this line
    # Check if query is valid
    if not query:
        return {"error": "Please provide a query parameter"}
    # Construct GET request to Custom Search JSON API
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": "AIzaSyCsWAb0PSkUA_hdU8BHwcw_RwxtrBPo2tY",
        "cx": "60e8c83068bc84aeb",
        "q": query, # Query parameter from user
        "searchType": "image",
        "num": 2
    }
    response = requests.get(url, params=params)
    # Check if response is valid
    if response.status_code != 200:
        return {"error": response.json().get("error")}
    # Parse JSON response and extract relevant information
    data = response.json()
    items = data.get("items")
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
    
    # Return results as JSON object
    return {"results": results}

# image_search("lion")