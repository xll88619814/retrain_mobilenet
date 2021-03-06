# -*- coding: utf-8 -*-
import tensorflow as tf
import numpy as np
import sys
import os

def read_tensor_from_image_file(file_name,input_height=224, input_width=224, input_mean=0, input_std=255):
    input_name = "file_reader"
    file_reader = tf.read_file(file_name, input_name)
    image_reader = tf.image.decode_jpeg(file_reader, channels=3, name="jpeg_reader")
    float_caster = tf.cast(image_reader, tf.float32)
    dims_expander = tf.expand_dims(float_caster, 0)
    resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
    normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
    sess = tf.Session()
    result = sess.run(normalized)
    return result


computerAcc = sys.argv[1]
MODEL_FILE_trash = 'tmp/model/trash_mobilenet_50.pb'
file_labels = open('tmp/labels.txt')
labels = []
for line in file_labels.readlines():
    labels.append(line.strip('\n'))
#labels = file_labels.readlines()
print(labels)
with tf.Graph().as_default() as graph:
    with tf.Session().as_default() as sess:
        with tf.gfile.FastGFile(MODEL_FILE_trash, 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())

        output_tensor, input_tensor = tf.import_graph_def(graph_def, return_elements=['final_result:0', 'import/input:0'])
       
        test_dir = '../retrain/test_images/'
        if computerAcc == 'True':
            acc = 0
            count = 0
            for image_dir in os.listdir(test_dir):
                count += 1
                image_path = test_dir+image_dir
                print(image_path)
                #image_data = tf.gfile.FastGFile(image_path, 'rb').read()
                image_data = read_tensor_from_image_file(image_path)
                feed_dict = {input_tensor:image_data}

                yy = sess.run(output_tensor, feed_dict)
                pred = labels[sess.run(tf.argmax(yy, 1))[0]]
                #print(pred)
                #print(yy)
                print('image {} class is {}'.format(image_path, pred))
                truth_label = image_dir.split('_')[0]
                if truth_label == pred:
                    acc += 1
            ratio = acc*1.0/count
            print('the test accuracy is %.1f%%' % (ratio*100))
        else:
            for image_dir in os.listdir(test_dir):                              
                image_path = test_dir+image_dir                                 
                print(image_path)                                               
                image_data = tf.gfile.FastGFile(image_path, 'rb').read()        
                feed_dict = {input_tensor:image_data}                           
                yy = sess.run(output_tensor, feed_dict)                         
                pred = labels[sess.run(tf.argmax(yy, 1))[0]]                    
                #print(pred)                                                    
                #print(yy)                                                      
                print('image {} class is {}'.format(image_path, pred))
