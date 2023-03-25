import random
import json
import hashlib
import time
import urllib.parse
import requests

class V2Ray:
    def __init__(self, ip, port, session):
        self.ip = ip
        self.port = port
        self.session = session
        self.headers = {
            "Host": f"{self.ip}:{self.port}",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
            "Cookie": f"session={self.session}"
        }

    def create_id(self):
        id = f"{str(hashlib.sha1((str(time.time()) + str(random.randint(111111, 999999))).encode('utf-8')).hexdigest())[0:8]}-" \
             f"{str(hashlib.sha1((str(time.time()) + str(random.randint(111111, 999999))).encode('utf-8')).hexdigest())[0:4]}-" \
             f"{str(hashlib.sha1((str(time.time()) + str(random.randint(111111, 999999))).encode('utf-8')).hexdigest())[0:4]}-" \
             f"{str(hashlib.sha1((str(time.time()) + str(random.randint(111111, 999999))).encode('utf-8')).hexdigest())[0:4]}-" \
             f"{str(hashlib.sha1((str(time.time()) + str(random.randint(111111, 999999))).encode('utf-8')).hexdigest())[0:12]}"
        return id

    
    def request(self, url, method=False, data=None, headers=None):
        if headers is None:
            headers = self.headers
        curl = requests.Session()
        curl.keep_alive = False
        response = curl.request(
            "POST" if method else "GET",
            url=url,
            data=data,
            headers=headers,
            timeout=10
        )
        response.close()
        result = response.text
        result = json.loads(result)
        return result

    def create_account(self, protocol, remark, total, expire=30, port=None, alert_id=1):
        url = f"http://{self.ip}:{self.port}/xui/inbound/add"
        id = self.create_id()
        if protocol == 'vmess':
            protocol = protocol
            _data = [
                f"\"alterId\":{alert_id}",
                "\"disableInsecureEncryption\":false"
            ]
        else:
            protocol = 'vless'
            _data = [
                "\"flow\":\"xtls-rprx-direct\"",
                "\"decryption\":\"none\",\"fallbacks\":[]"
            ]
        total = 1073741824 * total
        expire = (expire * 86400 + int(time.time())) * 1000
        if not port:
            port = random.randint(11111, 55555)
        data = f"up=0&down=0&total={total}&remark={remark}&enable=true&expiryTime={expire}&listen=&port={port}&protocol={protocol}&settings={{\"clients\":[{{\"id\":\"{id}\",{_data[0]}}}],{_data[1]}}}&streamSettings={{\"network\":\"ws\",\"security\":\"none\",\"wsSettings\":{{\"path\":\"/\",\"headers\":{{}}}}}}&sniffing={{\"enabled\": true,\"destOverride\":[\"http\",\"tls\"]}}"
        request = self.request(url, True, data, self.headers)
        if request['success'] is True:
            if protocol == 'vmess':
                server = f"vmess://{str(urllib.parse.quote(json.dumps({'add': self.ip, 'aid': alert_id, 'host': '', 'id': id, 'net': 'ws', 'path': '', 'port': port, 'ps': remark, 'scy': 'auto', 'sni': '', 'tls': 'none', 'type': '', 'v': '2'})))}"
            else:
                server = f"vless://{id}@{self.ip}:{port}?path=%2F&security=none&encryption=none&type=ws#{remark}"
            result = {
                "success": True,
                "time": int(expire / 1000),
                "server": server
            }
            result = json.dumps(result, ensure_ascii=False)
        else:
            result = False
        return result
    def delete_account(self, by):
        this_account = self.find_account(by)
        this_account = json.loads(this_account)
        if this_account:
            url = f"http://{self.ip}:{self.port}/xui/inbound/del/{this_account['id']}"
            result = self.request(url, True, headers=self.headers)
            result = json.dumps(result, ensure_ascii=False)
            return result
