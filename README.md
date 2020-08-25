# image_segmentation
Semantic segmentation can be done using a model pre-trained on images labeled using predefined list of categories. An example in this sense is the DeepLabV3 model, which is already implemented in PyTorch.

How can we serve such a model in an app with a streamlit frontend and a FastAPI backend?

One possibility is to have two services deployed in two Docker containers, orchestrated with docker-compose:
