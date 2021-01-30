# 论如何成为一个合格的阴阳带师

[TOC]

## 写在前面 | Write Head

这是一个关于阴阳师的脚本，如果你不小心点进来了，赶紧出去，现在还来得急。

**重要声明：**

1. 本篇文章是描述我怎么学习python的，而不是鼓励大家去用脚本来打破游戏平衡，降低自己和他人的游戏体验。

2. **仅供学习参考，不允许用于任何商业用途。** 使用该脚本造成任何后果与本人无关（主要是怕网易干我哈哈哈，网易如果想招我是可以考虑下的嘻嘻，毕竟去年面过网易）

3. **严禁任何转载**，毕竟万一以后火了，网易要打我，我只能说，与我无瓜，需要删除时跟我说啊，我删除不就完了嘛，但是总要给点巨款啥的吧哈哈哈。 *如果非有人要转载我的，我也没办法了啊，我也没时间去告他对吧，所以如果有所传播，那网易你们去追责这些人嗷。（歪头）*

4. 最后，希望所有阴阳师玩家、爱好者都谨慎使用，技术无罪，人心不古。祝大家都能抽到喜欢的式神。

5. **献给所有反抗996的打工人。**

   20210110，山东烟台

有哪里不懂的留言告诉我嗷，我会补充的。暂时不想写太细。（懒）

> 如果网易也不问我，也不跟我沟通，就让CSDN啥的（我肯定也有其他平台的博客）删我博客，我告诉你嗷，这是在玩火。这样的话，我一定不会屈服。

## 项目计划 | Project Plan

- TODO
  - [ ] 优化配置文件

    - 可以配置多个流程
    - 全空的流程无法运行
    - 封装流程，保存多个流程
    - 流程信息跟配置文件关联，一一对应
    - 如果导入流程，重名的取导入的，最新的要最新的，没有流程取旧的，配置信息全空。
    
  - [ ] 优化点的坐标颜色信息

    - 封装成一个类
    - 该类实现：根据多个点的颜色 **定位状态**
    - 然后点击某个点
    - 所以，这就需要优化每个流程，每个流程块要重复录入多个点信息，来判断是否处于某种状态，如果是则点击。这样用多点信息来定义一个状态，增加了准确性。
    - pro_color：状态颜色点位
    - pro_click：状态颜色对应后，点击的点位
    - pro_cc：既是颜色点位，又是识别后的点击点位
    
  - [ ] 增加补充点位功能
    
    - 发现新的状态后，直接在当前状态补充点位信息
    - 需要有个输入框，输入新增流程名
    - 定义点位补充的时间，放到类中
    - 所以一个功能中每个流程点的信息，必须封装为一个类，有创建时间，修改时间啊啥的（数据库？）
    
    - **注意：** 检测到状态之后，不一定是点一下，可能是点多下，比如关闭双倍御魂，所以功能也要封装，一个功能可能要包含其他功能
    
  - [ ] 补全报错信息位置
  
    - `traceback.format_exc()`和`traceback_print_exc()`
    - 完善异常输出到文件的功能，优化日志输出功能，重构为一个类叭
  
  - [ ] 实现暂停功能
  
  - [ ] 超时报警：
    
    没有点击的时间超过一定时间后，发送微信（邮件）给自己
    
  - [ ] 一键启动阴阳师：
    
    通过`v5沙盒`启动n个应用，所以需要你有`v5`
    
  - [ ] 设置快捷键特效：
    
    按快捷键后，button的按键也会随快捷键出现按下弹起的效果
    
  - [ ] 失败的坐标也要统计
    
    失败后就暂停了，很尴尬
    
  - [ ] 添加时间戳、预计运行时间、剩余体力检测
  
    预计运行时间：每次战斗时间取均值
  
  - [ ] 增加免打扰功能
  
    录入悬赏封印等点击位置，开启后，发现有人悬赏封印等情况，赶紧关掉
  
    做成check的格式，而不是button
  
  - [ ] 增加体力获取功能
  
    从有体力的界面中检测当前体力还剩多少，这样就可以自动计算脚本可以刷多久了
  
  - [ ] 配置文件优化，增加识别目标点颜色后，可以点击其他位置的功能
  
    - 现在是检验到目标点之后就要点击目标点
    
  - [ ] 同步检查到目标点颜色之后点击，否则等待
  
