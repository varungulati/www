from rest_framework import serializers

from providers_details.models import ProvidersDetails

class ProvidersDetailsSerializer(serializers.ModelSerializer):

  class Meta:
    model = ProvidersDetails
    fields = ('first_name', 'last_name', 'email')