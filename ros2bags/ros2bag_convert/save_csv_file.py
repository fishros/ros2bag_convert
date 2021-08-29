
import csv
import json
import time
import numpy as np

def save_csv_file(data, csv_file_name, version=0, print_out=False):
    """ Save data to a csv_file_name (use it after 'read_from_all_topics').
    """

    # Create csv file
    with open(csv_file_name, mode='w') as csv_file:
        # csv_file.write(str("topic_names = %s \n" %len(data)))
        # Create csv header
        field_names = ['topic_name', 'topic_type', 'time_stamp', 'message']
        writer = None

        # print("-------------------------------")
        nt,line_datas  =  data[0],data[1]
        for index in range(len(line_datas)):
            row_time,row_data  = nt[index],line_datas[index]
            row_time =  '{}.{}'.format(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(row_time / 1000 / 1000 / 1000)), row_time % (1000 * 1000 * 1000))
            if writer is None:
                field_names = ['time']+list(row_data.keys())
                writer = csv.DictWriter(csv_file,fieldnames=field_names)
                writer.writeheader()
            row_data["time"] = row_time
            # row_data = [row_time]+list(row_data.values())
            writer.writerow(row_data)
            # print(row_time,row_data)

            # print("-------------------------------")
            # print(line)
        #     if flag:
        #         # 获取属性列表
        #         keys = list(line.keys())
        #         print(keys)
        #         writer.writerow(keys) # 将属性列表写入csv中
        #         flag = False
        # # 读取json数据的每一行，将values数据一次一行的写入csv中
        # writer.writerow(list(line.values()))


        # Save data
        # for i in range(len(data)):
        #     topic_name = data[i][0]
        #     topic_type = data[i][1]

        #     for j in range(len(data[i][2])):
        #         writer.writerow({   'topic_name': topic_name,
        #                             'topic_type': topic_type, 
        #                             'time_stamp': data[i][2][j],
        #                             'message': data[i][3][j] })

    # if print_out:
    print('Saving', csv_file_name)
