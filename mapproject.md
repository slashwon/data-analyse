## OpenStreetMap Data Case Study   

---

## 地图区域
##### 中国，北京
* https://s3.amazonaws.com/mapzen.odes/ex_oMXexDr8EPEf7E8hBiT6dcKTPV2M7.osm.bz2

###### 选择该区域主要是由于工作在北京，对于一些地址比较熟悉。
## Problems Encountered

---
##### 原始数据大小：281.1Mb, 压缩样本大小：2.8Mb
##### 原始数据下载之后，通过转换格式导入数据库查询的方式查看数据，并没有发现有明显的异常信息，比如格式，时间戳错误等等，原始数据似乎比较干净
##### 再次筛查后发现如下几个问题：
* 在tag节点下，有些数据的key对应的属性是FixMe
* k属性有一些值是中文表示，而同字段的其他标签都是英文表示
* 在ways下面的node节点中，有一处数据value是韩语，但key标明是name:en
* nodes节点下，user数量和uid数量不一一致

### 以下是针对上述问题的解决方案：
#### 1. FIXME
##### 将含有'FixMe'的tag标签过滤:
```
if 'fixme' in tag.attrib['k'] or \
'FIXME' in tag.attrib['k']:
          continue
```
#### 2. 中文字符:
```
疏散人数
车库
黄南苑小区
```
##### 翻译成拼音.

#### 3. 韩语对应key值错误:

#### 从数据库中将其对应的key修改为name:kor
```
update nodes_tags set key='name:kor' where id =273092476 and key='name:en'
```
#### 4. nodes表中user和uid数量不一致
* 通过select命令查询user有1972个，uid有1968个
* 查找出现问题的user和对应的uid：
```
    def audit_user_uid():
        uid_raw = dao.my_execute("select distinct uid from nodes")
        uid_user = {}
        for uidd in uid_raw:
            uid = uidd[0]
            if uid not in uid_user:
                uid_user[uid]=set()
            user = dao.my_execute("select user from nodes where uid = \'" +str(uid)+"\'")
            for u in user:
                uid_user[uid].add(u[0])
    
        wrong = {}
        for uid, userset in uid_user.items():
            # 如果uid对应的user不止一个，就认为是有问题的
            if len(userset)>1:
                wrong[uid]=userset
    
        p.pprint("有问题的uid：")
        p.pprint(wrong)
```
* 上面代码执行结果：
```
     573955: {'MrX_FF', 'Haruka_ff'},
     4794671: {'快乐书香虎', 'booktiger'},
     6558010: {'duxiao', 'duxxp'},
     7120005: {'OOXXOO', 'Zerg~'}}
```
* 分析有可能是用户改了名，也可能是同一个用户的别名

###  项目主要过程:
* 将.osm文件转成.csv.
* 将.csv导入数据库.
* 检验数据，查看是否有格式错误.
* 使用SQL语句查询数据库.

### 项目中代码文件：
#### (1). check_data.py
* 检查时间戳是否合法，主要检验格式是否一致，日期，时分秒是否有数值错误
* 接口：check_timestamp

#### (2). common_tools.py
* 检验字符串中是否包含中文字符

#### (3). constant.py
* 常量数据模块，包含了数据库中各个字段名称

#### (4). dao.py
* 数据库操作模块
* 接口：execute 负责对指定的数据表执行sql语句

#### (5). main.py
* 测试类，包含了主要操作

#### (6). openstreetmap.py
* 原始osm文件的操作类，主要是解析osm中的各个节点，整理数据模型，并输出.csv文件格式.
* 注: 将csv文件导入到数据库时，没有找到相关的python api， 使用db.execute()方法，会报错，因此这里直接在sql shell执行插入数据命令:
    ```
        .mode csv
        .import nodes.csv nodes
        .import nodetags.csv nodes_tags
        .import ways.csv ways
        .import waytag.csv ways_tags
        .mode list
    ```
    
###数据库的查询结果
* 唯一用户数量：1972
* highway的数量：14068， shop的数量:1668
* nodes中的数据个数:1304097, ways中的数据个数168667