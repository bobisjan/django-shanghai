from django.contrib.auth.models import Group, User

from shanghai.resources import ModelResource


class GroupResource(ModelResource):

    model = Group


class UserResource(ModelResource):

    model = User
