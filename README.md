# 论如何成为一个合格的阴阳带师

[TOC]

## 写在前面

这是一个关于阴阳师的脚本，如果你不小心点进来了，赶紧出去，现在还来得急。

**重要声明：**

1. 本篇文章是描述我怎么学习python的，而不是鼓励大家去用脚本来打破游戏平衡，降低自己和他人的游戏体验。

2. **仅供学习参考，不允许用于任何商业用途。**使用该脚本造成任何后果与本人无关（主要是怕网易干我哈哈哈，网易如果想招我是可以考虑下的嘻嘻，毕竟去年面过网易）

3. **严禁任何转载**，毕竟万一以后火了，网易要打我，我只能说，与我无瓜，需要删除时跟我说啊，我删除不就完了嘛，但是总要给点巨款啥的吧哈哈哈。 *如果非有人要转载我的，我也没办法了啊，我也没时间去告他对吧，所以如果有所传播，那网易你们去追责这些人嗷。（歪头）*

4. 最后，希望所有阴阳师玩家、爱好者都谨慎使用，技术无罪，人心不古。祝大家都能抽到喜欢的式神。

5. **献给所有反抗996的打工人。**

   20210110，山东烟台

有哪里不懂的留言告诉我嗷，我会补充的。暂时不想写太细。（懒）

> 如果网易也不问我，也不跟我沟通，就让CSDN啥的（我肯定也有其他平台的博客）删我博客，我告诉你嗷，这是在玩火。这样的话，我一定不会屈服。

## 0. 从零开始

1. 首先，我想做一个双开刷御魂的脚本。这就需要：**识别挑战的位置**

   ![在这里插入图片描述](https://img-blog.csdnimg.cn/20210110081703644.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzIxNTc5MDQ1,size_16,color_FFFFFF,t_70#pic_center)

   ![在这里插入图片描述](https://img-blog.csdnimg.cn/20210110081434203.png)

2. 所以首先要做的就是：识别整个桌面上挑战的位置，然后点击，就可以开始刷图了对吧。

3. 这个观念也是这个脚本的核心，那就是从图片（整个阴阳师截图）上找到目标图片（挑战截图）的位置，然后利用鼠标模拟点击，实现各种流程的控制。后面无论是刷御魂也好，刷结界突破也好，带狗粮也是，都是这个思路。

## 1. 找到阴阳师程序

1. 所以我们最开始，也是最重要的，就是找到所有阴阳师程序（双开就是两个，所以叫所有），并获得页面的截图。

2. 直接上代码：

   ```python
   def find_onmyoji_handle():
       """找到所有阴阳师的界面的句柄，如果是多个同类的窗口，谁最后打开的，谁优先获取"""
       # 获取后台窗口的句柄，注意后台窗口不能最小化
       handle_name = '阴阳师-网易游戏'
       # 获取第一个阴阳师的句柄
       handle_last = win32gui.FindWindowEx(0, 0, "Win32Window", handle_name)
       handles = [handle_last]
       # 遍历获取其他阴阳师的句柄
       while True:
           handle_last = win32gui.FindWindowEx(0, handle_last, "Win32Window", handle_name)
           if handle_last == 0:
               break
           handles.append(handle_last)
   
       return handles
   ```

## 2. 获取截图

1. 程序都找到了，这里就要把图截下来，然后找目标图了对吧。

2. 直接上代码：

   ```python
   def show_handle(hWnd):
       """获取句柄的截图"""
       # 获取句柄窗口的大小信息
       left, top, right, bot = win32gui.GetWindowRect(hWnd)
       width = right - left
       height = bot - top
       # 返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
       hWndDC = win32gui.GetWindowDC(hWnd)
       # 创建设备描述表
       mfcDC = win32ui.CreateDCFromHandle(hWndDC)
       # 创建内存设备描述表
       saveDC = mfcDC.CreateCompatibleDC()
       # 创建位图对象准备保存图片
       saveBitMap = win32ui.CreateBitmap()
       # 为bitmap开辟存储空间
       saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
       # 将截图保存到saveBitMap中
       saveDC.SelectObject(saveBitMap)
       # 保存bitmap到内存设备描述表
       saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)
   
       def save_by_PIL(is_save=False, is_show=False):
           """方法1"""
           # 获取位图信息
           bmpinfo = saveBitMap.GetInfo()
           bmpstr = saveBitMap.GetBitmapBits(True)
           # 生成图像
           im_PIL = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
   
           if is_save:
               im_PIL.save("im_PIL.png")
           if is_show:
               im_PIL.show()
           return im_PIL
   
       def save_by_windows_api(is_save=False):
           """方法2"""
           if is_save:
               saveBitMap.SaveBitmapFile(saveDC, "img_Winapi.bmp")
           return saveBitMap
   
       def save_by_opencv(is_save=False, is_show=False):
           """方法3"""
           # 获取位图信息
           signedIntsArray = saveBitMap.GetBitmapBits(True)
           # PrintWindow成功，保存到文件，显示到屏幕
           im_opencv = np.frombuffer(signedIntsArray, dtype='uint8')
           im_opencv.shape = (height, width, 4)
           cv2.cvtColor(im_opencv, cv2.COLOR_BGRA2RGB)
   
           if is_save:
               cv2.imwrite("im_opencv.jpg", im_opencv, [int(cv2.IMWRITE_JPEG_QUALITY), 100])  # 保存
           if is_show:
               cv2.namedWindow('阴阳师后台截图')  # 命名窗口
               cv2.imshow("阴阳师后台截图", im_opencv)  # 显示
               cv2.waitKey(0)
               cv2.destroyAllWindows()
           return im_opencv
   ```

## 3. 在截图中找到目标图片的位置

### ~~3.1 使用aircv~~

1. 因为我是双开，所以目标截图需要在两个图中找。

2. 这里要用到aircv，如果安装报错：`AttributeError: module 'cv2.cv2' has no attribute 'xfeatures2d'`

   - 解决方法：要安装一个包：`pip install opencv-contrib-python`

   - 这里还有一个很重要的问题，就是即使把cv和上述这个包upgrade，也还是会出现：`Process finished with exit code -1073741819 (0xC0000005)`的问题

   - 所以， **最终解决办法 ** 为：

     ```
     pip install opencv-python == 3.4.2.16
     pip install opencv-contrib-python == 3.4.2.16
     ```

   - 参考链接：[module 'cv2.cv2' has no attribute 'xfeatures2d'](https://blog.csdn.net/weixin_43167047/article/details/82841750)

3. 附上代码：

   ```python
   def locate_pic(im_source, im_search_path):
       """获取对应图片在 im_source 的位置"""
       im_search = ac.imread(im_search_path)
       print(ac.find_sift(im_source, im_search))
   ```

4. 这里的im_source，也就是阴阳师的截图，是可以为步骤2中获取的截图的，也就是cv的返回值，后面的im_search是读取目录的对应的目标截图的路径。









------

我的CSDN：https://blog.csdn.net/qq_21579045

我的博客园：https://www.cnblogs.com/lyjun/

我的Github：https://github.com/TinyHandsome

纸上得来终觉浅，绝知此事要躬行~

欢迎大家过来OB~

by 李英俊小朋友