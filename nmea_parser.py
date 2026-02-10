"""
GPS NMEA センテンス解析モジュール
GPRMC と GPZDA に対応
"""
from datetime import datetime, timezone

class NMEAParser:
    def __init__(self):
        self.last_time = None
    
    def parse(self, sentence):
        """NMEA センテンスを解析"""
        if not sentence.startswith('$'):
            return None
        
        try:
            if sentence.startswith('$GPRMC'):
                return self._parse_gprmc(sentence)
            elif sentence.startswith('$GPZDA'):
                return self._parse_gpzda(sentence)
        except Exception:
            pass
        
        return None
    
    def _parse_gprmc(self, sentence):
        """$GPRMC,hhmmss.ss,A,lat,N,lon,E,spd,cog,ddmmyy,..."""
        parts = sentence.split(',')
        if len(parts) < 10:
            return None
        
        time_str = parts[1]  # hhmmss.ss
        status = parts[2]    # A=有効, V=無効
        date_str = parts[9]  # ddmmyy
        
        if status != 'A' or not time_str or not date_str:
            return None
        
        # 時刻パース
        hh = int(time_str[0:2])
        mm = int(time_str[2:4])
        ss = int(float(time_str[4:]))
        
        # 日付パース
        dd = int(date_str[0:2])
        month = int(date_str[2:4])
        yy = int(date_str[4:6]) + 2000
        
        dt = datetime(yy, month, dd, hh, mm, ss, tzinfo=timezone.utc)
        self.last_time = dt
        return dt
    
    def _parse_gpzda(self, sentence):
        """$GPZDA,hhmmss.ss,dd,mm,yyyy,xx,yy"""
        parts = sentence.split(',')
        if len(parts) < 5:
            return None
        
        time_str = parts[1]  # hhmmss.ss
        dd = int(parts[2])
        month = int(parts[3])
        yyyy = int(parts[4])
        
        hh = int(time_str[0:2])
        mm = int(time_str[2:4])
        ss = int(float(time_str[4:]))
        
        dt = datetime(yyyy, month, dd, hh, mm, ss, tz=timezone.utc)
        self.last_time = dt
        return dt
