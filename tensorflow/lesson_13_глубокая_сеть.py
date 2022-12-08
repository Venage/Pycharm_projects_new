import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.datasets import cifar10, mnist
import numpy as np
import matplotlib.pyplot as plt
#import graphviz
from keras.utils.vis_utils import plot_model
import pydot

tf.random.set_seed(1)


(x_train, y_train), (x_test, y_test) = cifar10.load_data()

x_train = x_train / 255
x_test = x_test / 255

y_train = keras.utils.to_categorical(y_train, 10)
y_test = keras.utils.to_categorical(y_test, 10)

inputs = keras.Input(shape=(32, 32, 3), name="img")
x = layers.Conv2D(32, 3, activation="relu")(inputs)
x = layers.Conv2D(64, 3, activation="relu")(x)
block_1_output = layers.MaxPooling2D(3)(x)

x = layers.Conv2D(64, 3, activation="relu", padding="same")(block_1_output)
x = layers.Conv2D(64, 3, activation="relu", padding="same")(x)
x = layers.Conv2D(64, 3, activation="relu", padding="same")(x)
x = layers.Conv2D(64, 3, activation="relu", padding="same")(x)
block_2_output = layers.add([x, block_1_output])

x = layers.Conv2D(64, 3, activation="relu", padding="same")(block_2_output)
x = layers.Conv2D(64, 3, activation="relu", padding="same")(x)
x = layers.Conv2D(64, 3, activation="relu", padding="same")(x)
x = layers.Conv2D(64, 3, activation="relu", padding="same")(x)
block_3_output = layers.add([x, block_2_output])

x = layers.Conv2D(64, 3, activation="relu")(block_3_output)
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dense(256, activation="relu")(x)
x = layers.Dropout(0.5)(x)

outputs = layers.Dense(10, activation='softmax')(x)

model = keras.Model(inputs, outputs, name="toy_resnet")
#model.summary()

model.compile(optimizer='adam',
             loss='categorical_crossentropy',
             metrics=['accuracy'])

model.fit(x_train, y_train, batch_size=64, epochs=15, validation_split=0.2)

print( model.evaluate(x_test, y_test) )
#0.6947
#0.6719
#0.7106

#keras.utils.plot_model(model, 'multi_input_and_output_model.png', show_shapes=True)
#predictions = model.predict(x_test)
"""
for i in range(10):
    n = i
    labels = '''airplane automobile bird cat deer dog frog horse ship truck'''.split()
    predict_label = predictions[n].argmax()
    original_label = np.argmax(y_test[n], axis=-1)

    print(f'Реальный тип - {labels[original_label]} \nпредсказанный - {labels[predict_label]}')
    plt.imshow(x_test[n])
    plt.xlabel(labels[original_label])
    plt.show()
"""






