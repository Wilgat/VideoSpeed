# VideoSpeed

A command-line video editing tool built in Python for cutting, speeding up, and applying a boomerang effect to MP4 videos. This project leverages FFmpeg for video processing and OpenCV to handle video file properties.

## Features

- **Cut segments** from MP4 videos.
- Change the **speed** of video clips.
- Apply a **boomerang effect** by reversing video segments.
- Simple command-line interface for user interaction.

## Installation

To install the VideoSpeed package, use the provided distributions:

1. Download the wheel or tar.gz file from the `dist` directory:
   - `VideoSpeed-1.0.0-py3-none-any.whl`
   - `VideoSpeed-1.0.0.tar.gz`

2. Install via pip:
   ```bash
   pip install dist/VideoSpeed-1.0.0-py3-none-any.whl
   ```

   Or
   ```bash
   pip install dist/VideoSpeed-1.0.0.tar.gz
   ```

## Usage

You can run the tool directly from the command line:

```bash
python -m VideoSpeed
```

### Steps:
1. Select the folder containing your MP4 files (default is the current directory).
2. Choose the video file from the listed options.
3. Specify the start and end time for the cut.
4. Enter the desired speed percentage for the clip.
5. Optionally, choose to add a boomerang effect.
6. The processed video will be saved in the same directory as the source file.

## Folder Structure

```
VideoSpeed
├── build/                # Contains build artifacts
├── dist/                 # Distributions for installation
├── docs/                 # Documentation files
│   ├── CHANGELOG.md      # Changes in each version
│   ├── folder-structure.md# Describes folder structure
│   └── LoggedExample-spec.md # Specifications for examples
├── src/                  # Source code directory
│   ├── VideoSpeed/        # Main package
│   ├── setup.py          # Installation script
└── README.md             # Project documentation
```

## Requirements

- Python 3.6 or higher
- FFmpeg installed on your system
- OpenCV library (`opencv-python`)

You can install OpenCV using pip:

```bash
pip install opencv-python
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- **FFmpeg**: A powerful multimedia framework for handling video files.
- **OpenCV**: A library for computer vision tasks.
