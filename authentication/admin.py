from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, attendence, leave, complaint


class CustomUserAdmin(BaseUserAdmin):
    model = User

    list_display = ('id', 'username', 'role', 'manager','is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Important Dates', {'fields': ('last_login',)}),
        ('Manager', {'fields': ('manager',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'role', 'manager', 'is_staff', 'is_active')}
        ),
    )

    search_fields = ('username',)
    ordering = ('id',)
    filter_horizontal = () 


@admin.register(attendence)
class AttendenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'date', 'status', 'manager_assigned')
    list_filter = ('status', 'date')
    search_fields = ('employee__username',)

    def manager_assigned(self, obj):
        return obj.employee.manager.username if obj.employee.manager else "No Manager"
    manager_assigned.short_description = "Manager"


@admin.register(leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'start_date', 'end_date', 'status', 'manager_assigned')
    list_filter = ('status', 'start_date', 'end_date')
    search_fields = ('employee__username',)

    def manager_assigned(self, obj):
        return obj.employee.manager.username if obj.employee.manager else "No Manager"
    manager_assigned.short_description = "Manager"


@admin.register(complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'status')
    list_filter = ('status',)
    search_fields = ('employee__username', 'complaint_text')


admin.site.register(User, CustomUserAdmin)