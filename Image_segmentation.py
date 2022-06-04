import streamlit as st
from requests_toolbelt.multipart.encoder import MultipartEncoder
import requests
from PIL import Image
import io

st.title('DeepLabV3 image segmentation')

# fastapi endpoint
url = 'http://fastapi:8000'
endpoint = '/segmentation'

st.write('''Obtain semantic segmentation maps of the image in input via DeepLabV3 implemented in PyTorch.
         This streamlit example uses a FastAPI service as backend.
         Visit this URL at `:8000/docs` for FastAPI documentation.''') # description and instructions

image = st.file_uploader('insert image')  # image upload widget


def process(image, server_url: str):

    m = MultipartEncoder(
        fields={'file': ('filename', image, 'image/jpeg')}
        )

    r = requests.post(server_url,
                      data=m,
                      headers={'Content-Type': m.content_type},
                      timeout=8000)

    return r



if st.button('Get segmentation map'):

    if image == None:
        st.write("Insert an image!")  # handle case with no image
    else:
        segments = process(image, url+endpoint)
        segmented_image = Image.open(io.BytesIO(segments.content)).convert('RGB')
        st.image([image, segmented_image], width=300)  # output dyptich

from fastapi import FastAPI, File
from starlette.responses import Response
import io
from segmentation import get_segmentator, get_segments

model = get_segmentator()

app = FastAPI(title="DeepLabV3 image segmentation",
              description='''Obtain semantic segmentation maps of the image in input via DeepLabV3 implemented in PyTorch.
                           Visit this URL at port 8501 for the streamlit interface.''',
              version="0.1.0",
              )


@app.post("/segmentation")
def get_segmentation_map(file: bytes = File(...)):
    '''Get segmentation maps from image file'''
    segmented_image = get_segments(model, file)
    bytes_io = io.BytesIO()
    segmented_image.save(bytes_io, format='PNG')
    return Response(bytes_io.getvalue
