from .permissions import IsStaffEditorPermissions
from rest_framework  import permissions

class StaffEditorPermissionsMixins():
    permission_classes = [IsStaffEditorPermissions]