import cv2

def change_video_fps(input_path, output_path, new_fps):
    # Open the input video
    cap = cv2.VideoCapture(input_path)
    
    # Get the original video properties
    original_fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Create the VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use 'mp4v' for MP4 format
    out = cv2.VideoWriter(output_path, fourcc, new_fps, (width, height))
    
    print(f'Original FPS: {original_fps}, New FPS: {new_fps}')
    
    # Read and write frames
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)
    
    # Release the VideoCapture and VideoWriter objects
    cap.release()
    out.release()
    print(f'Video saved to {output_path}')

# Example usage
input_path = 'C:/Users/lenovo/Desktop/my_proj/my.mp4'
output_path = 'C:/Users/lenovo/Desktop/my_proj/my_adjusted_fps.mp4'
new_fps = 60  # Desired FPS

change_video_fps(input_path, output_path, new_fps)
