# bigpipe（pagelet）
Bigpipe是Facebook发明的一种非阻塞式模型。
BigPipe目标：前后端分离，提高页面渲染速度。
它主要用来解决http请求的两大问题：
HTTP协议的底层是TCP/IP，而TCP/IP规定三次握手才建立一次连接。每一个新增的请求都要重新建立TCP/IP连接，从而消耗服务器的资源，而对于几种不同的服务器程序——Apache、Nginx、Node.js——所消耗的资源也不太一样。
现有的阻塞模型中，服务器生成页面需要时间（page generation），网络传输需要时间（network latency），页面在浏览器中渲染需要时间（page rendering），三者是阻塞式的，整个页面作为一个大块，需要完整地经历三个阶段，才能出现在浏览器中。
Bigpipe的实现原理：把页面分为很多模块— —称之为pagelet，比如头部、内容区域、边栏等等……Bigpipe允许客户端跟服务器建立一条管道，内容可以源源不断地输送过来。首先输送的是html+css，接下来会传输很多js对象，然后有专门的js代码来把对象所代表的内容渲染到页面上。这样在用户的感知上，页面超快。
BigPipe VS Ajax
BigPipe: 1、发送一个请求后多次返回数据
2、浏览器和服务器工作并行执行
3、只有一个请求，对服务器压力少
AJAX： 1、发送一个请求后只返回一次数据
2、浏览器和服务器工作顺序执行
3、有多个请求，对服务器压力大


# kafka（partition，replica，zookeeper）
Kafka不支持一个partition中的message由两个或两个以上的同一个consumer group下的consumer thread来处理，除非再启动一个新的consumer group。。所以如果想同时对一个topic做消费的话，启动多个consumer group就可以了。kafka为了保证吞吐量，只允许同一个consumer group下的一个consumer线程去访问一个partition。如果觉得效率不高的时候，可以加partition的数量来横向扩展，那么再加新的consumer thread去消费。如果想多个不同的业务都需要这个topic的数据，起多个consumer group就好了，大家都是顺序的读取message，offsite的值互不影响。这样没有锁竞争，充分发挥了横向的扩展性，吞吐量极高。这也就形成了分布式消费的概念。最优的设计就是，consumer group下的consumer thread的数量等于partition数量，这样效率是最高的。
Kafka是最初由Linkedin公司开发，是一个分布式、支持分区的（partition）、多副本的（replica），基于zookeeper协调的分布式消息系统。
它的最大的特性就是可以实时的处理大量数据以满足各种需求场景。
Kafka的使用场景：
- 日志收集：一个公司可以用Kafka可以收集各种服务的log，通过kafka以统一接口服务的方式开放给各种consumer，例如hadoop、Hbase、Solr等。
- 消息系统：解耦和生产者和消费者、缓存消息等。
- 用户活动跟踪：Kafka经常被用来记录web用户或者app用户的各种活动，如浏览网页、搜索、点击等活动，这些活动信息被各个服务器发布到kafka的topic中，然后订阅者通过订阅这些topic来做实时的监控分析，或者装载到hadoop、数据仓库中做离线分析和挖掘。
- 运营指标：Kafka也经常用来记录运营监控数据。包括收集各种分布式应用的数据，生产各种操作的集中反馈，比如报警和报告。
- 流式处理：比如spark streaming和storm
Kakfa Broker Leader的选举：
选取ISR列表中的一个replica作为partition leader（如果ISR列表中的replica全挂，选一个幸存的replica作为leader; 如果该partition的所有的replica都宕机了，则将新的leader设置为-1，等待恢复，等待ISR中的任一个Replica“活”过来，并且选它作为Leader；或选择第一个“活”过来的Replica（不一定是ISR中的）作为Leader）


# spark 分区
Spark RDD 是一种分布式的数据集，由于数据量很大，因此要它被切分并存储在各个结点的分区当中。从而当我们对RDD进行操作时，实际上是对每个分区中的数据并行操作。
HashPartitioner确定分区的方式：partition = key.hashCode () % numPartitions。
RangePartitioner会对key值进行排序，然后将key值被划分成3份key值集合。
CustomPartitioner可以根据自己具体的应用需求，自定义分区。
从HDFS读入文件默认是怎样分区的：
Spark从HDFS读入文件的分区数默认等于HDFS文件的块数(blocks)，HDFS中的block是分布式存储的最小单元。如果我们上传一个30GB的非压缩的文件到HDFS，HDFS默认的块容量大小128MB，因此该文件在HDFS上会被分为235块(30GB/128MB)；Spark读取SparkContext.textFile()读取该文件，默认分区数等于块数即235。
分区数太多意味着任务数太多，每次调度任务也是很耗时的，所以分区数太多会导致总体耗时增多。
合理的分区数是多少？如何设置？总核数=executor-cores * num-executor。一般合理的分区数设置为总核数的2~3倍

# olap

# elasticsearch
