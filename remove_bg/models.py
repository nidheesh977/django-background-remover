import requests
from io import BytesIO
from urllib.parse import urljoin
from rembg import remove
from django.core.files.base import ContentFile
from django.db import models
from django.conf import settings
import PIL
import numpy as np

class Image(models.Model):
    img = models.ImageField(upload_to="images")
    rmbg_img = models.ImageField(upload_to="images_rmbg", blank=True)
    is_downloaded = models.BooleanField(default = False)