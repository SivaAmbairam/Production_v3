# import os
# import subprocess
# import time
# import logging
# import threading
# from flask import Flask, request, jsonify
#
# app = Flask(__name__)
#
# # Global variables
# stop_execution = False
# script_status = {}
# script_output = {}
# SCRIPTS_DIRECTORY = r'C:\Users\G6\PycharmProjects\WebScrappingWebPage'
#
# def run_script(script_name):
#     global stop_execution, script_status, script_output
#     script_path = os.path.join(SCRIPTS_DIRECTORY, script_name)
#     script_status[script_name] = 'Running'
#     url_count = 0
#
#     try:
#         logging.debug(f"Starting script: {script_name}")
#         process = subprocess.Popen(['python', script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
#
#         while True:
#             if stop_execution or script_status[script_name] == 'Stopping':
#                 logging.debug(f"Stopping script: {script_name}")
#                 process.terminate()
#                 process.wait(timeout=5)
#                 if process.poll() is None:
#                     process.kill()
#                 script_status[script_name] = f'Stopped (URLs scraped: {url_count})'
#                 break
#
#             try:
#                 output = process.stdout.readline()
#                 if output == '' and process.poll() is not None:
#                     break
#                 if output:
#                     logging.debug(f'Script {script_name} output: {output.strip()}')
#                     script_output[script_name] = script_output.get(script_name, '') + output
#                     if output.strip().startswith('https://'):  # Count URLs
#                         url_count += 1
#                         script_status[script_name] = f'Running (URLs scraped: {url_count})'
#             except subprocess.TimeoutExpired:
#                 continue
#
#         stdout, stderr = process.communicate()
#         script_output[script_name] = script_output.get(script_name, '') + stdout + stderr
#         rc = process.poll()
#
#         if script_status[script_name] != f'Stopped (URLs scraped: {url_count})':
#             script_status[script_name] = f'Completed (URLs scraped: {url_count})' if rc == 0 else f'Error: {stderr.strip()}'
#             time.sleep(5)
#
#     except Exception as e:
#         logging.error(f"Exception running script {script_name}: {e}")
#         script_status[script_name] = f'Error: {str(e)}'
#     finally:
#         if script_name in script_status and 'Running' in script_status[script_name]:
#             script_status[script_name] = f'Completed (URLs scraped: {url_count})'
#
#
# # def run_comparison_scripts():
# #     comparison_scripts = [
# #         'export_csv.py',
# #         'script_2.py',
# #     ]
# #     for script_name in comparison_scripts:
# #         print(f"Running {script_name}")
# #         run_script(script_name)
# #         print(f"Output of {script_name}:\n{script_output.get(script_name, '')}")
# #         time.sleep(5)
#
# def run_comparison_scripts():
#     # comparison_scripts = ['export_csv.py', 'push_script.py',
#     #                       ['Flinn_vs_VWR.py', 'Flinn_vs_Wardsci.py', 'Flinn_vs_Carolina.py', 'Flinn_vs_Fisher.py',
#     #                        'Flinn_vs_Frey.py'], 'Consolidate_matches_All_Products', 'Cleaning_process',
#     #                       'Overall_Compare_Script', 'Matched_push_script']
#     comparison_scripts = ['export_csv.py', ['Flinn_vs_VWR.py', 'Flinn_vs_Wardsci.py', 'Flinn_vs_Carolina.py', 'Flinn_vs_Fisher.py', 'Flinn_vs_Frey.py']]
#
#     threads = []
#     for script_name in comparison_scripts:
#         thread = threading.Thread(target=run_script, args=(script_name,))
#         thread.start()
#         threads.append(thread)
#         time.sleep(1)  # Stagger start times slightly
#
#     for thread in threads:
#         thread.join()
#         print(f"Output of {thread.name}:\n{script_output.get(thread.name, '')}")
#
#
# if __name__ == '__main__':
#     logging.basicConfig(level=logging.DEBUG)
#     run_comparison_scripts()


import os
import subprocess
import time
import logging
import threading
from flask import Flask, request, jsonify

app = Flask(__name__)

# Global variables
stop_execution = False
script_status = {}
script_output = {}
SCRIPTS_DIRECTORY = r'C:\Users\G6\PycharmProjects\WebScrappingWebPage'


def run_script(script_name):
    global stop_execution, script_status, script_output
    script_path = os.path.join(SCRIPTS_DIRECTORY, script_name)
    script_status[script_name] = 'Running'
    url_count = 0

    try:
        logging.debug(f"Starting script: {script_name}")
        process = subprocess.Popen(['python', script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        while True:
            if stop_execution or script_status[script_name] == 'Stopping':
                logging.debug(f"Stopping script: {script_name}")
                process.terminate()
                process.wait(timeout=5)
                if process.poll() is None:
                    process.kill()
                script_status[script_name] = f'Stopped (Data scraped: {url_count})'
                break

            try:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    logging.debug(f'Script {script_name} output: {output.strip()}')
                    script_output[script_name] = script_output.get(script_name, '') + output
                    if output.strip().startswith('https://'):  # Count URLs
                        url_count += 1
                        script_status[script_name] = f'Running)'
            except subprocess.TimeoutExpired:
                continue

        stdout, stderr = process.communicate()
        script_output[script_name] = script_output.get(script_name, '') + stdout + stderr
        rc = process.poll()

        if script_status[script_name] != f'Stopped':
            script_status[script_name] = f'Completed' if rc == 0 else f'Error: {stderr.strip()}'
            time.sleep(5)

    except Exception as e:
        logging.error(f"Exception running script {script_name}: {e}")
        script_status[script_name] = f'Error: {str(e)}'
    finally:
        if script_name in script_status and 'Running' in script_status[script_name]:
            script_status[script_name] = f'Completed (Data scraped: {url_count})'


def run_sequence_scripts(scripts):
    for script_name in scripts:
        run_script(script_name)
        print(f"Output of {script_name}:\n{script_output.get(script_name, '')}")
        time.sleep(5)


def export_csv_scripts():
    run_sequence_scripts(['export_csv.py'])


def push_scripts():
    run_sequence_scripts(['push_script.py'])


def flinn_vs_competitors_scripts():
    # run_sequence_scripts(['Flinn_vs_Frey.py'])
    run_sequence_scripts(['Flinn_vs_Frey.py', 'Flinn_vs_Nasco.py', 'Flinn_vs_Carolina.py', 'Flinn_vs_VWR.py', 'Flinn_vs_Wardsci.py'])


def consolidate_scripts():
    run_sequence_scripts(['Consolidate_matches_All_Products.py'])


def cleaning_scripts():
    run_sequence_scripts(['Cleaning_process.py'])


def overall_compared_scripts():
    run_sequence_scripts(['Overall_Compare_Script.py'])


def matched_push_scripts():
    run_sequence_scripts(['Matched_push_script.py'])


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    export_csv_scripts()
    time.sleep(5)
    push_scripts()
    time.sleep(5)
    flinn_vs_competitors_scripts()
    time.sleep(5)
    consolidate_scripts()
    time.sleep(5)
    cleaning_scripts()
    time.sleep(5)
    overall_compared_scripts()
    time.sleep(10)
    matched_push_scripts()

