#coding=utf-8
import paddle
train_reader = paddle.dataset.mnist.train()
shuffled_reader = paddle.reader.shuffle(train_reader, buf_size=64)
batch_reader = paddle.batch(shuffled_reader, batch_size=32)

from paddle import fluid
images = fluid.layers.data(name='image', shape=[28, 28], dtype='float32')
labels = fluid.layers.data(name='label', shape=[1], dtype='int64')
data_feeder = fluid.DataFeeder(feed_list=[images, labels], place=fluid.CPUPlace())
exe = fluid.Executor(fluid.CPUPlace())
exe.run(fluid.default_startup_program())
epoch_num = 1
for epoch_id in range(epoch_num):
    for batch_data in batch_reader():
        result = exe.run(feed=data_feeder.feed(batch_data)) # Tensor 格式
# print result[0]
