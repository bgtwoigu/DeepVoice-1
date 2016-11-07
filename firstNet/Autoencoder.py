import tensorflow as tf
import numpy as np
import math
import random
import pandas as pd
import sys
import pickle

print("Loading data...")

data = pd.io.parsers.read_csv("data.csv")
data = data.as_matrix()

labels = pickle.load(open("labels.p", "rb"))

print("Preparing data...")

pairs = []

for i in range(data.shape[0]-1):
    for j in range(data.shape[0]-i-1):
        if labels[i] == labels[i+j+1]:
            pairs.append([data[i],data[i+j+1]])

# Code here for importing data from file

input = [p[0] for p in pairs] + [p[1] for p in pairs]

output = [p[1] for p in pairs] + [p[0] for p in pairs]

input_data = np.array(input)
output_data = np.array(output)

print("Generating neuronal network...")

# Autoencoder with 3 hidden layer
n_samp, n_input = input_data.shape
n_layer1 = 8000
n_layer2 = 7000
n_layer3 = 6000
n_hidden = 4000

x = tf.placeholder("float", [None, n_input])

# Weights and biases to first layer
Wl1 = tf.Variable(tf.random_uniform((n_input, n_layer1), -1.0 / math.sqrt(n_input), 1.0 / math.sqrt(n_input)))
bl1 = tf.Variable(tf.zeros([n_layer1]))
l1 = tf.nn.tanh(tf.matmul(x,Wl1) + bl1)
l1_drop = tf.nn.dropout(l1, keep_prob=0.90)

# Weights and biases to second layer

Wl2 = tf.Variable(tf.random_uniform((n_layer1, n_layer2), -1.0 / math.sqrt(n_layer1), 1.0 / math.sqrt(n_layer1)))
bl2 = tf.Variable(tf.zeros([n_layer2]))
l2 = tf.nn.tanh(tf.matmul(x,Wl2) + bl2)
l2_drop = tf.nn.dropout(l2, keep_prob=0.90)

# Weights and biases to third layer

Wl3 = tf.Variable(tf.random_uniform((n_layer2, n_layer3), -1.0 / math.sqrt(n_layer2), 1.0 / math.sqrt(n_layer2)))
bl3 = tf.Variable(tf.zeros([n_layer3]))
l3 = tf.nn.tanh(tf.matmul(x,Wl3) + bl3)
l3_drop = tf.nn.dropout(l3, keep_prob=0.90)

# Weights and biases to hidden layer

Wh = tf.Variable(tf.random_uniform((n_layer3, n_hidden), -1.0 / math.sqrt(n_layer3), 1.0 / math.sqrt(n_layer3)))
bh = tf.Variable(tf.zeros([n_hidden]))
h = tf.nn.tanh(tf.matmul(x,Wh) + bh)
h_drop = tf.nn.dropout(h, keep_prob=0.90)

# Weights and biases to fifth layer tied to hidden

Wl5 = tf.transpose(Wlh)
bl5 = tf.Variable(tf.zeros([n_layer3]))
l5 = tf.nn.tanh(tf.matmul(x,Wl5) + bl5)
l5_drop = tf.nn.dropout(l15, keep_prob=0.90)

# Weights and biases to sixth layer tied to third

Wl6 = tf.transpose(Wl3)
bl6 = tf.Variable(tf.zeros([n_layer2]))
l6 = tf.nn.tanh(tf.matmul(x,Wl6) + bl6)
l6_drop = tf.nn.dropout(l6, keep_prob=0.90)

# Weights and biases to seventh layer tied to first

Wl7 = tf.transpose(Wl2)
bl7 = tf.Variable(tf.zeros([n_layer1]))
l7 = tf.nn.tanh(tf.matmul(x,Wl7) + bl7)
l7_drop = tf.nn.dropout(l7, keep_prob=0.90)

# Weights and biases to output layer
Wo = tf.Variable(tf.random_uniform((n_layer1, n_input), -1.0 / math.sqrt(n_layer1), 1.0 / math.sqrt(n_layer1)))
bo = tf.Variable(tf.zeros([n_input]))
y = tf.nn.tanh(tf.matmul(x,Wo) + bo)

# Objective functions
y_ = tf.placeholder("float", [None,1])
cross_entropy = -tf.reduce_sum(y_*tf.log(y))
meansq = tf.reduce_mean(tf.square(y_-y))
train_step = tf.train.GradientDescentOptimizer(0.05).minimize(meansq)

# Add ops to save and restore all the variables.
saver = tf.train.Saver()


init = tf.initialize_all_variables()
sess = tf.Session()
sess.run(init)

n_rounds = 30
batch_size = min(50, n_samp)

print("Training...")

for i in range(n_rounds):
    sample = np.random.randint(n_samp, size=batch_size)
    batch_xs = input_data[sample][:]
    batch_ys = output_data[sample][:]
    sess.run(train_step, feed_dict={x: batch_xs, y_:batch_ys})
    if i % 100 == 0:
        print(i, sess.run(cross_entropy, feed_dict={x: batch_xs, y_:batch_ys}), sess.run(meansq, feed_dict={x: batch_xs, y_:batch_ys}))


# Save the variables to disk.
save_path = saver.save(sess, "model.ckpt")
print("Model saved in file: %s" % save_path)
