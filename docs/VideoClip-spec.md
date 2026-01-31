# Design Document for VideoSpeed

## Table of Contents

1. [Project Overview](#project-overview)
2. [Functional Requirements](#functional-requirements)
3. [Non-Functional Requirements](#non-functional-requirements)
4. [Architecture](#architecture)
   - [Modules](#modules)
5. [Data Flow](#data-flow)
6. [User Interface Design](#user-interface-design)
7. [Error Handling](#error-handling)
8. [Testing Strategy](#testing-strategy)
9. [Deployment](#deployment)

## 1. Project Overview

**VideoSpeed** is a command-line video editing tool developed in Python. It allows users to cut segments from MP4 videos, change the playback speed, and apply a boomerang effect using the FFmpeg and OpenCV libraries. The purpose of this project is to provide a simple yet powerful tool for basic video editing operations.

## 2. Functional Requirements

1. **Video Selection**:
   - The user can select a folder containing MP4 files.
   - The program lists all MP4 files in the folder.

2. **Cutting Video Segments**:
   - The user specifies a start and end time to define the segment to cut.

3. **Changing Speed**:
   - The user can specify a percentage to change the playback speed.

4. **Boomerang Effect**:
   - The user can choose to reverse the video segment after the original playback.

5. **Output**:
   - The edited video is saved in the same directory as the input video with an appropriate naming convention.

## 3. Non-Functional Requirements

1. **Performance**:
   - The tool must efficiently handle video processing to minimize wait times.

2. **Usability**:
   - The command-line interface should be user-friendly and provide clear prompts.

3. **Compatibility**:
   - The tool should work seamlessly with various MP4 files on multiple platforms (Windows, Linux, macOS).

## 4. Architecture

### Modules

- **cli.py**: Handles command-line interface and user interactions.
- **__init__.py**: Initializes the VideoSpeed module and defines the version.
- **__main__.py**: Entry point to the application, initiating the main processing flow.

### Interaction

- The user interacts with `cli.py` which manages inputs and outputs, invoking backend processing methods defined in the same file.

## 5. Data Flow

1. User specifies a folder.
2. The tool retrieves and lists MP4 files.
3. User selects a video file and specifies parameters (cut segment, speed, boomerang).
4. The tool processes the video using FFmpeg commands executed through subprocess calls.
5. The edited video is saved back to the directory.

## 6. User Interface Design

### Command-Line Interface

- Prompts will be clear and formatted for easy reading.
- Users will be guided through each step with specific instructions for input.

Example of CLI interaction:
```
Folder (Enter = current): 
1. video1.mp4
2. video2.mp4
Choose video (1-2): 
```

## 7. Error Handling

- If no MP4 files are found, the tool will display an error message and terminate.
- Invalid time ranges will prompt the user for re-entry.
- FFmpeg subprocess failures will be caught and reported to the user.

## 8. Testing Strategy

- Unit tests will be written for all core functionalities.
- Integration tests will verify the end-to-end workflow.
- Manual testing will ensure usability and responsiveness across different OS.

## 9. Deployment

- The project will be packaged using `setup.py` for easy installation.
- Instructions for installing FFmpeg must be provided in the documentation.

