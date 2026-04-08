from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response        
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import attendence
from .models import leave
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

@csrf_exempt
@api_view(['POST'])
def signup(request):
    username = request.data.get("username")
    password = request.data.get("password")
    role = request.data.get("role", "").lower()
    manager_id=request.data.get("manager_id")

    if User.objects.filter(username=username).exists():
        return Response({"message": "Username already exists!"}, status=status.HTTP_400_BAD_REQUEST)
    
    manager = None
    if role == 'employee' and manager_id:
        manager = User.objects.filter(id=manager_id, role='manager').first()
        if not manager:
            return Response({"message": "Manager does not exist!"}, status=status.HTTP_400_BAD_REQUEST)
        
    if role != 'employee':
        manager = None
    

    user = User.objects.create_user(
        username=username,
        password=password,
        role=role,
        manager=manager
    )
    if manager:
        manager_info=manager.username
    else:
        manager_info="no_manager"

    return Response({"message": f"User {username} created successfully!and the manager id of this user {manager_info}"}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get("username")
    password = request.data.get("password")
    db_user = User.objects.filter(username=username).first()

    if db_user is None:
        return Response({"message": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

    print("username from request:", repr(username))
    print("password from request:", repr(password))
    print("stored hash:", db_user.password)
    print("check_password:", db_user.check_password(password))

    user = authenticate(request, username=username, password=password)

    
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)

        return Response({"message": f"User {username} logged in successfully! {token}"}, status=status.HTTP_200_OK)
    
    return Response({"message": "Invalid credentials!"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_attendence(request):
    user=request.user
    date=request.data.get('date')
    status=request.data.get('status')

    Attendence, created= attendence.objects.get_or_create(employee=user, date=date)
    Attendence.status=status
    Attendence.save()

    return Response({"message": f"Attendence for {user.username} on {date} marked as {status}"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def apply_leave(request):
    user=request.user
    start_date=request.data.get('start_date')
    end_date=request.data.get('end_date')
    reason=request.data.get('reason')

    Leave=leave.objects.create(employee=user, start_date=start_date, end_date=end_date, reason=reason, status='pending')
    return Response({"message": "Leave applied successfully", "leave_id": Leave.id},status=status.HTTP_201_CREATED)

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def approve_leave(request, leave_id):
    Leave=leave.objects.get(id=leave_id)
    print("request.user:", request.user)
    print("username:", request.user.username)
    print("role:", request.user.role)
    print("leave applicant:", Leave.employee.username)
    print("leave applicant role:", Leave.employee.role)
    if request.user.role in ['admin', 'manager','employee']:
        Leave.status='approved'
        Leave.save()
        return Response({"message": f"Leave for {Leave.employee.username} approved!"}, status=status.HTTP_200_OK)
    
    return Response({"message": "Unauthorized!"}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_leave_history(request):
    user = request.user

    Leaves = leave.objects.filter(employee=user).order_by('-start_date')

    data = []
    for item in Leaves:
        data.append({   
            "leave_id": item.id,
            "start_date": item.start_date,
            "end_date": item.end_date,
            "reason": item.reason,
            "status": item.status,
        })

    return Response(
        {
            "message": f"Leave history for {user.username}",
            "total_leaves": len(data),
            "leaves": data
        },
        status=status.HTTP_200_OK
    )

# @csrf_exempt
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def associate_emplyee(request, user_id, manager_id):
#     Associate_users=User.objects.get(id=user_id, id=manager_id)
# if User.objects.filter(user, password).exists():
#         # user_id belongs to this user
#         return Response ({"user of this belongs or have a team memer of this manager field"})
# retun Response({"managers or user not exist"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def associate_employee(request):
    # if request.user.role not in ['admin', 'manager']:
    #     return Response(  
    #         {"message": "Only admin or manager can associate employees."},status=status.HTTP_403_FORBIDDEN)
    user_id = request.data.get('user_id')
    manager_id = request.data.get('manager_id')

    if not user_id or not manager_id:
        return Response(
            {"message": "user_id and manager_id are required."},status=status.HTTP_400_BAD_REQUEST)

    employee = User.objects.filter(id=user_id, role='employee').first()
    manager = User.objects.filter(id=manager_id, role='manager').first()

    print(f"Employee:{employee}")
    print(f"Manager:{manager}")

    if not employee or not manager:
        return Response(
            {"message": "Manager or employee does not exist."},
            status=status.HTTP_404_NOT_FOUND
        )

    employee.manager = manager
    employee.save()

    return Response(
        {
            "message": f"Employee {employee.username} is now assigned to manager {manager.username}.",
            "employee_id": employee.id,
            "employee_username": employee.username,
            "manager_id": manager.id,
            "manager_username": manager.username,
        },
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def manager_attendance_history(request):
    user = request.user

    if user.role != 'manager':
        return Response({"message": "Unauthorized! You must be a manager to view this."}, status=status.HTTP_403_FORBIDDEN)

    employees = User.objects.filter(manager=user)

    attendance_records = attendence.objects.filter(employee__in=employees)

    data = []
    for record in attendance_records:
        data.append({
            "employee": record.employee.username,
            "date": record.date,
            "status": record.status
        })

    return Response({
        "message": "Attendance records fetched successfully.",
        "attendance": data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def manager_leave_history(request):
    user = request.user

    if user.role != 'manager':
        return Response({"message": "Unauthorized! You must be a manager to view this."}, status=status.HTTP_403_FORBIDDEN)

    employees = User.objects.filter(manager=user)

    leave_records = leave.objects.filter(employee__in=employees)

    data = []
    for record in leave_records:
        data.append({
            "employee": record.employee.username,
            "start_date": record.start_date,
            "end_date": record.end_date,
            "reason": record.reason,
            "status": record.status
        })

    return Response({
        "message": "Leave records fetched successfully.",
        "leaves": data
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def associate_employee_admin(request):
    if request.user.role != 'admin':
        return Response({"message": "Unauthorized! Only admins can assign employees to managers."}, 
                        status=status.HTTP_403_FORBIDDEN)

    employee_id = request.data.get('employee_id')
    manager_id = request.data.get('manager_id')

    try:
        employee = User.objects.get(id=employee_id, role='employee')
        manager = User.objects.get(id=manager_id, role='manager')
    except User.DoesNotExist:
        return Response({"message": "Employee or Manager does not exist!"}, status=status.HTTP_404_NOT_FOUND)

    employee.manager = manager
    employee.save()

    return Response({"message": f"Employee {employee.username} is now associated with manager {manager.username}."}, 
                    status=status.HTTP_200_OK)