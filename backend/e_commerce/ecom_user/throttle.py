from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

class SMSAnonRateThrottle(AnonRateThrottle):
    rate = '2/minute'
    
class RegisterAnonRateThrottle(AnonRateThrottle):
    rate = '5/minute'