import json, datetime, os
from nextcloud_client import Client
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException

class BaseServer:

    def __init__(self, config):
        self.url_map = Map(
            [
                Rule("/upload/home", endpoint="index"),
                Rule("/upload", endpoint="upload"),
            ]
        )
        # 连接文件服务
        self.nextCloud = Client(config['NEXTCLOUD_URL'])
        self.config = config


    def on_index(self, request):
        data = {"name": "my upload", "cloud": "nextCloud"}
        return self.render_json(data)

    def on_upload(self, request):
        result = {"link_url": "无权上传!"}
        file_data = request.files['file']
        # 权限认证
        upload_key = request.form.get("upload_key", None)
        if upload_key is None or upload_key != "szhu9903gmail":
            return self.render_json(result)
        # 登录
        self.nextCloud.login(self.config['NEXTCLOUD_USER'], self.config['NEXTCLOUD_PWD'])
        # 文件保存位置 文件名
        now_date = datetime.datetime.now()
        file_name = now_date.strftime("%Y%m%d%H%M%S%f") + file_data.filename
        save_path = os.path.join(self.config['BLOG_IMAGES'], file_name)
        # 上传文件，获取共享连接
        self.nextCloud.put_file_contents(save_path, file_data)
        link_info = self.nextCloud.share_file_with_link(save_path)

        result['link_url'] = f'{link_info.get_link()}/preview'
        return self.render_json(result)

    def render_json(self, data):
        response_data = json.dumps(data)
        return Response(response_data, mimetype="application/json")

    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return getattr(self, f'on_{endpoint}')(request, **values)
        except HTTPException as Err:
            return Err

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


