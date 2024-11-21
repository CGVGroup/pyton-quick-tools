import psutil
import GPUtil
import time
import datetime
import argparse
import os

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Log system usage to a specified file.")
parser.add_argument("--output", type=str, help="Full path to the output file (e.g., C:\\logs\\system_usage_log.csv)")
parser.add_argument("--process_name", type=str, help="Name of the process to monitor (e.g., chrome.exe)")
args = parser.parse_args()

output_file = args.output
if output_file is None:
    print('No output file has been defined with the --output argument')
    output_file = './system_profiling_output.csv'
    

process_name = args.process_name

print(f'Looging system info to:{output_file}')
print(f'Profiling process:{process_name}')

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Function to get GPU information
def get_gpu_info():
    gpus = GPUtil.getGPUs()
    if gpus:
        gpu = gpus[0]  # Assuming one GPU; extend for multiple GPUs if needed
        return gpu.load * 100, gpu.memoryUsed, gpu.memoryTotal
    return None, None, None

# Function to find a process by name
def find_process_by_name(name):
    """Find a process by its name and return its psutil.Process object."""
    for proc in psutil.process_iter(attrs=["pid", "name"]):
        try:
            if proc.info["name"] == name:
                return psutil.Process(proc.info["pid"])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return None

# Write header to file
if not os.path.exists(output_file):
    with open(output_file, "w") as f:
        f.write("Timestamp,Process_Found,Process_CPU,Process_RAM_Usage,Total_CPU_Usage,Per_CPU_avg,Per_CPU_avg_no_zeros,Total_RAM_Usage,GPU_Usage,GPU_Memory_Used,GPU_Memory_Total\n")

# Log data periodically
sampling_interval = 0.5
try:
    while True:
        # Check if a specific process is provided and available
        if process_name:
            process = find_process_by_name(process_name)
            if process:
                try:
                    process_cpu = process.cpu_percent(interval=sampling_interval) # CPU usage percentage
                    process_memory = process.memory_info().rss / (1024 * 1024)  # Memory usage in MB
                    process_found = "Yes"
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    process_cpu = process_memory = None
                    process_found = "No"
            else:
                process_cpu = process_memory = None
                process_found = "No"
        else:
            process_cpu = process_memory = None
            process_found = "N/A"
        
        # Get total system information
        total_cpu = psutil.cpu_percent(sampling_interval)
        total_ram = psutil.virtual_memory().percent

        percpu_usage = psutil.cpu_percent(sampling_interval, percpu=True)
        average_cpu = sum(percpu_usage) / len(percpu_usage)

        filtered_cpu_usage = [value for value in percpu_usage if value > 0]
        if len(filtered_cpu_usage) > 0:
            average_no_zeros_cpu = sum(filtered_cpu_usage) / len(filtered_cpu_usage)
        else:
            average_no_zeros_cpu = 0.0


        gpu_usage, gpu_memory_used, gpu_memory_total = get_gpu_info()

        # Create a timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Write to file
        
        with open(output_file, "a") as f:
            f.write(
                f"{timestamp},{process_found},{process_cpu or 'N/A'},{process_memory or 'N/A'},{total_cpu},{average_cpu},{average_no_zeros_cpu},{total_ram},{gpu_usage or 'N/A'},{gpu_memory_used or 'N/A'},{gpu_memory_total or 'N/A'}\n"
            )
        
        
        # Print to console
        gpu_usage_str = f"{gpu_usage:.2f}%" if gpu_usage is not None else 'N/A'
        
        if process_found == "Yes":
            
            print(
                f"{timestamp} | Process: {process_name} FOUND | CPU: {process_cpu:.2f}% | RAM: {process_memory:.2f} MB | Total CPU: {total_cpu}% | xCPU avg: {average_cpu:.2f}% | xCPU avg (no-0): {average_no_zeros_cpu:0.2f} | Total RAM: {total_ram}% | GPU: {gpu_usage_str} | GPU Mem: {gpu_memory_used or 'N/A'}/{gpu_memory_total or 'N/A'} MB"
            )
        elif process_found == "No":
            print(f"{timestamp} | Process: {process_name} NOT FOUND | Total CPU: {total_cpu}% | xCPU avg: {average_cpu:.2f}% | xCPU avg (no-0): {average_no_zeros_cpu:0.2f} | Total RAM: {total_ram}% | GPU: {gpu_usage_str} | GPU Mem: {gpu_memory_used or 'N/A'}/{gpu_memory_total or 'N/A'} MB")
        else:
            print(f"{timestamp} | Monitoring entire system | Total CPU: {total_cpu}% | xCPU avg: {average_cpu:.2f}% | xCPU avg (no-0): {average_no_zeros_cpu:0.2f} | Total RAM: {total_ram}% | GPU: {gpu_usage_str} | GPU Mem: {gpu_memory_used or 'N/A'}/{gpu_memory_total or 'N/A'} MB")
        
        
        time.sleep(sampling_interval)

except KeyboardInterrupt:
    print("Logging stopped.")
