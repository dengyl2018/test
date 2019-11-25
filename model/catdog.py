#coding=utf-8
"""
根据图像的语义信息将不同类别图像区分
池化是非线性下采样的一种形式，主要作用是通过减少网络的参数来减小计算量，并且能够在一定程度上控制过拟合
最大池化：用不重叠的矩形框将输入层分成不同的区域
Batchnorm：每一层神经网络的输入保持相同分布
act:激活函数，卷积层采用relu，全连接层采用softmax
损失函数：交叉熵
关注准确率：
优化方法：Adam
"""

#导入需要的包
import paddle as paddle
import paddle.fluid as fluid
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os
from datetime import datetime
import pdb

BATCH_SIZE = 128
#用于训练的数据提供器
train_reader = paddle.batch(
    paddle.reader.shuffle(paddle.dataset.cifar.train10(), 
                          buf_size=128*100),           
    batch_size=BATCH_SIZE)                                
#用于测试的数据提供器
test_reader = paddle.batch(
    paddle.dataset.cifar.test10(),                            
    batch_size=BATCH_SIZE) 
print("01 - 准备数据 完成".decode("utf-8"))

def convolutional_neural_network(img):
    # 第一个卷积-池化层
    conv_pool_1 = fluid.nets.simple_img_conv_pool(
        input=img,         # 输入图像
        filter_size=5,     # 滤波器的大小
        num_filters=20,    # filter 的数量。它与输出的通道相同
        pool_size=2,       # 池化核大小2*2
        pool_stride=2,     # 池化步长
        act="relu")        # 激活类型
    conv_pool_1 = fluid.layers.batch_norm(conv_pool_1)
    # 第二个卷积-池化层
    conv_pool_2 = fluid.nets.simple_img_conv_pool(
        input=conv_pool_1,
        filter_size=5,
        num_filters=50,
        pool_size=2,
        pool_stride=2,
        act="relu")
    conv_pool_2 = fluid.layers.batch_norm(conv_pool_2)
    # 第三个卷积-池化层
    conv_pool_3 = fluid.nets.simple_img_conv_pool(
        input=conv_pool_2,
        filter_size=5,
        num_filters=50,
        pool_size=2,
        pool_stride=2,
        act="relu")
    # 以softmax为激活函数的全连接输出层，10类数据输出10个数字
    prediction = fluid.layers.fc(input=conv_pool_3, size=10, act='softmax')
    return prediction

#定义输入数据 [通道，高度，宽度]
data_shape = [3, 32, 32]
images = fluid.layers.data(name='images', shape=data_shape, dtype='float32')
label = fluid.layers.data(name='label', shape=[1], dtype='int64')
# 获取分类器，用cnn进行分类
predict =  convolutional_neural_network(images)
# 获取损失函数和准确率
cost = fluid.layers.cross_entropy(input=predict, label=label) # 交叉熵
avg_cost = fluid.layers.mean(cost)                            # 计算cost中所有元素的平均值
acc = fluid.layers.accuracy(input=predict, label=label)       #使用输入和标签计算准确率
# 获取测试程序
test_program = fluid.default_main_program().clone(for_test=True)
# 定义优化方法
optimizer = fluid.optimizer.Adam(learning_rate=0.001)
optimizer.minimize(avg_cost)
print("02 - 网络配置 完成".decode("utf-8"))

# 定义使用CPU还是GPU，使用CPU时use_cuda = False,使用GPU时use_cuda = True
use_cuda = False
place = fluid.CUDAPlace(0) if use_cuda else fluid.CPUPlace()
# 创建执行器，初始化参数
exe = fluid.Executor(place)
exe.run(fluid.default_startup_program())
feeder = fluid.DataFeeder( feed_list=[images, label],place=place)
all_train_iter=0
all_train_iters=[]
all_train_costs=[]
all_train_accs=[]
model_save_dir = "D:/git/testme/data/catdog.inference.model"
EPOCH_NUM = 20
for pass_id in range(EPOCH_NUM):
    # 开始训练
    begin_time = datetime.now()
    for batch_id, data in enumerate(train_reader()):                        #遍历train_reader的迭代器，并为数据加上索引batch_id
        train_cost,train_acc = exe.run(program=fluid.default_main_program(),#运行主程序
                             feed=feeder.feed(data),                        #喂入一个batch的数据
                             fetch_list=[avg_cost, acc])                    #fetch均方误差和准确率
        all_train_iter=all_train_iter+BATCH_SIZE
        all_train_iters.append(all_train_iter)
        all_train_costs.append(train_cost[0])
        all_train_accs.append(train_acc[0])
        #每100次batch打印一次训练、进行一次测试
        if batch_id % 1000 == 0:                                             
            print('Pass:%d, Batch:%d, Cost:%0.5f, Accuracy:%0.5f' % 
            (pass_id, batch_id, train_cost[0], train_acc[0]))
    # 开始测试
    test_costs = []                                                         #测试的损失值
    test_accs = []                                                          #测试的准确率
    for batch_id, data in enumerate(test_reader()):
        test_cost, test_acc = exe.run(program=test_program,                 #执行测试程序
                                      feed=feeder.feed(data),               #喂入数据
                                      fetch_list=[avg_cost, acc])           #fetch 误差、准确率
        test_costs.append(test_cost[0])                                     #记录每个batch的误差
        test_accs.append(test_acc[0])                                       #记录每个batch的准确率
    # 求测试结果的平均值
    test_cost = (sum(test_costs) / len(test_costs))                         #计算误差平均值（误差和/误差的个数）
    test_acc = (sum(test_accs) / len(test_accs))                            #计算准确率平均值（ 准确率的和/准确率的个数）
    print('Test:%d, Cost:%0.5f, ACC:%0.5f' % (pass_id, test_cost, test_acc))
    print 'model train %s timecost %ss' % (pass_id, (datetime.now() - begin_time).seconds)
