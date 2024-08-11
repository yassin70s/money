from django.db import models
from django.contrib.auth import models as auth_models
from django.contrib.contenttypes import models as contenttype_models
from django.contrib.contenttypes import fields as contenttype_fields
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib import admin
from . import views,utils
from django import forms
from django.utils.html import format_html
from django.utils.dateparse import parse_date,parse_datetime
from django.urls import reverse
from django.utils.translation import gettext as _
import os,shutil
from . import models as _models
from django.conf import settings
from django.core import management
from django.apps import apps
from collections import OrderedDict

import tarfile
BASE_DIR = settings.BASE_DIR
MEDIA_ROOT = settings.MEDIA_ROOT


class Item(models.Model):
    name = models.CharField(_("اسم الصنف"), max_length=50)
    class Meta:
        verbose_name = _("صنف")
        verbose_name_plural = _("الأصناف")

    def __str__(self):
        return self.name

class ClothItem(Item):
    pass
    
class WaterItem(Item):
    pass
    
class AssetItem(Item):
    pass
    
class CatItem(Item):
    pass
    



class Side(models.Model):
    name = models.CharField(_("اسم الجهة"), max_length=50)
    

    class Meta:
        verbose_name = _("Side")
        verbose_name_plural = _("Sides")

    def __str__(self):
        return self.name

class Box(models.Model):
    name = models.CharField(_("اسم الصندوق"), max_length=50)

    

    class Meta:
        verbose_name = _("Box")
        verbose_name_plural = _("Boxs")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Box_detail", kwargs={"pk": self.pk})

class SupportType(models.Model):
    name = models.CharField(_("نوع السند"), max_length=50)

    class Meta:
        verbose_name = _("support_type")
        verbose_name_plural = _("support_types")

    def __str__(self):
        return self.name



class Order(models.Model):
    box = models.ForeignKey(Box, verbose_name=_("الجهة"), on_delete=models.CASCADE)
    date = models.DateField(_("التاريخ"), auto_now=False, auto_now_add=False)
    amount = models.PositiveBigIntegerField(_("المبلغ"))
    side = models.ForeignKey(Side, verbose_name=_("المستفيد"), on_delete=models.CASCADE)
    support_type = models.ForeignKey(SupportType, verbose_name=_("نوع السند"), on_delete=models.CASCADE)
    support_number = models.PositiveBigIntegerField(_("رقم السند"))
    support_file = models.FileField(_("السند"), upload_to=None, max_length=100)
    notice = models.TextField(_("ملاحظة"),null=True,blank=True)

    class Meta:
        verbose_name = _("صرف")
        verbose_name_plural = _("الصرف")

    def __str__(self):
        return self.side.name

class SickType(models.Model):
    name = models.CharField(_("نوع الإصابة"), max_length=50)
    
    class Meta:
        verbose_name = _("نوع إصابة")
        verbose_name_plural = _("أنواع الإصابات")

    def __str__(self):
        return self.name


class Sick(models.Model):
    sicktype = models.ForeignKey(SickType, verbose_name=_("نوع الإصابة"), on_delete=models.CASCADE)
    name = models.CharField(_("اسم الإصابة"), max_length=50)
    
    class Meta:
        verbose_name = _("إصابة")
        verbose_name_plural = _("الإصابات")

    def __str__(self):
        return self.name

class MedicineType(models.Model):
    name = models.CharField(_("نوع الدواء"), max_length=50)
    
    class Meta:
        verbose_name = _("نوع دواء")
        verbose_name_plural = _("أنوا الأدوية")

    def __str__(self):
        return self.name
   


class Medicine(models.Model):
    medicinetype = models.ForeignKey(MedicineType, verbose_name=_("نوع الدواء"), on_delete=models.CASCADE)
    name = models.CharField(_("اسم الدواء"), max_length=50)

    class Meta:
        verbose_name = _("دواء")
        verbose_name_plural = _("الأدوية")

    def __str__(self):
        return self.name
    

