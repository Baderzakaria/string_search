import subprocess
import re

def run_test_and_extract_time(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    output = stdout.decode('utf-8')
    time_pattern = r'in ([\d.]+)s'
    match = re.search(time_pattern, output)
    if match:
        total_time = float(match.group(1))
    else:
        total_time = None
    return total_time

def average_test_time(command, runs=10):
    total_time = 0
    for _ in range(runs):
        time_taken = run_test_and_extract_time(command)
        if time_taken is not None:
            total_time += time_taken
    average_time = total_time / runs
    return average_time

def main():
    runs=5
    command_v3 = 'python -m pytest a9number_v3_old.py'
    command_v3_updated = 'python -m pytest a9number_v3.py'
    avg_time_v3 = average_test_time(command_v3, runs=runs)
    avg_time_v3_updated = average_test_time(command_v3_updated, runs=runs)
    print(f"Average time taken by a9number_v3_old.py over {runs} runs: {avg_time_v3:.2f} seconds")
    print(f"Average time taken by a9number_v3.py over {runs} runs: {avg_time_v3_updated:.2f} seconds")
    print(f"{(avg_time_v3_updated < 3.84*avg_time_v3/100)}")
    print(f"percentage of improvement {((avg_time_v3_updated/avg_time_v3)*100)}")
if __name__ == '__main__':
    main()
