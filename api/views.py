from rest_framework.generics import ListAPIView, RetrieveAPIView

from myapp.models import Post
from .serializers import PostSerializer


# Create your views here.

class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostRetrieveAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer