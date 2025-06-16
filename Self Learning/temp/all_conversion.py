import subprocess
from pathlib import Path

def convert_ipynb_to_pdf(file_path):
    print(f"➡️ Converting notebook: {file_path.name}")
    try:
        subprocess.run([
            "jupyter", "nbconvert", "--to", "pdf",
            "--output", file_path.stem,
            "--output-dir", str(file_path.parent),
            str(file_path)
        ], check=True)
        print(f"✅ Done: {file_path.with_suffix('.pdf').name}")
    except subprocess.CalledProcessError:
        print(f"❌ Failed to convert notebook: {file_path.name}")

def convert_py_to_pdf(file_path):
    print(f"➡️ Converting script: {file_path.name}")
    try:
        output_pdf = file_path.with_suffix(".pdf")
        subprocess.run([
            "pygmentize", "-f", "pdf", "-O", "full,style=monokai",
            "-o", str(output_pdf),
            str(file_path)
        ], check=True)
        print(f"✅ Done: {output_pdf.name}")
    except subprocess.CalledProcessError:
        print(f"❌ Failed to convert script: {file_path.name}")

def convert_all_files_to_pdf(folder_path):
    folder = Path(folder_path)

    if not folder.exists() or not folder.is_dir():
        print("❌ Provided path is not a valid folder.")
        return

    all_files = list(folder.rglob("*"))

    ipynb_files = [f for f in all_files if f.suffix == ".ipynb"]
    py_files = [f for f in all_files if f.suffix == ".py"]

    if not ipynb_files and not py_files:
        print("ℹ️ No .ipynb or .py files found.")
        return

    for file in ipynb_files:
        convert_ipynb_to_pdf(file)

    for file in py_files:
        convert_py_to_pdf(file)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python convert_all.py <folder_path>")
    else:
        convert_all_files_to_pdf(sys.argv[1])
