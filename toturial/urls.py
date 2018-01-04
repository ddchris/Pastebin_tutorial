from django.contrib import admin
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from snippets import views
from rest_framework.schemas import get_schema_view
 
schema_view = get_schema_view(title='Pastebin API')
urlpatterns = [
    url(r'^schema/$', schema_view),
]
'''
http http://127.0.0.1:8000/schema/ Accept:application/coreapi+json
HTTP/1.0 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/coreapi+json
'''



# Create a router and register our viewsets with it.
router = DefaultRouter()
'''
DefaultRouter automatically creates the API root view for us, so we can now delete the api_root method from our views module.
'''

router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)

# The API URLs are now determined automatically by the router.
'''
router會自動生成 url, 我們只需要額外提供可瀏覽性登入 API
'''
urlpatterns += [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls))
]

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls')),
]

"""
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from toturial.snippets import views
from toturial.snippets.views import SnippetViewSet, UserViewSet, api_root
from rest_framework import renderers

'''
將 HTTP 動作與 Viewset 內方法連結起來, 再放入 URLs,
使 URLs 更加淺顯易懂: bound  Resources into Views,
'''

snippet_list = SnippetViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
snippet_detail = SnippetViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
snippet_highlight = SnippetViewSet.as_view({
    'get': 'highlight'
}, renderer_classes=[renderers.StaticHTMLRenderer])
user_list = UserViewSet.as_view({
    'get': 'list'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})

urlpatterns = format_suffix_patterns([
    url(r'^$', api_root),
    url(r'^snippets/$', snippet_list, name='snippet-list'),
    url(r'^snippets/(?P<pk>[0-9]+)/$', snippet_detail, name='snippet-detail'),
    url(r'^snippets/(?P<pk>[0-9]+)/highlight/$', snippet_highlight, name='snippet-highlight'),
    url(r'^users/$', user_list, name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', user_detail, name='user-detail')
])
"""

"""
# API endpoints
urlpatterns = format_suffix_patterns([
    url(r'^$', views.api_root),
    url(r'^snippets/$',
        views.SnippetList.as_view(),
        name='snippet-list'),
    url(r'^snippets/(?P<pk>[0-9]+)/$',
        views.SnippetDetail.as_view(),
        name='snippet-detail'),
    url(r'^snippets/(?P<pk>[0-9]+)/highlight/$',
        views.SnippetHighlight.as_view(),
        name='snippet-highlight'),
    url(r'^users/$',
        views.UserList.as_view(),
        name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$',
        views.UserDetail.as_view(),
        name='user-detail')
])

'''
使用 += 合併串列(同 extend())
幫瀏覽器介面 API 設定登入
'''
urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls')),
]
"""

"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^snippets/$', views.SnippetList.as_view()),
    url(r'^snippets/(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view()),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),

]

'''
使用 += 合併串列(同 extend())
幫瀏覽器介面 API 設定登入
'''
urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls')),
]

urlpatterns += [
    url(r'^$', views.api_root),
    url(r'^snippets/(?P<pk>[0-9]+)/highlight/$', views.SnippetHighlight.as_view()),
]


urlpatterns = format_suffix_patterns(urlpatterns)
"""


