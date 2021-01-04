def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义jwt认证成功返回数据
    """

    res = {}
    res['code'] = 2000
    data = {}
    data['token'] = token
    res['data'] = data
    return res


def jwt_response_payload_error_handler(serializer, request = None):
    results = {
        "msg": "用户名或者密码错误",
        "code": 401,
        "detail": serializer.errors
    }
    return {'data': results}


#注意，脚本路径需要与settings.py 定义的一样

from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        print(response.data)
        response.data.clear()
        response.data['code'] = response.status_code

        if response.status_code == 404:
            try:
                response.data['message'] = response.data.pop('detail')
                response.data['message'] = "Not found"
            except KeyError:
                response.data['message'] = "Not found"

        if response.status_code == 400:
            response.data['code'] = 50008
            response.data['message'] = "账号或者密码错误"

        elif response.status_code == 401:
            response.data['code'] = 50008
            response.data['message'] = "Login failed, unable to get user details."

        elif response.status_code >= 500:
            response.data['message'] =  "Internal service errors"

        elif response.status_code == 403:
            response.data['message'] = "Access denied"

        elif response.status_code == 405:
            response.data['message'] = 'Request method error'
    return response