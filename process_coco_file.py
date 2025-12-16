import json
import re  # Imported for future extensions (e.g. regex-based name cleaning)


def format_category_name(name):
    """
    Cleans a COCO category name.

    - Removes the 'Labels - ' prefix if it exists
    - Capitalizes the first letter of each remaining word

    Example:
        'Labels - corner break' -> 'Corner Break'
    """
    if name.startswith("Labels - "):
        # Remove prefix only once (safety in case of repeated text)
        name = name.replace("Labels - ", "", 1)

        # Capitalize each word for consistency
        name = " ".join(word.capitalize() for word in name.split())

    return name


def update_coco_file(input_path, output_path):
    """
    Updates a COCO JSON file by:
    1. Renaming 'taqadam_filename' to 'file_name' everywhere
    2. Cleaning category names in the 'categories' section

    Args:
        input_path (str): Path to the original COCO JSON file
        output_path (str): Path where the updated file will be saved
    """

    # Load the original COCO file
    with open(input_path, "r", encoding="utf-8") as f:
        coco = json.load(f)

    # --- Step 1: Rename 'taqadam_filename' to 'file_name' globally ---
    # We convert the dict to a string to ensure replacement
    # in all nested locations, then convert back to JSON.
    coco_str = json.dumps(coco)
    coco_str = coco_str.replace("taqadam_filename", "file_name")
    coco = json.loads(coco_str)

    # --- Step 2: Clean category names ---
    if "categories" in coco:
        for category in coco["categories"]:
            if "name" in category:
                category["name"] = format_category_name(category["name"])

    # Save the updated COCO file with indentation for readability
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(coco, f, indent=4)

    print(f"Updated COCO file saved to: {output_path}")


# ------------------------------------------------------------------
# Script entry point
# Allows this file to be imported without executing the update
# ------------------------------------------------------------------
if __name__ == "__main__":
    update_coco_file(
        input_path="/Users/oreyeon/Desktop/NRV1104.coco.json",
        output_path="/Users/oreyeon/Desktop/NRV1104.json"
    )
