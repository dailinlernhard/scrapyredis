__author__ = 'dailin'
import requests
import json
class PositionUtil(object):
    """ 根据位置信息，调用百度api获取经纬度(lat,lng)"""
    @classmethod
    def get_position(cls,position):
        """根据位置获取经纬度"""
        url = 'http://api.map.baidu.com/geocoder?address='  + position + \
              '&output=json&scope=2&ak=N57oahI2Fb1C6wDGQ4sDtZi4ch29HCtu'

        res = requests.get(url=url)
        lat = None
        lng = None

        location_info = json.loads(res.text)

        if type(location_info['result']) is dict:
            location = location_info['result']['location']

            lat = location['lat']
            lng = location['lng']

        return lat,lng

    @classmethod
    def get_detail_position(cls,lat,lng):
        """根据经纬度获取具体位置信息"""
        url = "http://api.map.baidu.com/geocoder/v2/?ak=N57oahI2Fb1C6wDGQ4sDtZi4ch29HCtu&location=" \
        + str(lat) + "," + str(lng) + "&output=json&pois=1"

        response = requests.get(url)
        detail = json.loads(response.text)

        return detail['result']['addressComponent']


if __name__ == '__main__':
    import json

    position = PositionUtil().get_position("山东圣安医药连锁有限公司海情药店")

    print(position)

    position = PositionUtil().get_detail_position(position[0],position[1])

    print(position)