import argparse
import os
from typing import List

import cv2
import numpy as np

# 支持识别的图片扩展名集合
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff', '.gif'}


def iter_images(folder: str) -> List[str]:
	"""Return image file paths under folder, ordered by relative path."""
	if not os.path.isdir(folder):
		raise FileNotFoundError(f"输入文件夹不存在: {folder}")
	entries = []
	for root, _, files in os.walk(folder):
		for name in files:
			if os.path.splitext(name)[1].lower() in IMAGE_EXTENSIONS:
				entries.append(os.path.join(root, name))
	entries.sort(key=lambda path: os.path.relpath(path, folder))
	return entries


def _target_rel_path(rel_path: str) -> str:
	base, _ = os.path.splitext(rel_path)
	return f"{base}.jpg"


def read_image(path: str):
	"""Read image with Unicode path support."""
	try:
		data = np.fromfile(path, dtype=np.uint8)
	except OSError as exc:
		print(f"警告: 无法读取图片 {path}: {exc}")
		return None
	if data.size == 0:
		print(f"警告: 文件为空或无法读取 {path}")
		return None
	image = cv2.imdecode(data, cv2.IMREAD_COLOR)
	if image is None:
		print(f"警告: 解码图片失败 {path}")
	return image


def save_jpeg(path: str, image, quality: int = 95) -> bool:
	"""Save image as JPEG handling Unicode paths."""
	ok, buffer = cv2.imencode('.jpg', image, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
	if not ok:
		return False
	try:
		buffer.tofile(path)
		return True
	except OSError as exc:
		print(f"警告: 写入 JPEG 失败 {path}: {exc}")
		return False


def sample_images(input_dir: str, output_dir: str, interval: int) -> None:
	if interval <= 0:
		raise ValueError("抽取间隔必须大于 0")
	images = iter_images(input_dir)
	if not images:
		print(f"未在 {input_dir} 找到图片文件。")
		return
	os.makedirs(output_dir, exist_ok=True)
	saved = 0
	for idx, img_path in enumerate(images):
		if idx % interval == 0:
			rel_name = os.path.relpath(img_path, input_dir)
			rel_jpg = _target_rel_path(rel_name)
			target_path = os.path.join(output_dir, rel_jpg)
			target_dir = os.path.dirname(target_path)
			if target_dir:
				os.makedirs(target_dir, exist_ok=True)
			image = read_image(img_path)
			if image is None:
				continue
			if not save_jpeg(target_path, image):
				print(f"警告: 保存 JPEG 失败 {target_path}")
				continue
			saved += 1
	print(f"从 {len(images)} 张图片中抽取并保存 {saved} 张到 {output_dir}")


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="按照间隔抽取图片")
	parser.add_argument('--input_dir', required=True, help='输入图片文件夹路径')
	parser.add_argument('--output_dir', required=True, help='输出图片文件夹路径')
	parser.add_argument('--interval', type=int, required=True, help='抽取间隔（每隔多少张保存一张）')
	return parser.parse_args()


def main() -> None:
	args = parse_args()
	sample_images(args.input_dir, args.output_dir, args.interval)


if __name__ == '__main__':
	main()