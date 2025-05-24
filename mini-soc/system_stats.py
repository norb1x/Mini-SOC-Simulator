#optional !!

import subprocess
import psutil

def get_cpu_temp():
    # Get CPU temperature from Raspberry Pi using vcgencmd command
    result = subprocess.run(['vcgencmd', 'measure_temp'], stdout=subprocess.PIPE, text=True)
    temp_str = result.stdout
    temp = float(temp_str.replace("temp=", "").replace("'C\n", ""))
    return temp

def get_ram_usage_percent():
    # Get RAM usage percent via psutil
    return psutil.virtual_memory().percent
