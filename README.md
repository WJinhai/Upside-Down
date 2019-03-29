# 倒置图像识别

## 目前方法

用SIFT提取特征，根据特征点进行匹配。若匹配到特征点对数量满足特定阈值，则认为匹配成功；若不满足，认为匹配失败。

![image](https://github.com/foamliu/Upside-Down/raw/master/images/current_method.png)

## 倒置问题

同一张图，特征点仍可匹配，是倒置图通过检测的原因。

匹配过程中得到单应矩阵（H矩阵）

单应矩阵中包含旋转信息
获取此信息即可知是否倒置

![image](https://github.com/foamliu/Upside-Down/raw/master/images/upside_down.png)

## 欧拉角

欧拉角（Euler Angles）是一种描述三维旋转的方式：

![image](https://github.com/foamliu/Upside-Down/raw/master/images/euler_angles.png)

## 正置与倒置欧拉角的差别

![image](https://github.com/foamliu/Upside-Down/raw/master/images/compare.png)

## 倒置判别

当Roll > π/2（1.57） 或 < - π/2（-1.57） 时确认为倒置。
