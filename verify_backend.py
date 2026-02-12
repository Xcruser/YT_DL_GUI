from downloader import Downloader
import os

def test_backend():
    print("Testing Backend...")
    dl = Downloader(output_path="test_downloads")
    
    # Test Video URL (User Provided)
    url = "https://www.youtube.com/watch?v=I0eLjOIO9LQ" 
    
    print(f"1. Testing Video Download from {url}...")
    success, msg = dl.download_video(url)
    if success:
        print("   [PASS] Video Download: Success")
    else:
        print(f"   [FAIL] Video Download: {msg}")

    print(f"2. Testing Audio Extraction from {url}...")
    success, msg = dl.download_audio(url, format='mp3')
    if success:
        print("   [PASS] Audio Download: Success")
    else:
        print(f"   [FAIL] Audio Download: {msg}")

    # Check files
    files = os.listdir("test_downloads")
    print(f"Files in test_downloads: {files}")
    
    if len(files) >= 2:
        print("VERIFICATION SUCCESSFUL: Files created.")
    else:
        print("VERIFICATION FAILED: Missing files.")

if __name__ == "__main__":
    test_backend()
