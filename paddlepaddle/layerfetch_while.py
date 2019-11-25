#coding=utf-8
from paddle import fluid
a = fluid.layers.fill_constant(shape=[2, 2], dtype='float32', value=1.0)
i = fluid.layers.zeros([1], dtype='int64')
until = fluid.layers.fill_constant([1], dtype='int64', value=10)
data_arr = fluid.layers.array_write(a, i)

cond = fluid.layers.less_than(x=i, y=until)
while_op = fluid.layers.While(cond=cond)
with while_op.block():
    a = fluid.layers.array_read(data_arr, i)
    a += 1
    i = fluid.layers.increment(x=i, value=1, in_place=True)
    fluid.layers.less_than(x=i, y=until, cond=cond)
    fluid.layers.array_write(a, i, data_arr)
ret = fluid.layers.array_read(data_arr, i - 1)

exe = fluid.Executor(fluid.CPUPlace())
exe.run(fluid.default_startup_program())
result = exe.run(fetch_list=[ret])
print result[0] # [10, 10]