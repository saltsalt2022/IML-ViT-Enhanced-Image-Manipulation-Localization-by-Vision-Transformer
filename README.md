This project enhances Vision Transformer (ViT) for image manipulation localization. Updates include single-GPU training, checkpoint handling, parameter freezing, and adjusted model saving/testing. A new classification branch, trained with BCEWithLogitsLoss, predicts image authenticity.

### 1.对代码的修改包括：

将分布式改为可选在单一显卡上运行

将仅支持读取完整的checkpoint改为可支持读取仅包含state_dict of model的checkpoint.pth

冻结非 `predict_head` 和 `global_classifier` 开头的参数，将 `requires_grad` 设置为 `False`。

每50epoch保存一次模型改为每2次，每训练4次测试1次改为每1一次都测试

在utils中增加了一个json文件和生成器，读取tp_list.txt和au_list.txt生成对应要求格式的json文件，以保证训练时能够读入真实图像Au,由于GT中全是png的格式，与Tp中不一致，为方便生成json，将Tp中非png格式的图片全部改为png，同时修改Tp_list

### 2.对模型的修改：

![](D:\study_data\study\classes\3up\new_shot_class\homework\作业4-github复现实践\绘图1.jpg)

#### 在decoderhead的PredictHead 模块中增加分类值预测分支：

原来仅有像素级预测`mask_logits` ，它将特征融合的结果进行规范化、失活处理（self.norm` 、 `self.dropout），最终通过卷积层（self.linear_predict）将融合特征的通道数转换为目标通道数，生成每个像素的预测值。

现在新增分类值预测分支`class_logits`，它将特征融合的结果通过全局平均池化缩小为一个标量，再展平为一维向量，最后通过全连接层得到图像的分类预测值。然后有两个使用方案：我比较后选择了方案二：

###### 方案一：基于GT_mask的均值计算预测值

通过计算 `GT_mask`（裁剪为原始图像大小后） 的均值作为预测值，再与 全连接生成的分类值 直接进行损失计算，即以此代表伪造区域在整个图像中的比例。这种方法的缺点在于，伪造区域在整个图像中的比例不太make sense，关键是判断有无伪造，而不是伪造的多少；并且如果伪造的比例太小，容易被误判为没有伪造。

###### **方案二：根据masks是否为空生成标签，计算BCEloss**

将分类值 通过 `sigmoid()` 激活函数转换为预测概率，并与预测标签计算 `BCEWithLogitsLoss`。其中预测标签的生成原理为：直接检查 `masks`.max 是否为0，如果 ==0 则生成标签 `1`（伪造），否则生成标签 `0`（真实）。

### 结果

根据文末中的训练的数据可以看到训练4了epoch的时候calss_loss的更新就比较缓慢了，然后修改Demo对测试图像进行测试，可用看到里面输出class_logits预测值为0.9876接近1，可以清晰分辨这是伪造图像。![image-20241213141050350](C:\Users\salt salt\AppData\Roaming\Typora\typora-user-images\image-20241213141050350.png)





### 实验中遇到的问题：

1.没有理解清楚它数据集读取的方式，没有使用Au图像进行训练，导致得到的模型输出的分类值都近1，得重新训练了。。

2.添加了Au图像之后则变成输出的分类值都近0，我认为这是因为json文件没有对图像进行打乱，而是按TP组和Au组的顺序排列，导致训练时相当于使用全假训练1epoch后再用全真训练1epoch。

3.还有一个是以为真实图像的mask是NONE的，后面发现是会生成全为0的mask

4.test_batch_size默认是2，导致我的一些改动有问题，后面debug发现改好就行了。

