from PIL import Image
import numpy as np
import requests
from io import BytesIO
import json

#preProcessing Fn
def preProcess(data):
    # Read the PNG image recived from the post request
    image = Image.open(data)

    # Resize the image to 28x28 using bilinear interpolation
    resized_image = image.resize((28, 28), Image.BILINEAR)

    # Convert the image to a NumPy array
    image_array = np.array(resized_image)

    # Calculate grayscale manually
    gray_array = np.mean(image_array, axis=-1, keepdims=True).astype(np.uint8)
    gray_array = gray_array.reshape(28,28,1)

    # Finally change the reshape
    return gray_array.reshape((1,28,28,1))

def lambda_handler(event, context):
    #get the image from s3
    data = requests.get(event['img_url'])
    data.raise_for_status()  # Check for HTTP errors

    #do pre processing
    result_array = preProcess(BytesIO(data.content))

    #send to back to the UI
    return {
        'statusCode': 200,
        'body': json.dumps({'Pre Processed Image': result_array.tolist()})
    }