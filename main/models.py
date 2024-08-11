from collections.abc import MutableMapping
from typing import Any
from django.db import models
from django.contrib.auth import models as auth_models
from django.urls import reverse
from django.contrib.contenttypes import models as contenttype_models
from django.contrib.contenttypes import fields as contenttype_fields
from django.utils.translation import gettext as _
from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user
)



