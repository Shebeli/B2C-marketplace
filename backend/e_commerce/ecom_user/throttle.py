from rest_framework.throttling import AnonRateThrottle

class SMSAnonRateThrottle(AnonRateThrottle):
    rate = '2/minute'
    
class CodeSubmitAnonRateThrottle(AnonRateThrottle):
    rate = '5/minute'