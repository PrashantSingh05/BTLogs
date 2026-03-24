# import time
# import psutil
# from app import create_app
# from app.services.log_service import create_log

# app = create_app()

# # Store previous process list
# previous_processes = set()


# def get_current_processes():
#     processes = set()
#     for proc in psutil.process_iter(['pid', 'name']):
#         try:
#             processes.add((proc.info['pid'], proc.info['name']))
#         except:
#             pass
#     return processes


# def monitor_processes():
#     global previous_processes

#     print("🔍 Process monitoring started...")

#     with app.app_context():
#         previous_processes = get_current_processes()

#         while True:
#             time.sleep(5)

#             current_processes = get_current_processes()

#             # New processes
#             new_procs = current_processes - previous_processes

#             # Stopped processes
#             stopped_procs = previous_processes - current_processes

#             # Log new processes
#             for pid, name in new_procs:
#                 create_log({
#                     "title": f"Process Started: {name}",
#                     "description": f"PID {pid} started",
#                     "category": "process",
#                     "system_name": "local",
#                     "created_by": "system"
#                 })

#             # Log stopped processes
#             for pid, name in stopped_procs:
#                 create_log({
#                     "title": f"Process Stopped: {name}",
#                     "description": f"PID {pid} stopped",
#                     "category": "process",
#                     "system_name": "local",
#                     "created_by": "system"
#                 })

#             previous_processes = current_processes