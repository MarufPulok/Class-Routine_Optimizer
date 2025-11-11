from django.contrib import admin
from.models import *

# Django admin doesn't support MongoDB documents (mongoengine models)
# These models are registered in MongoDB, not Django ORM
