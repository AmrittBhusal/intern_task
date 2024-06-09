from rest_framework.permissions import BasePermission

class IsSuppervisor(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role=='suppervisor'
    


class IsIntern(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'intern'