import os
#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
import numpy as np
import time

class DenseNN(tf.Module):
    def __init__(self, outputs, activate="relu"):
        super().__init__()
        self.outputs = outputs
        self.activate = activate
        self.fl_init = False

    def __call__(self, x):
        if not self.fl_init:
            self.w = tf.random.truncated_normal((x.shape[-1], self.outputs), stddev=0.1, name="w")
            self.b = tf.zeros([self.outputs], dtype=tf.float32, name="b")

            self.w = tf.Variable(self.w)
            self.b = tf.Variable(self.b, trainable=False)

            self.fl_init = True

        y = x @ self.w + self.b

        if self.activate == "relu":
            return tf.nn.relu(y)
        elif self.activate == "softmax":
            return tf.nn.softmax(y)

        return y


class SequentialModule(tf.Module):
    def __init__(self):
        super().__init__()
        self.layer_1 = DenseNN(128)
        self.layer_2 = DenseNN(10, activate="softmax")

    def __call__(self, x):
        return self.layer_2(self.layer_1(x))


(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = x_train / 255
x_test = x_test / 255

x_train = tf.reshape(tf.cast(x_train, tf.float32), [-1, 28*28])
x_test = tf.reshape(tf.cast(x_test, tf.float32), [-1, 28*28])

y_train = to_categorical(y_train, 10)


model = SequentialModule()
# layer_1 = DenseNN(128)
# layer_2 = DenseNN(10, activate="softmax")
#print(model.submodules)

cross_entropy = lambda y_true, y_pred: tf.reduce_mean(tf.losses.categorical_crossentropy(y_true, y_pred))
opt = tf.optimizers.Adam(learning_rate=0.001)

BATCH_SIZE = 32
EPOCHS = 10
TOTAL = x_train.shape[0]

train_dataset = tf.data.Dataset.from_tensor_slices((x_train, y_train))
train_dataset = train_dataset.shuffle(buffer_size=1024).batch(BATCH_SIZE)


@tf.function
def train_batch(x_batch, y_batch):
    with tf.GradientTape() as tape:
        f_loss = cross_entropy(y_batch, model(x_batch))

    grads = tape.gradient(f_loss, model.trainable_variables)
    opt.apply_gradients(zip(grads, model.trainable_variables))

    return f_loss


for n in range(EPOCHS):
    start = time.perf_counter()
    loss = 0
    for x_batch, y_batch in train_dataset:
        loss += train_batch(x_batch, y_batch)
    print(time.perf_counter() - start)
    print(loss.numpy())


y = model(x_test)
y2 = tf.argmax(y, axis=1).numpy()
acc = len(y_test[y_test == y2])/y_test.shape[0] * 100
print(acc)

acc = tf.metrics.Accuracy()
acc.update_state(y_test, y2)
print( acc.result().numpy() * 100 )