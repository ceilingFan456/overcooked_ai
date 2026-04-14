"""
Generate sprite assets for new ingredients (cucumber, rice) to extend overcooked_ai.
Run once to create/update the sprite sheet PNGs and JSON atlas files.

Usage: python generate_new_sprites.py
"""

import json
import os
from PIL import Image, ImageDraw

GRAPHICS_DIR = os.path.join(
    os.path.dirname(__file__),
    "src", "overcooked_ai_py", "data", "graphics"
)

TILE = 15  # Unscaled tile size
PAD = 1    # Padding between frames in sprite sheets (matches existing)

# Colors for new ingredients
CUCUMBER_COLOR = (34, 139, 34)       # Forest green
CUCUMBER_DARK = (0, 100, 0)          # Dark green (outline)
CUCUMBER_LIGHT = (144, 238, 144)     # Light green (highlight)
RICE_COLOR = (255, 248, 220)         # Cornsilk / beige
RICE_DARK = (210, 180, 140)          # Tan (outline)
RICE_LIGHT = (255, 255, 240)         # Ivory (highlight)

# Existing colors from sprite sheets
COUNTER_BG = (155, 101, 0)           # Brown counter background
POT_GRAY = (128, 128, 128)          # Pot color
TRANSPARENT = (0, 0, 0, 0)


def draw_cucumber_dispenser(draw, x, y):
    """Draw a cucumber dispenser tile (counter with cucumbers on top)."""
    # Counter base (brown)
    draw.rectangle([x, y, x+14, y+14], fill=(155, 101, 0, 255))
    # Counter top edge
    draw.rectangle([x, y, x+14, y+2], fill=(180, 120, 20, 255))
    # Cucumber items (green elongated shapes)
    draw.ellipse([x+2, y+4, x+7, y+8], fill=CUCUMBER_COLOR + (255,), outline=CUCUMBER_DARK + (255,))
    draw.ellipse([x+6, y+7, x+12, y+11], fill=CUCUMBER_COLOR + (255,), outline=CUCUMBER_DARK + (255,))
    draw.ellipse([x+3, y+10, x+10, y+13], fill=CUCUMBER_COLOR + (255,), outline=CUCUMBER_DARK + (255,))


def draw_rice_dispenser(draw, x, y):
    """Draw a rice dispenser tile (counter with rice on top)."""
    # Counter base (brown)
    draw.rectangle([x, y, x+14, y+14], fill=(155, 101, 0, 255))
    # Counter top edge
    draw.rectangle([x, y, x+14, y+2], fill=(180, 120, 20, 255))
    # Rice bowl/pile (beige oval shapes)
    draw.ellipse([x+3, y+5, x+11, y+12], fill=RICE_COLOR + (255,), outline=RICE_DARK + (255,))
    # Rice grains on top
    draw.rectangle([x+5, y+4, x+7, y+6], fill=RICE_LIGHT + (255,))
    draw.rectangle([x+8, y+5, x+10, y+7], fill=RICE_LIGHT + (255,))


def draw_cucumber_object(draw, x, y):
    """Draw a cucumber object (held item)."""
    # Cucumber shape - elongated green oval
    draw.ellipse([x+2, y+3, x+12, y+11], fill=CUCUMBER_COLOR + (255,), outline=CUCUMBER_DARK + (255,))
    # Highlight
    draw.line([x+4, y+5, x+9, y+5], fill=CUCUMBER_LIGHT + (255,))


def draw_rice_object(draw, x, y):
    """Draw a rice object (held item) - a small bowl of rice."""
    # Bowl
    draw.arc([x+2, y+5, x+12, y+13], 0, 180, fill=RICE_DARK + (255,))
    draw.ellipse([x+3, y+4, x+11, y+10], fill=RICE_COLOR + (255,), outline=RICE_DARK + (255,))
    # Rice grains
    draw.point((x+5, y+5), fill=RICE_DARK + (255,))
    draw.point((x+7, y+6), fill=RICE_DARK + (255,))
    draw.point((x+9, y+5), fill=RICE_DARK + (255,))


