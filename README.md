# facelocker

因为公司要求离开电脑必须锁屏，于是写了`facelocker`这个小工具来实现自动锁屏。原理就是每隔5秒调用摄像头进行拍照，如果未在图像中检测到人脸，则锁屏。面部识别使用了[face_recognition](https://github.com/ageitgey/face_recognition)库，以后有时间可以考虑升级为人脸识别锁屏。 

## 使用方式

```bash
# maybe different
git clone https://github.com/zhvala/facelocker.git
cd facelocker
chmod +x run_facelocker.sh
sh run_facelocker.sh
```

## 支持平台

| 操作系统 | 是否支持 |
| -------- | -------- |
| Mac OS X | 支持     |
| Linux    | 支持dibian系     |
