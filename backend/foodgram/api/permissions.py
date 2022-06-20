from rest_framework.permissions import BasePermission


class DeletePatchPutIsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            (request.method in ('DELETE', 'PATCH', 'PUT')
             and obj.author == request.user)
            or request.user.is_authenticated
        )
