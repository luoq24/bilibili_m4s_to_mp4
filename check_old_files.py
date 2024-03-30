import os


def read_mp4_headers(directory):
    # 遍历目录下的所有文件
    for root, dirs, files in os.walk(directory):
        for filename in files:
            # 确保文件是以 .mp4 结尾的
            if filename.endswith('.mp4'):
                filepath = os.path.join(root, filename)
                try:
                    # 打开文件并读取前 32 个字节
                    with open(filepath, 'rb') as f:
                        header_data = f.read(32)
                    # 打印文件名和文件头的前 32 位数据
                    print(f"File: {filename}, Header: \n{header_data}")
                except Exception as e:
                    print(f"Error reading file {filename}: {e}")


def read_mp4_name(directory):
    # 遍历目录下的所有文件
    for root, dirs, files in os.walk(directory):
        for filename in files:
            # 确保文件是以 .mp4 结尾的
            if filename.endswith('.mp4') or filename.endswith('.flv'):
                print(filename)


if __name__ == '__main__':
    # 指定目录进行遍历
    directory_path = 'J:/Misamisa s/source'
    # read_mp4_headers(directory_path)
    read_mp4_name(directory_path)
