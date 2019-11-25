#coding=utf-8
from paddle import fluid
x = fluid.layers.fill_constant(shape=[1], dtype='int64', value=5)
y = fluid.layers.fill_constant(shape=[1], dtype='int64', value=1) 
z = x + y
exe = fluid.Executor(fluid.CPUPlace())
result = exe.run(fluid.default_main_program(), fetch_list=[z])
print result[0] # 6