def draw_ingredient_in_pot(draw, x, y, ingredient, count, is_top=True):
    """Draw small ingredient indicators in a pot area."""
    positions = [(x+3, y+2), (x+7, y+2), (x+5, y+5)][:count]
    for px, py in positions:
        if ingredient == "cucumber":
            draw.ellipse([px, py, px+3, py+2], fill=CUCUMBER_COLOR + (255,))
        elif ingredient == "rice":
            draw.ellipse([px, py, px+2, py+2], fill=RICE_COLOR + (255,), outline=RICE_DARK + (255,))


def update_terrain_sprites():
    """Add cucumber and rice dispenser tiles to terrain.png & terrain.json."""
    print("Updating terrain sprites...")
    
    terrain_img = Image.open(os.path.join(GRAPHICS_DIR, "terrain.png"))
    with open(os.path.join(GRAPHICS_DIR, "terrain.json")) as f:
        terrain_json = json.load(f)
    
    old_w, old_h = terrain_img.size
    
    # Check if already added
    if "cucumbers.png" in terrain_json["frames"]:
        print("  Already has cucumber terrain sprite, skipping.")
        return
    
    # Add 2 new tiles (cucumber, rice) to the right
    new_w = old_w + (TILE + PAD + 1) * 2
    new_img = Image.new("RGBA", (new_w, old_h), TRANSPARENT)
    new_img.paste(terrain_img, (0, 0))
    
    draw = ImageDraw.Draw(new_img)
    
    # Cucumber dispenser at next position
    cx = old_w + 1
    draw_cucumber_dispenser(draw, cx, 1)
    terrain_json["frames"]["cucumbers.png"] = {
        "frame": {"x": cx, "y": 1, "w": TILE, "h": TILE},
        "rotated": False,
        "trimmed": False,
        "spriteSourceSize": {"x": 0, "y": 0, "w": TILE, "h": TILE},
        "sourceSize": {"w": TILE, "h": TILE}
    }
    
    # Rice dispenser
    rx = cx + TILE + PAD + 1
    draw_rice_dispenser(draw, rx, 1)
    terrain_json["frames"]["rice.png"] = {
        "frame": {"x": rx, "y": 1, "w": TILE, "h": TILE},
        "rotated": False,
        "trimmed": False,
        "spriteSourceSize": {"x": 0, "y": 0, "w": TILE, "h": TILE},
        "sourceSize": {"w": TILE, "h": TILE}
    }
    
    # Update size in meta if it exists
    if "meta" in terrain_json:
        terrain_json["meta"]["size"] = {"w": new_w, "h": old_h}
    
    new_img.save(os.path.join(GRAPHICS_DIR, "terrain.png"))
    with open(os.path.join(GRAPHICS_DIR, "terrain.json"), "w") as f:
        json.dump(terrain_json, f, indent=4)
    
    print(f"  Added cucumber and rice terrain tiles. New size: {new_w}x{old_h}")


def update_object_sprites():
    """Add cucumber and rice object sprites to objects.png & objects.json."""
    print("Updating object sprites...")
    
    objects_img = Image.open(os.path.join(GRAPHICS_DIR, "objects.png"))
    with open(os.path.join(GRAPHICS_DIR, "objects.json")) as f:
        objects_json = json.load(f)
    
    if "cucumber.png" in objects_json["frames"]:
        print("  Already has cucumber object sprite, skipping.")
        return
    
    old_w, old_h = objects_img.size
    new_w = old_w + (TILE + PAD + 1) * 2
    new_img = Image.new("RGBA", (new_w, old_h), TRANSPARENT)
    new_img.paste(objects_img, (0, 0))
    
    draw = ImageDraw.Draw(new_img)
    
    # Cucumber object
    cx = old_w + 1
    draw_cucumber_object(draw, cx, 1)
    objects_json["frames"]["cucumber.png"] = {
        "frame": {"x": cx, "y": 1, "w": TILE, "h": TILE},
        "rotated": False,
        "trimmed": False,
        "spriteSourceSize": {"x": 0, "y": 0, "w": TILE, "h": TILE},
        "sourceSize": {"w": TILE, "h": TILE}
    }
    
    # Rice object
    rx = cx + TILE + PAD + 1
    draw_rice_object(draw, rx, 1)
    objects_json["frames"]["rice.png"] = {
        "frame": {"x": rx, "y": 1, "w": TILE, "h": TILE},
        "rotated": False,
        "trimmed": False,
        "spriteSourceSize": {"x": 0, "y": 0, "w": TILE, "h": TILE},
        "sourceSize": {"w": TILE, "h": TILE}
    }
    
    if "meta" in objects_json:
        objects_json["meta"]["size"] = {"w": new_w, "h": old_h}
    
    new_img.save(os.path.join(GRAPHICS_DIR, "objects.png"))
    with open(os.path.join(GRAPHICS_DIR, "objects.json"), "w") as f:
        json.dump(objects_json, f, indent=4)
    
    print(f"  Added cucumber and rice object sprites. New size: {new_w}x{old_h}")


