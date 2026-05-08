import requests

BASE_RUL_GEO='https://api.openweathermap.org/geo/1.0/direct' 
BASE_URL_WEATHER='https://api.openweathermap.org/data/2.5/weather'
API_KEY='8cec5208ef8f7ba6b5b918721b8bc20e'

def get_coordinates(city):
    """"用城市名获取经纬度"""
    params={
        'q':f'{city},CN',
        'limit':5,
        'appid':API_KEY
    }

    response=requests.get(BASE_RUL_GEO,params=params,timeout=10)
    response.raise_for_status()

    data=response.json()

    if not data:
        return None,None

    lat=data[0]['lat']
    lon=data[0]['lon']
    return lat,lon


def get_weather(lat,lon):
    """"用经纬度获取天气"""
    params={
        'lat':lat,
        'lon':lon,
        'appid':API_KEY,
        'units':'metric',
        'lang':'zh_cn'
    }
    
    response=requests.get(BASE_URL_WEATHER,params=params,timeout=10)
    response.raise_for_status()

    data=response.json()

    temp=data['main']['temp']
    description=data['weather'][0]['description']

    return temp,description

def weather_search():
    """"主函数：交互式查询天气"""
    while True:
        city=input('输入您想查询的城市(如四川),输入quit则退出:')
        if city.lower() == 'quit':
            print("再见咯")
            break

        if not city.strip():
            print("城市名不能为空")
            continue
        
        try:
            lat,lon=get_coordinates(city)
           
            if lat is None:
                print(f'未找到城市{city},请检查后再试')
                continue
            
            temp,description=get_weather(lat,lon)
            
            print(f"{city}的天气情况如下：{temp}℃,{description}")

        except requests.exceptions.Timeout:
            print("请求超时，请稍后再试")
            continue
        except requests.exceptions.ConnectionError:
            print("网络连接失败，请检查网络之后再试")
            continue
        except requests.exceptions.HTTPError as e:
            # raise_for_status() 抛出的异常在这里捕获
            print(f"HTTP 错误：{e}")
            continue
        except requests.exceptions.RequestException as e:
            print(f"请求出错：{e}")
            continue

        
if __name__ == "__main__":
    weather_search()