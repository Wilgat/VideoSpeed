#!/usr/bin/env python
from __future__ import print_function, unicode_literals
import cv2
import sys
from ChronicleLogger import ChronicleLogger
import subprocess
from pathlib import Path
import tempfile
import os

def run_ffmpeg(cmd):
    print(f"   Running → {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

def get_mp4_files(folder="."):
    folder = Path(folder)
    files = list(folder.rglob("*.mp4")) + list(folder.rglob("*.MP4"))
    files = [f for f in files if f.is_file()]
    files.sort(key=lambda x: x.name.lower())
    return files

def get_duration_cv2(video_path):
    cap = cv2.VideoCapture(str(video_path))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    return frame_count / fps if fps > 0 else 0

def format_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}"[3:] if h == 0 else f"{h:02d}:{m:02d}:{s:06.3f}"

def cut_clip(src, start, end, output_path):
    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(src),
        "-vf", f"trim=start={start}:end={end},setpts=PTS-STARTPTS",
        "-af", f"atrim=start={start}:end={end},asetpts=PTS-STARTPTS",
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "17",
        "-c:a", "aac", "-avoid_negative_ts", "make_zero",
        str(output_path)
    ]
    print(" ".join(cmd))

    run_ffmpeg(cmd)

def speed_change(input_path, ratio_percent, output_path):
    speed = 100.0 / ratio_percent
    cmd = [
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(input_path),
        "-filter_complex",
        f"[0:v]setpts={1/speed:.6f}*PTS[v];[0:a]atempo={speed:.6f}[a]",
        "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart",
        str(output_path)
    ]
    print(" ".join(cmd))
    run_ffmpeg(cmd)

def add_boomerang(forward_clip, final_output):
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
        reverse_clip = Path(tmp.name)
    
    run_ffmpeg([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-i", str(forward_clip), "-vf", "reverse", "-af", "areverse", str(reverse_clip)
    ])
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write(f"file '{forward_clip}'\nfile '{reverse_clip}'\n")
        concat_list = Path(f.name)
    run_ffmpeg([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
        "-f", "concat", "-safe", "0", "-i", str(concat_list),
        "-c", "copy", str(final_output)
    ])
    os.unlink(reverse_clip)
    os.unlink(concat_list)

def main():
    print("ULTIMATE Video Editor: Cut → Speed → Optional Boomerang")
    print("=" * 62)

    folder = input("Folder (Enter = current): ").strip() or "."
    files = get_mp4_files(folder)
    if not files:
        print("No MP4 files found!"); return
    for i, f in enumerate(files, 1):
        print(f"{i:2d}. {f.name}")
    video_path = files[int(input(f"\nChoose video (1-{len(files)}): ")) - 1]

    duration = get_duration_cv2(video_path)
    print(f"\nSelected: {video_path.name}")
    print(f"Duration: {format_time(duration)} ({duration:.3f}s)\n")

    while True:
        print("Step 1/4 – Cut segment")
        start_str = input("   Start seconds (default 0.0): ").strip()
        start = 0.0 if start_str == "" else float(start_str)
        print(f"   → Using start: {start:.3f}s")

        end_str = input(f"   End seconds [{duration:.3f}]: ").strip()
        end = duration if end_str == "" else float(end_str)

        if not (0 <= start < end <= duration):
            print("Invalid range!\n"); continue

        print("\nStep 2/4 – Resize length (20–200%)")
        ratio_str = input("   New length % [100%]: ").strip() or "100"
        ratio = float(ratio_str.replace("%", ""))

        print("\nStep 3/4 – Add boomerang effect?")
        boomerang = input("   Make it go forward + backward (y/n) [n]: ").strip().lower() == 'y'

        name = f"{video_path.stem}_cut{start:.1f}-{end:.1f}s_{int(ratio)}pct"
        if boomerang: name += "_BOOMERANG"
        name += ".mp4"
        final_out = video_path.parent / name

        print(f"\nProcessing → {final_out}\n")

        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as t1, \
             tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as t2:
            cut_temp = Path(t1.name)
            speed_temp = Path(t2.name)

        try:
            print("1. Cutting segment...")
            cut_clip(video_path, start, end, cut_temp)
            print(f"2. Changing length to {ratio}%...")
            speed_change(cut_temp, ratio, speed_temp)
            if boomerang:
                print("3. Creating boomerang...")
                add_boomerang(speed_temp, final_out)
            else:
                os.replace(speed_temp, final_out)
            print(f"\nSUCCESS → {final_out}\n")
        finally:
            for p in (cut_temp, speed_temp):
                if p.exists(): os.unlink(p)

        if input("Again? (y/n): ").lower() != 'y': break

    print("Done.")

if __name__ == "__main__":
    main()