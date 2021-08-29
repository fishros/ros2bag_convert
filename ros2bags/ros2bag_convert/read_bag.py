import sqlite3
import numpy as np
from rcl_interfaces import msg
from rosidl_runtime_py.utilities import get_message
from rclpy.serialization import deserialize_message
# import sys
# sys.path.append("/home/ros2/rosbag2_csv/rosbag2/")
from . import message_converter
import json

def connect(sqlite_file):
    """ Make connection to an SQLite database file. """
    connection = sqlite3.connect(sqlite_file)
    cursor = connection.cursor()
    return connection, cursor

def close(connection):
    """ Close connection to the database. """
    connection.close()

def count_rows(cursor, table_name, print_out=False):
    """ Returns the total number of rows in the database. """
    cursor.execute('SELECT COUNT(*) FROM {}'.format(table_name))
    count = cursor.fetchall()
    if print_out:
        print('\nTotal rows: {}'.format(count[0][0]))
    return count[0][0]

def get_headers(cursor, table_name, print_out=False):
    """ Returns a list of tuples with column informations:
    (id, name, type, notnull, default_value, primary_key)
    """
    # Get headers from table "table_name"
    cursor.execute('PRAGMA TABLE_INFO({})'.format(table_name))
    info = cursor.fetchall()
    if print_out:
        print("\nColumn Info:\nID, Name, Type, NotNull, DefaultVal, PrimaryKey")
        for col in info:
            print(col)
    return info

def get_all_elements(cursor, table_name, print_out=False):
    """ Returns a dictionary with all elements of the table database.
    """
    # Get elements from table "table_name"
    cursor.execute('SELECT * from({})'.format(table_name))
    records = cursor.fetchall()
    if print_out:
        print("\nAll elements:")
        for row in records:
            print(row)
    return records

def is_topic(cursor, topic_name, print_out=False):
    """ Returns topic_name header if it exists. If it doesn't, returns empty.
        It returns the last topic found with this name.
    """
    bool_is_topic = False
    topicFound = []

    # Get all records for 'topics'
    records = get_all_elements(cursor, 'topics', print_out=False)

    # Look for specific 'topic_name' in 'records'
    for row in records:
        if(row[1] == topic_name): # 1 is 'name' TODO
            bool_is_topic = True
            topicFound = row
    if print_out:
        if bool_is_topic:
             # 1 is 'name', 0 is 'id' TODO
            print('\nTopic named', topicFound[1], ' exists at id ', topicFound[0] ,'\n')
        else:
            print('\nTopic', topic_name ,'could not be found. \n')

    return topicFound

def get_all_msgs_from_topic(cursor, topic_name, print_out=False):
    """ Returns all timestamps and messages from specific topic.
    There is no deserialization for the BLOB data.
    """
    count = 0
    timestamps = []
    messages = []

    # Find if topic exists and its id
    topicFound = is_topic(cursor, topic_name, print_out=False)

    # If not find return empty
    if not topicFound:
        print('Topic', topic_name ,'could not be found. \n')
    else:
        records = get_all_elements(cursor, 'messages', print_out=False)

        # Look for message with the same id from the topic
        for row in records:
            if row[1] == topicFound[0]:     # 1 and 0 is 'topic_id' TODO
                count = count + 1           # count messages for this topic
                timestamps.append(row[2])   # 2 is for timestamp TODO
                messages.append(row[3])     # 3 is for all messages

        # Print
        if print_out:
            print('\nThere are ', count, 'messages in ', topicFound[1])

    return timestamps, messages

def get_all_topics_names(cursor, print_out=False):
    """ Returns all topics names.
    """
    topicNames = []
    # Get all records for 'topics'
    records = get_all_elements(cursor, 'topics', print_out=False)

    # Save all topics names
    for row in records:
        topicNames.append(row[1])  # 1 is for topic name TODO
    if print_out:
        print('\nTopics names are:')
        print(topicNames)

    return topicNames

def get_all_msgs_types(cursor, print_out=False):
    """ Returns all messages types.
    """
    msgsTypes = []
    # Get all records for 'topics'
    records = get_all_elements(cursor, 'topics', print_out=False)

    # Save all message types
    for row in records:
        msgsTypes.append(row[2])  # 2 is for message type TODO
    if print_out:
        print('\nMessages types are:')
        print(msgsTypes)

    return msgsTypes

def get_msg_type(cursor, topic_name, print_out=False):
    """ Returns the message from specific topic.
    """
    msg_type = []
    # Get all topics names and all message types
    topic_names = get_all_topics_names(cursor, print_out=False)
    msgs_types = get_all_msgs_types(cursor, print_out=False)

    # look for topic at the topic_names list, and find its index
    for index, element in enumerate(topic_names):
        if element == topic_name:
            msg_type = msgs_types[index]
    if print_out:
        print('\nMessage type in', topic_name, 'is', msg_type)

    return msg_type

def read_from_topic(bag_file, topic_name, print_out=False):
    """ Returns all timestamps and messages from specific topic.
    Data is deserialized.
    """
    # Connect to the database
    connection, cursor = connect(bag_file)

    # Get all topics names
    topic_names = get_all_topics_names(cursor, print_out=False)

    # Get all messages types
    topic_types = get_all_msgs_types(cursor, print_out=False)

    # Get all timestamps and all messages (no deserialization)
    timestamps, messages_cdr = get_all_msgs_from_topic(cursor, topic_name, print_out=False)

    # Create a map for quicker lookup
    type_map = {topic_names[i]:topic_types[i] for i in range(len(topic_types))}
    # Get message type
    msg_type = get_message(type_map[topic_name])

    # Deserialize messages
    messages = []
    for i in range(len(messages_cdr)):
        # messages.append(deserialize_message(messages_cdr[i], msg_type))
        msg = deserialize_message(messages_cdr[i], msg_type)
        dic_data = message_converter.convert_ros_message_to_dictionary(msg)
        messages.append(dic_data)
    if print_out:
        print(len(messages_cdr), 'messages deserialized from ', topic_name)

    # Close connection to the database
    close(connection)

    return timestamps, messages

def read_from_all_topics(bag_file, print_out=False):
    """ Returns all timestamps and messages from all topics.
    """
    # Connect to the database
    connection, cursor = connect(bag_file)

    # Get all topics names and types
    topic_names = get_all_topics_names(cursor, print_out=False)
    print(topic_names)
    topic_types = get_all_msgs_types(cursor, print_out=False)

    # Get all messages types
    topic_types = get_all_msgs_types(cursor, print_out=False)
    data = []

    # Get all timestamps and messages for each topic
    for i in range(len(topic_names)):
        timestamps, messages = read_from_topic(bag_file, topic_names[i], print_out)
        data.append((topic_names[i], topic_types[i], timestamps, messages))

    # Close connection to the database
    close(connection)

    return data
