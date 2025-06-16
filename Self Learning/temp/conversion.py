import subprocess
import sys
from pathlib import Path
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.fonts import addMapping
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import tempfile

def check_dependencies():
    """Check if required dependencies are available"""
    dependencies = {
        'jupyter': 'jupyter nbconvert',
        'pygmentize': 'pygmentize',
        'reportlab': 'python -c "import reportlab"'
    }
    
    available = {}
    for dep, cmd in dependencies.items():
        try:
            subprocess.run(cmd.split(), check=True, capture_output=True)
            available[dep] = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            available[dep] = False
    
    return available

def convert_ipynb_to_pdf(file_path):
    """Convert Jupyter notebook to PDF"""
    print(f"➡️ Converting notebook: {file_path.name}")
    try:
        subprocess.run([
            "jupyter", "nbconvert", "--to", "pdf",
            "--output", file_path.stem,
            "--output-dir", str(file_path.parent),
            str(file_path)
        ], check=True, capture_output=True)
        print(f"✅ Done: {file_path.with_suffix('.pdf').name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to convert notebook: {file_path.name}")
        print(f"   Error: {e.stderr.decode() if e.stderr else 'Unknown error'}")
        return False

def convert_py_to_pdf_pygments(file_path):
    """Convert Python file to PDF using Pygments"""
    print(f"➡️ Converting script with Pygments: {file_path.name}")
    try:
        output_pdf = file_path.with_suffix(".pdf")
        subprocess.run([
            "pygmentize", "-f", "pdf", "-O", "full,style=monokai",
            "-o", str(output_pdf),
            str(file_path)
        ], check=True, capture_output=True)
        print(f"✅ Done: {output_pdf.name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Pygments failed for: {file_path.name}")
        print(f"   Error: {e.stderr.decode() if e.stderr else 'Unknown error'}")
        return False

def convert_py_to_pdf_reportlab(file_path):
    """Convert Python file to PDF using ReportLab"""
    print(f"➡️ Converting script with ReportLab: {file_path.name}")
    try:
        # Read the Python file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create PDF
        output_pdf = file_path.with_suffix(".pdf")
        doc = SimpleDocTemplate(str(output_pdf), pagesize=A4)
        
        # Get styles
        styles = getSampleStyleSheet()
        code_style = ParagraphStyle(
            'Code',
            parent=styles['Normal'],
            fontName='Courier',
            fontSize=8,
            leading=10,
            leftIndent=20,
            rightIndent=20,
            spaceAfter=6,
        )
        
        # Build PDF content
        story = []
        
        # Add title
        title_style = styles['Title']
        story.append(Paragraph(f"Python Script: {file_path.name}", title_style))
        story.append(Spacer(1, 20))
        
        # Add code content
        # Split content into manageable chunks to avoid ReportLab limitations
        lines = content.split('\n')
        chunk_size = 50  # lines per chunk
        
        for i in range(0, len(lines), chunk_size):
            chunk = '\n'.join(lines[i:i+chunk_size])
            # Escape HTML characters
            chunk = chunk.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            story.append(Preformatted(chunk, code_style))
            if i + chunk_size < len(lines):
                story.append(Spacer(1, 12))
        
        # Build PDF
        doc.build(story)
        print(f"✅ Done: {output_pdf.name}")
        return True
        
    except Exception as e:
        print(f"❌ ReportLab failed for: {file_path.name}")
        print(f"   Error: {str(e)}")
        return False

