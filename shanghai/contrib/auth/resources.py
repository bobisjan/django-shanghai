from django.contrib.auth.models import Group, User

from shanghai.resources import ModelResource


class GroupResource(ModelResource):

    name = 'groups'
    model = Group


class UserResource(ModelResource):

    name = 'users'
    model = User
