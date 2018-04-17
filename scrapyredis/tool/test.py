import requests

from fake_useragent import UserAgent


class test:
    def getConnection(self):
        ua = UserAgent()
        userAgent = ua.random
        headers = {
            'x-signkey': '3.0.1',
            'x-origin': 'vap',
            'x-gzip': '1',
            'referer': 'https://android.weidian.com',
            'origin': 'android.weidian.com',
            'user-agent': 'Android/5.1.1 WDAPP(WDBuyer/5.0.2) VAP/1.0.7',
            'content-type': 'application/octet-stream; charset=utf-8',
            'content-length': '448',
            'accept-encoding': 'gzip'
        }
        headers = {}
        headers['User-Agent'] = userAgent
        response = requests.get(url="https://weidian.com/item.html?itemID=2228117975&wfr=wxBuyerShare", headers=headers, timeout=2)

        print(response.text)

    def post(self):
        url = 'https://yaoser.jd.com/list/catTree'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': '99',
            'Host': 'yaoser.jd.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.7.0'
        }

        d = {
            'lon': '125.3246',
            'clientType': 'android',
            'uuid': '868375033945079',
            'clientVersion': '2.1.0',
            'osVersion': '7.0',
            'lat': '43.83219'
        }
        r = requests.post(url, data=d, headers=headers)
        print(r.text)


# test = test()
# test.getConnection()


class APPCrawl(object):
    def test(self):
        import urllib3.contrib.pyopenssl
        urllib3.contrib.pyopenssl.inject_into_urllib3()
        import requests
        headers = {}
        headers['User-Agent'] = 'Dalvik/2.1.0 (Linux; U; Android 7.0; BND-AL00 Build/HONORBND-AL00)'
        response = requests.get(
            url="https://open.yaofangwang.com/app_gateway.ashx?app_key=4fb44b67d0be2af36f7135586d38d658&app_version=2.9.1&longitude=0.0&market=huawei&latitude=0.0&timestamp=2018-03-27+10%3A12%3A41&service=get_server_datetime&os=android&account_id=1527627&sign=ea3af2071dcf3070574f930090eb2d71",
            headers=headers, verify=False)
        print(response.text)

    def test1(self):
        s = requests.Session()
        headers = {}
        headers['User-Agent'] = 'Dalvik/2.1.0 (Linux; U; Android 7.0; BND-AL00 Build/HONORBND-AL00)'
        r1 = s.get('https://open.yaofangwang.com', verify=False, headers=headers)
        print(r1.text)


class APPCrawl2(object):
    def getHtml(url):
        import urllib
        import ssl

        ssl._create_default_https_context = ssl._create_unverified_context
        page = urllib.request.urlopen(url)
        html = page.read()
        html = html.decode('utf-8')
        return html



class TestCrawl(object):

    @classmethod
    def get_page(cls,url):
        import requests
        return requests.get(url)

if __name__ == '__main__':
    # response = TestCrawl.get_page("https://vap.gw.weidian.com/com.koudai.weidian.buyer/ares/item.getItemDetail/1.3")
    # print(response.text)

    test().getConnection()

# //table[@class='table table-bordered table-striped']//tr
