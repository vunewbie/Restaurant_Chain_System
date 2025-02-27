from .serializers import *
from .models import *
from .authentication import *
from .utils import *
from .permissions import *

from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from django.utils import timezone
from django.contrib.auth import login, get_user_model
import requests

# return a pair of access and refresh token when username/email and password are correct
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# validate customer registration data -> save OTP and data to cache -> send OTP to email
class CustomerCreateAPIView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data
            otp_code = create_otp()
            email = data['user']['email']

            register_data_cache(data, otp_code)
            send_registration_otp_email(email, otp_code)

            response = {
                "message": "Mã OTP đã được gửi đến email của bạn",
                "email_hash": hash_email(email)
            }

            return Response(response, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# customer retrieve and update information
class CustomerRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsOwner]
    authentication_classes = [CustomTokenAuthentication]

    def get(self, request, pk):
        customer = self.get_object()
        serializer = self.serializer_class(customer)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, pk):
        customer = self.get_object()
        
        serializer = self.serializer_class(customer, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = {
            "message": "Thông tin đã được cập nhật thành công.",
            "data": serializer.data
        }

        return Response(response, status=status.HTTP_200_OK)
  
class EmployeeListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = EmployeeSerializer
    permission_classes = [IsManager]
    authentication_classes = [CustomTokenAuthentication]

    # get all employees in the same branch as the manager without django filter
    def get_queryset(self):
        branch = getattr(self.request, 'branch', None)
        
        if branch is None:
            return Employee.objects.none()
        
        return Employee.objects.filter(branch=branch)
    
    def get(self, request):
        employees = self.get_queryset()
        serializer = self.serializer_class(employees, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    # validate employee registration data -> save OTP and data to cache -> send OTP to email
    def post(self, request):
        data = request.data.copy()

        if hasattr(request, 'branch'):
            data['branch'] = request.branch.id

        serializer = self.get_serializer(data=data)
        
        if serializer.is_valid():
            data = serializer.validated_data
            otp_code = create_otp()
            email = data['user']['email']

            register_data_cache(data, otp_code)
            send_registration_otp_email(email, otp_code)

            response = {
                "message": "Mã OTP đã được gửi đến email của bạn",
                "email_hash": hash_email(email)
            }

            return Response(response, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsEmployeeOrSameBranchManager]
    authentication_classes = [CustomTokenAuthentication]

    # get employee by id
    def get(self, request, pk):
        employee = self.get_object()
        serializer = self.serializer_class(employee)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # update employee information
    def patch(self, request, pk):
        employee = self.get_object()

        # employee can only update their own information
        if request.user.type == 'E':
            allowed_user_fields = [
                'username', 'phone_number', 'email', 'citizen_id', 
                'full_name', 'gender', 'date_of_birth', 'avatar'
            ]
            allowed_employee_fields = ['address']
        # manager can only update employee's department
        elif request.user.type == 'M':
            allowed_user_fields = []
            allowed_employee_fields = ['department']
        else:
            return Response({"detail": "Bạn không có quyền thực hiện hành động này"}, status=status.HTTP_403_FORBIDDEN)
        
        user_data = {}
        employee_data = {}

        # split user and employee data
        for key, value in request.data.items():
            if key.startswith("user."):
                user_field = key.split(".", 1)[1]
                user_data[user_field] = value
            else:
                employee_data[key] = value

        # filter out invalid fields
        user_data = {key: value for key, value in user_data.items() if key in allowed_user_fields}
        employee_data = {key: value for key, value in employee_data.items() if key in allowed_employee_fields}

        serializer = self.get_serializer(employee, data={'user': user_data, **employee_data}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = {
            "message": "Thông tin đã được cập nhật thành công.",
            "data": serializer.data
        }

        return Response(response, status=status.HTTP_200_OK)
    
    # delete employee
    def delete(self, request, pk):
        if request.user.type != 'M':
            return Response({"detail": "Bạn không có quyền thực hiện hành động này"}, status=status.HTTP_403_FORBIDDEN)

        employee = self.get_object()
        user = employee.user

        user.is_active = False
        user.save()
        employee.resignation_date = timezone.now()
        employee.save()

        return Response({"message": "Sa thải nhân viên thành công."}, status=status.HTTP_200_OK)
    
class ManagerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer
    permission_classes = [IsAdmin]
    authentication_classes = [CustomTokenAuthentication]

    # get all managers
    def get(self, request):
        managers = self.get_queryset()
        serializer = self.serializer_class(managers, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # validate manager registration data -> save OTP and data to cache -> send OTP to email
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            data = serializer.validated_data
            otp_code = create_otp()
            email = data['user']['email']

            register_data_cache(data, otp_code)
            send_registration_otp_email(email, otp_code)

            response = {
                "message": "Mã OTP đã được gửi đến email của bạn",
                "email_hash": hash_email(email)
            }

            return Response(response, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    
class ManagerRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer
    permission_classes = [IsManagerOrAdmin]
    authentication_classes = [CustomTokenAuthentication]

    # get manager by id
    def get(self, request, pk):
        manager = self.get_object()
        serializer = self.serializer_class(manager)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # update manager information
    def patch(self, request, pk):
        manager = self.get_object()

        # managers can only update their own information
        if request.user.type == 'M':
            allowed_user_fields = [
                'username', 'phone_number', 'email', 'citizen_id', 
                'full_name', 'gender', 'date_of_birth', 'avatar'
            ]
            allowed_manager_fields = ['address', 'years_of_experience']
        # admin can only update manager's branch and salary
        elif request.user.type == 'A':
            allowed_user_fields = []
            allowed_manager_fields = ['branch', 'salary']
        else:
            return Response({"detail": "Bạn không có quyền thực hiện hành động này"}, status=status.HTTP_403_FORBIDDEN)

        user_data = {}
        manager_data = {}

        for key, value in request.data.items():
            if key.startswith("user."):
                user_field = key.split(".", 1)[1]
                user_data[user_field] = value
            else:
                manager_data[key] = value

        user_data = {key: value for key, value in user_data.items() if key in allowed_user_fields}
        manager_data = {key: value for key, value in manager_data.items() if key in allowed_manager_fields}

        serializer = self.get_serializer(manager, data={'user': user_data, **manager_data}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = {
            "message": "Thông tin đã được cập nhật thành công",
            "data": serializer.data
        }

        return Response(response, status=status.HTTP_200_OK)
    
    # delete manager
    def delete(self, request, pk):
        if request.user.type != "A":
            return Response({"detail": "Bạn không có quyền thực hiện hành động này"}, status=status.HTTP_403_FORBIDDEN)
        
        manager = self.get_object()
        user = manager.user

        user.is_active = False
        user.save()
        
        manager.resignation_date = timezone.now()
        manager.save()

        return Response({"message": "Sa thải quản lý thành công"}, status=status.HTTP_200_OK)

# validate otp code -> create user -> create customer/manager/employee -> delete cache
class RegisterVerifyOTPAPIView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        otp_code = request.data.get('otp_code')
        hashed_email = hash_email(email)
        cache_key = f"register_{hashed_email}"
        cache_data = cache.get(cache_key)
        
        if cache_data:
            cache_data = json.loads(cache_data)
            if cache_data['otp_code'] == otp_code:
                data = cache_data['data']
                user = User.objects.create_user(**data['user'])
                
                if data['user']['type'] == 'C':
                    Customer.objects.create(user=user)
                elif data['user']['type'] == 'M':
                    # cache stores id not object
                    branch = Branch.objects.get(id=data['branch'])
                    Manager.objects.create(user=user, address=data['address'], years_of_experience=data['years_of_experience'], salary=data['salary'], branch=branch)
                elif data['user']['type'] == 'E':
                    department = Department.objects.get(id=data['department'])
                    branch = Branch.objects.get(id=data['branch'])
                    Employee.objects.create(user=user, address=data['address'], department=department, branch=branch)
                
                cache.delete(cache_key)
                
                return Response({"message": "Tài khoản được tạo thành công"}, status=status.HTTP_201_CREATED)
            return Response({"detail": "Mã OTP không hợp lệ"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Mã OTP hết hạn hoặc không hợp lệ"}, status=status.HTTP_400_BAD_REQUEST)

# client send hashed email -> resend otp if hashed email exists in cache 
class ResendRegisterOTPAPIView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        try:
            hashed_email = request.data.get('hashed_email')

            if not hashed_email:
                return Response({"detail": "Không có thông tin email"}, status=status.HTTP_400_BAD_REQUEST)
            
            resend_registration_otp_email(hashed_email)

            return Response({"message": "Mã OTP đã được gửi lại"}, status=status.HTTP_200_OK)
        
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"detail": "Lỗi"}, status=status.HTTP_400_BAD_REQUEST)
        
# client send username or email -> send otp to email -> cache otp code
class ForgotPasswordAPIView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username_or_email = request.data.get('username_or_email')

        if not username_or_email:
            return Response({"detail": "Vui lòng nhập tên đăng nhập/email"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(Q(username=username_or_email) | Q(email=username_or_email)).first()

        if not user:
            return Response({"detail": "Tài khoản không tồn tại"}, status=status.HTTP_400_BAD_REQUEST)
        
        otp_code = create_otp()

        forgot_password_data_cache(user.username, otp_code)

        send_forgot_password_otp_email(user.username, user.email, otp_code)

        response = {        
            "message": "Mã OTP đã được gửi đến email của bạn",
            "username": user.username
        }

        return Response(response, status=status.HTTP_200_OK)

# validate otp code -> create reset token -> return reset token
class ForgotPasswordVerifyOTPAPIView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        otp_code = request.data.get('otp_code')

        cache_key = f"forgot_password_{username}"
        cache_data = cache.get(cache_key)

        if cache_data:
            cache_data = json.loads(cache_data)
            if cache_data['otp_code'] == otp_code:
                cache.delete(cache_key)
                
                user = User.objects.filter(username=username).first()
                
                if not user:
                    return Response({"detail": "Tài khoản không tồn tại"}, status=status.HTTP_400_BAD_REQUEST)
                
                reset_token = RefreshToken.for_user(user).access_token
                response = {
                    "message": "Mã OTP hợp lệ",
                    "reset_token": str(reset_token)
                }
                
                return Response(response, status=status.HTTP_200_OK)
            
            return Response({"detail": "Mã OTP không hợp lệ"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"detail": "Mã OTP đã hết hạn hoặc không hợp lệ"}, status=status.HTTP_400_BAD_REQUEST)

# validate token -> validate new password -> reset password
class ResetPasswordAPIView(generics.GenericAPIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        if not request.user or not hasattr(request.user, 'id'):
            return Response({"detail": "Lỗi xác thực"}, status=status.HTTP_401_UNAUTHORIZED)

        user_id = request.user.id

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "Người dùng không tồn tại"}, status=status.HTTP_404_NOT_FOUND)

        new_password = request.data.get('new_password')
        
        if not new_password:
            return Response({"detail": "Hãy nhập mật khẩu mới"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"detail": "Đặt lại mật khẩu thành công"}, status=status.HTTP_200_OK)

# validate username -> send otp to email -> set new cache otp code
class ResendForgotPasswordOTPAPIView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        try:
            username = request.data.get('username')

            if not username:
                return Response({"detail": "Không tìm thấy username. Thử lại sau."}, status=status.HTTP_400_BAD_REQUEST)
            
            user = User.objects.filter(username=username).first()
            
            if not user:
                return Response({"detail": "Người dùng không tồn tại"}, status=status.HTTP_400_BAD_REQUEST)
            
            resend_forgot_password_otp_email(username)

            return Response({"detail": "Mã OTP đã được gửi lại đến email của bạn"}, status=status.HTTP_200_OK)
        
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# validate token -> validate new password -> change password
class ChangePasswordAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomTokenAuthentication]

    def post(self, request):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not old_password or not new_password:
            return Response({"detail": "Vui lòng nhập đầy đủ thông tin"}, status=status.HTTP_400_BAD_REQUEST)

        if not request.user.check_password(old_password):
            return Response({"detail": "Mật khẩu cũ không chính xác"}, status=status.HTTP_400_BAD_REQUEST)

        if old_password == new_password:
            return Response({"detail": "Mật khẩu mới phải khác mật khẩu cũ"}, status=status.HTTP_400_BAD_REQUEST)

        request.user.set_password(new_password)
        request.user.save()

        return Response({"detail": "Password has been changed successfully"}, status=status.HTTP_200_OK)

# validate refresh token -> blacklist token
class LogoutAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get('refresh')

            if not refresh_token:
                return Response({"detail": "Token lỗi."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                token = RefreshToken(refresh_token)
                token.blacklist()

                return Response({"message": "Đăng xuất thành công."}, status=status.HTTP_200_OK)

            except TokenError as e:
                return Response({"detail": f"Gặp lỗi khi đăng xuất: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"detail": f"Lỗi: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GoogleLoginAPIView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # one-time code from Google when user clicks "Sign in with Google"
        code = request.data.get("code")

        if not code:
            return Response({"error": "Không có code trả về"}, status=400)

        # send code to Google to get access token
        google_token_url = "https://oauth2.googleapis.com/token"
        params = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI,
            "client_id": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
            "client_secret": settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
        }

        token_response = requests.post(google_token_url, data=params)

        if token_response.status_code != 200:
            return Response({"error": "Lấy token thất bại"}, status=400)

        google_access_token = token_response.json().get("access_token")

        # get user info from Google
        google_user_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        user_response = requests.get(google_user_url, headers={"Authorization": f"Bearer {google_access_token}"})
        google_data = user_response.json()

        email = google_data.get("email")
        full_name = google_data.get("name")
        avatar_url = google_data.get("picture")

        if not email:
            return Response({"error": "Không lấy được email"}, status=400)

        # if user exists, log in else create new user
        user, created = User.objects.get_or_create(
            email=email,
            defaults={"username": email.split("@")[0], "full_name": full_name}
        )

        # set unusable password for social login and additional info
        if created:
            user.set_unusable_password()

            if avatar_url:
                avatar_path = download_and_save_avatar(avatar_url, email)
                if avatar_path:
                    user.avatar = avatar_path

            user.save()

        user.backend = "django.contrib.auth.backends.ModelBackend"
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")

        # generate JWT token
        refresh = RefreshToken.for_user(user)
        refresh["type"] = user.type

        return Response({
            # return essential user info and JWT token
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user_id": user.id,
            "type": user.type,
            "avatar": request.build_absolute_uri(user.avatar.url) if user.avatar else None
        })

class FacebookLoginAPIView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        code = request.data.get("code")

        if not code:
            return Response({"error": "Không lấy được code"}, status=400)

        fb_token_url = "https://graph.facebook.com/v17.0/oauth/access_token"
        params = {
            "client_id": settings.SOCIAL_AUTH_FACEBOOK_KEY,
            "client_secret": settings.SOCIAL_AUTH_FACEBOOK_SECRET,
            "redirect_uri": settings.SOCIAL_AUTH_FACEBOOK_REDIRECT_URI,
            "code": code
        }

        token_response = requests.get(fb_token_url, params=params)

        if token_response.status_code != 200:
            return Response({"error": "Không lấy được token"}, status=400)

        fb_access_token = token_response.json().get("access_token")

        fb_user_url = "https://graph.facebook.com/me?fields=id,name,email,picture"
        user_response = requests.get(fb_user_url, params={"access_token": fb_access_token})

        if user_response.status_code != 200:
            return Response({"error": "Không lấy được thông tin người dùng"}, status=400)

        fb_data = user_response.json()
        email = fb_data.get("email")
        full_name = fb_data.get("name")
        avatar_url = fb_data["picture"]["data"]["url"] if "picture" in fb_data else None

        if not email:
            return Response({"error": "Email is required"}, status=400)

        user, created = User.objects.get_or_create(
            email=email,
            defaults={"username": email.split("@")[0], "full_name": full_name}
        )

        if created:
            user.set_unusable_password()

            if avatar_url:
                avatar_path = download_and_save_avatar(avatar_url, email)
                if avatar_path:
                    user.avatar = avatar_path

            user.save()

        user.backend = "django.contrib.auth.backends.ModelBackend"
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")

        refresh = RefreshToken.for_user(user)
        refresh["type"] = user.type

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user_id": user.id,
            "type": user.type,
            "avatar": request.build_absolute_uri(user.avatar.url) if user.avatar else None
        })

class LinkedInLoginAPIView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        code = request.data.get("code")

        if not code:
            return Response({"error": "Không lấy được code"}, status=400)

        linked_in_token_url = "https://www.linkedin.com/oauth/v2/accessToken"
        params = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": settings.SOCIAL_AUTH_LINKEDIN_OAUTH2_REDIRECT_URI,
            "client_id": settings.SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY,
            "client_secret": settings.SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET,
        }

        token_response = requests.post(linked_in_token_url, data=params)

        if token_response.status_code != 200:
            return Response({"error": f"Lỗi khi lấy token: {token_response.text}"}, status=400)

        linked_in_access_token = token_response.json().get("access_token")

        user_info_url = "https://api.linkedin.com/v2/me"
        email_url = "https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))"
        headers = {"Authorization": f"Bearer {linked_in_access_token}"}
        user_response = requests.get(user_info_url, headers=headers)
        email_response = requests.get(email_url, headers=headers)

        if user_response.status_code != 200 or email_response.status_code != 200:
            return Response({"error": "Failed to fetch user info"}, status=400)

        linked_in_data = user_response.json()
        email_data = email_response.json()

        email = email_data["elements"][0]["handle~"]["emailAddress"]
        first_name = linked_in_data.get("localizedFirstName", "")
        last_name = linked_in_data.get("localizedLastName", "")
        full_name = f"{first_name} {last_name}".strip()

        avatar_elements = linked_in_data.get("profilePicture", {}).get("displayImage~", {}).get("elements", [])
        avatar_url = avatar_elements[-1]["identifiers"][0]["identifier"] if avatar_elements else None

        if not email:
            return Response({"error": "Email is required"}, status=400)

        user, created = User.objects.get_or_create(
            email=email,
            defaults={"username": email.split("@")[0], "full_name": full_name}
        )

        if created:
            user.set_unusable_password()

            if avatar_url:
                avatar_path = self.download_and_save_avatar(avatar_url, email)
                if avatar_path:
                    user.avatar = avatar_path

            user.save()

        user.backend = "django.contrib.auth.backends.ModelBackend"
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")

        refresh = RefreshToken.for_user(user)
        refresh["type"] = user.type

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user_id": user.id,
            "type": user.type,
            "avatar": request.build_absolute_uri(user.avatar.url) if user.avatar else None
        })

class GitHubLoginAPIView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        code = request.data.get("code")
        print(f"📌 Received GitHub code: {code}")

        if not code:
            print("❌ No code provided in request.")
            return Response({"error": "No code provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Step 1: Exchange code for access token
        github_token_url = "https://github.com/login/oauth/access_token"
        params = {
            "client_id": settings.SOCIAL_AUTH_GITHUB_KEY,
            "client_secret": settings.SOCIAL_AUTH_GITHUB_SECRET,
            "code": code,
            "redirect_uri": settings.SOCIAL_AUTH_GITHUB_REDIRECT_URI
        }

        headers = {"Accept": "application/json"}
        print(f"🔄 Requesting GitHub access token with params: {params}")

        token_response = requests.post(github_token_url, data=params, headers=headers)

        print(f"📥 GitHub token response status: {token_response.status_code}")
        print(f"📥 GitHub token response body: {token_response.json()}")

        if token_response.status_code != 200:
            return Response({"error": "Failed to exchange code for token"}, status=status.HTTP_400_BAD_REQUEST)

        github_access_token = token_response.json().get("access_token")
        print(f"✅ Received GitHub access token: {github_access_token}")

        # Step 2: Fetch user profile from GitHub
        github_user_url = "https://api.github.com/user"
        github_email_url = "https://api.github.com/user/emails"

        headers = {"Authorization": f"Bearer {github_access_token}"}

        print("🔄 Requesting GitHub user profile...")
        user_response = requests.get(github_user_url, headers=headers)

        if user_response.status_code != 200:
            return Response({"error": "Failed to fetch user info"}, status=status.HTTP_400_BAD_REQUEST)

        github_data = user_response.json()
        email = github_data.get("email")
        full_name = github_data.get("name") or github_data.get("login")
        avatar_url = github_data.get("avatar_url")

        # Nếu email không có trong dữ liệu user, cần lấy email từ API email của GitHub
        if not email:
            print("🔄 Requesting GitHub user email...")
            email_response = requests.get(github_email_url, headers=headers)

            if email_response.status_code == 200:
                emails = email_response.json()
                primary_email = next((e["email"] for e in emails if e["primary"] and e["verified"]), None)
                email = primary_email or (emails[0]["email"] if emails else None)

        print(f"📌 Extracted user info - Email: {email}, Full Name: {full_name}, Avatar URL: {avatar_url}")

        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Step 3: Create or get user
        user, created = User.objects.get_or_create(
            email=email,
            defaults={"username": email.split("@")[0], "full_name": full_name}
        )

        if created:
            print(f"🆕 Creating new user: {email}")
            user.set_unusable_password()

            if avatar_url:
                print(f"📥 Downloading avatar from: {avatar_url}")
                avatar_path = download_and_save_avatar(avatar_url, email)
                if avatar_path:
                    user.avatar = avatar_path

            user.save()

        user.backend = "django.contrib.auth.backends.ModelBackend"
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")

        # Step 4: Generate JWT token
        refresh = RefreshToken.for_user(user)
        refresh["type"] = user.type

        print(f"✅ User logged in - Email: {email}, Token generated.")

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user_id": user.id,
            "type": user.type,
            "avatar": request.build_absolute_uri(user.avatar.url) if user.avatar else None
        })








