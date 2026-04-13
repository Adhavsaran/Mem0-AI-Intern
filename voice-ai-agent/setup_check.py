#!/usr/bin/env python3
"""
Verification script to check if all dependencies are installed and LM Studio is running.
LM Studio Edition - Uses local LLM instead of OpenAI API
"""
import sys
import os


def print_header(text):
    """Print styled header."""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def check_python_version():
    """Check Python version >= 3.8"""
    print_header("1. Checking Python Version")
    version_info = sys.version_info
    version_str = f"{version_info.major}.{version_info.minor}.{version_info.micro}"
    print(f"✓ Python {version_str} detected")
    
    if version_info.major < 3 or (version_info.major == 3 and version_info.minor < 8):
        print("✗ Python 3.8+ required!")
        return False
    return True


def check_lm_studio():
    """Check if LM Studio is running."""
    print_header("2. Checking LM Studio Connection")
    
    try:
        from config import check_lm_studio, LM_STUDIO_BASE_URL
        
        if check_lm_studio():
            print(f"✓ LM Studio is running")
            print(f"  Endpoint: {LM_STUDIO_BASE_URL}")
            return True
        else:
            print(f"✗ LM Studio is NOT running!")
            print(f"  Expected at: {LM_STUDIO_BASE_URL}")
            print("\n  To fix:")
            print("    1. Download LM Studio from: https://lmstudio.ai")
            print("    2. Open LM Studio and load a model")
            print("    3. Go to Settings → Developer")
            print("    4. Start Local Server")
            return False
    except Exception as e:
        print(f"✗ Error checking LM Studio: {e}")
        return False


def check_python_packages():
    """Check if required Python packages are installed."""
    print_header("3. Checking Python Packages")
    
    required_packages = [
        "gradio",
        "transformers",
        "torch",
        "torchaudio",
        "numpy",
        "soundfile",
        "openai",
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} NOT installed")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing: {', '.join(missing)}")
        print(f"\n  Install with: pip install -r requirements.txt")
        return False
    
    return True


def check_project_structure():
    """Check if project structure is correct."""
    print_header("4. Checking Project Structure")
    
    required_dirs = ["app", "core", "tools", "utils", "output"]
    required_files = [
        "config.py",
        "requirements.txt",
        "app/main.py",
        "app/ui.py",
        "core/stt.py",
        "core/intent.py",
        "core/orchestrator.py",
        "tools/file_tool.py",
        "tools/code_tool.py",
        "tools/summary_tool.py",
        "tools/chat_tool.py",
        "utils/parser.py",
        "utils/logger.py",
    ]
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    all_ok = True
    for dir_name in required_dirs:
        dir_path = os.path.join(base_dir, dir_name)
        if os.path.isdir(dir_path):
            print(f"✓ {dir_name}/")
        else:
            print(f"✗ {dir_name}/ NOT FOUND")
            all_ok = False
    
    for file_name in required_files:
        full_path = os.path.join(base_dir, file_name)
        if os.path.isfile(full_path):
            print(f"✓ {file_name}")
        else:
            print(f"✗ {file_name} NOT FOUND")
            all_ok = False
    
    return all_ok


def main():
    """Run all checks."""
    print_header("🎤 Voice AI Agent - Setup Verification (LM Studio Edition)")
    
    checks = [
        ("Python Version", check_python_version),
        ("LM Studio Connection", check_lm_studio),
        ("Python Packages", check_python_packages),
        ("Project Structure", check_project_structure),
    ]
    
    results = {}
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"\n✗ Error during {name} check: {e}")
            results[name] = False
    
    # Summary
    print_header("Setup Summary")
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nResult: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n✨ All checks passed! Ready to launch!")
        print("\nRun the app with:")
        print("  python app/main.py")
        print("\nThen open your browser to: http://127.0.0.1:7860")
        return 0
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("  1. Install LM Studio: https://lmstudio.ai")
        print("  2. Load a model in LM Studio")
        print("  3. Start local server (Settings → Developer)")
        print("  4. Install packages: pip install -r requirements.txt")
        return 1


if __name__ == "__main__":
    sys.exit(main())
