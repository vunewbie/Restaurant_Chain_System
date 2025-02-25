from .models import *
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

class IsOwner(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, User):
            return obj.id == request.user.id
        elif isinstance(obj, Manager):
            return obj.user.id == request.user.id
        elif isinstance(obj, Employee):
            return obj.user.id == request.user.id
        elif isinstance(obj, Customer):
            return obj.user.id == request.user.id
        else:
            raise PermissionDenied('Quyền truy cập bị từ chối')
        
class IsSameBranchManager(BasePermission):
    def has_permission(self, request, view):
        try:
            if not request.user.is_authenticated:
                raise PermissionDenied('Quyền truy cập bị từ chối')
            
            if request.user.type != 'M':
                raise PermissionDenied('Bạn không phải quản lý chi nhánh')
            
            manager = Manager.objects.get(user_id=request.user.id)

            if manager.resignation_date:
                raise PermissionDenied('Bạn đã từ chức')
            
            if manager.branch is None:
                raise PermissionDenied('Bạn chưa được phân công chi nhánh')
            
            request.branch = manager.branch
            
            return True
        
        except Exception as e:
            raise ValueError(f'Quyền truy cập bị từ chối: {str(e)}')
        
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Employee):
            if obj.branch != request.branch:
                raise PermissionDenied('Nhân viên không thuộc chi nhánh của bạn')
            
            return True
        return False
    
class IsManager(BasePermission):
    def has_permission(self, request, view):
        try:
            if not request.user.is_authenticated:
                raise PermissionDenied('Quyền truy cập bị từ chối')
            
            if request.user.type != 'M':
                raise PermissionDenied('Bạn không phải quản lý chi nhánh')
            
            manager = Manager.objects.get(user_id=request.user.id)

            if manager.resignation_date:
                raise PermissionDenied('Bạn đã từ chức')
            
            if manager.branch is None:
                raise PermissionDenied('Bạn chưa được phân công chi nhánh')
            
            request.branch = manager.branch

            return True
        
        except Exception as e:
            raise ValueError(f'Quyền truy cập bị từ chối: {str(e)}')
        
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Employee):
            return True
        return False
    
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise PermissionDenied('Quyền truy cập bị từ chối')
        
        if request.user.type != 'A':
            raise PermissionDenied('Bạn không phải chủ chuỗi nhà hàng')
        
        return True
    
    def has_object_permission(self, request, view, obj):
        return True
    
class IsEmployeeOrSameBranchManager(BasePermission):
    def has_permission(self, request, view):
        try:
            if not request.user.is_authenticated:
                raise PermissionDenied('Quyền truy cập bị từ chối')
            
            if request.user.type in ['A', 'C']:
                raise PermissionDenied('Bạn không phải nhân viên cũng như quản lý chi nhánh này')
            
            if request.user.type == 'E':
                employee = Employee.objects.get(user_id=request.user.id)

                if employee.resignation_date:
                    raise PermissionDenied('Bạn đã nghỉ việc')
                
                request.employee = employee
                
                return True
            
            if request.user.type == 'M':
                manager = Manager.objects.get(user_id=request.user.id)

                if manager.resignation_date:
                    raise PermissionDenied('Bạn đã từ chức')
                
                if manager.branch is None:
                    raise PermissionDenied('Bạn chưa được phân công chi nhánh')
                
                request.branch = manager.branch
                request.manager = manager

                return True
            
        except Employee.DoesNotExist:
            raise PermissionDenied('Nhân viên không tồn tại')
        except Manager.DoesNotExist:
            raise PermissionDenied('Quản lý không tồn tại')
        except Exception as e:
            raise ValueError(f'Quyền truy cập bị từ chối: {str(e)}')
        
        return False
    
    def has_object_permission(self, request, view, obj):
        try: 
            if isinstance(obj, User):
                return obj.id == request.user.id
            
            elif isinstance(obj, Employee):
                if obj.user.id == request.user.id:
                    return True
                
                if request.user.type == 'M' and hasattr(request, 'branch') and obj.branch == request.branch:
                    return True
            
            elif isinstance(obj, Manager):
                if obj.user.id == request.user.id:
                    return True
                
        except Exception as e:
            raise PermissionDenied(f'Quyền truy cập bị từ chối: {str(e)}')
        
        return False
    
class IsManagerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise PermissionDenied('Quyền truy cập bị từ chối')
        
        if request.user.type in ['A', 'M']:
            return True
        
        return False
    
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, User):
            if request.user.type == 'A' or obj.id == request.user.id:
                return True
            
        elif isinstance(obj, Manager):
            if request.user.type == 'A' or obj.user.id == request.user.id:
                return True

        return False
         
            