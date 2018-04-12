1. settings中增加JZBHTTP_CACHE = 'django.core.cache'
2. 导入包 from jzbhttp.httpservice import HttpService
3. HttpService().get(url="")
