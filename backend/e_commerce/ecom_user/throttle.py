from rest_framework.throttling import AnonRateThrottle


class SMSAnonRateThrottle(AnonRateThrottle):
    rate = "6/minute"


class CodeSubmitAnonRateThrottle(AnonRateThrottle):
    rate = "10/minute"
