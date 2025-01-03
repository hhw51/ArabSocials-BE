from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'location', 'event_date', 'approval_status', 'user')  # Fields to display
    list_filter = ('approval_status', 'event_type')  # Add filters for easier navigation
    search_fields = ('title', 'location', 'user__username')  # Enable search for these fields
    actions = ['approve_events', 'disapprove_events']  # Add custom actions

    # Custom action to approve events
    @admin.action(description='Approve selected events')
    def approve_events(self, request, queryset):
        queryset.update(approval_status='approved')  # Update the approval_status to 'approved'
        self.message_user(request, "Selected events have been approved.")

    # Custom action to disapprove events
    @admin.action(description='Disapprove selected events')
    def disapprove_events(self, request, queryset):
        queryset.update(approval_status='disapproved')  # Update the approval_status to 'disapproved'
        self.message_user(request, "Selected events have been disapproved.")
