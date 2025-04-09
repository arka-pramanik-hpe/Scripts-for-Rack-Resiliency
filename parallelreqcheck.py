#!/usr/bin/env python3
import subprocess
import time
import multiprocessing
import csv
from datetime import datetime
import random
import os
import json

# Commands to execute
commands = [
    "cray rrs zones list",
    "cray rrs zones describe cscs-rack-x3001",
    "cray rrs zones describe cscs-rack-x3000",
    "cray rrs zones describe cscs-rack-x3002",
    "cray rrs criticalservices list",
    "cray rrs criticalservices describe cray-hbtd",
    "cray rrs criticalservices describe cray-keycloak",
    "cray rrs criticalservices describe cray-spire-server",
    "cray rrs criticalservices describe coredns",
    "cray rrs criticalservices describe kube-multus-ds",
    "cray rrs criticalservices status list",
    "cray rrs criticalservices status describe cray-hmnfd",
    "cray rrs criticalservices status describe cray-spire-server",
    "cray rrs criticalservices status describe coredns",
    "cray rrs criticalservices status describe kube-multus-ds",
    "cray rrs criticalservices status describe cray-keycloak",
]

# Output directory
output_dir = "api_output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Results CSV file
results_file = f"{output_dir}/performance_results.csv"
log_file = f"{output_dir}/execution_log.txt"

