from django.apps import AppConfig
from django.db import connection
from django.db import models as db_models
class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    #verbose_name = ""
    
    def ready(self):
        tables = connection.introspection.table_names()
        super().ready()
        
        pre = [
            "view_entry","add_entry","change_","delete_",
            "view_entrydiagnosicategore","add_entrydiagnosicategore","change_","delete_",
            "view_entryprocedure","add_entryprocedure","change_","delete_",
            "view_entrydiagnosi","add_entrydiagnosi","change_","delete_",
            "view_entryitem","add_entryitem","change_","delete_",
            "view_bigg","add_bigg","change_","delete_",
            "view_newentry","add_newentry","change_","delete_",
            "view_backentry","add_backentry","change_","delete_",
            "view_turnentry","add_turnentry","change_","delete_",
            "view_result","add_result","change_","delete_",
            "view_teratmentresult","add_teratmentresult","change_","delete_",
            "view_turnresult","add_turnresult","change_","delete_",
            "view_backresult","add_backresult","change_","delete_",
            "view_deathresult","add_deathresult","change_","delete_",
            "view_profilemedical","add_","change_","delete_",
            "view_","add_","change_","delete_",
            "view_","add_","change_","delete_",

        ]
        from django.contrib.auth import models as auth_models
        if len(tables) > 0:
            auth_models.Group.objects.get_or_create(
                name="users"
            )[0].permissions.set(
                auth_models.Permission.objects.filter(codename__in=pre)
            )

            