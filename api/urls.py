from home.views import person,index,PersonAPI,PersonViewSet,RegisterAPI,LoginAPI,CompanyViewSet,EmployeeViewSet
from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"people", PersonViewSet, basename="user")
router.register(r"company", CompanyViewSet)
router.register(r"employee", EmployeeViewSet)
urlpatterns = router.urls

urlpatterns = [
    path("", include(router.urls)),
    path("register/", RegisterAPI.as_view()),
    path("login/", LoginAPI.as_view()),
    path("index/",index),
    path("person/",person),
    path("persons/", PersonAPI.as_view())
]
