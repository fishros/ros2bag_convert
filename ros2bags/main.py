from ros2bag_convert import read_bag,save_csv_file
import sys

argvs = sys.argv
argc = len(argvs)



def main():
    if (argc != 2):
        print('Usage: # python3 %s source' % argvs[0])
        quit()
    file_url = argvs[1]
    data = read_bag.read_from_all_topics(file_url,True)
    print("------------------------------------------")
    for i in range(len(data)):
        topic_name,topic_type = data[i][0],data[i][1]
        # print(topic_name,topic_type)
        save_csv_file.save_csv_file(data[i][2:],"/home/ros2/rosbag2_csv/ros2bag_convert"+topic_name+".csv")

if __name__ == '__main__':
    main()