def convert_py_to_pdf_html_method(file_path):
    """Convert Python file to PDF via HTML (fallback method)"""
    print(f"➡️ Converting script via HTML method: {file_path.name}")
    try:
        # Read the Python file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create HTML with syntax highlighting
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>{file_path.name}</title>
            <style>
                body {{ 
                    font-family: 'Courier New', monospace; 
                    font-size: 10px; 
                    line-height: 1.4;
                    margin: 20px;
                }}
                pre {{ 
                    white-space: pre-wrap; 
                    word-wrap: break-word;
                    background-color: #f5f5f5;
                    padding: 10px;
                    border: 1px solid #ddd;
                }}
                .header {{
                    font-size: 14px;
                    font-weight: bold;
                    margin-bottom: 20px;
                    border-bottom: 2px solid #333;
                    padding-bottom: 10px;
                }}
            </style>
        </head>
        <body>
            <div class="header">Python Script: {file_path.name}</div>
            <pre>{content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')}</pre>
        </body>
        </html>
        """
        
        # Write temporary HTML file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as temp_html:
            temp_html.write(html_content)
            temp_html_path = temp_html.name
        
        # Convert HTML to PDF using wkhtmltopdf if available
        output_pdf = file_path.with_suffix(".pdf")
        try:
            subprocess.run([
                "wkhtmltopdf", "--page-size", "A4", "--margin-top", "0.75in",
                "--margin-right", "0.75in", "--margin-bottom", "0.75in",
                "--margin-left", "0.75in", temp_html_path, str(output_pdf)
            ], check=True, capture_output=True)
            print(f"✅ Done: {output_pdf.name}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Try with weasyprint as fallback
            try:
                subprocess.run([
                    "weasyprint", temp_html_path, str(output_pdf)
                ], check=True, capture_output=True)
                print(f"✅ Done: {output_pdf.name}")
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                return False
        finally:
            # Clean up temp file
            Path(temp_html_path).unlink(missing_ok=True)
            
    except Exception as e:
        print(f"❌ HTML method failed for: {file_path.name}")
        print(f"   Error: {str(e)}")
        return False

def convert_py_to_pdf(file_path, available_deps):
    """Convert Python file to PDF using the best available method"""
    methods = []
    
    # Try Pygments first if available
    if available_deps.get('pygmentize', False):
        methods.append(convert_py_to_pdf_pygments)
    
    # Try ReportLab if available
    if available_deps.get('reportlab', False):
        methods.append(convert_py_to_pdf_reportlab)
    
    # Try HTML method as fallback
    methods.append(convert_py_to_pdf_html_method)
    
    # Try each method until one succeeds
    for method in methods:
        if method(file_path):
            return True
    
    print(f"❌ All methods failed for: {file_path.name}")
    return False

def convert_all_files_to_pdf(folder_path):
    """Convert all .ipynb and .py files in folder to PDF"""
    folder = Path(folder_path)
    if not folder.exists() or not folder.is_dir():
        print("❌ Provided path is not a valid folder.")
        return
    
    # Check available dependencies
    print("🔍 Checking available dependencies...")
    available_deps = check_dependencies()
    for dep, available in available_deps.items():
        status = "✅" if available else "❌"
        print(f"   {status} {dep}")
    print()
    
    # Find all files
    all_files = list(folder.rglob("*"))
    ipynb_files = [f for f in all_files if f.suffix == ".ipynb"]
    py_files = [f for f in all_files if f.suffix == ".py"]
    
    if not ipynb_files and not py_files:
        print("ℹ️ No .ipynb or .py files found.")
        return
    
    print(f"📋 Found {len(ipynb_files)} notebook(s) and {len(py_files)} Python file(s)")
    print()
    
    # Convert notebooks
    if ipynb_files and available_deps.get('jupyter', False):
        print("📓 Converting Jupyter notebooks...")
        for file in ipynb_files:
            convert_ipynb_to_pdf(file)
        print()
    elif ipynb_files:
        print("⚠️ Jupyter notebooks found but jupyter not available. Skipping notebooks.")
        print()
    
    # Convert Python files
    if py_files:
        print("🐍 Converting Python files...")
        for file in py_files:
            convert_py_to_pdf(file, available_deps)
    
    print("\n🎉 Conversion process completed!")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python all_conversion.py <folder_path>")
        print("\nThis script converts .ipynb and .py files to PDF format.")
        print("Required dependencies:")
        print("  - jupyter (for notebook conversion)")
        print("  - pygmentize + reportlab (for Python file conversion)")
        print("  - wkhtmltopdf or weasyprint (optional, for HTML fallback)")
    else:
        convert_all_files_to_pdf(sys.argv[1])
