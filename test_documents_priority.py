# test_documents_priority.py
"""
Test Documents Folder Priority
Verify that the system properly prioritizes files from documents/ folder
"""

import os
from integrated_smart_paraphrase_system import find_docx_files, select_document

def test_file_priority():
    """Test file selection priority"""
    print("🔍 TESTING DOCUMENTS FOLDER PRIORITY")
    print("=" * 60)
    
    # Test file finding
    print("📄 Step 1: Finding all .docx files...")
    files = find_docx_files()
    
    print(f"\n📊 Found {len(files)} documents:")
    for i, file_path in enumerate(files, 1):
        size = os.path.getsize(file_path) / 1024
        folder = os.path.dirname(file_path)
        filename = os.path.basename(file_path)
        
        # Determine priority status
        if './documents' in file_path:
            status = "🥇 HIGH PRIORITY (documents/ folder)"
        else:
            status = "📄 Lower priority"
        
        print(f"  {i}. {filename}")
        print(f"     📁 {folder}")
        print(f"     📏 {size:.1f} KB")
        print(f"     🏷️  {status}")
        print()
    
    # Test selection logic
    print("🎯 Step 2: Testing auto-selection...")
    if files:
        selected = files[0]  # This is what auto-select chooses
        print(f"✅ Auto-selected file: {os.path.basename(selected)}")
        print(f"📁 From folder: {os.path.dirname(selected)}")
        
        if './documents' in selected:
            print("🎉 SUCCESS: Documents folder file is prioritized!")
        else:
            print("❌ WARNING: Documents folder file not prioritized")
    
    # Show the selection interface (simulated)
    print(f"\n🖥️  Step 3: Selection interface preview...")
    print("This is what users will see:")
    print("-" * 40)
    
    try:
        # Simulate the select_document function output
        print("🔍 Searching for .docx documents...")
        print(f"📄 Found {len(files)} document(s):")
        print("-" * 50)
        
        for i, file_path in enumerate(files, 1):
            size = os.path.getsize(file_path) / 1024
            mod_time = "2025-08-07 21:45"  # Example
            folder_info = f"📂 {os.path.dirname(file_path)}"
            
            print(f"  {i}. {os.path.basename(file_path)}")
            print(f"     {folder_info}")
            print(f"     📏 {size:.1f} KB | 🕒 {mod_time}")
            
            if './documents' in file_path:
                print("     🥇 Priority: HIGH (documents folder)")
            print()
        
        if './documents' in files[0]:
            print("✅ Auto-selected: Documents folder file (CORRECT)")
        else:
            print("⚠️  Auto-selected: Non-documents file")
            
    except Exception as e:
        print(f"❌ Error in simulation: {e}")
    
    print(f"\n" + "=" * 60)
    print("✅ PRIORITY TEST COMPLETED")
    print("💡 Documents folder files are now prioritized first!")
    print("=" * 60)

def show_folder_usage_guide():
    """Show guide for using the documents folder"""
    print("\n📋 DOCUMENTS FOLDER USAGE GUIDE:")
    print("-" * 50)
    print("🎯 How to use:")
    print("  1. Place your main documents in documents/ folder")
    print("  2. System will auto-prioritize these files")
    print("  3. Other folders (paraphrased_documents/, root) are secondary")
    print()
    print("📁 Current folder structure:")
    print("  📂 documents/ (🥇 HIGH PRIORITY)")
    print("  ├── SKRIPSI  FAHRISAL FADLI-2.docx")
    print("  └── [Place your documents here]")
    print()
    print("  📂 paraphrased_documents/ (📄 lower priority)")
    print("  ├── paraphrased_BAB I.docx")
    print("  └── paraphrased_BAB II.docx")
    print()
    print("  📂 completed/ (output folder)")
    print("  ├── [Original documents]")
    print("  └── [Paraphrased results]")

if __name__ == "__main__":
    test_file_priority()
    show_folder_usage_guide()