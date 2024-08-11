
from collections import OrderedDict
from collections.abc import Callable, Sequence
from typing import Any
from django.contrib.admin import (
    ModelAdmin,TabularInline,StackedInline,AdminSite,site,register,display
)
from django.db.models import Sum
from django.contrib.admin.helpers import AdminForm
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.shortcuts import render
from django.urls.resolvers import URLPattern
from . import utils,models,views
from easy_select2 import select2_modelform
from easy_select2 import select2_modelform
from django.urls import path,reverse
from django.utils.html import format_html
from django.utils.dateparse import parse_date,parse_datetime
import json
from django.http.response import JsonResponse,HttpResponseRedirect
from django.utils.timezone import datetime
from django.contrib.admin.utils import (
    NestedObjects,
    construct_change_message,
    flatten_fieldsets,
    get_deleted_objects,
    lookup_spawns_duplicates,
    model_format_dict,
    model_ngettext,
    quote,
    unquote,
    
)
from django.contrib.admin.utils import (
    display_for_field,
    flatten_fieldsets,
    help_text_for_field,
    label_for_field,
    lookup_field,
    quote,
)
from django.contrib.admin.templatetags.admin_list import result_list
class ModelAdmin(ModelAdmin):
    def model_form(self,request,object_id=None):
        obj = None
        change = False
        if object_id != None:
            obj = self.get_object(request,object_id)
            change = True
        fieldsets = self.get_fieldsets(request, obj)
        ModelForm = self.get_form(
            request, obj, change, fields=flatten_fieldsets(fieldsets)
        )
        return ModelForm(request.POST, request.FILES, instance=obj)
    def admin_form(self,request,object_id=None):
        obj = None
        change = False
        if object_id:
            obj = self.get_object(request,object_id)
            change = True
        fieldsets = self.get_fieldsets(request, obj)
        if change and not self.has_change_permission(request, obj):
            readonly_fields = flatten_fieldsets(fieldsets)
        else:
            readonly_fields = self.get_readonly_fields(request, obj)
        form = self.model_form(request,object_id)
        admin_form = AdminForm(
            form,
            list(fieldsets),
            # Clear prepopulated fields on a view-only form to avoid a crash.
            self.get_prepopulated_fields(request, obj)
            if not change or self.has_change_permission(request, obj)
            else {},
            readonly_fields,
            model_admin=self,
        )
        return admin_form
    
    def changelist_view(self, request, extra_context=None):
        if not self.change_list_template:
            self.change_list_template = None or [
                f"{self.admin_site.name}/{self.opts.app_label}/{self.opts.model_name}/change_list.html",
                f"{self.admin_site.name}/{self.opts.app_label}/change_list.html",
                f"{self.admin_site.name}/change_list.html",
                f"change_list.html",
                f"admin/change_list.html",
            ]
        return super().changelist_view(request, extra_context)
    
    def get_urls(self):
        my_urls = [
            path(f"{self.opts.app_label}_{self.opts.model_name}_change_form_api/",self.admin_site.admin_view(self.change_form_api),name=f"{self.opts.app_label}_{self.opts.model_name}_change_form_api"),
        ]
        return my_urls + super().get_urls()
    def change_form_api(self,request):
        data = dict(**json.loads(request.body))
        self.elements = data["elements"]
        for element in data["elements"]:
            element = element or {}
            if "name" in element and element["name"]:
                element_api_name = f"element_api_{element['name']}"
                if hasattr(self,element_api_name):
                    element.update(getattr(self,element_api_name)(request,**element))
                elif len(str(element["name"]).split("-")) == 3:
                    el = str(element["name"]).split("-")
                    if el[1].isdigit():
                        el_model_inline = el[0].split('_')[0]
                        el_index = int(el[1])
                        el_field_inline = el[2]
                        element_modelinline_field_name = f"element_{el_model_inline}_{el_field_inline}_api"
                        if hasattr(self,element_modelinline_field_name):
                            #element.update()
                            f = getattr(self,element_modelinline_field_name)(request,el_model_inline,el_field_inline,el_index,**element)
                            element.update(f)
        #print(data)
        return JsonResponse(data=data)
    
    def element_modelinline_field_api(self,request,modelinline,field,index,**element):
        return element
    def element_inlines_api(self,request,formset,**kwargs):
        pass
    def element_api_name(self,request,**element):
        return element
    def element_get_data(self,elment_name):
        for element in self.elements:
            if element["name"] == elment_name:
                return element 
    def element_inline_get_data(self,modelinline,index,field):
        for element in self.elements:
            if element["name"] == f"{modelinline}_set-{index}-{field}":
                return element 
    def changeform_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        extra_context.update(
            change_form_api_url = reverse(f"{self.admin_site.name}:{self.opts.app_label}_{self.opts.model_name}_change_form_api")
        )
        
        ff = super().changeform_view(request, object_id, form_url, extra_context)
        #print(super().message_user(request,""))
        return ff
    
   

   



