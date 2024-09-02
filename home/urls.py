

from django.urls import path,include

from .views import BlogView,PublicBlogView

urlpatterns = [

  path('blogs/',BlogView.as_view()),
  path('pblogs/',PublicBlogView.as_view()),

]
