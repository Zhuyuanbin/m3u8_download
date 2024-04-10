import os
import subprocess



def merge_ts_namelist_to_mp4(ts_folder, output_file):
    # 获取文件夹内所有TS文件
    ts_files = [f for f in sorted(os.listdir(ts_folder)) if f.endswith('.ts')]
    
    if not ts_files:
        print("No TS files found in the folder.")
        return
    
    print("开始生成ffmpeg读取文件列表")
    ts_files_fullname= os.path.join(ts_folder, "nameList.txt")
    with open(ts_files_fullname, "w") as f:
        for file_name in ts_files:
            f.write("file '{}'\n".format(file_name))
    print(f"生成{ts_files_fullname}文件列表成功")



    # 构造ffmpeg命令
    ffmpeg_command = [
        'ffmpeg',
        '-f', 'concat',
        '-i', ts_files_fullname,
        '-c', 'copy',
        output_file
    ]
    # 执行ffmpeg命令
    try:
        subprocess.run(ffmpeg_command, check=True)
        print("Merge completed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print("Error merging files:", e)
    return False

def merge_ts_to_mp4(ts_folder, output_file):
    # 获取文件夹内所有TS文件
    ts_files = [f for f in sorted(os.listdir(ts_folder)) if f.endswith('.ts')]
    
    if not ts_files:
        print("No TS files found in the folder.")
        return
    
    # 生成ffmpeg命令
    ffmpeg_command = [
        'ffmpeg',
        '-i', 'concat:' + '|'.join([os.path.join(ts_folder, f) for f in ts_files]),
        '-c', 'copy',
        output_file
    ]
    #print(ffmpeg_command)
    # 执行ffmpeg命令
    try:
        subprocess.run(ffmpeg_command, check=True)
        print("Merge completed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print("Error merging files:", e)
    return False

# 设置文件夹和输出文件
ts_folder = './wwmxd'
output_file = './output.mp4'

# 调用函数进行合并
#merge_ts_to_mp4(ts_folder, output_file)

output_file = './output1.mp4'
merge_ts_namelist_to_mp4(ts_folder, output_file)