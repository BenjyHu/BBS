from django.shortcuts import redirect,reverse
from django.utils.deprecation import MiddlewareMixin


class Middleware(MiddlewareMixin):

    def process_request(self,request):
        visited_path = request.path_info
        white_list = ['/login/', '/register/', '/index/']
        if visited_path in white_list:
            return
        return redirect(reverse('login'))
