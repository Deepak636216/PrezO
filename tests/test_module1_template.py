"""
Test Module 1: Template Management System
Tests template analysis and function generation
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.template_analyzer import analyze_ppt_template, generate_template_functions


def test_template_analysis():
    """Test analyzing the presentation template"""
    template_path = "presentation-template.pptx"

    if not os.path.exists(template_path):
        print(f"[FAIL] Template file not found: {template_path}")
        return False

    print("=" * 70)
    print("MODULE 1 TEST: Template Analysis & Function Generation")
    print("=" * 70)

    # Test 1: Analyze template
    print("\n[Test 1] Analyzing template...")
    try:
        metadata = analyze_ppt_template(template_path)
        print(f"[PASS] Template analyzed successfully")
        print(f"   Template ID: {metadata['template_id']}")
        print(f"   Template Name: {metadata['template_name']}")
        print(f"   Slide Dimensions: {metadata['slide_width_inches']}\" x {metadata['slide_height_inches']}\"")
        print(f"   Layouts Found: {len(metadata['layouts'])}")

        print(f"\n   Layout Details:")
        for layout in metadata['layouts']:
            print(f"     - Layout {layout['layout_index']}: {layout['layout_name']}")
            print(f"       Placeholders: {len(layout['slots'])}")
            for slot_name, slot_info in layout['slots'].items():
                print(f"         * {slot_name} ({slot_info['placeholder_type']})")

    except Exception as e:
        print(f"[FAIL] Template analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Test 2: Generate functions
    print("\n[Test 2] Generating template functions...")
    try:
        func_path = generate_template_functions(metadata, output_dir="templates")
        print(f"[PASS] Functions generated successfully")
        print(f"   Functions file: {func_path}")

        # Check if file exists and has content
        if os.path.exists(func_path):
            with open(func_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                print(f"   Lines of code: {len(lines)}")
        else:
            print(f"[FAIL] Functions file not created")
            return False

    except Exception as e:
        print(f"[FAIL] Function generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Test 3: Verify metadata JSON was saved
    print("\n[Test 3] Verifying metadata JSON...")
    metadata_path = os.path.join("templates", f"{metadata['template_id']}_metadata.json")
    if os.path.exists(metadata_path):
        print(f"[PASS] Metadata JSON saved: {metadata_path}")
    else:
        print(f"[FAIL] Metadata JSON not found")
        return False

    print("\n" + "=" * 70)
    print("[PASS] MODULE 1 TEST: ALL TESTS PASSED")
    print("=" * 70)

    return True


if __name__ == "__main__":
    success = test_template_analysis()
    sys.exit(0 if success else 1)
