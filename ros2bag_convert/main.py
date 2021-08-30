from .ros2bag_convert import read_bag,save_csv_file
import sys

argvs = sys.argv
argc = len(argvs)



def main():
    if (argc != 2):
        print('Usage: #ros2bag-convert xxx.db3')
        quit()
    file_url = argvs[1]
    data = read_bag.read_from_all_topics(file_url,True)
    for i in range(len(data)):
        topic_name,topic_type = data[i][0],data[i][1]
        save_csv_file.save_csv_file(data[i][2:],file_url[:file_url.rfind("/")]+""+topic_name+".csv")

if __name__ == '__main__':
    main()


