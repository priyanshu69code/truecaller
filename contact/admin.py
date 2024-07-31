from django.contrib import admin
from .models import Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'email', 'phone', "user",
        'created_at', 'updated_at', 'spam',
        'spam_likelihood_display',
        # 'get_country_display', 'get_phone_number_display'
    )

    def spam_likelihood_display(self, obj):
        return obj.spam_likelihood()

    spam_likelihood_display.short_description = 'Spam Likelihood'

    # def get_country_display(self, obj):
    #     return obj.get_country()

    # def get_phone_number_display(self, obj):
    #     return obj.get_phone_number()

    # get_country_display.short_description = 'Country'
    # get_phone_number_display.short_description = 'Phone Number'


admin.site.register(Contact, ContactAdmin)
