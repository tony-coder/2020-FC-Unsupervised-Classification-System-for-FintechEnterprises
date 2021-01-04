from django.utils.deprecation import MiddlewareMixin


class CORSMiddleware(MiddlewareMixin):

    def process_response(self,request,response):
        # 添加响应头
        # 允许相应的域名来访问，多个域名中间以逗号隔开，如果全部可使用'*'
        response['Access-Control-Allow-Origin'] = "*"
        # 允许携带的请求头，多个中间以逗号隔开
        response['Access-Control-Allow-Headers'] = "Content-Type"
        # 允许发送的请求方式
        response['Access-Control-Allow-Methods'] = "DELETE,PUT"
        return response