"""
Definition of urls for djangoapp.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views

import app.forms
import app.views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^$', app.views.login, name='login'),
    url('user_login', app.views.user_login, name='user_login'),
    url('train_model', app.views.train_model, name='train_model'),
    url('test_model', app.views.test_model, name='test_model'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