print('03 - 模型训练&评估 完成'.decode("utf-8"))

#保存模型
# 如果保存路径不存在就创建
if not os.path.exists(model_save_dir):
    os.makedirs(model_save_dir)
print ('save models to %s' % (model_save_dir))
fluid.io.save_inference_model(model_save_dir,
                              ['images'],
                              [predict],
                              exe)
print('04 - 模型保存 完成'.decode("utf-8"))

def draw_train_process(title,iters,costs,accs,label_cost,lable_acc):
    plt.title(title, fontsize=24)
    plt.xlabel("iter", fontsize=20)
    plt.ylabel("cost/acc", fontsize=20)
    plt.plot(iters, costs,color='red',label=label_cost) 
    plt.plot(iters, accs,color='green',label=lable_acc) 
    plt.legend()
    plt.grid()
    # plt.show()
    plt.savefig("D:/git/testme/data/catdog_train_process.png")
draw_train_process("training",all_train_iters,all_train_costs,all_train_accs,"trainning cost","trainning acc")

def load_image(file):
    #打开图片
    im = Image.open(file)
    #将图片调整为跟训练数据一样的大小 32*32，设定ANTIALIAS，即抗锯齿.resize是缩放
    im = im.resize((32, 32), Image.ANTIALIAS)
    #建立图片矩阵 类型为float32
    im = np.array(im).astype(np.float32)
    #矩阵转置 将 opencv的 [高度，宽度，通道] 转为 paddlepaddle的 [通道，高度，宽度]
    im = im.transpose((2, 0, 1))                               
    #将像素值从【0-255】转换为【0-1】
    im = im / 255.0
    print(im[0][1])      
    im = np.expand_dims(im, axis=0)
    # 保持和之前输入image维度一致
    print('im_shape demension：', im.shape)
    return im

def load_image2(file):
    import cv2
    im = cv2.imread(filename=file)
    im = cv2.resize(src=im, dsize=(32, 32))
    im = im.transpose((2, 0 , 1))
    im = (im / 255.0).astype(np.float32)
    im = np.expand_dims(im, axis=0)
    print('im_shape demension：', im.shape)
    return im

# infer_path='D:/git/testme/data/dog2.png'
# img = load_image2(infer_path)

# 模型预测
model_save_dir = "D:/git/testme/data/catdog.inference.model"
use_cuda = False
place = fluid.CUDAPlace(0) if use_cuda else fluid.CPUPlace()
infer_exe = fluid.Executor(place)
inference_scope = fluid.core.Scope() 
begin_time = datetime.now()
with fluid.scope_guard(inference_scope):
    #从指定目录中加载 推理model(inference model)
    [inference_program, # 预测用的program
     feed_target_names, # 是一个str列表，它包含需要在推理 Program 中提供数据的变量的名称。 
     fetch_targets] = fluid.io.load_inference_model(model_save_dir,#fetch_targets：是一个 Variable 列表，从中我们可以得到推断结果。
                                                    infer_exe)     #infer_exe: 运行 inference model的 executor
    infer_path='D:/git/testme/data/dog2.png'
    # img = Image.open(infer_path)
    # plt.imshow(img)   
    # plt.show()  
    img = load_image2(infer_path)
    results = infer_exe.run(inference_program,                 #运行预测程序
                            feed={feed_target_names[0]: img},  #喂入要预测的img
                            fetch_list=fetch_targets)          #得到推测结果
    print('results',results)
    label_list = [
        "airplane", "automobile", "bird", "cat", "deer", "dog", "frog", "horse",
        "ship", "truck"
        ]
    print("infer results: %s" % label_list[np.argmax(results[0])])
    print("预测结果为：")
    print("----------------------------")
    probs = results[0][0]
    max_idx = np.argmax(probs)
    for idx in range(10):
        prob = "{0:4}: {1:10s}: {2:.4f}".format(idx, label_list[idx], probs[idx])
        if idx == max_idx:
            print(prob + " ok")
        else:
            print(prob)
print 'model predict timecost %ss' % ((datetime.now() - begin_time).seconds)
print('05 - 模型预测 完成'.decode("utf-8"))





