import os

# 设置文件夹路径
folder_path = r'D:\study_data\study\classes\3up\new_shot_class\homework\code\MIL-VIT\IML-ViT-main\IML-ViT-main\casia\Gt'  # 替换为你要处理的文件夹路径

# 获取文件夹中所有文件
for filename in os.listdir(folder_path):
    # 构建文件的完整路径
    file_path = os.path.join(folder_path, filename)
    
    # 检查文件是否是文件而不是子文件夹
    if os.path.isfile(file_path):
        # 分离文件名和扩展名
        name, ext = os.path.splitext(filename)
        
        # 如果扩展名不是.png，则修改为.png
        if ext.lower() != '.png':
            new_filename = name + '.png'  # 新文件名
            new_file_path = os.path.join(folder_path, new_filename)
            
            # 重命名文件
            os.rename(file_path, new_file_path)
            print(f'已将 "{filename}" 重命名为 "{new_filename}"')
