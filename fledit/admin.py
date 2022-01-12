from .models import TripModel, RootModel, TodoModel
from django.contrib import admin

# Register your models here.
admin.site.register(TripModel)
admin.site.register(RootModel)
admin.site.register(TodoModel)