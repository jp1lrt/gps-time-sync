"""
Windows システム時刻同期モジュール
"""
import ctypes
import sys
from datetime import datetime

class TimeSynchronizer:
    def __init__(self):
        self.is_admin = self._check_admin()
    
    def _check_admin(self):
        """管理者権限チェック"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            return False
    
    def sync_time(self, target_time):
        """
        Windows システム時刻を同期
        target_time: datetime オブジェクト (UTC)
        """
        if not self.is_admin:
            return False, "管理者権限が必要です"
        
        try:
            # SYSTEMTIME 構造体
            class SYSTEMTIME(ctypes.Structure):
                _fields_ = [
                    ('wYear', ctypes.c_uint16),
                    ('wMonth', ctypes.c_uint16),
                    ('wDayOfWeek', ctypes.c_uint16),
                    ('wDay', ctypes.c_uint16),
                    ('wHour', ctypes.c_uint16),
                    ('wMinute', ctypes.c_uint16),
                    ('wSecond', ctypes.c_uint16),
                    ('wMilliseconds', ctypes.c_uint16),
                ]
            
            st = SYSTEMTIME()
            st.wYear = target_time.year
            st.wMonth = target_time.month
            st.wDay = target_time.day
            st.wHour = target_time.hour
            st.wMinute = target_time.minute
            st.wSecond = target_time.second
            st.wMilliseconds = target_time.microsecond // 1000
            st.wDayOfWeek = 0  # システムが自動設定
            
            # SetSystemTime を呼び出し
            result = ctypes.windll.kernel32.SetSystemTime(ctypes.byref(st))
            
            if result:
                time_str = target_time.strftime("%Y-%m-%d %H:%M:%S UTC")
                return True, f"システム時刻を {time_str} に設定しました"
            else:
                return False, "SetSystemTime が失敗しました"
            
        except Exception as e:
            return False, f"エラー: {e}"