class MedicineOrder(Order):
    sick = models.ForeignKey(Sick, verbose_name=_("الإصابة"), on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, verbose_name=_("الدواء"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("دواء")
        verbose_name_plural = _("الأدوية")


class Province(models.Model):
    name = models.CharField(("اسم المحافظة"), max_length=150,unique=True)
    def __str__(self):
        return self.name

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'محافظة'
        verbose_name_plural = 'المحافظات'
class Directorate(models.Model):
    province = models.ForeignKey(Province, verbose_name=("المحافظة"), on_delete=models.CASCADE)
    name = models.CharField(("اسم المديرية"), max_length=150,unique=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'مديرية'
        verbose_name_plural = 'المديريات'
class Area(models.Model):
    directorate = models.ForeignKey(Directorate, verbose_name=("المديرية"), on_delete=models.CASCADE)
    name = models.CharField(("اسم المنطقة"), max_length=150,unique=True)
    def __str__(self):
        return self.name

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'منطقة'
        verbose_name_plural = 'الحارات / المناطق'


class CashVisit(Order):
    sick = models.ForeignKey(Sick, verbose_name=_("الإصابة"), on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, verbose_name=_("الدواء"), on_delete=models.CASCADE)
    area = models.ForeignKey(Area, verbose_name=_("محل الإقامة"), on_delete=models.CASCADE)
    period = models.PositiveSmallIntegerField(_("مدة الزيارة"))
    class Meta:
        verbose_name = _("مزاورات نقدية")
        verbose_name_plural = _("المزاورات النقدية")


class Statement(models.Model):
    name = models.CharField(("اسم المنطقة"), max_length=150,unique=True)

    class Meta:
        verbose_name = _("بيان")
        verbose_name_plural = _("البيانات")

    def __str__(self):
        return self.name



class Transport(Order):
    into = models.CharField(_("من إلى"), max_length=50)
    statement = models.ForeignKey(Statement, verbose_name=_("البيان"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("مواصلات")
        verbose_name_plural = _("المواصلات")



class Cloth(Order):
    clothitem = models.ForeignKey(ClothItem, verbose_name=_("الصنف"), on_delete=models.CASCADE)
    statement = models.ForeignKey(Statement, verbose_name=_("البيان"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("ملابس")
        verbose_name_plural = _("الملبوسات")

class CommunicationType(models.Model):
    name = models.CharField(_("نوع الإتصالات"), max_length=50)
    class Meta:
        verbose_name = _("نوع اتصال")
        verbose_name_plural = _("انواع الإتصالات")


class Communication(Order):
    Communicationtype = models.ForeignKey(CommunicationType, verbose_name=_("نوعه"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("اتصال")
        verbose_name_plural = _("الاتصالات")


class Water(Order):
    wateritem = models.ForeignKey(WaterItem, verbose_name=_("الصنف"), on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(_("الكمية"))
    statement = models.ForeignKey(Statement, verbose_name=_("البيان"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("ماء")
        verbose_name_plural = _("الماء والثلج")

class Company(models.Model):
    name = models.CharField(_("اسم الشركة"), max_length=50)
    
    class Meta:
        verbose_name = _("شركة")
        verbose_name_plural = _("الشركات")

    def __str__(self):
        return self.name


class Asset(Order):
    quantity = models.PositiveIntegerField(_("الكمية"))
    assetitem = models.ForeignKey(AssetItem, verbose_name=_("اسم الصنف"), on_delete=models.CASCADE)

    serialnumber = models.PositiveBigIntegerField(_("الرقم التسلسلي"))
    company = models.ForeignKey(Company, verbose_name=_("الشركة المصنعة"), on_delete=models.CASCADE)
    detail = models.TextField(_("المواصفات"))
    ward_number = models.PositiveIntegerField(_("رقم التوريد"))

    class Meta:
        verbose_name = _("اصل")
        verbose_name_plural = _("الأصول")




class Feed(Order):
    statement = models.ForeignKey(Statement, verbose_name=_("البيان"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("تغذية")
        verbose_name_plural = _("التغذية")

class Average(models.Model):
    name = models.CharField(_("اسم المقوت"), max_length=50)
    

    class Meta:
        verbose_name = _("مقوت")
        verbose_name_plural = _("المقاوته")

    def __str__(self):
        return self.name



class Cat(Order):
    average = models.ForeignKey(Average, verbose_name=_("المقوت"), on_delete=models.CASCADE)
    catitem = models.ForeignKey(CatItem, verbose_name=_("نوع القات"), on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(_("الكمية"))

    class Meta:
        verbose_name = _("قات")
        verbose_name_plural = _("القات")

















class MedicineOrderR(MedicineOrder):
    date_gte = models.DateField(_("من تاريخ"), auto_now=False, auto_now_add=False)
    date_lte = models.DateField(_("حتى تاريخ"), auto_now=False, auto_now_add=False)
    
    class Meta:
        verbose_name = _("دواء")
        verbose_name_plural = _("تفاصيل الأدوية")


class CashVisitR(CashVisit):
    date_gte = models.DateField(_("من تاريخ"), auto_now=False, auto_now_add=False)
    date_lte = models.DateField(_("حتى تاريخ"), auto_now=False, auto_now_add=False)
    
    class Meta:
        verbose_name = _("")
        verbose_name_plural = _("تفاصيل مزاورات نقدية")


class TransportR(Transport):
    date_gte = models.DateField(_("من تاريخ"), auto_now=False, auto_now_add=False)
    date_lte = models.DateField(_("حتى تاريخ"), auto_now=False, auto_now_add=False)
    
    class Meta:
        verbose_name = _("")
        verbose_name_plural = _("تفاصيل النقل والتنقلات")

class ClothR(Cloth):
    date_gte = models.DateField(_("من تاريخ"), auto_now=False, auto_now_add=False)
    date_lte = models.DateField(_("حتى تاريخ"), auto_now=False, auto_now_add=False)
    
    class Meta:
        verbose_name = _("")
        verbose_name_plural = _("تفاصيل الملبوسات")

class CommunicationR(Communication):
    date_gte = models.DateField(_("من تاريخ"), auto_now=False, auto_now_add=False)
    date_lte = models.DateField(_("حتى تاريخ"), auto_now=False, auto_now_add=False)
    
    class Meta:
        verbose_name = _("")
        verbose_name_plural = _("تفاصيل الإتصالات")

class WaterR(Water):
    date_gte = models.DateField(_("من تاريخ"), auto_now=False, auto_now_add=False)
    date_lte = models.DateField(_("حتى تاريخ"), auto_now=False, auto_now_add=False)
    
    class Meta:
        verbose_name = _("")
        verbose_name_plural = _("تفاصيل الماء")

class AssetR(Asset):
    date_gte = models.DateField(_("من تاريخ"), auto_now=False, auto_now_add=False)
    date_lte = models.DateField(_("حتى تاريخ"), auto_now=False, auto_now_add=False)
    
    class Meta:
        verbose_name = _("")
        verbose_name_plural = _("تفاصيل العهد الثابتة")

class FeedR(Feed):
    date_gte = models.DateField(_("من تاريخ"), auto_now=False, auto_now_add=False)
    date_lte = models.DateField(_("حتى تاريخ"), auto_now=False, auto_now_add=False)
    
    class Meta:
        verbose_name = _("")
        verbose_name_plural = _("تفاصيل التغذية")

class CatR(Cat):
    date_gte = models.DateField(_("من تاريخ"), auto_now=False, auto_now_add=False)
    date_lte = models.DateField(_("حتى تاريخ"), auto_now=False, auto_now_add=False)
    
    class Meta:
        verbose_name = _("")
        verbose_name_plural = _("تفاصيل القات")
