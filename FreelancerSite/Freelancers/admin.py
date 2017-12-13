# user: admin, pass: adminpassword

from django.contrib import admin
from .models import Employer, Freelancer, Project

# Register your models here.
admin.site.register(Employer)
admin.site.register(Freelancer)
admin.site.register(Project)