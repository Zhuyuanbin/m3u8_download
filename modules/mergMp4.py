#!/usr/bin/env python3 
# -*- coding:utf-8 _*-  


"""
调用ffmpeg,实现将ts合并成MP4

脚本执行 
-o ts的文件目录 必填
-n 合并的MP4文件名 必填
-t nameList/files  默认是按文件合并
"""

import os
import argparse
import subprocess
from logger import logPrint


def merge_ts_namelist_to_mp4(ts_folder, output_file):
    # 获取文件夹内所有TS文件
    ts_files = [f for f in sorted(os.listdir(ts_folder)) if f.endswith('.ts')]
    
    if not ts_files:
        print("No TS files found in the folder.")
        return
    
    logPrint("开始生成ffmpeg读取文件列表")
    ts_files_fullname= os.path.join(ts_folder, "nameList.txt")
    with open(ts_files_fullname, "w") as f:
        for file_name in ts_files:
            f.write("file '{}'\n".format(file_name))
    logPrint(f"生成{ts_files_fullname}文件列表成功")



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

# copy/b *.ts aa.mp4



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
    print(ffmpeg_command)
    # 执行ffmpeg命令
    try:
        subprocess.run(ffmpeg_command, check=True)
        print("Merge completed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print("Error merging files:", e)
    return False







if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="merg ts file to mp4")
    parser.add_argument("-o", "--output", help="ts files directory ", required=True)
    parser.add_argument("-n", "--name", help="merg ts to movie name", required=True)
    parser.add_argument("-t", "--type", help="use files or files nameList to merg ", required=False)
    args = parser.parse_args()

    merg_type = "files"

    if args.type:
        merg_type = args.type

    if merg_type == "files":
        merge_ts_to_mp4(args.output,args.name)
    elif merg_type == "nameList":
        merge_ts_namelist_to_mp4(args.output, args.name)
    else:
        print(f"{merg_type} is not avaliable args, please input -t nameList or -t files")