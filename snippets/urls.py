from django.contrib import admin
from django.conf.urls import url,include
import views
 
'''
將 views 內方法串接至特定 url
'''
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^snippets/$', views.snippet_list),
    url(r'^snippets/(?P<pk>[0-9]+)/$', views.snippet_detail),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
]
 
'''
We can test our API using curl or httpie. Httpie is a user friendly http client that's written in Python:
'''
# http http://127.0.0.1:8000/snippets/
# http http://127.0.0.1:8000/snippets/2/



