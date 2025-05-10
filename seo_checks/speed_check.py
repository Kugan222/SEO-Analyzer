import requests
import time

def check_speed(url):
    try:
        start_time = time.time()
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        end_time = time.time()
        
        load_time = round(end_time - start_time, 2)  # in seconds
        status = "Fast" if load_time < 2 else "Moderate" if load_time < 4 else "Slow"
        
        return {
            "load_time_seconds": load_time,
            "speed_status": status
        }
    except Exception as e:
        return {
            "load_time_seconds": None,
            "speed_status": f"Error: {e}"
        }
