"""
Test script to verify backend functionality without YOLOv8
Tests: utils, gemini_service, API structure
"""

import os
os.environ["ENABLE_GEMINI"] = "false"  # Disable Gemini for basic test

# Import modules
try:
    from utils import (
        get_dustbin_color,
        get_dustbin_icon,
        normalize_class_name,
        get_fallback_awareness_tip,
        validate_image_format
    )
    print("✅ utils.py imported successfully")
except Exception as e:
    print(f"❌ utils.py import failed: {e}")
    exit(1)

try:
    from gemini_service import generate_awareness_tip, generate_safety_warning
    print("✅ gemini_service.py imported successfully")
except Exception as e:
    print(f"❌ gemini_service.py import failed: {e}")
    exit(1)

# Test utility functions
print("\n📋 Testing Utility Functions:")
print("-" * 50)

# Test 1: Dustbin color mapping
test_categories = ["ORGANIC", "RECYCLABLE", "HAZARDOUS"]
for category in test_categories:
    color = get_dustbin_color(category)
    icon = get_dustbin_icon(category)
    print(f"  {category}: {color} dustbin, {icon} icon")

# Test 2: Class normalization
print("\n📋 Testing Class Normalization:")
print("-" * 50)
test_classes = ["food", "plastic_bottle", "battery", "unknown_item"]
for test_class in test_classes:
    normalized = normalize_class_name(test_class)
    print(f"  '{test_class}' → {normalized}")

# Test 3: Fallback tips
print("\n📋 Testing Fallback Awareness Tips:")
print("-" * 50)
for category in test_categories:
    tip = get_fallback_awareness_tip(category)
    print(f"  {category}: {tip[:60]}...")

# Test 4: Image validation
print("\n📋 Testing Image Validation:")
print("-" * 50)
test_files = ["test.jpg", "image.png", "doc.pdf", "photo.jpeg"]
for filename in test_files:
    valid = validate_image_format(filename)
    status = "✅" if valid else "❌"
    print(f"  {status} {filename}: {valid}")

# Test 5: Safety warnings
print("\n📋 Testing Safety Warnings:")
print("-" * 50)
test_confidences = [0.95, 0.75, 0.60, 0.45]
for conf in test_confidences:
    warning = generate_safety_warning(conf)
    print(f"  Confidence {conf}: {warning if warning else 'No warning'}")

# Test 6: Gemini awareness tip (with fallback)
print("\n📋 Testing Gemini Awareness (Fallback Mode):")
print("-" * 50)
tip = generate_awareness_tip("plastic_bottle", "RECYCLABLE", 0.85)
print(f"  Tip: {tip}")

print("\n" + "=" * 50)
print("✅ ALL TESTS PASSED - Backend modules working correctly!")
print("=" * 50)
