"""apitest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import include, url
from slip.views import *


urlpatterns = [
   # API
    #url(r'^$', select_data1, name='select_data1'),
    url(r'^$', basic_view, name='basic'),
    url(r'^(?P<from_date>\d+)~(?P<to_date>\d+)/$', basic_view, name='select_data'),
    url(r'^cashbalnce/from_date/(?P<from_date>\d+)/to_date/(?P<to_date>\d+)/$', cash_balnce, name='select_cash'),
    url(r'^from_date/(?P<from_date>\d+)/to_date/(?P<to_date>\d+)/$', basic_view, name='select_data'),
    url(r'^(?P<question_id>\d+)/$', detail_data1, name='detail_data'),
    #url(r'^insert_data', insert_data, name='inset_data'),
    #url(r'^delete_data', delete_data, name='delete_data'),
    #url(r'^update_data', update_data, name='update_data'),
    #url(r'^slip/', include('slip.urls')),
    #url(r'^trade/', include('trade.urls')),
]
