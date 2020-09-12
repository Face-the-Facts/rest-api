from django.contrib import admin
from .models import Vote
# Register your models here.
class VoteAdmin(admin.ModelAdmin):
    pass

admin.site.register(Vote, VoteAdmin)