def log_message(message):
    """Log a message to the log file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def execute_command(task_info):
    """Execute a command and return the execution time and result"""
    cmd = task_info["command"]
    request_id = task_info["request_id"]
    output_file = f"{output_dir}/request_{request_id}.txt"
    
    start_time = time.time()
    try:
        # Execute the command - compatible with older Python versions
        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True  # This is equivalent to text=True in newer Python
        )
        
        try:
            stdout, stderr = process.communicate(timeout=60)
            return_code = process.returncode
            
            # Calculate execution time
            execution_time = time.time() - start_time
            
            # Save output to file
            with open(output_file, "w") as f:
                f.write(f"COMMAND: {cmd}\n")
                f.write(f"STDOUT:\n{stdout}\n")
                f.write(f"STDERR:\n{stderr}\n")
                f.write(f"RETURN CODE: {return_code}\n")
                f.write(f"EXECUTION TIME: {execution_time:.4f} seconds\n")
            
            return {
                "request_id": request_id,
                "command": cmd,
                "execution_time": execution_time,
                "status": "success" if return_code == 0 else "error",
                "return_code": return_code,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        except subprocess.TimeoutExpired:
            # Kill the process if it times out
            process.kill()
            process.communicate()
            
            execution_time = time.time() - start_time
            with open(output_file, "w") as f:
                f.write(f"COMMAND: {cmd}\n")
                f.write("TIMEOUT: Command execution timed out after 60 seconds\n")
                f.write(f"EXECUTION TIME: {execution_time:.4f} seconds\n")
            
            return {
                "request_id": request_id,
                "command": cmd,
                "execution_time": execution_time,
                "status": "timeout",
                "return_code": -1,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
    except Exception as e:
        execution_time = time.time() - start_time
        with open(output_file, "w") as f:
            f.write(f"COMMAND: {cmd}\n")
            f.write(f"ERROR: {str(e)}\n")
            f.write(f"EXECUTION TIME: {execution_time:.4f} seconds\n")
        
        return {
            "request_id": request_id,
            "command": cmd,
            "execution_time": execution_time,
            "status": "exception",
            "return_code": -2,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

def result_writer(result_queue):
    """Process to continuously write results to CSV from the queue"""
    with open(results_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["request_id", "command", "execution_time", "status", "return_code", "timestamp"])
    
    while True:
        result = result_queue.get()
        if result == "DONE":
            break
            
        with open(results_file, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                result["request_id"],
                result["command"],
                result["execution_time"],
                result["status"],
                result["return_code"],
                result["timestamp"]
            ])

def generate_tasks(total_requests):
    """Generate a list of tasks with random commands"""
    tasks = []
    for i in range(total_requests):
        # Select a random command from the list
        cmd = random.choice(commands)
        tasks.append({
            "command": cmd,
            "request_id": i+1
        })
    return tasks

def main():
    total_requests = 1000
    # Get CPU count safely for older Python versions
    try:
        cpu_count = multiprocessing.cpu_count()
    except NotImplementedError:
        cpu_count = 4  # Default to 4 if we can't detect
    
    max_processes = min(cpu_count * 2, 50)  # Use 2x CPU cores but cap at 50
    
    log_message(f"Total CPU cores detected: {cpu_count}")
    log_message(f"Max processes set to: {max_processes}")
    log_message(f"Total requests to execute: {total_requests}")
    log_message(f"Starting parallel execution of {total_requests} API requests with {max_processes} processes")
    print(f"Starting {total_requests} requests using {max_processes} parallel processes...")
    
    # Set up multiprocessing components
    manager = multiprocessing.Manager()
    result_queue = manager.Queue()
    
    # Start the result writer process
    writer_process = multiprocessing.Process(target=result_writer, args=(result_queue,))
    writer_process.start()
    
    # Generate all tasks
    tasks = generate_tasks(total_requests)
    
    # Start timing
    start_time = time.time()
    
    # Create process pool and execute tasks
    with multiprocessing.Pool(processes=max_processes) as pool:
        # Use imap_unordered to process results as they arrive
        completed = 0
        for result in pool.imap_unordered(execute_command, tasks):
            result_queue.put(result)
            completed += 1
            
            # Log progress periodically
            if completed % 100 == 0:
                log_message(f"Completed {completed} requests")
                print(f"Progress: {completed}/{total_requests} requests completed")
    
    # Signal the result writer to finish
    result_queue.put("DONE")
    writer_process.join()
    
    total_time = time.time() - start_time
    
    # Read results for analysis
    results = []
    with open(results_file, "r", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            results.append({
                "request_id": int(row["request_id"]),
                "command": row["command"],
                "execution_time": float(row["execution_time"]),
                "status": row["status"],
                "return_code": int(row["return_code"]),
                "timestamp": row["timestamp"]
            })
    
    # Calculate statistics
    success_count = sum(1 for r in results if r["status"] == "success")
    error_count = sum(1 for r in results if r["status"] == "error")
    timeout_count = sum(1 for r in results if r["status"] == "timeout")
    exception_count = sum(1 for r in results if r["status"] == "exception")
    
    execution_times = [r["execution_time"] for r in results]
    avg_time = sum(execution_times) / len(execution_times) if execution_times else 0
    min_time = min(execution_times) if execution_times else 0
    max_time = max(execution_times) if execution_times else 0
    
    # Generate summary stats file
    stats = {
        "total_requests": total_requests,
        "total_time_seconds": total_time,
        "requests_per_second": total_requests / total_time if total_time > 0 else 0,
        "success_count": success_count,
        "error_count": error_count,
        "timeout_count": timeout_count,
        "exception_count": exception_count,
        "avg_execution_time": avg_time,
        "min_execution_time": min_time,
        "max_execution_time": max_time
    }
    
    with open(f"{output_dir}/summary_stats.json", "w") as f:
        json.dump(stats, f, indent=2)
    
    # Log final statistics
    log_message(f"Completed all {total_requests} requests in {total_time:.2f} seconds")
    log_message(f"Success: {success_count}, Errors: {error_count}, Timeouts: {timeout_count}, Exceptions: {exception_count}")
    log_message(f"Average execution time: {avg_time:.4f} seconds")
    log_message(f"Min execution time: {min_time:.4f} seconds")
    log_message(f"Max execution time: {max_time:.4f} seconds")
    
    # Print summary
    print(f"\nExecution Summary:")
    print(f"Total requests: {total_requests}")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Requests per second: {total_requests / total_time:.2f}")
    print(f"Success: {success_count}, Errors: {error_count}, Timeouts: {timeout_count}, Exceptions: {exception_count}")
    print(f"Average execution time: {avg_time:.4f} seconds")
    print(f"Min execution time: {min_time:.4f} seconds")
    print(f"Max execution time: {max_time:.4f} seconds")
    print(f"\nResults saved to: {results_file}")
    print(f"Individual outputs saved to: {output_dir}/request_*.txt")
    print(f"Summary statistics: {output_dir}/summary_stats.json")
    print(f"Log file: {log_file}")

if __name__ == "__main__":
    # For Windows compatibility
    if hasattr(multiprocessing, 'freeze_support'):
        multiprocessing.freeze_support()
    main()