from .permissions import IsStaffEditorPermissions
from rest_framework  import permissions

class StaffEditorPermissionsMixins():
    permission_classes = [IsStaffEditorPermissions]


class UserQuerySetMixin():
    user_field = 'user'

    def get_queryset(self , *args, **kwargs):
        lookup_data ={}
        lookup_data[self.user_field] = self.request.user
        qs = super().get_queryset(*args, **kwargs)
        
        return qs.filter(**lookup_data)