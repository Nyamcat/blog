from ipware.ip import get_ip
from django.utils import timezone

from .models import Visitor


class VisitorCountMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        if request.method == 'GET':
            ip = get_ip(request)
            ip_display = ip.split('.')[0] + '.' + ip.split('.')[1] + '. * . *'
            print(ip)

            try:
                visitor = Visitor.objects.get(ip=ip, date=timezone.now())

            except Exception as e:
                # 처음 블로그를 방문한 경우엔 조회 기록이 없음
                print(e)
                visitor = Visitor(ip=ip, date=timezone.now(), ip_display=ip_display)

            else:
                # 방문 기록은 있으나, 날짜가 다른 경우
                if not visitor.date == timezone.now().date():
                    visitor = Visitor(ip=ip, date=timezone.now(), ip_display=ip_display)
                # 날짜가 같은 경우
                else:
                    visitor.number_of_get_request = visitor.number_of_get_request + 1
            visitor.save()
        else:
            pass

        # Code to be executed for each request/response after
        # the view is called.

        return response
