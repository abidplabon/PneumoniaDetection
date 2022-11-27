# import numpy as np
# from PIL import Image
# from sklearn.preprocessing import LabelEncoder
# from tensorflow.keras.models import load_model


# def getPrediction(filename):
    
#     classes = ["Normal", "Lung Opacity"]
#     le = LabelEncoder()
#     le.fit(classes)
#     le.inverse_transform([2])
    
    
#     #Load model
#     my_model=load_model("model/HAM10000_100epochs.h5")
    
#     SIZE = 32 #Resize to same size as training images
#     img_path = 'static/images/'+filename
#     img = np.asarray(Image.open(img_path).resize((SIZE,SIZE)))
    
#     img = img/255.      #Scale pixel values
    
#     img = np.expand_dims(img, axis=0)  #Get it tready as input to the network       
    
#     pred = my_model.predict(img) #Predict                    
    
#     #Convert prediction to class name
#     pred_class = le.inverse_transform([np.argmax(pred)])[0]
#     print("Diagnosis is:", pred_class)
#     return pred_class







# from fastapi import FastAPI, File, UploadFile
# from fastapi.middleware.cors import CORSMiddleware
# import uvicorn
# import numpy as np
# from io import BytesIO
# from PIL import Image
# import tensorflow as tf
# import requests
# from tensorflow.keras.models import load_model
# import asyncio
# from flask import Flask,request







# app = FastAPI()

# origins = [
#     "http://localhost",
#     "http://localhost:3000",
# ]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# endpoint = "http://localhost:8601/v1/models/pneumonia_model:predict"

# CLASS_NAMES = ["Normal", "Lung Opacity"]

# @app.get("/ping")
# async def ping():
#     return "Hello, I am alive"

# def read_file_as_image(data) -> np.ndarray:
#     image = np.array(Image.open(BytesIO(data)))
#     return image

# @app.post("/predict")
# async def getPrediction(
#     file: UploadFile = File(...)
# ):
    
#     # print(request.files.getlist("file"))
#     # SIZE=32
#     # file = request.files['file']
#     # img_path = 'static/images/'+file
#     # img = np.asarray(Image.open(img_path).resize((SIZE,SIZE)))
#     image = read_file_as_image(file)
#     img_batch = np.expand_dims(image, 0)

#     json_data = {
#         "instances": img_batch.tolist()
#     }

#     response =requests.post(endpoint, json=json_data)
#     print(response)
#     prediction = np.array(response.json()["predictions"][0])

#     predicted_class = CLASS_NAMES[np.argmax(prediction)]
#     print(predicted_class)
#     confidence = np.max(prediction)

#     # return {
#     #     "class": predicted_class,
#     #     "confidence": float(confidence)
#     # }
#     return predicted_class
# if __name__ == "__main__":
#     uvicorn.run(app, host='localhost', port=8000)

# app = FastAPI()

# origins = [
#     "http://localhost",
#     "http://localhost:3000",
# ]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# endpoint = "http://localhost:8601/v1/models/pneumonia_model:predict"
# #endpoint=load_model("model/HAM10000_100epochs.h5")

# CLASS_NAMES = ["Normal", "Lung Opacity"]

# # @app.get("/ping")
# # async def ping():
# #     return "Hello, I am alive"

# def read_file_as_image(data) -> np.ndarray:
#     image = np.array(Image.open(BytesIO(data)))
#     return image

# # @app.post("/predict")
# async def predict(
#     filename: UploadFile = File(...)
# ):
#     image = read_file_as_image(await filename.read())
#     img_batch = np.expand_dims(image, 0)

#     json_data = {
#         "instances": img_batch.tolist()
#     }

#     response = requests.post(endpoint, json=json_data)
#     prediction = np.array(response.json()["predictions"][0])

#     predicted_class = CLASS_NAMES[np.argmax(prediction)]
#     confidence = np.max(prediction)

#     return predicted_class
import io
import numpy as np
from PIL import Image
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import load_model
from torchvision import transforms


def getPrediction(filename):
    
    classes = ['Normal', 'Lung Opacity']
    
    #Load model
    my_model=load_model("model/densenet_balanced.h5")
    
    SIZE = 32 #Resize to same size as training images
    img_path = 'static/images/'+filename                
    
    #Convert prediction to class name
    pred = test(img_path)
    pred_class = classes[np.argmax(pred)]
    
    print("Diagnosis is:", pred_class)
    return pred_class


from PIL import Image
import numpy as np
from skimage import transform
from keras.models import load_model
# # in_path="C:\\Users\\User\\Downloads\\Compressed\\CHEST_PA_2577.dcm"
# # image_path="C:\\Users\\User\\Downloads\\Compressed\\CHEST_PA_2577.dcm"
try:
    # keras 2.2
    import keras_preprocessing.image.utils as KPImageUtils
    import keras_preprocessing.image as KPImage
except:
    # keras 2.1
    import keras.preprocessing.image as KPImage
    
#from PIL import Image
import pydicom #pydicom==1.2.0

def read_dicom_image(in_path):
    img_arr = pydicom.read_file(in_path).pixel_array
    return img_arr/img_arr.max()
    
class medical_pil():
    @staticmethod
    def open(in_path):
        if '.dcm' in in_path:
            c_slice = read_dicom_image(in_path)
            int_slice =  (255*c_slice).clip(0, 255).astype(np.uint8) # 8bit images are more friendly
            return Image.fromarray(int_slice)
        else:
            return Image.open(in_path)
    fromarray = Image.fromarray
    
KPImageUtils.pil_image = medical_pil
  

def load(filename):
   if '.dcm' in filename:
     np_image = KPImageUtils.pil_image.open(filename)
   else:
     np_image = Image.open(filename)
   np_image = np.array(np_image).astype('float32')/255
   np_image = transform.resize(np_image, (224, 224, 3))
   np_image = np.expand_dims(np_image, axis=0)
   return np_image

def test(image_path):
  #output pred_score returns an array like this [[9.256325e-08, 0.9999999]] where the first value 0 (not pneumonia), second value is 1 (pneumonia)
  #load model
   model_path ="model/densenet_balanced.h5"
   model = load_model(model_path)
   image = load(image_path)
   pred_score = model.predict(image)
   print("****************************************")
   print(pred_score)
   print("****************************************")
   return pred_score
