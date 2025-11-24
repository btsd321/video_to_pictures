import os
import argparse
import cv2

VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.mpeg', '.mpg'}

def list_videos(folder):
	"""返回文件夹下所有视频文件的完整路径，按文件名排序。"""
	videos = []
	for root, _, files in os.walk(folder):
		for name in files:
			if os.path.splitext(name)[1].lower() in VIDEO_EXTENSIONS:
				videos.append(os.path.join(root, name))
	videos.sort(key=lambda x: os.path.relpath(x, folder))
	return videos

def extract_frames_from_video(video_path, output_dir, interval):
	base_name = os.path.splitext(os.path.basename(video_path))[0]
	cap = cv2.VideoCapture(video_path)
	if not cap.isOpened():
		print(f"无法打开视频文件: {video_path}")
		return 0
	frame_count = 0
	saved_count = 0
	while True:
		ret, frame = cap.read()
		if not ret:
			break
		if frame_count % interval == 0:
			img_name = f"{base_name}_{frame_count:06d}.jpg"
			img_path = os.path.join(output_dir, img_name)
			if not cv2.imwrite(img_path, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 95]):
				print(f"警告: 保存图片失败 {img_path}")
			else:
				saved_count += 1
		frame_count += 1
	cap.release()
	print(f"视频 {os.path.basename(video_path)}: 总帧数 {frame_count}, 已保存 {saved_count} 张图片")
	return saved_count

def main():
	parser = argparse.ArgumentParser(description="批量视频抽帧保存图片")
	parser.add_argument('--input_dir', required=True, help='输入视频文件夹路径')
	parser.add_argument('--output_dir', required=True, help='输出图片文件夹路径')
	parser.add_argument('--interval', type=int, required=True, help='抽帧间隔（每隔多少帧保存一张）')
	args = parser.parse_args()

	os.makedirs(args.output_dir, exist_ok=True)
	videos = list_videos(args.input_dir)
	if not videos:
		print(f"未在 {args.input_dir} 找到视频文件。")
		return
	total_saved = 0
	for video in videos:
		total_saved += extract_frames_from_video(video, args.output_dir, args.interval)
	print(f"共处理 {len(videos)} 个视频，保存图片总数: {total_saved}")

if __name__ == '__main__':
	main()