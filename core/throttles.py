from rest_framework.throttling import SimpleRateThrottle


class InquiryThrottle(SimpleRateThrottle):
    scope = "inquiry"

    def get_cache_key(self, request, view):
        ident = self.get_ident(request)
        return self.cache_format % {
            "scope": self.scope,
            "ident": ident
        }


class AuthThrottle(SimpleRateThrottle):
    scope = "auth"

    def get_cache_key(self, request, view):
        ident = self.get_ident(request)
        return self.cache_format % {
            "scope": self.scope,
            "ident": ident
        }


class GlobalThrottle(SimpleRateThrottle):
    scope = "global"

    def get_cache_key(self, request, view):
        ident = self.get_ident(request)
        return self.cache_format % {
            "scope": self.scope,
            "ident": ident
        }