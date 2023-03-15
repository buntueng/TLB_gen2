import yaml
import mysql.connector
import datetime
import pystray
from PIL import Image
import logging
import threading
import time

debug_mode = False
# ======================== add logging =========================
logger = logging.getLogger('main_logger')
logger.setLevel(logging.DEBUG)
logging_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

fileHandler = logging.FileHandler(filename="./software_log.log")
fileHandler.setFormatter(logging_format)
logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logging_format)
logger.addHandler(consoleHandler)
# ============== functions =====================================
def check_tlb_used():
    main_db = None
    main_db_cursor = None
    total_used = None
    tlb_used = None
    try:
        now = datetime.datetime.now()
        begin_query_time = now.strftime('%Y-%m-%d  0:0:1')
        end_query_time = now.strftime('%Y-%m-%d %H:%M:%S')
        #=========================== read data from local server =====================
        with open(r'./db_config.yaml') as file:
            server_params = yaml.load(file, Loader=yaml.FullLoader)

        if server_params != None:
            if debug_mode == True:
                logger.debug('Run debug mode')
            else:
                hospital_name = server_params['HospitalName']

                main_db = mysql.connector.connect(
                host = server_params['local_server_ip'],
                database = server_params['local_db_name'],
                port = int(server_params['local_server_port']),
                user = server_params['local_username'],
                password = server_params['local_password'],
                connection_timeout = 1    )
                main_db_cursor = main_db.cursor()
                logger.info('open link to database on local server')

                online_db = mysql.connector.connect(
                host = server_params['global_server_ip'],
                database = server_params['global_db_name'],
                port = int(server_params['global_server_port']),
                user = server_params['global_username'],
                password = server_params['global_password'],
                connection_timeout = 1    )
                online_db_cursor = online_db.cursor()
                logger.info('open link to database on online server')

            if main_db and main_db_cursor and online_db and online_db_cursor:
                query_string = "SELECT COUNT(lab_order_number) FROM lab_label WHERE time_Stamp BETWEEN  '{begin_query_time}' AND '{end_query_time}'"
                main_db_cursor.execute(query_string)
                total_used = main_db_cursor.fetchall()

                query_string = f"SELECT COUNT(*) FROM (SELECT count(lab_order_number) FROM lab_label WHERE time_Stamp BETWEEN '{begin_query_time}' AND '{end_query_time}' GROUP BY lab_order_number) AS c"
                main_db_cursor.execute(query_string)
                tlb_used = main_db_cursor.fetchall()
                main_db_cursor.close()
                main_db.close()

                query_string = f"INSERT INTO tlb_use (hospital,total_print,total_used) VALUES('{hospital_name}',{total_used[0][0]},{tlb_used[0][0]})"
                logger.debug(query_string)
                online_db_cursor.execute(query_string)
                online_db.commit()
                online_db_cursor.close()
                online_db.close()
                logger.info("insert data to online server")
        else:
            logger.info('Server params does not exist')
    except:
        logger.error('Can not read write database')

def quit_window(main_icon, main_item):
    logger.info('quit command was executed')
    main_icon.stop()

def generate_pystray_object():
    image=Image.open("micons.png")
    menu=(pystray.MenuItem('Quit', quit_window), )
    main_icon=pystray.Icon("name", image, "System Tray Icon", menu)
    return main_icon

def run_state():
    main_state = 0
    delay_time = 5
    while True:
        logger.debug(main_state)
        match main_state:
            case 0:
                now = datetime.datetime.now()
                present_hour =  int(now.strftime('%H'))
                present_minute = int(now.strftime('%M'))
                if present_hour >= 6 and present_hour <= 18 and present_minute == 0:
                    check_tlb_used()
                    main_state = 1
                else:
                    delay_time = 10
                    logger.debug('wait to execute cmd')
            case 1:
                now = datetime.datetime.now()
                present_minute = int(now.strftime('%M'))
                if present_minute > 0:
                    main_state = 0
                    delay_time = 1
                else:
                    delay_time = 10
            case _:
                pass
        time.sleep(delay_time)
# ===============================================================
logger.info('Start main program')
tray_object = generate_pystray_object()
scheduler_thread = threading.Thread(target=run_state, daemon=True)
scheduler_thread.start()
tray_object.run()