class AdminSite(AdminSite):
    site_title = "ALMALIK"
    site_header = "almalik"
    index_title = "الرئيسية"
    site_url = False
    def __init__(self,name):
        super().__init__(name)
        self.login_template = f"{self.name}/login.html"
    def index(self, request, extra_context = None):
        self.index_template = None or [
            f"{self.name}/index.html",
            f"index.html",
        ]
        return super().index(request, extra_context)
    def app_index(self, request, app_label, extra_context = None):
        self.app_index_template = None or [
            f"{self.name}/{app_label}/app_index.html",
            f"{self.name}/app_index.html",
            f"app_index.html",
            f"admin/app_index.html",

        ]
        return super().app_index(request, app_label, extra_context)

    def login(self, request, extra_context = None):
        return super().login(request, extra_context)
    def logout(self, request, extra_context=None):
        
        return super().logout(request,extra_context)
site = AdminSite(name="admin")

from django.contrib import messages



class UserModelAdmin(ModelAdmin):
    def get_fields(self, request, obj=None):
        return ["name"]
    list_display = ["id","name","username","_groups","is_active","is_staff"]
    list_editable = ["is_active","is_staff"]
    @display(description="القسم - المجموعة")
    def _groups(self,obj):
        return obj.groups.first().name
    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)
class BaseReport(ModelAdmin):
    
    report_title = None
    report_logo = None
    report_logo_2 = None
    
    report_is_horizontal = True
    report_style_list = ["vendor/adminlte/css/adminlte_ar.min.css"]
    report_margin = {"top":"3mm","bottom":"3mm","left":"3mm","right":"3mm"}
    report_address_list = [
       
    ]
    report_footer_list = [
        #"المختص:","المسؤول:",
    ]
    report_fieldsets = []
    report_inline_fieldsets = []
    def report_get_context(self,request,object_id=None,extra_context=None):
        
        cl = self.get_changelist_instance(request)
        #print(cl,99999999999999)
        cl.formset = None
        inline_result_list = None
        result_fieldsets_list = []







        if object_id != None:
            
            obj = self.get_object(request,object_id)
            
            form = self.model_form(request,object_id)
            
            formsets, inline_instances = self._create_formsets(
                request,
                form.instance,
                change=True,
            )
            
            for name,fieldset in self.report_fieldsets:
                _fields = []
                for a_field in fieldset["fields"]:
                    f,attr,value = lookup_field(a_field,obj,self)
                    
                    _fields += [{"name":label_for_field(a_field,self.model,self),"value":value}]
                result_fieldsets_list += [{"name":name,"fields":_fields}]
            inline_result_list = {}
            for inline_formsets in self.get_inline_formsets(request,formsets,inline_instances,obj):
                result_headers = []
                results = []
                
                for qs in inline_formsets.formset.queryset:
                    result = []
                    #print(inline_formsets.opts.__dict__,7)
                    for name,field_sets in inline_formsets.model_admin.report_inline_fieldsets:
                        for field in field_sets["fields"]:
                            #print(field_sets,66)
                            
                            f,attr,value = lookup_field(field,qs,inline_formsets.model_admin)
                            
                            if value == None:
                                value = ""
                                

                            
                            result.append(format_html(f"<td>{value}</td>"))
                    results += [result]
                
                for name,field_sets in inline_formsets.model_admin.report_inline_fieldsets:
                    for field in field_sets["fields"]:
                        result_headers += [{
                            "text":label_for_field(field,inline_formsets.opts.model,inline_formsets.model_admin),
                        }]
                inline_result_list["result_headers"] = result_headers
                inline_result_list["results"] = results
                
                




                #inline_admin_form.readonly_fields = ["medicine"]
        
       
        extra_context = extra_context or {}

        context = {
            "result_fieldsets_list":result_fieldsets_list,
            "inline_result_list":inline_result_list,
            "result_list":result_list(cl),
            "admin_form":self.admin_form(request),
            "logo":self.report_logo or "/static/logo.png",
            "logo_2":self.report_logo_2,
            "title_report": self.report_get_title(request,object_id),
            "address_list":self.report_get_address_list(request,object_id),
            #"footer_list":self.report_get_footer_list(request,object_id),
            "date_report":datetime.now().date(),
            
            "font_Bader":"/static/fonts/Bader.ttf",

            "size":self.report_get_size(),
            "margin":self.report_margin,
        }
        context.update(
            extra_context
        )
        return context
    
    def report_get_size(self,is_horizontal=False):
        if self.report_is_horizontal or is_horizontal:
            return {"width":"204mm","height":"291mm"}
        else:
            return {"width":"291mm","height":"204mm"}

    def report_get_header_list(self,request,object_id):
        return{}
    def report_get_title(self,request,object_id):
        return self.report_title or self.opts.verbose_name_plural
    def report_get_address_list(self,request,object_id):
        return self.report_address_list
    def report_get_footer_list(self,request,object_id):
        return self.report_footer_list
    def report_get_style_list(self):
        return self.report_style_list
    def report_get_pdf_name(self,request,object_id=None):
        return f"{self.report_get_title(request,object_id)}"



