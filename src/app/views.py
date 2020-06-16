from datetime import datetime

from django.contrib import messages
from django.http import *
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from app.forms import ImageTestForm
from app.models import CleanImage, MessyImage, NotcrImage, CleanValidateImage, NotcrValidateImage, MessyValidateImage, \
    TestImage
from messy_or_not_train_model import train_conf_model
from djangoapp import settings
import MessyOrNot_run as mor
import time

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
            if train_output == "Success":
                messages.success(request, 'Successfully uploaded image files and trained the model.')
            else:
                messages.error(request, 'Error! model training failed')
        if not clean_file_list and not messy_file_list and not nocr_file_list:
            messages.warning(request, 'Warning! Upload image file(s).')
    else:
        return render(request, 'app/login.html')

    return render(request, 'app/train_wireframe.html')


@csrf_protect
def test_model(request):
    if request.method == 'POST':
        mor.delete_files()
        form = ImageTestForm(request.POST, request.FILES)
        if form.is_valid():
            test_file = request.FILES['test_image']
            img_model = TestImage()
            img_model.image = test_file
            img_model.save()
            # new object
            resp_img_model = TestImage()
            resp_img_model.image = settings.BASE_DIR +  str(img_model.image)
            while not mor.get_test_filename():
                time.sleep(10)
            test_response = mor.messy_or_not()
            print('test_response=',test_response)
            if test_response:
                image_tested = 'The image uploaded was ' + test_response
                messages.success(request, image_tested)
            return render(request, 'app/test_wireframe.html', {'img_model': resp_img_model})
        else:
            messages.warning(request, 'Warning! Upload Test image file.')
    return render(request, 'app/test_wireframe.html')


def save_images(file_list, img_model, img_val_model):
    tot = len(file_list)
    pr = -1
    if tot > 0:
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

