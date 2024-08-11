from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

# Create your models here.




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
