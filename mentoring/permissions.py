from rest_framework.permissions import IsAuthenticated

class IsAuthenticatedMentee(IsAuthenticated):
    """
    Custom permission class that requires the user to be authenticated and have the 'mentee' role.
    """
    
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not super().has_permission(request, view):
            return False  # The user is not authenticated

        # Check if the user's role is 'mentee'
        user = request.user
        return user.role == 'mentee'


class IsAuthenticatedMentor(IsAuthenticated):
    """
    Custom permission class that requires the user to be authenticated and have the 'mentee' role.
    """
    
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not super().has_permission(request, view):
            return False  # The user is not authenticated

        # Check if the user's role is 'mentee'
        user = request.user
        return user.role == 'mentor'