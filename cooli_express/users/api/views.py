from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import UserDetailsSerializer

User = get_user_model()


class UserViewSet(ModelViewSet):
    serializer_class = UserDetailsSerializer
    queryset = User.objects.all()
    lookup_field = "uuid"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(uuid=self.request.user.uuid)

    # @action(detail=False, methods=["GET"])
    # def me(self, request):
    #     serializer = UserSerializer(request.user, context={"request": request})
    #     return Response(status=status.HTTP_200_OK, data=serializer.data)