- FINISHED

  - [x] 防检测处理：20210117

    实现鼠标点击随机偏移，鼠标连点随机时间间隔

  - [x] 优化配置文件：20210121

    自动读取功能配置文件中的流程信息（`functions.ini`）

  - [x] 调整窗口大小，在界面输入值进行调整，点击后更新大小：20210123

    第一个窗口：`-10,0,300,width`

    第二个窗口：`-10,width-8,300,width`

    第三个窗口：`width+2,0,300,width`

  - [x] 界面太长，需要重新布局：20210122

    - 调试前：

      ![在这里插入图片描述](https://img-blog.csdnimg.cn/2021012123474372.png)

    - 调试后：

      ![在这里插入图片描述](https://img-blog.csdnimg.cn/20210121235932819.png)

  - [x] 设置界面是否置顶的选项：20210123

  - [x] 新增log日志功能，自动清空7天前的日志：20210123

  - [x] 优化输出功能：20210124

    - 建立信息输出队列，新建一个类，专门处理。
    - 输出放两个label，一个用来存最新，一个用来存历史
    
  - [x] 实现保存到文件功能：20210124

  - [x] 给用户界面参数：20210130

    写死第二个界面纵坐标和第三个位置横坐标的配置参数

- 现有问题：

  1. 无法进行图像识别，需要人工加点

  2. 调整阴阳师位置的时候，可能出现异常，不准确，忽大忽小

     这是因为，阴阳师会自动调整比例，但是设置的时候，长和宽都要设置，所以造成缩放和移动的时候会出现：**一会儿按长调整大小，一会儿按宽调整大小** 的情况。

  

## 从零开始 | Start Zero

1. 首先，我想做一个双开刷御魂的脚本。这就需要：**识别挑战的位置**

   ![在这里插入图片描述](https://img-blog.csdnimg.cn/20210110081703644.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzIxNTc5MDQ1,size_16,color_FFFFFF,t_70#pic_center)

2. 所以首先要做的就是：识别整个桌面上挑战的位置，然后点击，就可以开始刷图了对吧。

3. 这个观念也是这个脚本的核心，那就是从桌面上找到目标图片（挑战截图）中心的位置，然后利用鼠标模拟点击，实现各种流程的控制。后面无论是刷御魂也好，刷结界突破也好，带狗粮也是，都是这个思路。

## 使用方法 | Using Method

> 如果不懂编程的话，下面对你来说真的很难，但是没关系，所有的快乐都是努力之后得到的。成功的喜悦会覆盖所有的懊恼和气馁，一起加油叭。（有任何问题，很简单也不要紧，留言告诉我叭，我会在上面补充的。）

1. **下载`python3.78`**：[官网地址](https://www.python.org/downloads/release/python-378/)，然后安装啊啥的

2. **安装一个特殊的依赖包**：在cmd中输入：`pip install pyHook-1.5.1-cp37-cp37m-win_amd64.whl`，注意，这里的pyHook是拖进来的显示的应该是绝对路径，如下图：（[`pyhook`安装地址](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyhook)）

   ![在这里插入图片描述](https://img-blog.csdnimg.cn/20210120224908459.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzIxNTc5MDQ1,size_16,color_FFFFFF,t_70)

3. 升级一下pip：`python -m pip install --upgrade pip -i https://pypi.douban.com/simple/` 

4. 去我的[GitHub](https://github.com/TinyHandsome/FxxkOnmyoji)，下载工程文件，解压。

   ![在这里插入图片描述](https://img-blog.csdnimg.cn/2021012022520347.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzIxNTc5MDQ1,size_16,color_FFFFFF,t_70)

5. **安装依赖包**：打开文件夹，看到这个`requirements.txt`了没，跟上面安装`whl`一样，输入：`pip install -r requirements.txt -i https://pypi.douban.com/simple/`，这里的`requirements.txt`也是要拖进来的，反正是个绝对路径和相对路径的问题。如果有不懂的，留言，我慢慢补充。（tips：按住shift+右键，可以在当前路径召唤`cmd`或者`powershell`）（懂编程的人，自己看着下包就好了，我这里有很多跟这个项目无关的包，懒得改了）

   ![在这里插入图片描述](https://img-blog.csdnimg.cn/2021012023005290.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzIxNTc5MDQ1,size_16,color_FFFFFF,t_70)

   安装完毕：

   ![在这里插入图片描述](https://img-blog.csdnimg.cn/20210120231522657.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzIxNTc5MDQ1,size_16,color_FFFFFF,t_70)

6. 





------

我的CSDN：https://blog.csdn.net/qq_21579045

我的博客园：https://www.cnblogs.com/lyjun/

我的Github：https://github.com/TinyHandsome

纸上得来终觉浅，绝知此事要躬行~

欢迎大家过来OB~

by 李英俊小朋友