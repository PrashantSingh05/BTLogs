# import time
# import psutil
# from app import create_app
# from app.services.log_service import create_log

# app = create_app()

# last_bytes_sent = 0


# def monitor_network():
#     global last_bytes_sent

#     print("🌐 Network monitoring started...")

#     with app.app_context():
#         while True:
#             net = psutil.net_io_counters()
#             current = net.bytes_sent

#             if last_bytes_sent != 0:
#                 diff = current - last_bytes_sent

#                 if diff > 1000000:  # ~1MB spike
#                     create_log({
#                         "title": "High Network Usage",
#                         "description": f"Sent {diff} bytes in interval",
#                         "category": "network",
#                         "system_name": "local",
#                         "created_by": "system"
#                     })

#             last_bytes_sent = current
#             time.sleep(5)