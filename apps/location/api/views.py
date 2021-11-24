from rest_framework import viewsets, permissions

from .serializers import CountrySerializer
from ..models import Country


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [permissions.IsAuthenticated]
