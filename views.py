from datetime import datetime

from django.contrib import messages
from django.http import *
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache, cache_control
from django.views.decorators.csrf import csrf_protect
from app.forms import ImageTestForm
from app.models import CleanImage, MessyImage, NotcrImage, CleanValidateImage, NotcrValidateImage, MessyValidateImage, \
    TestImage
from messy_or_not_train_model import train_conf_model
import messy_or_not_train_model as tr
from djangoapp import settings
import MessyOrNot_run as mor
import time
import json
from django.http.response import JsonResponse

media_path = settings.MEDIA_ROOT

@csrf_protect
def user_login(request):
    return render(request, 'app/test_wireframe.html')

@csrf_protect
def user_login(request):
    # TODO
    trainer_role = 'train'
    trainer_pwd = 'Im$gescnn8957'
    test_role = 'test'
    test_pwd = 'Im$gescnn8957'

    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        if username.lower() == trainer_role and password == trainer_pwd:
            return render(request, 'app/train_wireframe.html')
        elif username.lower() == test_role and password == test_pwd:
            return render(request, 'app/test_wireframe.html')
        elif username.lower() == 'admin' and password == test_pwd:
            return render(request, 'app/test_wireframe.html')
        else:
            messages.error(request, 'Login failed: Invalid username or password.')
    return render(request, 'app/login.html')

@csrf_protect
def login(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/login.html',
        {
            'title': 'Home Page',
            'year': datetime.now().year,
        }
    )

@cache_control(no_cache=True, no_store=True)
@csrf_protect
def train_model(request):

    if request.method == 'POST':
        clean_file_list = request.FILES.getlist("clean_files")
        img_model = CleanImage()
        img_val_model = CleanValidateImage()
        save_images(clean_file_list, img_model, img_val_model)

        messy_file_list = request.FILES.getlist("messy_files")
        img_model = MessyImage()
        img_val_model = MessyValidateImage()
        save_images(messy_file_list, img_model, img_val_model)

        nocr_file_list = request.FILES.getlist("nocr_files")
        img_model = NotcrImage()
        img_val_model = NotcrValidateImage()
        save_images(nocr_file_list, img_model, img_val_model)

        if clean_file_list or messy_file_list or nocr_file_list:
            train_output = train_conf_model()
            print('Test-1', train_output)
            messages.error(request, 'Successfully uploaded image files and model will be trained, Thanks for upload.')
        if not clean_file_list and not messy_file_list and not nocr_file_list:
            messages.warning(request, 'Warning! Upload image file(s).')
    else:
        return render(request, 'app/login.html')

    return render(request, 'app/train_wireframe.html')

@cache_control(no_cache=True, no_store=True)
@csrf_protect
def test_model(request):
    if request.method == 'POST':
        radio_flag = request.POST.get('image_response_flag')
        image_response =  request.POST.get('image_response')
        if radio_flag:
            radio_flag_lower = radio_flag.lower()
            if image_response == "Right":
                print("radio_flag=",radio_flag)
                if "clean" in radio_flag_lower:
                    mor.move_files("/train/clean")
                elif "messy" in radio_flag_lower:
                    mor.move_files("/train/messy")
                else:
                    mor.move_files("/train/notcr")
                return render(request, 'app/right_wireframe.html', {'resp_right': 'Right'})
            elif image_response== "Wrong":
                return render(request, 'app/wrong_wireframe.html')
            else:
                # messages.warning(request, 'Warning! Choose Right or Wrong.')
                return render(request, 'app/test_wireframe.html')
        else:
            mor.delete_files()
            form = ImageTestForm(request.POST, request.FILES)
            if form.is_valid():
                test_file = request.FILES['test_image']
                img_model = TestImage()
                img_model.image = test_file
                img_model.save()
                # new object
                resp_img_model = TestImage()
                resp_img_model.image =  str(img_model.image)
                print("resp_img_model.image=",resp_img_model.image)
                mor.get_test_filename()
                #while not mor.get_test_filename():
                #    time.sleep(5)
                test_response = mor.messy_or_not()
                print('test_response=',test_response)
                if test_response:
                    image_tested = test_response
                    messages.success(request, image_tested)
                return render(request, 'app/test_wireframe.html', {'img_model': resp_img_model})
            else:
                messages.warning(request, 'Warning! Upload Test image file.')
    return render(request, 'app/test_wireframe.html')

@csrf_protect
def get_smarter(request):
    return redirect('test_model')

@csrf_protect
def add_classification(request):
    if request.method == 'POST':
        wr_image_response = request.POST.get('wr_image_response')
        if wr_image_response:
            print("wr_image_response=", wr_image_response)
            if wr_image_response == "Clean":
                mor.move_files("/train/clean")
            elif wr_image_response == "Messy":
                mor.move_files("/train/messy")
            elif wr_image_response == "NotCr":
                mor.move_files("/train/notcr")
        else:
            # messages.warning(request, 'Warning! Choose the right classification.')
            return render(request, 'app/wrong_wireframe.html')
        return render(request, 'app/right_wireframe.html')

def auto_train(request):
    responseData = {
        'Status': 'SUCCESS',
        'Code': '200',
        'Message': 'Training proecess triggered, thanks.'
    }
    if request.method == 'POST':
        rs = tr.auto_train_conf_model()
        print("train_conf_model response", rs)
        return JsonResponse(responseData)
    return JsonResponse(responseData)

def save_images(file_list, img_model, img_val_model):
    tot = len(file_list)
    pr = -1
    if tot > 10:
        pr = int(tot * .1)
    else:
        pr = 1
    for i in range(len(file_list)):
        filename = file_list[i]
        if i >= pr:
            img_model.image = filename
            img_model.save()
        else:
            img_val_model.image = filename
            img_val_model.save()
