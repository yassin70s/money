from django_api_admin.options import APIModelAdmin
from django_api_admin.sites import APIAdminSite
from .admin import AdminSite
from django.urls import path,reverse
from django.utils.html import format_html
from django.utils.timezone import datetime
from django.http.response import JsonResponse
from django_api_admin.views.admin_views import ChangeListView as _ChangeListView




class ChangeListView(_ChangeListView):
    pass

class ModelApi(APIModelAdmin):
    inlines = []
    def changelist_view(self, request, **kwargs):
        defaults = {
            'permission_classes': self.admin_site.default_permission_classes
        }
        return ChangeListView.as_view(**defaults)(request,self)

class Site(APIAdminSite,AdminSite):
    def get_urls(self):
        
        
        my_urls = [
            path("login/",self.api_admin_view(self.login),name="login"),
           # path("register_user/",self.api_admin_view(self.register_user),name="register_user"),
           

        ]
        return my_urls + super().get_urls()


site = Site(name="api")