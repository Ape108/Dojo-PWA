from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Intercepts the login process right after the user has authenticated
        with the social provider, but before the login is finalized.
        This helps connect existing users who first signed up with a password.
        """
        User = get_user_model()
        email = sociallogin.account.extra_data.get('email')

        # If the user is already logged in, just proceed.
        if sociallogin.is_existing:
            return

        # Check if a user with this email already exists.
        if email:
            try:
                user = User.objects.get(email=email)
                # If we find an existing user, we connect the social account to them.
                sociallogin.connect(request, user)
            except User.DoesNotExist:
                # If no user is found, the regular signup process will continue.
                pass
