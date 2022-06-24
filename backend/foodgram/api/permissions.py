from rest_framework.permissions import BasePermission, SAFE_METHODS


class DeletePatchPutOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            (
                request.method in ('DELETE', 'PATCH', 'PUT')
                and (obj.author == request.user or request.user.is_staff)
            ) or request.method in SAFE_METHODS
        )
