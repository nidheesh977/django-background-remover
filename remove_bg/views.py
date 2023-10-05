from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from rembg import remove
from .models import Image
from django.core.files.base import ContentFile
import PIL
from io import BytesIO, StringIO  

# Create your views here.

class TestView(View):
  def get(self, request):
    return render(request, "remove_bg/index.html")
  
  def post(self, request):
    print(request.FILES)
    image = request.FILES["image"]
    img = PIL.Image.open(image)
    img_data = remove(img)
    img_bytes = BytesIO()
    img_data.save(img_bytes, format = "PNG")
    img_byte_arr = img_bytes.getvalue()
    image_obj = Image.objects.create(img = image)
    image_obj.rmbg_img.save(f'background_removed.png', ContentFile(img_byte_arr), save=False)
    image_obj.save()
    return redirect("/download/")
  
class DownloadImages(View):
  def get(self, request):
    images = Image.objects.all()
    return render(request, "remove_bg/download_img.html", context = {"images": images})