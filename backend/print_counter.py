import yaml
import mysql.connector
import time
import datetime

server_params = None
with open(r'./db_config.yaml') as file:
    server_params = yaml.load(file, Loader=yaml.FullLoader)


main_db = None
main_db_cursor = None
if server_params != None:
    main_db = mysql.connector.connect(
    host = server_params['server_ip'],
    database = server_params['db_name'],
    port = int(server_params['server_port']),
    user = server_params['username'],
    password = server_params['password'],
    connection_timeout = 1    )

    main_db_cursor = main_db.cursor()

if main_db and main_db_cursor:
    start_time = datetime.datetime.now()
    # query_string = "SELECT lab_order_number FROM lab_label WHERE time_Stamp BETWEEN '2023-03-08 0:0:1' AND '2023-03-08 23:59:59'"
    # query_string = "SELECT COUNT(lab_order_number) FROM lab_label WHERE time_Stamp BETWEEN '2023-03-08 0:0:1' AND '2023-03-08 23:59:59'"
    query_string = "SELECT COUNT(*) FROM (SELECT count(lab_order_number) FROM lab_label WHERE time_Stamp BETWEEN '2023-03-08 0:0:1' AND '2023-03-08 23:59:59' GROUP BY lab_order_number) AS c"

    main_db_cursor.execute(query_string)
    query_result = main_db_cursor.fetchall()
    main_db_cursor.close()
    main_db.close()
    stop_time = datetime.datetime.now()
    total_time = stop_time-start_time

    print("Execution time: ",total_time.microseconds," microseconds")

    # print(len(query_result))

    # for result in query_result:
    #     print(result)



