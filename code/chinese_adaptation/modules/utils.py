# trump_annotation/utils.py
import os

def ensure_dir_exists(path: str):
    """
    如果目录不存在则创建。
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)


def get_output_path(input_csv_path: str, output_dir: str) -> str:
    """
    根据输入CSV文件名生成输出XML路径。
    """
    filename = os.path.splitext(os.path.basename(input_csv_path))[0] + ".xml"
    return os.path.join(output_dir, filename)
