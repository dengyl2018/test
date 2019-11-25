#coding=utf-8
from paddle import fluid
a = fluid.layers.fill_constant(shape=[2, 1], dtype='int64', value=5)
b = fluid.layers.fill_constant(shape=[2, 1], dtype='int64', value=6) 
ifcond = fluid.layers.less_than(x=a, y=b)
ie = fluid.layers.IfElse(ifcond)
with ie.true_block():
    c = ie.input(a)
    c += 1
    ie.output(c)
exe = fluid.Executor(fluid.CPUPlace())
result = exe.run(fluid.default_main_program(), fetch_list=[c])
print result[0] # 6