class ModelActionReport(BaseReport):
    report_is_horizontal = True
    def get_list_display(self, request):
       list_display = list(super().get_list_display(request))
       return list_display + ["report_action_url"]
    def get_urls(self):
        return [path("<object_id>/pdf/",self.report_action_admin)] + super().get_urls()
    @display(description="_")
    def report_action_url(self,obj):
       return format_html(f"""<a data-popup="yes" class='related-widget-wrapper-link add-related' href='{obj.id}/pdf/'>طباعة</a>""")
        
        #return format_html(d)
    def report_action_admin(self,request,object_id,extra_context=None):
        
        extra_context = extra_context or {}
        pdf_viewer_url = views.render_to_pdf(
                request, 
                template_name=None or [
                    f"report/{self.opts.app_label}/{self.opts.model_name}/change_object.html",
                    f"report/{self.opts.app_label}/change_object.html",
                    f"report/change_object.html",
                ],
                    context =self.report_get_context(request,object_id,extra_context),
                    styles = self.report_get_style_list(),
                    pdf_name=self.report_get_pdf_name(request,object_id),
                )
        
         
        extra_context.update(
            **self.changeform_view(request,object_id,"",extra_context).context_data
        )
        extra_context.update(
            title = None,
            subtitle = None
        )
        extra_context.update(
            pdf_viewer_url=pdf_viewer_url
        )
        #self.change_list_template = "report/viewer.html"
        return render(request,"report/viewer_object.html",extra_context)
    
    
       

class ModelReport(BaseReport):
    actions = None
    list_display_links = None
    list_per_page = 1000
    change_list_template = "report/viewer.html"

    def changelist_view(self, request, extra_context=None):
        if not request.method == "POST":
            return HttpResponseRedirect("add/")
        extra_context = extra_context or {}
        
        pdf_viewer_url = views.render_to_pdf(
                    request, 
                    template_name=None or [
            f"report/{self.opts.app_label}/{self.opts.model_name}/change_list.html",
            f"report/{self.opts.app_label}/change_list.html",
            f"report/change_list.html",
        ],
                    context = self.report_get_context(request,None,None),
                    styles = self.report_get_style_list(),
                    pdf_name=self.report_get_pdf_name(request,None),
                )
        extra_context.update(
            pdf_viewer_url=pdf_viewer_url
        )
        return super().changelist_view(request,extra_context)
    
    
   
    
    
    def changeform_view(self, request, object_id = None, form_url = "", extra_context = None):
        extra_context = extra_context or {}
        extra_context.update(
            title = f"حدد الخيارات المناسبة لإظهار {self.opts.verbose_name_plural}",
            show_save = False,
            show_save_as_new = False,
            show_save_and_add_another = False,
            show_delete_link = False,
            show_close = False,
        )
        if request.method == "POST":
            if self.model_form(request).is_valid():
                self.data = dict(**self.model_form(request).data)
                extra_context.update(
                    title = None,
                    suptitle = None,
                )
                return self.changelist_view(request,extra_context)
        
        return super().changeform_view(request, object_id, form_url, extra_context )
    
    
    def report_get_context(self,request,object_id=None,extra_context=None):
        cl = self.get_changelist_instance(request)
        cl.formset = None
        inline_result_list = None
        result_fieldsets_list = []


        for name,fieldset in self.report_fieldsets:
            _fields = []
            for a_field in fieldset["fields"]:
                if a_field in self.model_form(request).fields:
                    _field = self.model_form(request)[a_field]
                    value = _field.value()
                    if value:
                        if hasattr(_field.field,"_queryset"):
                            _queryset = _field.field._queryset
                            value = _queryset.get(id=value)
                        elif hasattr(_field.field,"_choices"):
                            _choices = _field.field._choices
                            for ch_key,ch_value in _choices:
                                if ch_key == value:
                                    value = ch_value
                    else:
                        if hasattr(_field.field,"_queryset") or hasattr(_field.field,"_choices"):
                            value = "الكل"
                    _fields += [{"name":label_for_field(a_field,self.model,self),"value":value}]
                elif hasattr(self,a_field):
                    _fields += [{"name":label_for_field(a_field,self.model,self),"value":getattr(self,a_field)()}]

            result_fieldsets_list += [{"name":name,"fields":_fields}]
            
        extra_context = extra_context or {}
        for r in result_list(cl)["results"]:
            for h in r:
                print(h,7878)
        context = {
            "result_fieldsets_list":result_fieldsets_list,
            "inline_result_list":inline_result_list,
            "result_list":result_list(cl),
            "admin_form":self.admin_form(request),
            "logo":self.report_logo or "/static/logo.png",
            "title_report": self.report_get_title(request,object_id),
            "address_list":self.report_get_address_list(request,object_id),
            "footer_list":self.report_get_footer_list(request,object_id),
            "date_report":datetime.now().date(),

            "size":self.report_get_size(),
            "margin":self.report_margin,
        }
        extra_context.update(
            context
        )
        return super().report_get_context(request,object_id,extra_context)
    

    


  
    





