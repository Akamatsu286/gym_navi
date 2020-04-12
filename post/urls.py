from django.urls import path
from. import views

app_name = 'post'
urlpatterns = [
    path('index/', views.postindex.as_view(), name='index'),
    path('<int:pk>/',views.postdetail.as_view(),name='detail'),
    path('create/',views.postcreate.as_view(),name='create'),
    path('<int:pk>/update',views.postupdate.as_view(),name='update')
]