def update_soup_sprites():
    """Add soup sprites for all combinations involving cucumber and rice."""
    print("Updating soup sprites...")
    
    with open(os.path.join(GRAPHICS_DIR, "soups.json")) as f:
        soups_json = json.load(f)
    
    soups_img = Image.open(os.path.join(GRAPHICS_DIR, "soups.png"))
    
    existing_frames = {f["filename"] for f in soups_json["textures"][0]["frames"]}
    
    # Check if already updated
    if any("cucumber" in name for name in existing_frames):
        print("  Already has cucumber soup sprites, skipping.")
        return
    
    # We need soup sprites for ALL combinations with 4 ingredients and max 3 total
    # Format: soup_{status}_tomato_{N}_onion_{M}_cucumber_{K}_rice_{J}.png
    # where N+M+K+J >= 1 and N+M+K+J <= 3
    
    # But to avoid a massive rewrite of the naming system, we'll keep the old sprites
    # for onion/tomato-only combos, and generate new sprites for combos involving cucumber/rice.
    # We use the EXTENDED naming: soup_{status}_tomato_{N}_onion_{M}_cucumber_{K}_rice_{J}
    
    ingredients = ["tomato", "onion", "cucumber", "rice"]
    statuses = ["idle", "cooked", "done"]
    max_total = 3
    
    # Collect all NEW frames needed
    new_frames_needed = []
    for status in statuses:
        for t in range(max_total + 1):
            for o in range(max_total + 1 - t):
                for c in range(max_total + 1 - t - o):
                    for r in range(max_total + 1 - t - o - c):
                        total = t + o + c + r
                        if total < 1 or total > max_total:
                            continue
                        
                        # Check if this combo involves only onion/tomato (already exists)
                        if c == 0 and r == 0:
                            continue  # Old naming handles these
                        
                        name = f"soup_{status}_tomato_{t}_onion_{o}_cucumber_{c}_rice_{r}.png"
                        if name not in existing_frames:
                            new_frames_needed.append((name, status, t, o, c, r))
    
    if not new_frames_needed:
        print("  All soup sprites already exist.")
        return
    
    # Load reference soup sprite to use as base (get the pot/bowl shape)
    # We'll use soup_idle_tomato_0_onion_1 as reference for pot shape
    ref_frame = None
    for f in soups_json["textures"][0]["frames"]:
        if f["filename"] == "soup_idle_tomato_0_onion_1.png":
            ref_frame = f["frame"]
            break
    
    old_w, old_h = soups_img.size
    
    # We'll add new frames in rows
    frames_per_row = 9  # Match existing layout
    num_new = len(new_frames_needed)
    new_rows = (num_new + frames_per_row - 1) // frames_per_row
    
    new_h = old_h + new_rows * (TILE + 2)
    new_w = max(old_w, frames_per_row * (TILE + 2))
    
    new_img = Image.new("RGBA", (new_w, new_h), TRANSPARENT)
    new_img.paste(soups_img, (0, 0))
    draw = ImageDraw.Draw(new_img)
    
    # Color map for ingredients in soups
    SOUP_COLORS = {
        "onion": (255, 255, 0),      # Yellow
        "tomato": (255, 0, 0),        # Red
        "cucumber": (34, 139, 34),    # Green
        "rice": (255, 248, 220),      # Beige
    }
    
    STATUS_POT_COLOR = {
        "idle": (128, 128, 128, 255),     # Gray pot
        "cooked": (128, 128, 128, 255),   # Gray pot with steam
        "done": (200, 200, 200, 255),     # Light (held in dish)
    }
    
    for idx, (name, status, t, o, c, r, ) in enumerate(new_frames_needed):
        row = idx // frames_per_row
        col = idx % frames_per_row
        fx = col * (TILE + 2) + 1
        fy = old_h + row * (TILE + 2) + 1
        
        pot_color = STATUS_POT_COLOR[status]
        
        if status == "done":
            # Soup in a dish (being carried) - draw dish-like shape
            draw.ellipse([fx+1, fy+3, fx+13, fy+13], fill=(200, 200, 200, 255), outline=(100, 100, 100, 255))
        else:
            # Pot shape
            draw.rectangle([fx+1, fy+5, fx+13, fy+13], fill=pot_color)
            draw.rectangle([fx+0, fy+4, fx+14, fy+6], fill=pot_color)
        
        # Draw ingredient dots/circles inside
        ingredient_list = []
        ingredient_list.extend(["tomato"] * t)
        ingredient_list.extend(["onion"] * o)
        ingredient_list.extend(["cucumber"] * c)
        ingredient_list.extend(["rice"] * r)
        
        total = len(ingredient_list)
        # Position dots
        if total == 1:
            positions = [(fx+5, fy+7)]
        elif total == 2:
            positions = [(fx+3, fy+7), (fx+8, fy+7)]
        else:
            positions = [(fx+3, fy+7), (fx+8, fy+7), (fx+5, fy+10)]
        
        for i, ing in enumerate(ingredient_list[:3]):
            px, py = positions[i]
            color = SOUP_COLORS[ing] + (255,)
            draw.ellipse([px, py, px+4, py+3], fill=color)
        
        # Add steam effect for cooked
        if status == "cooked":
            draw.line([fx+4, fy+1, fx+4, fy+3], fill=(200, 200, 200, 180))
            draw.line([fx+7, fy+0, fx+7, fy+2], fill=(200, 200, 200, 180))
            draw.line([fx+10, fy+1, fx+10, fy+3], fill=(200, 200, 200, 180))
        
        # Add to JSON
        soups_json["textures"][0]["frames"].append({
            "filename": name,
            "frame": {"x": fx, "y": fy, "w": TILE, "h": TILE},
            "rotated": False,
            "trimmed": False,
            "spriteSourceSize": {"x": 0, "y": 0, "w": TILE, "h": TILE},
            "sourceSize": {"w": TILE, "h": TILE}
        })
    
    # Update texture size
    soups_json["textures"][0]["size"] = {"w": new_w, "h": new_h}
    
    new_img.save(os.path.join(GRAPHICS_DIR, "soups.png"))
    with open(os.path.join(GRAPHICS_DIR, "soups.json"), "w") as f:
        json.dump(soups_json, f, indent=2)
    
    print(f"  Added {len(new_frames_needed)} new soup sprites. New size: {new_w}x{new_h}")


