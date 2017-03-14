# Group
# Model: Baseline Convolutional Neural Network
# Purpose: Baseline CNN for classifying emotions in images
# Developers: Russel Daries, Lewis Moffat, Rafiel Faruq, Hugo Phillion, Nitish Mutha

# Nesscary Imports

import tensorflow as tf
import numpy as np
import pandas as pd
import time
from misc_functions import *
from cnn_functions import *

#--------- Section for importing image dataset ----------#
# Read data from file or function

# Import data and create class for it
dataset_train = import_dataset(data_train,train_labels)
dataset_test = import_dataset(data_test,test_labels)

#--------- Section for importing image dataset ----------#

# Tensorboard training directory
logs_path = '../model/iteration1'
print('Log Path: '+ logs_path)

# Model Saving directory
model_path = '../model/tf_iteration1.ckpt'
print('Model Path: ' + model_path)

start_time = time.ctime()

# Boolean statements
TRAINING_MODE = True
PLOT_MODE = False
SAVE_MODE = False

# Size Declarations
OPTIMIZER = 'Adam'
EPOCHS = 5
batch_size = 100
image_dimension = 28
image_dimension_sq = image_dimension * image_dimension
learning_rate = 0.001
emotion_classes = 8
display_step = 10

# Layer Parameters
layer_1_patch_size = 5
layer_1_features = 32
layer_1_activation = 'relu'
layer_1_dropout = True
layer_1_batch_norm = True

layer_2_patch_size = 5
layer_2_features = 64
layer_2_activation = 'relu'
layer_2_dropout = True
layer_2_batch_norm = True

# Defining initial place holder variables
x = tf.placeholder(tf.float32, shape=[None, image_dimension_sq])
y_ = tf.placeholder(tf.float32, shape=[None, emotion_classes])
keep_prob = tf.placeholder(tf.float32)
phase_train = tf.placeholder(tf.bool, name='TRAINING_PHASE')

# Create Convolutional Neural-Network
layer_1 = ConvPoolLayer(x,layer_1_patch_size,layer_1_features,1,image_dimension,'relu',keep_prob,
                        True,False,True,False,phase_train)
layer_2 = ConvPoolLayer(layer_1.output,layer_2_patch_size,layer_2_features, layer_1_features,'relu',
                        keep_prob,False,False,True,False,phase_train)
layer_3 = DenselyConnectedLayer(layer_2.output,7,64,1024,'relu',keep_prob,False,False)
layer_4 = ReadOutLayer(layer_3.output,1024,emotion_classes,keep_prob,True)

y = layer_4.output

# Cross-entropy calculation
with tf.name_scope('Loss'):
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits = y, labels = y_))

# Optimizer selection
if(OPTIMIZER=='Adam'):
    optimizer = tf.train.AdamOptimizer(learning_rate).minimize(cost)
elif(OPTIMIZER=='SGD'):
    optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)
elif(OPTIMIZER=='Momentum'):
    optimizer = tf.train.MomentumOptimizer(learning_rate).minimize(cost)
else:
    optimizer = tf.train.AdamOptimizer(learning_rate).minimize(cost)

with tf.name_scope('Accuracy'):
    correct_pred = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

# Create a summary to monitor cost tensor
tf.summary.scalar("Loss", cost)
# Create a summary to monitor accuracy tensor
tf.summary.scalar("Accuracy", accuracy)
# Merge all summaries into a single op
merged_summary_op = tf.summary.merge_all()

# Initializing the variables
init = tf.global_variables_initializer()
saver = tf.train.Saver()

with tf.Session() as sess:
    sess.run(init)
    # Condtional statement to restore the model or start training the model
    if(TRAINING_MODE):

        #Write logs to Tensorboard directory
        summary_writer = tf.summary.FileWriter(logs_path, graph=tf.get_default_graph())
        print('----Training Baseline CNN Model Running----')
        # Keep training until reach max iterations
        train_acc = 0.0
        train_loss = 0.0

        # Number of loop repititions of model
        for epoch in range(EPOCHS):

            avg_loss = 0.0
            avg_acc = 0.0

            total_batch = int(dataset_train.num_examples/batch_size)

            # Loop for number of batches for training data
            for j in range(total_batch):

                batch_x, batch_y = dataset_train.next_batch(batch_size)

                # Reshape data to get batch size by 784 tensor
                batch_x = batch_x.reshape((batch_size, image_dimension_sq))

                # Run optimization
                sess.run(optimizer, feed_dict={x: batch_x, y: batch_y, keep_prob: 0.5, phase_train: True})
                acc, loss, summary = sess.run([accuracy, cost, merged_summary_op],
                                              feed_dict={x: batch_x, y: batch_y, keep_prob: 1.0, phase_train:False})

                summary_writer.add_summary(summary, epoch * total_batch + j)
                avg_acc += acc
                avg_loss += loss

                # Print condition to check state of model
                if j % display_step == 0:
                    print("Epoch " + str(epoch + 1) + ", Batch Number " + str(j + 1) + ", Batch Loss= " + \
                          "{:.5f}".format(loss) + ", Batch Accuracy= " + \
                          "{:.5f}".format(acc))

            # Average out accuracy over batches
            avg_acc = avg_acc / total_batch
            avg_loss = avg_loss / total_batch
            train_acc+=avg_acc
            train_loss+=avg_loss

            print("Epoch " + str(epoch + 1) + ", Epoch Loss= " + "{:.5f}".format(avg_loss) + ", Epoch Accuracy= " + \
                  "{:.5f}".format(avg_acc))

        print("Optimization Finished!")
        train_loss = train_loss/epoch
        train_acc = train_acc/epoch

        # Display training accuracy and loss achieved.
        print("Train Loss: "+ "{:.5f}".format(train_loss))
        print("Train Accuracy: "+ "{:.5f}".format(train_acc))

        end_time = time.ctime()
        # Check the training time it took the model to complete.
        print("Training Start Time : ", start_time)
        print("Training End Time : ", end_time)


        if(SAVE_MODE):
            pass
        else:
            pass

    else:



        if(PLOT_MODE):
            pass
        else:
            pass

