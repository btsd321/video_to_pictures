import cv2
import os
import argparse

def extract_frames(video_path, output_dir, interval):
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)
	cap = cv2.VideoCapture(video_path)
	if not cap.isOpened():
		print(f"无法打开视频文件: {video_path}")
		return
	frame_count = 0
	saved_count = 0
	while True:
		ret, frame = cap.read()
		if not ret:
			break
		if frame_count % interval == 0:
			img_name = os.path.join(output_dir, f"frame_{frame_count:06d}.jpg")
			cv2.imwrite(img_name, frame)
			saved_count += 1
		frame_count += 1
	cap.release()
	print(f"总帧数: {frame_count}, 已保存: {saved_count} 张图片到 {output_dir}")

def main():
	parser = argparse.ArgumentParser(description="视频抽帧保存图片")
	parser.add_argument('--video_path', type=str, required=True, help='输入视频路径')
	parser.add_argument('--output_dir', type=str, required=True, help='输出图片文件夹路径')
	parser.add_argument('--interval', type=int, default=10, help='抽帧间隔（每隔多少帧保存一张）')
	args = parser.parse_args()
	extract_frames(args.video_path, args.output_dir, args.interval)

if __name__ == "__main__":
	main()