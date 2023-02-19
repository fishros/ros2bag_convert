from .ros2bag_convert import read_bag
import sys, os

argvs = sys.argv
argc = len(argvs)



def main():
    if (argc != 2):
        print('Usage: #ros2bag-convert xxx.db3')
        quit()
    file_url = argvs[1]
    read_bag.read_write_from_all_topics(file_url,True)

if __name__ == '__main__':
    main()


