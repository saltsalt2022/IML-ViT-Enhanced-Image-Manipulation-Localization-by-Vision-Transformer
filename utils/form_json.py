import json

# Define file paths
tp_file = r'D:/study_data/study/classes/3up/new_shot_class/homework/code/MIL-VIT/IML-ViT-main/IML-ViT-main/casia/tp_list.txt'
au_file = r'D:/study_data/study/classes/3up/new_shot_class/homework/code/MIL-VIT/IML-ViT-main/IML-ViT-main/casia/au_list.txt'
output_json = r'D:/study_data/study/classes/3up/new_shot_class/homework/code/MIL-VIT/IML-ViT-main/IML-ViT-main/casia/dataset.json'

# Function to read lines from file and clean them
def read_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

# Read TP and AU files
tp_list = read_file(tp_file)
au_list = read_file(au_file)

# Generate the JSON data structure
dataset = []

# Process TP list to create image_GT pairs
for line in tp_list:
    image_path= line  # Assuming each line has two space-separated paths
    dataset.append([f"D:/study_data/study/classes/3up/new_shot_class/homework/code/MIL-VIT/IML-ViT-main/IML-ViT-main/casia/Tp/{image_path}", f"D:/study_data/study/classes/3up/new_shot_class/homework/code/MIL-VIT/IML-ViT-main/IML-ViT-main/casia/Gt/{image_path.replace('.jpg', '_gt.jpg').replace('.png', '_gt.png').replace('.tif', '_gt.tif')}"])

# Process AU list to create image_label pairs
for line in au_list:
    image_path=line  # Assuming each line has two space-separated elements
    label = "Negative"
    dataset.append([f"D:/study_data/study/classes/3up/new_shot_class/homework/code/MIL-VIT/IML-ViT-main/IML-ViT-main/casia/Au/{image_path}", label])

# Write the output to a JSON file
with open(output_json, 'w') as json_file:
    json.dump(dataset, json_file, indent=4)

print(f"Dataset JSON file has been successfully created at {output_json}")
