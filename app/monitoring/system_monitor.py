# import time
# import psutil
# from app import create_app
# from app.services.log_service import create_log

# app = create_app()


# def monitor_system():
#     print("⚡ System monitoring started...")

#     with app.app_context():
#         while True:
#             cpu = psutil.cpu_percent(interval=2)

#             if cpu > 80:
#                 create_log({
#                     "title": "High CPU Usage",
#                     "description": f"CPU usage reached {cpu}%",
#                     "category": "hardware",
#                     "system_name": "local",
#                     "created_by": "system"
#                 })

#             time.sleep(5)