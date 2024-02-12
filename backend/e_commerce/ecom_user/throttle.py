from rest_framework.throttling import SimpleRateThrottle

class SMSThrottle(SimpleRateThrottle):
    def get_cache_key(self, request, view):
        
        return super().get_cache_key(request, view)