
from django.contrib import admin
from .models import *
from .profile import *
# Register your models here.
admin.site.register(User)

admin.site.register(AdvocateProfile)
admin.site.register(EducationModel)
admin.site.register(CaseProfile)
admin.site.register(UserProfile)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Rating)
admin.site.register(InstantAdvice)
admin.site.register(ContactUs)
admin.site.register(Follower)
admin.site.register(ActiveChat)

class InstantAdviceAdmin(admin.ModelAdmin):
    readonly_fields = {'transaction_id'}