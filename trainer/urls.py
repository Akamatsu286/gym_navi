from django.urls import path
from. import views

app_name = 'trainer'

urlpatterns = [
    path('', views.Top.as_view(), name='top'),
    path('login/', views.Trainer_login.as_view(), name='login'),
    path('logout/', views.Trainer_logout.as_view(), name='logout'),
    path('trainer_create/', views.TrainerCreate.as_view(), name='trainer_create'),
    path('trainer_create/done', views.TrainerCreateDone.as_view(),
         name='trainer_create_done'),
    path('trainer_create/complete/<token>/',
         views.TrainerCreateComplete.as_view(), name='trainer_create_complete'),
    path('trainer_detail/<int:pk>/',
         views.TrainerDetail.as_view(), name='trainer_detail'),
    path('trainer_update/<int:pk>/',
         views.TrainerUpdate.as_view(), name='trainer_update'),

    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDone.as_view(),
         name='password_change_done'),
    path('password_reset/', views.PasswordReset.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDone.as_view(),
         name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/',
         views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', views.PasswordResetComplete.as_view(),
         name='password_reset_complete'),

    path('email/change/', views.EmailChange.as_view(), name='email_change'),
    path('email/change/done/', views.EmailChangeDone.as_view(),
         name='email_change_done'),
    path('email/change/complete/<str:token>/',
         views.EmailChangeComplete.as_view(), name='email_change_complete'),
    path('mypage/<int:pk>/', views.MyPageWithPk.as_view(), name='my_page_with_pk'),
]
