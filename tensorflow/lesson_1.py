import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf

x = tf.Variable(1.0)
z = tf.Variable([2., 3.])


with tf.GradientTape() as tape:
    y = tf.constant(2.0) + x**2 + z * x + z

df = tape.gradient(y,[x,z])
print(df[0], df[1], sep="\n")



