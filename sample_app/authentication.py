from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # disable all CSRF protections locally - DO NOT DO THIS IN PRODUCTION
