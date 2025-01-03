from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings  # Import settings to reference the User model

class Event(models.Model):
    ONLINE = 'online'
    OFFLINE = 'offline'
    EVENT_TYPE_CHOICES = [
        (ONLINE, _('Online')),
        (OFFLINE, _('Offline')),
    ]

    # Event Information
    title = models.CharField(_("Event Title"), max_length=255)
    event_type = models.CharField(
        _("Event Type"), 
        max_length=10, 
        choices=EVENT_TYPE_CHOICES, 
        default=ONLINE
    )
    location = models.CharField(_("Location"), max_length=255)
    flyer = models.ImageField(_("Event Flyer"), upload_to='event_flyers/', null=True, blank=True)
    description = models.TextField(_("Event Description"))
    event_date = models.DateTimeField(_("Event Date & Time"))
    ticket_link = models.URLField(_("Ticket/Registration Link"), null=True, blank=True)
    promo_code = models.CharField(_("Promo Code"), max_length=50, null=True, blank=True)
    
    # Foreign Key to User (Organizer)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # This is the User model that is being referenced
        on_delete=models.CASCADE,  # Cascade delete - if user is deleted, their events are also deleted
        related_name='events',  # This will allow you to access the events related to the user like user.events.all()
        verbose_name=_("Organizer")
    )

    # Status and Approval
    APPROVAL_PENDING = 'pending'
    APPROVAL_APPROVED = 'approved'
    APPROVAL_DISAPPROVED = 'disapproved'
    APPROVAL_STATUS_CHOICES = [
        (APPROVAL_PENDING, _('Pending')),
        (APPROVAL_APPROVED, _('Approved')),
        (APPROVAL_DISAPPROVED, _('Disapproved')),
    ]
    approval_status = models.CharField(
        _("Approval Status"), 
        max_length=30, 
        choices=APPROVAL_STATUS_CHOICES, 
        default=APPROVAL_PENDING
    )
    
    # Timestamps
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
        ordering = ['event_date']










class EventRegistration(models.Model):
    REGISTERED = 'registered'
    CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (REGISTERED, 'Registered'),
        (CANCELLED, 'Cancelled'),
    ]

    # Fields
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Linking to the User model via ForeignKey
        on_delete=models.CASCADE,  # If the user is deleted, the registration is also deleted
        related_name='registrations',  # Allows easy access to a user's event registrations
        verbose_name='User'
    )
    event = models.ForeignKey(
        Event,  # Linking to the Event model via ForeignKey
        on_delete=models.CASCADE,  # If the event is deleted, the registration is also deleted
        related_name='registrations',  # Allows easy access to an event's registrations
        verbose_name='Event'
    )
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default=REGISTERED,  # Default status is 'Registered'
        verbose_name='Status'
    )
    registered_at = models.DateTimeField(
        auto_now_add=True,  # Automatically sets the date and time when the registration is created
        verbose_name='Registered At'
    )

    def __str__(self):
        return f"{self.user} - {self.event.title} - {self.status}"

    class Meta:
        verbose_name = 'Event Registration'
        verbose_name_plural = 'Event Registrations'
        ordering = ['registered_at']