import os
import argparse
import cv2
import numpy as np

IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff', '.gif'}

def iter_images(folder):
	images = []
	for root, _, files in os.walk(folder):
		for name in files:
			if os.path.splitext(name)[1].lower() in IMAGE_EXTENSIONS:
				images.append(os.path.join(root, name))
	images.sort(key=lambda x: os.path.relpath(x, folder))
	return images

def read_image_unicode(path):
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

def save_jpeg_unicode(path, image, quality=95):
	ok, buffer = cv2.imencode('.jpg', image, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
	if not ok:
		return False
	try:
		buffer.tofile(path)
		return True
	except OSError as exc:
		print(f"警告: 写入 JPEG 失败 {path}: {exc}")
		return False

def convert_images(input_dir, output_dir):
	images = iter_images(input_dir)
	if not images:
		print(f"未在 {input_dir} 找到图片文件。")
		return
	for img_path in images:
		rel_path = os.path.relpath(img_path, input_dir)
		base, _ = os.path.splitext(rel_path)
		out_path = os.path.join(output_dir, base + '.jpg')
		out_dir = os.path.dirname(out_path)
		if out_dir:
			os.makedirs(out_dir, exist_ok=True)
		image = read_image_unicode(img_path)
		if image is None:
			continue
		if not save_jpeg_unicode(out_path, image):
			print(f"警告: 保存 JPEG 失败 {out_path}")
	print(f"已完成 {len(images)} 张图片的格式转换，全部保存为 JPG 至 {output_dir}")

def main():
	parser = argparse.ArgumentParser(description="批量图片格式转换为JPG")
	parser.add_argument('--input_dir', required=True, help='输入图片文件夹路径')
	parser.add_argument('--output_dir', required=True, help='输出图片文件夹路径')
	args = parser.parse_args()
	convert_images(args.input_dir, args.output_dir)

if __name__ == '__main__':
	main()