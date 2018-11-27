"""EasyTest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import url
from base.views import *

urlpatterns = [

    url(r'/project/', project_index),
    url(r'/project_add/', project_add),
    url(r'/project_update/', project_update),
    url(r'/project_delete/', project_delete),

    url(r'/sign/', sign_index),
    url(r'/sign_add/', sign_add),
    url(r'/sign_update/', sign_update),

    url(r'/env/', env_index),
    url(r'/env_add/', env_add),
    url(r'/env_update/', env_update),
    url(r'/env_delete/', env_delete),

    url(r'/interface/', interface_index),
    url(r'/interface_add/', interface_add),

    url(r'/case/', case_index),
    url(r'/case_add/', case_add),
    url(r'/case_run/', case_run),

    url(r'/plan/', plan_index),
    url(r'/plan_add/', plan_add),
    url(r'/plan_run/', plan_run),

    url(r'/report/', report_index),

    url(r'/findata/', findata),

    url(r'/person/', ClientTypeData.person_index),
    url(r'/person_add/', ClientTypeData.person_add),
    url(r'/person_detail/', ClientTypeData.person_detail),
    url(r'/person_delete/', ClientTypeData.person_delete),
    url(r'/organ/', ClientTypeData.organ_index),
    url(r'/organ_add/', ClientTypeData.organ_add),
    url(r'/organ_detail/', ClientTypeData.organ_detail),
    url(r'/organ_delete/', ClientTypeData.organ_delete),
    url(r'/specialorgan/', ClientTypeData.specialorgan_index),
    url(r'/specialorgan_add/', ClientTypeData.specialorgan_add),
    url(r'/specialorgan_detail/', ClientTypeData.specialorgan_detail),
    url(r'/specialorgan_delete/', ClientTypeData.specialorgan_delete),
    url(r'/asset/', ClientTypeData.asset_index),
    url(r'/asset_add/', ClientTypeData.asset_add),
    url(r'/asset_detail/', ClientTypeData.asset_detail),
    url(r'/asset_delete/', ClientTypeData.asset_delete),

    url(r'download_file', ClientTypeData.download_file),
]

