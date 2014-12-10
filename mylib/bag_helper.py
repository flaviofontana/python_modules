# -*- coding: utf-8 -*-
"""
Created on Tue Dec  9 22:57:46 2014

@author: ffontana
"""
import rosbag
import rospy
import yaml
from collections import namedtuple
import matplotlib.pyplot as plt

### list all topics in a bag file
def get_topics(bag_handle):
    topic_item_list = yaml.load(bag_handle._get_yaml_info()).get('topics')
    topic_list = list()
    for item in topic_item_list:
        topic_list.append(item['topic'] )
    return topic_list
    
### find the first stamp in a bag file
def get_first_stamp(bag_handle):
    t0 = float('Inf')
    for topic in get_topics(bag_handle):
        first_msg = bag_handle.read_messages(topics = topic).next()[1]
        if(hasattr(first_msg, 'header')):
            if( first_msg.header.stamp.to_sec() < t0 ):
                t0 = first_msg.header.stamp.to_sec()
    if t0 == float('inf'):
        t0 = 0
    return rospy.Time(t0)
    
### import a bagfile
def import_bag_file(bag_name, use_bag_time=False, topic_list=[]):
    bag_handle = rosbag.Bag(bag_name)
    t0 = get_first_stamp(bag_handle)
    if(len(topic_list) == 0):
        topic_list = get_topics(bag_handle)
    data=dict()    
    for topic in topic_list:
        print topic
        data[topic] = []
        for topic, msg, bagtime in bag_handle.read_messages(topics = topic):
            bagtime -= t0
            if(hasattr(msg, 'header') and not use_bag_time):
                msg.header.stamp -= t0;
                time = msg.header.stamp.to_sec()
            else:
                time = bagtime.to_sec()
            data[topic].append(namedtuple('Data',['time', 'msg', 'bagtime'])(time,msg,bagtime.to_sec()))
    bag_handle.close()
    print('...done')
    return data
    
def bag_plotter( input ):
    x,y = zip(*input)
    plt.plot(x,y)
    
if __name__ == "__main__":
    data = import_bag_file('mybag.bag', topic_list=['/drdre/optitrack_corrected','/drdre/state_estimate'])