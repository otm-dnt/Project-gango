from django.contrib import admin
from .models import Event, Participation

class ParticipationInline(admin.TabularInline):
    model = Participation
    extra = 0

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'created_by', 'participant_count')
    list_filter = ('date', 'created_by')
    search_fields = ('title', 'description')
    date_hierarchy = 'date'
    inlines = [ParticipationInline]
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si c'est une création (pas une modification)
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'is_attending', 'updated_at')
    list_filter = ('is_attending', 'event')
    search_fields = ('user__username', 'event__title')
