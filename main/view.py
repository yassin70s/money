from main import admin
from django.urls import reverse,path
from django.http.response import HttpResponseRedirect,JsonResponse
from . import context_processors
class ModelView(admin.ModelAdmin):
    pass
        
class ViewSite(admin.AdminSite):
    site_menu = [
        {
            "name":"",
            "children":[
                {
                    "name":"",
                    "url":"",
                }
            ]
        }
        
    ]
    logout_template = "view/logout.html"
    site_title = "Almalik"
    site_header = "Almalik"
    index_title = "الرئيسية"
    def each_context(self, request):
        return dict(**{
            #"notice_change_list_api_url":reverse(f"api:almalik_noticeuser_changelist"),
            **super().each_context(request),

            "site_menu":self.site_menu,
        })
    def login(self, request, extra_context = None):
        extra_context = extra_context or {}

        is_login = True
        is_soon = True
        is_knowledge = True




        extra_context.update(
            is_login = is_login,
            is_soon = is_soon,
            is_knowledge = is_knowledge,

            #register_user_url = reverse("api:register_user"),
            login_api_url = reverse("api:login"),
            location_url = reverse("admin:index",current_app=self.name),
            

        )
        return super().login(request, extra_context)
    

site = ViewSite(name="view")






