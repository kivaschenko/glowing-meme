from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions


SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
MODIFY_METHODS = ('PUT', 'PATCH', 'DELETE')


class CustomJWTAuthentication(JWTAuthentication):
    def get_header(self, request):
        header = request.META.get("HTTP_AUTHORIZATION")
        return header

    def get_raw_token(self, header):
        """
        Extracts an unvalidated JSON web token from the given "Authorization"
        header value.
        """
        parts = header.split()
        if len(parts) == 0 or parts[0] != "Bearer":
            return None
        if len(parts) != 2:
            raise AuthenticationFailed(
                "Authorization header must contain two space-delimited values",
                code="bad_authorization_header",
            )
        return parts[1]


class IsAuthorOrReadOnly(permissions.BasePermission):
    jwt_authenticator = CustomJWTAuthentication()

    def has_permission(self, request, view):
        super().has_permission(request, view)
    def has_object_permission(self, request, view, obj):
        """
        validate token and extract user_id
        check user_id == obj.author.id
        """

        if request.method in SAFE_METHODS:
            return True
        else:
            try:
                user, _ = self.jwt_authenticator.authenticate(request)
            except Exception as e:
                return False
            if user.is_active:
                if request.method == 'POST':
                    return True
                elif request.method in MODIFY_METHODS:
                    return obj.author == user


class IsAdminOrReadonly(permissions.BasePermission):
    jwt_authenticator = CustomJWTAuthentication()

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            try:
                user, _ = self.jwt_authenticator.authenticate(request)
                return user.is_admin
            except:
                return False
