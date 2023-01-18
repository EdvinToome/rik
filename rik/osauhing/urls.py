from django.urls import path

from . import views

urlpatterns = [
    path('', views.OsauhingList.as_view(), name='osauhing_list'),
    path('view/<int:pk>', views.OsauhingView.as_view(), name='osauhing_view'),
    path('new', views.OsauhingCreate.as_view(), name='osauhing_new'),
    path('view/<int:pk>', views.OsauhingView.as_view(), name='osauhing_view'),
    path('edit/<int:pk>', views.OsauhingUpdate.as_view(), name='osauhing_edit'),
    path('delete/<int:pk>', views.OsauhingDelete.as_view(), name='osauhing_delete'),
]