def update_chef_sprites():
    """Add chef sprites holding cucumber and rice (and soup variants)."""
    print("Updating chef sprites...")
    
    chefs_img = Image.open(os.path.join(GRAPHICS_DIR, "chefs.png"))
    with open(os.path.join(GRAPHICS_DIR, "chefs.json")) as f:
        chefs_json = json.load(f)
    
    if "NORTH-cucumber.png" in chefs_json["frames"]:
        print("  Already has cucumber chef sprites, skipping.")
        return
    
    directions = ["NORTH", "SOUTH", "EAST", "WEST"]
    new_items = ["cucumber", "rice", "soup-cucumber", "soup-rice"]
    
    # For each new held item, we'll copy the base chef sprite and overlay the item
    # Get base sprite positions for each direction
    base_frames = {}
    for d in directions:
        key = f"{d}.png"
        if key in chefs_json["frames"]:
            base_frames[d] = chefs_json["frames"][key]["frame"]
    
    # Also get onion-holding frames as reference for positioning
    onion_frames = {}
    for d in directions:
        key = f"{d}-onion.png"
        if key in chefs_json["frames"]:
            onion_frames[d] = chefs_json["frames"][key]["frame"]
    
    old_w, old_h = chefs_img.size
    
    # Count new frames needed
    needed = []
    for d in directions:
        for item in new_items:
            key = f"{d}-{item}.png"
            if key not in chefs_json["frames"]:
                needed.append((d, item, key))
    
    if not needed:
        print("  All chef sprites already exist.")
        return
    
    # Add new frames to the right of existing image
    frames_per_col = len(needed)
    new_w = old_w + (TILE + 2) * ((len(needed) + 3) // 4)
    new_h = max(old_h, 4 * (TILE + 2) + 2)
    
    new_img = Image.new("RGBA", (new_w, new_h), TRANSPARENT)
    new_img.paste(chefs_img, (0, 0))
    
    for idx, (direction, item, key) in enumerate(needed):
        col = idx // 4
        row = idx % 4
        fx = old_w + col * (TILE + 2) + 1
        fy = row * (TILE + 2) + 1
        
        # Copy base chef sprite
        bf = base_frames[direction]
        base_region = chefs_img.crop((bf["x"], bf["y"], bf["x"] + bf["w"], bf["y"] + bf["h"]))
        new_img.paste(base_region, (fx, fy))
        
        draw = ImageDraw.Draw(new_img)
        
        # Determine item position based on direction
        if direction == "SOUTH":
            ix, iy = fx + 5, fy + 10
        elif direction == "NORTH":
            ix, iy = fx + 5, fy + 1
        elif direction == "EAST":
            ix, iy = fx + 10, fy + 6
        elif direction == "WEST":
            ix, iy = fx + 1, fy + 6
        
        # Draw the held item
        if item == "cucumber":
            draw.ellipse([ix, iy, ix+4, iy+3], fill=CUCUMBER_COLOR + (255,), outline=CUCUMBER_DARK + (255,))
        elif item == "rice":
            draw.ellipse([ix, iy, ix+4, iy+3], fill=RICE_COLOR + (255,), outline=RICE_DARK + (255,))
        elif item == "soup-cucumber":
            draw.ellipse([ix-1, iy, ix+5, iy+4], fill=(128, 128, 128, 255))
            draw.ellipse([ix, iy+1, ix+3, iy+3], fill=CUCUMBER_COLOR + (255,))
        elif item == "soup-rice":
            draw.ellipse([ix-1, iy, ix+5, iy+4], fill=(128, 128, 128, 255))
            draw.ellipse([ix, iy+1, ix+3, iy+3], fill=RICE_COLOR + (255,))
        
        # Add frame to JSON
        chefs_json["frames"][key] = {
            "frame": {"x": fx, "y": fy, "w": TILE, "h": TILE},
            "rotated": False,
            "trimmed": False,
            "spriteSourceSize": {"x": 0, "y": 0, "w": TILE, "h": TILE},
            "sourceSize": {"w": TILE, "h": TILE}
        }
    
    if "meta" in chefs_json:
        chefs_json["meta"]["size"] = {"w": new_w, "h": new_h}
    
    new_img.save(os.path.join(GRAPHICS_DIR, "chefs.png"))
    with open(os.path.join(GRAPHICS_DIR, "chefs.json"), "w") as f:
        json.dump(chefs_json, f, indent=4)
    
    print(f"  Added {len(needed)} new chef sprites. New size: {new_w}x{new_h}")


if __name__ == "__main__":
    print("Generating new ingredient sprites for overcooked_ai...")
    print(f"Graphics dir: {GRAPHICS_DIR}")
    print()
    
    update_terrain_sprites()
    update_object_sprites()
    update_soup_sprites()
    update_chef_sprites()
    
    print()
    print("Done! All sprite assets have been updated.")
