from django import template
import math

register = template.Library()

@register.filter
def format_duration(duration):
    """將分鐘數格式化為 MM:SS 格式"""
    if duration is None:
        return "0:00"
    
    minutes = math.floor(duration)
    seconds = math.round((duration - minutes) * 60)
    
    # 確保秒數在 0-59 範圍內
    if seconds >= 60:
        minutes += 1
        seconds = 0
    
    return f"{minutes}:{seconds:02d}"
