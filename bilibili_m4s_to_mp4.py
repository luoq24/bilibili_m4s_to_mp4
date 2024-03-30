import glob
import re
import subprocess
import json
import os

# 函数源代码来源 https://www.bilibili.com/video/BV1gv4y1M7yn


def fix_m4s(m4s_path: str, mp4_path: str, bufsize: int = 256 * 1024 * 1024) -> None:
    assert bufsize > 0
    with open(m4s_path, "rb") as target_file:
        header = target_file.read(32)

        # 核心：文件头修正
        new_header = header.replace(b"000000000", b"")
        new_header = new_header.replace(b"$", b" ")
        if new_header.find(b"avc1") > 0:
            new_header = new_header.replace(b"avc1", b"")
        elif new_header.find(b"isomiso") > 0:
            new_header = new_header.replace(b"isomiso", b"iso")
        else:
            raise Exception("新的 m4s 头，不会解析!")

        with open(mp4_path, "wb") as output_file:
            output_file.write(new_header)
            i = target_file.read(bufsize)
            while i:
                output_file.write(i)
                i = target_file.read(bufsize)


def clean_filename(filename):
    # 定义不允许在Windows文件名中出现的特殊字符
    illegal_chars = r'[\/:*?"<>|]'

    # 使用正则表达式将非法字符替换为空格
    cleaned_filename = re.sub(illegal_chars, '', filename)

    return cleaned_filename


def main():
    DIR_DOWNLOAD = "./video_downloads"
    DIR_OUTPUT = "."
    SUBFIX_CONVERTED = '_converted'
    for root, dirs, files in os.walk(DIR_DOWNLOAD):
        # print(root, dirs, files)
        if root != DIR_DOWNLOAD and not root.endswith(SUBFIX_CONVERTED):
            print('开始处理目录：', root)
            m4s_files = glob.glob("*.m4s", root_dir=root)
            mp4_file_list = []

            for m4s_file in m4s_files:
                m4s_path = os.path.join(root, m4s_file)
                mp4_path = m4s_path.rsplit(".", 1)[0] + ".mp4"
                fix_m4s(m4s_path, mp4_path)
                mp4_file_list.append(mp4_path)

            # print(mp4_file_list)

            with open(os.path.join(root, ".videoinfo"), "rb") as f:
                videoinfo = f.read()
                videoinfo = str(videoinfo, "utf-8")
                json_videoinfo = json.loads(videoinfo)
                mp4_file_name = clean_filename(json_videoinfo["title"]) + ".mp4"
                path_out = os.path.join(DIR_OUTPUT, mp4_file_name)

            subprocess.run(
                f'ffmpeg.exe -i {mp4_file_list[0]} -i {mp4_file_list[1]} -c copy "{path_out}"'
            )

            os.remove(mp4_file_list[0])
            os.remove(mp4_file_list[1])

            # 处理过的文件夹，标注为的 converted
            dir_new = root + SUBFIX_CONVERTED
            os.rename(root, dir_new)

            print('合成完毕：', mp4_file_name)


if __name__ == '__main__':
    main()
