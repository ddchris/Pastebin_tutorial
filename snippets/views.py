from .models import Snippet
from .serializers import SnippetSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework import permissions

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from .serializers import SnippetSerializer, UserSerializer
from rest_framework import renderers




'''
ViewSet 為我們提供了默認的 URL 結構, 使得我們能更專注於 API 本身. ViewSet類與 View 類幾乎是相同的
, 但提供的是 read 或 update, 而不是 http 動作 get 或 put .
ViewSet 類在實例化後, 通過Router類, 最終將URL與ViewSet方法綁定. 
'''

from rest_framework import viewsets

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

# 使用 Viewset 取代以下 2 classes:
'''
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
'''

'''
使用 ModelViewSet 類實現讀寫操作 API. 我們使用了 @detail_route 修飾器來創建自定義的 highlight 動作
, 這一修飾器可以用於創建非標準路徑. @detail_route 修飾器對應的是 GET, 如果想對應 POST,
可以使用 @detail_route 的 method 參數.
'''

from rest_framework.decorators import detail_route
from rest_framework.response import Response

class SnippetViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet 提供了 `list`, `create`, `retrieve`,
    `update` and `destroy` 等動作.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# 取代以下3個 classes
"""
'''
由於我們返回的並不是一個 object 實例, 而是一個實例的某個屬性, DRF 沒有提供該 GCVB.
因此我們需要使用基本的 view, 並創建 get() 方法:
'''
from rest_framework import renderers

class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)


'''
同 Django, DRF 為我們提供了現成的 generic CVB.
接下來我們使用這些 GCBVs 再一次修改原有的 views.py :
可以發現, 使用GCBVs後, 代碼變得的更為精簡易懂.
'''

class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permissions_class = permissions.IsAuthenticatedOrReadOnly

    def perform_create(self, serializer):
       serializer.save(owner=self.request.user)
    '''
    複寫 create() 使得 Snippet 跟 User 關聯話
    The user isn't sent as part of the serialized representation, but is instead a property of 
    the incoming request.
    '''


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                      IsOwnerOrReadOnly,)
"""
# ________________________________________________________



"""
@api_view(['GET'])
def api_root(request, format=None):
    '''
    "format" 參數用來定義 response 格式, 例如: csv, json 等等
    '''

    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })
"""

'''
使用 CBV 的一大好處是, 我們可以使用各種 mixin.
DRF 為我們提供了許多現成的 mixins, 方便我們像使用 model-backed API一樣構建 "CRUD" API.
'''

'''
class SnippetList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SnippetDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
'''