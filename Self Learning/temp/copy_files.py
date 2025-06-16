import os
import shutil

def copy_pdf_files(src_dir, dst_dir):
    # Walk through the source directory and subdirectories
    for root, dirs, files in os.walk(src_dir):
        # Check if there are any PDF files
        for file in files:
            if file.endswith('.pdf'):
                # Build the full path of the source file
                src_file = os.path.join(root, file)
                
                # Build the corresponding destination directory
                relative_path = os.path.relpath(root, src_dir)
                dst_folder = os.path.join(dst_dir, relative_path)
                
                # Create the destination folder if it doesn't exist
                if not os.path.exists(dst_folder):
                    os.makedirs(dst_folder)
                
                # Build the full path for the destination file
                dst_file = os.path.join(dst_folder, file)
                
                # Copy the file
                shutil.copy(src_file, dst_file)
                print(f"Copied: {src_file} -> {dst_file}")

# Example usage:
src_directory = '/media/biswash/SSD_1/Python, DSA/Udemy_Python_Data_StructuresAlgorithms_LEETCODE_Exercises_2024/'
dst_directory = '/media/biswash/SSD_1/Python, DSA/new'

copy_pdf_files(src_directory, dst_directory)
