from rest_framework.throttling import SimpleRateThrottle

class NormalThrottle(SimpleRateThrottle):
    """匿名用户根据 IP 限制每分钟访问 3 次"""
    scope = 'Hubery'
    def get_cache_key(self, request, view):
        if request.user:
            return None
        return self.get_ident(request)


class UserThrottle(SimpleRateThrottle):
    """登录用户限制每分钟可以访问 10 次"""
    scope = 'Jun'       # 随便定义
    def get_cache_key(self, request, view):
        if not request.user:
            return None
        return request.user.username