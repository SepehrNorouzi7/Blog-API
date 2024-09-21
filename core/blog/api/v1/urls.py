from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("post", views.PostModelViewSet, basename="post")
router.register("category", views.CategoryModelViewSet, basename="category")
urlpatterns = router.urls

app_name = "api-v1"

# urlpatterns = [
#     # path('post/', views.postList,name='post-list'),
#     path('post/<int:id>/', views.postDetail, name='post-detail'),
# ]
