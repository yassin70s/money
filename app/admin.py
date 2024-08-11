from collections.abc import Sequence
from django.db.models.fields.related import ForeignKey
from django.db.models.query import QuerySet
from django.forms.models import ModelChoiceField
from django.http.request import HttpRequest
from main.admin import *
from . import models,utils
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth import models as auth_models
from django.contrib.auth import admin as auth_admin

site.register(auth_models.User,auth_admin.UserAdmin)
site.register(auth_models.Group,auth_admin.GroupAdmin)

class ModelAdmin(ModelAdmin):
    list_per_page = 15
site.site_title = "المالية"
site.site_header = "المالية"


class ModelReport(ModelReport):
    report_logo_2 = "/static/app/logo.jpg"
    report_address_list = [
        "الجمهورية اليمنية",
        "وزارة الدفاع",
        "رئاسة هيئة الأركان العامة",
        "المنطقة العسكرية الخامسة",
        
    ]

site.register(
    model_or_iterable=[
        models.ClothItem,
        models.WaterItem, models.AssetItem,
        models.CatItem,
        models.Side,
        models.Province,
        models.Directorate,
        models.Area,
        models.Box,
        models.Medicine,models.MedicineType,
        models.Sick,models.SickType,
        models.SupportType,
        models.Statement,
        models.Average,
        models.Company,
        models.CommunicationType,
    ]
)

class OrderAdmin(ModelAdmin):
    list_display = ["date","amount","side","support_type","support_number","support_file","notice"]



class MedicineOrderAdmin(OrderAdmin):
    pass
site.register(models.MedicineOrder,MedicineOrderAdmin)

class CashVisitAdmin(OrderAdmin):
    pass
site.register(models.CashVisit,CashVisitAdmin)

class TransportAdmin(OrderAdmin):
    pass
site.register(models.Transport,TransportAdmin)


class ClothAdmin(OrderAdmin):
    pass
site.register(models.Cloth,ClothAdmin)

class CommunicationAdmin(OrderAdmin):
    pass
site.register(models.Communication,CommunicationAdmin)

class WaterAdmin(OrderAdmin):
    pass
site.register(models.Water,WaterAdmin)

class AssetAdmin(OrderAdmin):
    pass
site.register(models.Asset,AssetAdmin)

class FeedAdmin(OrderAdmin):
    pass
site.register(models.Feed,FeedAdmin)

class CatAdmin(OrderAdmin):
    pass
site.register(models.Cat,CatAdmin)













class OrderReport(ModelReport):
    list_display = ["date","amount","side","support_type","support_number","notice"]
    fields = ["date_gte","date_lte","box"]
    def get_queryset(self, request):
        model = getattr(models,self.__class__.__name__[:-6]) or models.Order
        queryset = model.objects.get_queryset()
        box = models.Box.objects.get(id=self.data["box"][0])
        date_gte = parse_date(str(self.data["date_gte"][0]))
        date_lte = parse_date(str(self.data["date_lte"][0]))
        queryset = queryset.filter(date__gte=date_gte,date__lte=date_lte,box=box)
        print(model)

        return queryset
    report_fieldsets = (
        (None, {
            "fields": (
                "box",
            ),
        }),
        (None, {
            "fields": (
                "date_gte","date_lte",
            ),
        }),
    )
    report_footer_list = [
        "المالي:",
        "المسؤول",
    ]
    



class MedicineOrderReport(OrderReport):
    pass
site.register(models.MedicineOrderR,MedicineOrderReport)

class CashVisitReport(OrderReport):
    pass
site.register(models.CashVisitR,CashVisitReport)

class TransportReport(OrderReport):
    pass
site.register(models.TransportR,TransportReport)


class ClothReport(OrderReport):
    pass
site.register(models.ClothR,ClothReport)

class CommunicationReport(OrderReport):
    pass
site.register(models.CommunicationR,CommunicationReport)

class WaterReport(OrderReport):
    pass
site.register(models.WaterR,WaterReport)

class AssetReport(OrderReport):
    pass
site.register(models.AssetR,AssetReport)

class FeedReport(OrderReport):
    pass
site.register(models.FeedR,FeedReport)

class CatReport(OrderReport):
    pass
site.register(models.CatR,CatReport)

