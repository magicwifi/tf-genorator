#! -*- coding: utf-8 -*-
import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils

# 读取txt文件
filename = "my_a_news_art.csv"
with open(filename, 'r', encoding='utf-8') as f:
    raw_text = f.read().lower()

# 创建文字和对应数字的字典
chars = sorted(list(set(raw_text)))
#print(chars)
char_to_int = dict((c, i) for i, c in enumerate(chars))
int_to_char = dict((i, c) for i, c in enumerate(chars))
# 对加载数据做总结
n_chars = len(raw_text)
n_vocab = len(chars)
print("总的文字数: ", n_chars)
print("总的文字类别: ", n_vocab)

# 解析数据集，转化为输入向量和输出向量
seq_length = 10
dataX = []
dataY = []
for i in range(0, n_chars-seq_length, 1):
    seq_in = raw_text[i:i + seq_length]
    seq_out = raw_text[i + seq_length]
    dataX.append([char_to_int[char] for char in seq_in])
    dataY.append(char_to_int[seq_out])
n_patterns = len(dataX)
print("Total Patterns: ", n_patterns)
# 将X重新转化为[samples, time steps, features]的形状
X = numpy.reshape(dataX, (n_patterns, seq_length, 1))
# 正则化
X = X/n_vocab
# 对输出变量做one-hot编码
y = np_utils.to_categorical(dataY)

# 定义LSTM模型
model = Sequential()
model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2])))
model.add(Dropout(0.2))
model.add(Dense(y.shape[1], activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam')
#print(model.summary())

# 定义checkpoint
filepath="./weights-improvement-{epoch:02d}-{loss:.4f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint]
# 训练模型，每批训练128个样本，总共训练1000次
epochs = 1000
model.fit(X, y, epochs=epochs, batch_size=128, callbacks=callbacks_list)
