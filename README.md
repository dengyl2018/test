# test
测试用，随便尝试

# 20181222
开始使用github
目标：1、熟悉一些常用的代码概念
2、将代码间的概念进行整合升级

git add .
git commit -m"test"
git push

# 20191106
房价预测：model/house_price_model.py

# 20191123
知识图谱：
决策：认知规则 + 记忆知识。
爬虫：从外面获取数据，从而总结或预测。

模型 = 网络结构 + 模型参数
架构（Architecture）和框架（Framework）：框架是软件（半成品），架构不是软件，是关于软件如何设计的重要策略。我们不能指着某些代码，说这就是软件架构，因为软件架构是比具体代码高一个抽象层次的概念。架构势必被代码所体现和遵循，但任何一段具体的代码都代表不了架构。
软件通过架构，可以设计出很多不同的框架。在一个框架中，也可以使用很多的设计模式。
一个典型的模型通常包含4个部分，分别是：输入数据定义，搭建网络（模型前向计算逻辑），定义损失函数，以及选择优化算法。

https://www.paddlepaddle.org.cn/documentation/docs/zh/beginners_guide/index_cn.html
https://github.com/PaddlePaddle/book/blob/develop/02.recognize_digits/train.py
fc:全连接网络
cross_entropy
Adam
RNN
learning rate scheduler
layers.relu
program = layers + tensor-variable
batch - Epoch - shuffle - random crop - flip
python - generator - yield


模型并行：数据统一，模型拆分到各个机器：
数据并行：模型复制，数据拆分到各个机器：
parameter server进程，保存完整的模型参数，各个trainer进程请求pserver同步。
collective模式：每个trainer进程都保存一份完整的模型参数。
分布式程序转换器：DistributeTranspiler
VisualDL可视化模型评估指标：损失函数 准确率


