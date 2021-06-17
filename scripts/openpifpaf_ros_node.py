#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from openpifpaf.predictor import Predictor
from openpifpaf_ros.msg import Poses, Pose


class OpenPifpafProc(object):
    def __init__(self, in_topic, out_topic, scale):
        self.predictor = Predictor()
        self.sub = rospy.Subscriber(in_topic, Image, self.callback, queue_size=1)
        self.pub = rospy.Publisher(out_topic, Poses, queue_size=1)
        self.bridge = CvBridge()
        self.scale = scale

    def callback(self, data):
        rgb_img = self.bridge.imgmsg_to_cv2(data, "rgb8")
        if self.scale != 1.0:
            rgb_img = cv2.resize(rgb_img, None, fx=self.scale, fy=self.scale)
        pred, _, meta = self.predictor.numpy_image(rgb_img)

        poses = []
        for p in pred:
            pose = p.json_data()
            if scale != 1.0:
                d = p.data.reshape((-1, 3))
                d[d[:, 2] != 0, 0:2] /= self.scale
                d = d.reshape(-1)
                pose['keypoints'] = list(d)
            poses.append(pose)

        self.publish(data.header, poses)

    def publish(self, header, poses):
        msg = Poses()
        msg.header.stamp = header.stamp
        msg.poses = []

        for p in poses:
            pmsg = Pose()
            pmsg.keypoints = p['keypoints']
            msg.poses.append(pmsg)

        self.pub.publish(msg)


if __name__ == "__main__":
    rospy.init_node("openpifpaf_ros", anonymous=True)
    in_topic = rospy.get_param('~in_topic', 'image_color')
    out_topic = rospy.get_param('~out_topic', 'human_pose')
    scale = rospy.get_param('~scale', 1.0)

    recog = OpenPifpafProc(in_topic, out_topic, scale)
    rospy.spin()
