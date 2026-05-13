import re
import yaml

def scout_documentation(feature_name, file_inventory, git_client):
    """
    Core logic for Skill 2: Scout.
    """
    feature_name = feature_name.lower()
    
    # STEP 1: Filename Pass
    for path in file_inventory:
        if feature_name in path.lower():
            return {
                "status": "match_found",
                "path": path,
                "reason": "Filename match",
                "message": f"A documentation page already exists at '{path}'. Consider updating it to reflect your new change rather than creating a new page."
            }

    # STEP 2: Metadata Existence Check
    metadata_exists_anywhere = False
    potential_matches = []

    for path in file_inventory:
        # Optimization: Only fetch the 'head' of the file
        raw_content = git_client.get_file_content(path, lines=10)
        
        # Check for YAML frontmatter (starts and ends with ---)
        if raw_content.startswith("---"):
            metadata_exists_anywhere = True
            
            # Parse the metadata block
            try:
                # Extract text between the first two sets of ---
                parts = raw_content.split('---')
                if len(parts) >= 3:
                    metadata = yaml.safe_load(parts[1])
                    
                    # STEP 3: Match against your specific metadata keys
                    # (e.g., title, tags, description)
                    if any(feature_name in str(val).lower() for val in metadata.values()):
                        return {"status": "match_found", "path": path, "reason": "Metadata match"}
            except yaml.YAMLError:
                continue

    # STEP 4: The "Stop" Gate
    if not metadata_exists_anywhere:
        return {
            "status": "metadata_missing_stop",
            "message": "STOP: No metadata found in documentation pages. Add metadata to enable scouting."
        }

    # STEP 5: New Page Recommendation
    return {
        "status": "new_page_required",
        "message": f"No existing match for '{feature_name}'. A new documentation page should be created."
    }