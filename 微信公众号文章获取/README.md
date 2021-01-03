## 保存微信公众号付费文章至本地的方法

微信公众号付费文章完成付费后，并不能右键复制，所以很多优质文章无法保存。

本文将详述如何将微信公众号付费文章保存至本地。

**工具**：

```text
1. fiddler
	用于抓包
2. https://zaixianwangyebianji.bmcx.com/
	用于将html文本转换为正常的文章
```

### 1、抓包

打开fiddler

工具——选项——HTTPS

![fiddler](https://github.com/LMFrank/CrawlerProject/blob/master/%E5%BE%AE%E4%BF%A1%E5%85%AC%E4%BC%97%E5%8F%B7%E6%96%87%E7%AB%A0%E8%8E%B7%E5%8F%96/image/fiddler.jpg)

寻找包含`s?__biz=&mid=`字段的URL

![fiddler01](https://github.com/LMFrank/CrawlerProject/blob/master/%E5%BE%AE%E4%BF%A1%E5%85%AC%E4%BC%97%E5%8F%B7%E6%96%87%E7%AB%A0%E8%8E%B7%E5%8F%96/image/fiddler01.jpg)

寻找文章主体部分，可以参考查找`<div class="rich_media_content`字段，复制`div`标签内的所有内容

### 2、转换html文本

打开https://zaixianwangyebianji.bmcx.com/

先点击`html代码`按钮

![html](https://github.com/LMFrank/CrawlerProject/blob/master/%E5%BE%AE%E4%BF%A1%E5%85%AC%E4%BC%97%E5%8F%B7%E6%96%87%E7%AB%A0%E8%8E%B7%E5%8F%96/image/html.jpg)

复制之前的内容

再点击`html代码`按钮

这样文章的正常格式就会显示出来，可以自行复制保存



参考：

1、https://www.juyifx.cn/article/498322890.html