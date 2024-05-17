from rest_framework.throttling import AnonRateThrottle

class SMSAnonRateThrottle(AnonRateThrottle):
    rate = '25/minute'
    
class CodeSubmitAnonRateThrottle(AnonRateThrottle):
    rate = '5/minute'