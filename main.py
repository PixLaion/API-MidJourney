import requests
import json
import time
import requests
from datetime import datetime
from PIL import Image

with open('apikey.txt', 'r') as f:
    API_KEY = f.read().strip()

headers = {
    "X-API-KEY": API_KEY
}

def generateMJImage(prompt="") : 
    
    try:
        data = {
            "prompt": prompt,
            "process_mode": "fast"
        }

        response = requests.post("https://api.midjourneyapi.xyz/mj/v2/imagine", headers=headers, data=json.dumps(data))
        print(response.json())
        fns = fetchImage(response.json()['task_id'], prompt)
        return fns
    except Exception as e:
        print("error")
        return []


def fetchImage(taskId, prompt):
    fileNames = []
    while True:
        # Send a GET request to ID URL
        time.sleep(4)

        fetchUrl = "https://api.midjourneyapi.xyz/mj/v2/fetch"

        data = {
            "task_id": taskId
        }
        response = requests.post(fetchUrl, data=json.dumps(data))
        print(response.json()['status'])

        # # Check if the request was successful
        res = response.json()
        if response.status_code == 200:
            if res['status'] == "finished" :

                urls = saveImage(res['task_result']['image_url'])
                # url = downloadImage(taskId, 1, prompt)
                fileNames = urls
                break
            elif res['status'] == "failed" :
                break
        else:
            print(f"Failed to retrieve image. Status code: {response.status_code}")
            break


    return fileNames

def downloadImage(taskId):
    while True:
        url = "https://api.midjourneyapi.xyz/mj/v2/fetch"
        data = {
            "task_id": taskId
        }

        res = requests.post(url, data=json.dumps(data))
        result = res.json()
        print(result['status'])
        if result['status'] == "finished":
            print(result['task_result'])
            files = saveImage(result['task_result']['image_url'])

            return files
            # break
        elif result['status'] == "failed":
            return []
        
        time.sleep(4)
            

def saveImage(url, timestamp = datetime.now().strftime("%Y%m%d%H%M%S")):
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        with open(f"generated/{timestamp}.png", "wb") as file:
            file.write(res.content)
        
        urls = splitImage(f"generated/{timestamp}.png")
        return urls
    return []

def splitImage(url):
    urls = []
    img = Image.open(url)  # Replace with your image path

    # Calculate the width and height of each split
    width, height = img.size
    split_width = width // 2
    split_height = height // 2

    # Split the image into 2x2 grid
    top_left = img.crop((0, 0, split_width, split_height))
    top_right = img.crop((split_width, 0, width, split_height))
    bottom_left = img.crop((0, split_height, split_width, height))
    bottom_right = img.crop((split_width, split_height, width, height))

    # Save each of the split images
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    top_left.save(f"generated/{timestamp}_1.png")
    top_right.save(f"generated/{timestamp}_2.png")
    bottom_left.save(f"generated/{timestamp}_3.png")
    bottom_right.save(f"generated/{timestamp}_4.png")

    urls.append(f"generated/{timestamp}_1.png")
    urls.append(f"generated/{timestamp}_2.png")
    urls.append(f"generated/{timestamp}_3.png")
    urls.append(f"generated/{timestamp}_4.png")

    return urls

urls = generateMJImage(
    prompt="Create a digital painting of a serene and mystical forest at twilight. The forest is illuminated by the soft glow of fireflies, with ancient trees towering into the sky. Their trunks are twisted and covered in luminous moss and delicate ivy. A gentle stream meanders through the forest, reflecting the last rays of the setting sun. In the background, a quaint wooden cabin with a thatched roof emits a warm light from its windows, suggesting a cozy refuge in the heart of the woods. The sky above is a gradient of deep indigo and violet, with the first stars of the night beginning to twinkle. A majestic owl is perched on a gnarled branch, surveying the enchanting scene.")

print(urls)
