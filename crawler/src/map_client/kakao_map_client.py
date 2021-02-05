import requests
class KakaoMapClient:
    def __init__(self):
        self.kakao_map_url = "https://dapi.kakao.com/v2/local/search/address.json"

    def get_latitude_and_longitudes(self, pharmacies):
        searched_pharamacies = []
        for pharmacy in pharmacies:
            (latitude, longitude) = self.get_latitude_and_longitude(pharmacy[1])
            pharmacy.append(latitude)
            pharmacy.append(longitude)
            searched_pharamacies.append(pharmacy)
        return searched_pharamacies



    def get_latitude_and_longitude(self, addr):
        # parse addr by road name

        parsed_addr=""
        for idx, entity in reversed(list(enumerate(addr.split()))):
            if ("로" in entity) or ("길" in entity):
                parsed_addr = " ".join(addr.split()[:(idx+2)])
        print("searching address : " + parsed_addr)
        query_pharams = {
            'query': parsed_addr,
            'analyze_type': 'similar',
            'page': 1,
            'size': 10
        }

        auth_header = {
            'Authorization': 'KakaoAK ' + 'bd90571519a564f9fdd75a7a001ce148'
        }

        response = requests.get(self.kakao_map_url, params=query_pharams, headers=auth_header)
        latitude = "0"
        longitude = "0"
        try:
            response_addr = response.json()["documents"][0]["address"]
            latitude=response_addr["y"]
            longitude=response_addr["x"]
        except:
            print("no info : " + parsed_addr)
        # print("longitude: " + longitude + "latitude: " + latitude)
        return (latitude, longitude)

