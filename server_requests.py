import requests

def get_server(url):
    response = requests.get(url + "servers-open")
    json_data = response.json();
    servers = []
    for server in  json_data['data']:
        server_obj = {
            'servercode': server['ServerCode'],
            'servername': server['ServerName'],
            'serverstatus':server['IsActive']
            }
        servers.append(server_obj)

    return servers


def get_data(server, url):
        response = requests.get(url+'stations-open?serverCode='+ server)
        json_data =  response.json();
        stations = []
        for station in json_data['data']:
            station_obj = {
                'name': station['Name'],
                'available': len(station["DispatchedBy"]) == 0
            }
            stations.append(station_obj)
        return stations

