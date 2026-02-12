from downloader import Downloader
import os
import shutil

def test_custom_path():
    print("Testing Custom Path...")
    dl = Downloader()
    
    custom_dir = "custom_downloads_test"
    if os.path.exists(custom_dir):
        shutil.rmtree(custom_dir)
    os.makedirs(custom_dir)
    
    # Test Video URL
    url = "https://www.youtube.com/watch?v=jNQXAC9IVRw" 
    
    print(f"1. Testing Video Download to '{custom_dir}'...")
    success, msg = dl.download_video(url, output_path=custom_dir)
    
    if success:
        files = os.listdir(custom_dir)
        if len(files) > 0:
            print(f"   [PASS] Video Download: Success. Found {files}")
        else:
            print("   [FAIL] Video Download: File not found in custom dir.")
    else:
        print(f"   [FAIL] Video Download: {msg}")

    # Cleanup
    # shutil.rmtree(custom_dir) 

if __name__ == "__main__":
    test_custom_path()
