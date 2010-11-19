from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend

from google.appengine.api import users

from models import UserPermissionList, GroupPermissionList


class NonrelPermissionBackend(ModelBackend):
    """
    Implements Django's permission system on Django-Nonrel
    """
    supports_object_permissions = False
    supports_anonymous_user = True

    def get_group_permissions(self, user_obj, user_perm_obj=None):
        """
        Returns a set of permission strings that this user has through his/her
        groups.
        """
        if not hasattr(user_obj, '_group_perm_cache'):
            perms = set([])
            if user_perm_obj is None:
                user_perm_obj, created = UserPermissionList.objects.get_or_create(user=user_obj)

            group_perm_lists = GroupPermissionList.objects.filter(group__id__in=user_perm_obj.group_fk_list)

            for group_perm_list in group_perm_lists:
                perms.update(group_perm_list.permission_list)

            user_obj._group_perm_cache = perms
        return user_obj._group_perm_cache

    def get_all_permissions(self, user_obj):
        if user_obj.is_anonymous():
            return set()
        if not hasattr(user_obj, '_perm_cache'):
            try:
                pl = UserPermissionList.objects.get(user=user_obj)
                user_obj._perm_cache = set(pl.permission_list)

            except UserPermissionList.DoesNotExist:
                pl = None
                user_obj._perm_cache = set()

            user_obj._perm_cache.update(self.get_group_permissions(user_obj,
                                                                   pl))
        return user_obj._perm_cache

    def has_perm(self, user_obj, perm):
        return perm in self.get_all_permissions(user_obj)

    def has_module_perms(self, user_obj, app_label):
        """
        Returns True if user_obj has any permissions in the given app_label.
        """
        for perm in self.get_all_permissions(user_obj):
            if perm[:perm.index('.')] == app_label:
                return True
        return False

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class GoogleAccountBackend(NonrelPermissionBackend):
    """
    backend for authentication via Google Accounts on Google
    App Engine

    A Django auth.contrib.models.User object is linked to
    a Google Account via the password field, that stores
    the unique Google Account ID
    The Django User object is created the first time a user logs
    in with his Google Account.
    """

    def authenticate(self):
        g_user = users.get_current_user()

        if g_user == None:
            return None

        username = g_user.email().split('@')[0]

        if hasattr(settings, 'ALLOWED_USERS'):
            try:
                settings.ALLOWED_USERS.index(username)
            except ValueError:
                return None

        try:
            user = User.objects.get(password=g_user.user_id())
            if user.email is not g_user.email():
                user.email = g_user.email()
                user.username = username
                user.save()

            return user
        except User.DoesNotExist:
                user = User.objects.create_user(username,\
                                                g_user.email())
                user.password = g_user.user_id()
                if users.is_current_user_admin():
                    user.is_staff = True
                    user.is_superuser = True
                user.save()
                return user
