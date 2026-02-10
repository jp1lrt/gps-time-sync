"""
NTP クライアントモジュール
"""
import socket
import struct
import time
from datetime import datetime, timezone

class NTPClient:
    def __init__(self, server='pool.ntp.org', timeout=5):
        self.server = server
        self.timeout = timeout
        self.port = 123
    
    def set_server(self, server):
        self.server = server
    
    def get_time(self):
        """NTP サーバーから時刻を取得"""
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            client.settimeout(self.timeout)
            
            # NTP パケット作成 (48 bytes, LI=0, VN=3, Mode=3)
            data = b'\x1b' + 47 * b'\0'
            
            t1 = time.time()
            client.sendto(data, (self.server, self.port))
            
            response, _ = client.recvfrom(1024)
            t4 = time.time()
            
            client.close()
            
            # NTP タイムスタンプ解析 (transmit timestamp at bytes 40-47)
            transmit_timestamp = struct.unpack('!I', response[40:44])[0]
            
            # NTP epoch (1900-01-01) から Unix epoch (1970-01-01) への変換
            NTP_DELTA = 2208988800  # 70年分の秒数
            unix_time = transmit_timestamp - NTP_DELTA
            
            ntp_time = datetime.fromtimestamp(unix_time, tz=timezone.utc)
            
            # オフセット計算 (ミリ秒)
            offset = ((t4 - t1) / 2) * 1000
            
            return ntp_time, offset
            
        except Exception as e:
            print(f"NTP error: {e}")
            return None, None
