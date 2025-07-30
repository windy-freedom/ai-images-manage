#!/usr/bin/env python3
"""
Demo script to intelligently classify and organize all images based on AI analysis
"""

import os
import shutil
import re
from pathlib import Path
from image_renamer import ImageRenamer

def get_smart_category(renamer, image_path):
    """Use AI to intelligently determine the best category for an image"""
    try:
        from PIL import Image
        image = Image.open(image_path)
        
        prompt = """Analyze this image and determine the most appropriate category folder name for organizing it.
        
        Look at the main subject/content and suggest a simple, descriptive category name (1-2 words, lowercase, use underscore for spaces).
        
        Examples of good category names:
        - cats, dogs, birds, animals
        - people, children, portraits
        - food, cooking, drinks
        - nature, landscapes, flowers
        - cars, vehicles, transportation
        - buildings, architecture
        - art, paintings, drawings
        - technology, computers, phones
        - sports, games, activities
        
        Respond with only the category name, no additional text or explanation.
        """
        
        response = renamer.model.generate_content([prompt, image])
        
        if response.text:
            category = response.text.strip().lower()
            # Clean up the category name
            category = re.sub(r'[^a-z0-9_]', '', category)
            category = re.sub(r'_+', '_', category)
            category = category.strip('_')
            
            if category and len(category) > 0:
                return category
            else:
                return 'misc'
        return 'misc'
        
    except Exception as e:
        print(f"Error getting smart category for {image_path}: {e}")
        return 'misc'

def classify_and_organize_all_images(rename_files=True):
    """Intelligently classify and organize all images based on AI analysis, with optional renaming"""
    print("=== Smart Image Classification and Organization ===\n")
    
    try:
        # Initialize the renamer (it will read API key from config.json)
        renamer = ImageRenamer()
        
        # Define the pics directory
        pics_dir = Path("pics")
        
        # Supported image extensions
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
        
        # Find all image files in pics directory (not in subdirectories)
        image_files = []
        for ext in image_extensions:
            image_files.extend(pics_dir.glob(f"*{ext}"))
            image_files.extend(pics_dir.glob(f"*{ext.upper()}"))
        
        if not image_files:
            print(f"No image files found in pics directory to classify")
            return
        
        print(f"Found {len(image_files)} image(s) to analyze and organize...")
        if rename_files:
            print("Mode: Rename + Smart Classification")
        else:
            print("Mode: Smart Classification Only")
        
        # Track categories and counts
        category_counts = {}
        created_folders = set()
        
        for image_file in image_files:
            print(f"\nAnalyzing: {image_file.name}")
            
            # Get smart category suggestion from AI
            category = get_smart_category(renamer, image_file)
            print(f"  → AI suggested category: {category}")
            
            # Get descriptive name if renaming is enabled
            new_name = None
            if rename_files:
                new_name = renamer.analyze_image(image_file)
                if new_name:
                    print(f"  → AI suggested name: {new_name}")
                else:
                    print(f"  → Could not generate new name, keeping original")
                    new_name = image_file.stem
            
            # Create category folder if it doesn't exist
            category_dir = pics_dir / category
            if category not in created_folders:
                category_dir.mkdir(exist_ok=True)
                created_folders.add(category)
                if category not in category_counts:
                    category_counts[category] = 0
            
            # Determine final filename
            if rename_files and new_name:
                final_filename = f"{new_name}{image_file.suffix}"
            else:
                final_filename = image_file.name
            
            # Move to category folder
            destination = category_dir / final_filename
            
            # Handle filename conflicts
            counter = 1
            original_destination = destination
            while destination.exists():
                if rename_files and new_name:
                    destination = category_dir / f"{new_name}_{counter}{image_file.suffix}"
                else:
                    stem = image_file.stem
                    suffix = image_file.suffix
                    destination = category_dir / f"{stem}_{counter}{suffix}"
                counter += 1
            
            try:
                shutil.move(str(image_file), str(destination))
                if rename_files and new_name and destination.name != image_file.name:
                    print(f"  → Renamed and moved to: {category}/{destination.name}")
                else:
                    print(f"  → Moved to: {category}/{destination.name}")
                category_counts[category] += 1
            except Exception as e:
                print(f"  ✗ Error moving file: {e}")
        
        print(f"\n=== Classification Summary ===")
        print(f"Total images processed: {len(image_files)}")
        print(f"Categories created: {len(created_folders)}")
        
        for category, count in sorted(category_counts.items()):
            print(f"  {category}: {count} images")
        
        # Show contents of each category folder
        print(f"\n=== Folder Contents ===")
        for category in sorted(created_folders):
            category_path = pics_dir / category
            files = [f for f in category_path.glob("*") if f.is_file() and f.suffix.lower() in image_extensions]
            if files:
                print(f"\n{category}/ ({len(files)} files):")
                for file in sorted(files):
                    print(f"  - {file.name}")
        
    except Exception as e:
        print(f"Error: {e}")

def identify_and_organize_animals():
    """Legacy function - now calls the smart classification function"""
    classify_and_organize_all_images()

def demo_classification():
    """Original demo function for backward compatibility"""
    print("=== Image Classification Demo ===\n")
    
    # Check if we have API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("Please set GEMINI_API_KEY environment variable to run this demo")
        print("You can get an API key from: https://makersuite.google.com/app/apikey")
        return
    
    try:
        # Initialize the renamer
        renamer = ImageRenamer()
        
        print("Available categories:")
        for category, keywords in renamer.categories.items():
            print(f"  {category}: {', '.join(keywords[:5])}...")
        
        print("\n=== Dry Run - Classification Mode ===")
        renamer.process_directory("pics", mode="classify", dry_run=True)
        
        print("\n=== Dry Run - Both Mode (Rename + Classify) ===")
        renamer.process_directory("pics", mode="both", dry_run=True)
        
    except Exception as e:
        print(f"Error: {e}")

def main():
    """Main function with mode selection"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Smart Image Classification and Organization with AI")
    parser.add_argument("--mode", choices=["classify", "rename-classify", "classify-only"], 
                       default="rename-classify",
                       help="Processing mode: classify (legacy), rename-classify (rename + smart classify), classify-only (smart classify without renaming)")
    parser.add_argument("--directory", default="pics", help="Directory containing images (default: pics)")
    
    args = parser.parse_args()
    
    if args.mode == "classify":
        # Legacy mode using original classification
        identify_and_organize_animals()
    elif args.mode == "rename-classify":
        # New mode: rename + smart classification
        classify_and_organize_all_images(rename_files=True)
    elif args.mode == "classify-only":
        # New mode: smart classification without renaming
        classify_and_organize_all_images(rename_files=False)

if __name__ == "__main__":
    main()
