import time
from pynvml import *
import json
from os.path import join, dirname
from typing import *
import requests

def send_message(message):
    url = "https://open.feishu.cn/open-apis/bot/v2/hook/1a8ad0b2-15cf-4926-a24f-a02f4cc9c984"
    json_data = {"msg_type": "text", "content": {"text": message}}
    try:
        r = requests.post(url, data=json.dumps(json_data))
    except Exception:
        print("POST ERROR")

def monitor():
    # Initialize NVML
    nvmlInit()

    # Get the number of GPUs
    device_count = nvmlDeviceGetCount()

    # Check if there are at least 4 GPUs
    if device_count < 4:
        print("Warning: Less than 4 GPUs detected")

    try:
        while True:
            gpu_usages = []
            # Monitor the last 4 GPUs
            for i in range(device_count - 4, device_count):
                try:
                    # Get handle to the GPU
                    handle = nvmlDeviceGetHandleByIndex(i)

                    # Get GPU utilization
                    util = nvmlDeviceGetUtilizationRates(handle)


                    # If GPU utilization is 0, print a warning
                    if util.gpu == 0:
                        print(f"Warning: GPU {i} is not being used")
                        gpu_usages.append(0)
                    else:
                        # Print GPU utilization
                        print(f"GPU {i} utilization: {util.gpu}%")
                        gpu_usages.append(1)

                except NVMLError as error:
                    # Print error message if an error occurs
                    print(f"Failed to get utilization for GPU {i}: {error}")
                time.sleep(1)

            if gpu_usages.count(0) > 2:
                send_message("two gpus are down!")
                # Wait for a second before the next iteration
            time.sleep(1800)
    except:
        # Shutdown NVML
        pass
    finally:
        print("nvml shut down!")
        nvmlShutdown()
        
        
if __name__ == "__main__":
    monitor()