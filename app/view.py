from main.view import *
from . import models,admin

class ViewSite(ViewSite):
    site_title = "المالية"
    site_header = "المالية"

    site_menu = [
        {
            "name":"الصرف",
            "children":[
                {
                    "name":"الأدوية",
                    "url":"/admin/app/medicineorder",
                },
                {
                    "name":"مزاورات نقدية",
                    "url":"/admin/app/cashvisit",
                },
                {
                    "name":"النقل والتنقلات",
                    "url":"/admin/app/transport",
                },
                {
                    "name":"الملبوسات",
                    "url":"/admin/app/cloth",
                },
                {
                    "name":"الإتصالات",
                    "url":"/admin/app/communication",
                },
                {
                    "name":"الماء",
                    "url":"/admin/app/water",
                },
                {
                    "name":"العهد الثابتة",
                    "url":"/admin/app/asset",
                },
                {
                    "name":"التغذية العينية",
                    "url":"/admin/app/feed",
                },
                {
                    "name":"القات",
                    "url":"/admin/app/cat",
                },
            ]
        },
        
       
        
        {
            "name":"التقارير",
            "children":[

                {
                    "name":"الأدوية",
                    "url":"/admin/app/medicineorderr",
                },
                {
                    "name":"مزاورات نقدية",
                    "url":"/admin/app/cashvisitr",
                },
                {
                    "name":"النقل والتنقلات",
                    "url":"/admin/app/transportr",
                },
                {
                    "name":"الملبوسات",
                    "url":"/admin/app/clothr",
                },
                {
                    "name":"الإتصالات",
                    "url":"/admin/app/communicationr",
                },
                {
                    "name":"الماء",
                    "url":"/admin/app/waterr",
                },
                {
                    "name":"العهد الثابتة",
                    "url":"/admin/app/assetr",
                },
                {
                    "name":"التغذية العينية",
                    "url":"/admin/app/feedr",
                },
                {
                    "name":"القات",
                    "url":"/admin/app/catr",
                },
                
            ]

        },

        {
            "name":"الإعدادات",
            "children":[
                
            ]
        },
        

    ]
site = ViewSite(name="view")

