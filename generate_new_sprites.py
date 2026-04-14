"""
Generate sprite assets for new ingredients to extend overcooked_ai.
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

# Colors for existing custom ingredients
CUCUMBER_COLOR = (34, 139, 34)       # Forest green
CUCUMBER_DARK = (0, 100, 0)          # Dark green (outline)
CUCUMBER_LIGHT = (144, 238, 144)     # Light green (highlight)
RICE_COLOR = (255, 248, 220)         # Cornsilk / beige
RICE_DARK = (210, 180, 140)          # Tan (outline)
RICE_LIGHT = (255, 255, 240)         # Ivory (highlight)

# Colors for NEW ingredients
OLIVE_COLOR = (75, 0, 110)           # Deep eggplant purple
OLIVE_DARK = (48, 0, 72)             # Darker purple
OLIVE_LIGHT = (120, 40, 140)         # Lighter purple highlight

FETA_COLOR = (255, 215, 0)           # Gold/yellow
FETA_DARK = (200, 165, 32)           # Dark goldenrod
FETA_LIGHT = (255, 255, 150)         # Light yellow highlight

BUN_COLOR = (160, 82, 45)            # Sienna/brown
BUN_DARK = (120, 60, 25)             # Saddle brown
BUN_LIGHT = (210, 150, 100)          # Light brown highlight

SOY_SAUCE_CAP = (220, 20, 20)       # Red cap
SOY_SAUCE_BODY = (30, 30, 30)       # Near-black body
SOY_SAUCE_LABEL = (240, 240, 240)   # White label

FROZEN_PEAS_GREEN = (50, 180, 50)   # Green
FROZEN_ICE = (140, 200, 240)        # Light blue ice

FROZEN_CARROTS_ORANGE = (240, 130, 20)  # Orange

FRIDGE_COLOR = (210, 215, 225)      # Light gray body
FRIDGE_DARK = (140, 145, 160)       # Darker gray border
FRIDGE_HANDLE = (90, 95, 110)       # Handle color

# Existing colors from sprite sheets
COUNTER_BG = (155, 101, 0)           # Brown counter background
POT_GRAY = (128, 128, 128)          # Pot color
TRANSPARENT = (0, 0, 0, 0)

# Map ingredient name to drawing color (for chef sprite overlay)
INGREDIENT_COLORS = {
    "cucumber": CUCUMBER_COLOR,
    "rice": RICE_COLOR,
    "olive": OLIVE_COLOR,
    "feta_cheese": FETA_COLOR,
    "hamburger_bun": BUN_COLOR,
    "soy_sauce": SOY_SAUCE_BODY,
    "frozen_peas": FROZEN_PEAS_GREEN,
    "frozen_carrots": FROZEN_CARROTS_ORANGE,
}


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


# ---------- NEW INGREDIENT DRAWING FUNCTIONS ----------

def draw_counter_base(draw, x, y):
    """Draw the standard counter base for dispensers."""
    draw.rectangle([x, y, x+14, y+14], fill=(155, 101, 0, 255))
    draw.rectangle([x, y, x+14, y+2], fill=(180, 120, 20, 255))


def draw_olive_dispenser(draw, x, y):
    """Draw olive dispenser tile (counter with dark purple olives on top)."""
    draw_counter_base(draw, x, y)
    draw.ellipse([x+2, y+4, x+6, y+8], fill=OLIVE_COLOR+(255,), outline=OLIVE_DARK+(255,))
    draw.ellipse([x+7, y+6, x+11, y+10], fill=OLIVE_COLOR+(255,), outline=OLIVE_DARK+(255,))
    draw.ellipse([x+4, y+9, x+9, y+13], fill=OLIVE_COLOR+(255,), outline=OLIVE_DARK+(255,))


def draw_feta_dispenser(draw, x, y):
    """Draw feta cheese dispenser tile (counter with yellow cheese block)."""
    draw_counter_base(draw, x, y)
    draw.rectangle([x+3, y+5, x+11, y+12], fill=FETA_COLOR+(255,), outline=FETA_DARK+(255,))
    draw.rectangle([x+4, y+4, x+10, y+6], fill=FETA_LIGHT+(255,))


def draw_bun_dispenser(draw, x, y):
    """Draw hamburger bun dispenser tile (counter with brown buns)."""
    draw_counter_base(draw, x, y)
    draw.ellipse([x+2, y+4, x+12, y+9], fill=BUN_COLOR+(255,), outline=BUN_DARK+(255,))
    draw.rectangle([x+3, y+8, x+11, y+13], fill=BUN_COLOR+(255,), outline=BUN_DARK+(255,))
    draw.point((x+5, y+5), fill=BUN_LIGHT+(255,))
    draw.point((x+8, y+5), fill=BUN_LIGHT+(255,))


def draw_soy_sauce_dispenser(draw, x, y):
    """Draw soy sauce dispenser tile (counter with bottle)."""
    draw_counter_base(draw, x, y)
    draw.rectangle([x+5, y+3, x+9, y+5], fill=SOY_SAUCE_CAP+(255,))
    draw.rectangle([x+4, y+5, x+10, y+12], fill=SOY_SAUCE_BODY+(255,))
    draw.rectangle([x+5, y+7, x+9, y+10], fill=SOY_SAUCE_LABEL+(255,))


def draw_fridge_peas_dispenser(draw, x, y):
    """Draw fridge dispenser for frozen peas (fridge with green indicator)."""
    draw.rectangle([x+1, y+0, x+13, y+14], fill=FRIDGE_COLOR+(255,), outline=FRIDGE_DARK+(255,))
    draw.line([x+1, y+6, x+13, y+6], fill=FRIDGE_DARK+(255,))
    draw.rectangle([x+10, y+2, x+11, y+5], fill=FRIDGE_HANDLE+(255,))
    draw.rectangle([x+10, y+8, x+11, y+12], fill=FRIDGE_HANDLE+(255,))
    # Green dots inside lower compartment
    draw.ellipse([x+3, y+8, x+5, y+10], fill=FROZEN_PEAS_GREEN+(255,))
    draw.ellipse([x+6, y+9, x+8, y+11], fill=FROZEN_PEAS_GREEN+(255,))
    # Ice sparkles
    draw.point((x+4, y+12), fill=FROZEN_ICE+(255,))
    draw.point((x+7, y+12), fill=FROZEN_ICE+(255,))


def draw_fridge_carrots_dispenser(draw, x, y):
    """Draw fridge dispenser for frozen carrots (fridge with orange indicator)."""
    draw.rectangle([x+1, y+0, x+13, y+14], fill=FRIDGE_COLOR+(255,), outline=FRIDGE_DARK+(255,))
    draw.line([x+1, y+6, x+13, y+6], fill=FRIDGE_DARK+(255,))
    draw.rectangle([x+10, y+2, x+11, y+5], fill=FRIDGE_HANDLE+(255,))
    draw.rectangle([x+10, y+8, x+11, y+12], fill=FRIDGE_HANDLE+(255,))
    # Orange rods inside lower compartment
    draw.line([x+3, y+9, x+6, y+9], fill=FROZEN_CARROTS_ORANGE+(255,), width=1)
    draw.line([x+4, y+11, x+7, y+11], fill=FROZEN_CARROTS_ORANGE+(255,), width=1)
    # Ice sparkles
    draw.point((x+4, y+12), fill=FROZEN_ICE+(255,))
    draw.point((x+7, y+12), fill=FROZEN_ICE+(255,))


def draw_olive_object(draw, x, y):
    """Draw an olive object (held/on counter) - dark purple oval."""
    draw.ellipse([x+3, y+3, x+11, y+11], fill=OLIVE_COLOR+(255,), outline=OLIVE_DARK+(255,))
    draw.ellipse([x+5, y+5, x+8, y+8], fill=OLIVE_LIGHT+(255,))


def draw_feta_object(draw, x, y):
    """Draw a feta cheese object - yellow block."""
    draw.rectangle([x+3, y+4, x+11, y+11], fill=FETA_COLOR+(255,), outline=FETA_DARK+(255,))
    draw.line([x+4, y+6, x+10, y+6], fill=FETA_LIGHT+(255,))


def draw_bun_object(draw, x, y):
    """Draw a hamburger bun object - brown dome."""
    draw.ellipse([x+2, y+3, x+12, y+9], fill=BUN_COLOR+(255,), outline=BUN_DARK+(255,))
    draw.rectangle([x+3, y+7, x+11, y+12], fill=BUN_COLOR+(255,), outline=BUN_DARK+(255,))
    draw.point((x+5, y+5), fill=BUN_LIGHT+(255,))
    draw.point((x+8, y+5), fill=BUN_LIGHT+(255,))


def draw_soy_sauce_object(draw, x, y):
    """Draw a soy sauce bottle object - red cap, black body."""
    draw.rectangle([x+5, y+2, x+9, y+4], fill=SOY_SAUCE_CAP+(255,))
    draw.rectangle([x+4, y+4, x+10, y+12], fill=SOY_SAUCE_BODY+(255,))
    draw.rectangle([x+5, y+6, x+9, y+9], fill=SOY_SAUCE_LABEL+(255,))


def draw_frozen_peas_object(draw, x, y):
    """Draw frozen peas object - green dots with blue ice sprinkles."""
    for px, py in [(x+4, y+4), (x+8, y+4), (x+6, y+6), (x+4, y+8), (x+8, y+8), (x+6, y+10)]:
        draw.ellipse([px, py, px+2, py+2], fill=FROZEN_PEAS_GREEN+(255,))
    for px, py in [(x+3, y+3), (x+10, y+5), (x+5, y+11), (x+9, y+9)]:
        draw.point((px, py), fill=FROZEN_ICE+(255,))


def draw_frozen_carrots_object(draw, x, y):
    """Draw frozen carrots object - orange rods with blue ice sprinkles."""
    draw.line([x+3, y+4, x+8, y+4], fill=FROZEN_CARROTS_ORANGE+(255,), width=2)
    draw.line([x+5, y+7, x+11, y+7], fill=FROZEN_CARROTS_ORANGE+(255,), width=2)
    draw.line([x+3, y+10, x+9, y+10], fill=FROZEN_CARROTS_ORANGE+(255,), width=2)
    for px, py in [(x+3, y+3), (x+10, y+5), (x+4, y+12), (x+9, y+9)]:
        draw.point((px, py), fill=FROZEN_ICE+(255,))


# Map from item name to its object drawing function
OBJECT_DRAW_FUNCS = {
    "olive": draw_olive_object,
    "feta_cheese": draw_feta_object,
    "hamburger_bun": draw_bun_object,
    "soy_sauce": draw_soy_sauce_object,
    "frozen_peas": draw_frozen_peas_object,
    "frozen_carrots": draw_frozen_carrots_object,
}

# Map from terrain frame name to its dispenser drawing function
TERRAIN_DRAW_FUNCS = {
    "olives": draw_olive_dispenser,
    "feta_cheese": draw_feta_dispenser,
    "hamburger_buns": draw_bun_dispenser,
    "soy_sauce": draw_soy_sauce_dispenser,
    "fridge_peas": draw_fridge_peas_dispenser,
    "fridge_carrots": draw_fridge_carrots_dispenser,
}


def update_terrain_sprites():
    """Add new dispenser tiles to terrain.png & terrain.json."""
    print("Updating terrain sprites...")
    
    terrain_img = Image.open(os.path.join(GRAPHICS_DIR, "terrain.png"))
    with open(os.path.join(GRAPHICS_DIR, "terrain.json")) as f:
        terrain_json = json.load(f)
    
    old_w, old_h = terrain_img.size
    
    # Check if cucumber already added (from original script run)
    has_cucumber = "cucumbers.png" in terrain_json["frames"]
    
    # Collect all terrain frames to add
    to_add = []
    if not has_cucumber:
        to_add.append(("cucumbers.png", draw_cucumber_dispenser))
        to_add.append(("rice.png", draw_rice_dispenser))
    
    for frame_name, draw_func in TERRAIN_DRAW_FUNCS.items():
        png_name = frame_name + ".png"
        if png_name not in terrain_json["frames"]:
            to_add.append((png_name, draw_func))
    
    if not to_add:
        print("  All terrain sprites already exist.")
        return
    
    new_w = old_w + (TILE + PAD + 1) * len(to_add)
    new_img = Image.new("RGBA", (new_w, old_h), TRANSPARENT)
    new_img.paste(terrain_img, (0, 0))
    draw = ImageDraw.Draw(new_img)
    
    for i, (png_name, draw_func) in enumerate(to_add):
        tx = old_w + i * (TILE + PAD + 1) + 1
        draw_func(draw, tx, 1)
        terrain_json["frames"][png_name] = {
            "frame": {"x": tx, "y": 1, "w": TILE, "h": TILE},
            "rotated": False,
            "trimmed": False,
            "spriteSourceSize": {"x": 0, "y": 0, "w": TILE, "h": TILE},
            "sourceSize": {"w": TILE, "h": TILE}
        }
    
    if "meta" in terrain_json:
        terrain_json["meta"]["size"] = {"w": new_w, "h": old_h}
    
    new_img.save(os.path.join(GRAPHICS_DIR, "terrain.png"))
    with open(os.path.join(GRAPHICS_DIR, "terrain.json"), "w") as f:
        json.dump(terrain_json, f, indent=4)
    
    print(f"  Added {len(to_add)} terrain tiles. New size: {new_w}x{old_h}")


def update_object_sprites():
    """Add new object sprites to objects.png & objects.json."""
    print("Updating object sprites...")
    
    objects_img = Image.open(os.path.join(GRAPHICS_DIR, "objects.png"))
    with open(os.path.join(GRAPHICS_DIR, "objects.json")) as f:
        objects_json = json.load(f)
    
    has_cucumber = "cucumber.png" in objects_json["frames"]
    
    to_add = []
    if not has_cucumber:
        to_add.append(("cucumber.png", draw_cucumber_object))
        to_add.append(("rice.png", draw_rice_object))
    
    for item_name, draw_func in OBJECT_DRAW_FUNCS.items():
        png_name = item_name + ".png"
        if png_name not in objects_json["frames"]:
            to_add.append((png_name, draw_func))
    
    if not to_add:
        print("  All object sprites already exist.")
        return
    
    old_w, old_h = objects_img.size
    new_w = old_w + (TILE + PAD + 1) * len(to_add)
    new_img = Image.new("RGBA", (new_w, old_h), TRANSPARENT)
    new_img.paste(objects_img, (0, 0))
    draw = ImageDraw.Draw(new_img)
    
    for i, (png_name, draw_func) in enumerate(to_add):
        ox = old_w + i * (TILE + PAD + 1) + 1
        draw_func(draw, ox, 1)
        objects_json["frames"][png_name] = {
            "frame": {"x": ox, "y": 1, "w": TILE, "h": TILE},
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
    
    print(f"  Added {len(to_add)} object sprites. New size: {new_w}x{old_h}")


def update_soup_sprites():
    """Add soup sprites for all ingredient combinations.
    
    Since we now have many ingredients, we generate sprites for all combinations
    with the 4 original ingredients (onion, tomato, cucumber, rice) plus combos
    involving new ingredients up to max 3.
    """
    print("Updating soup sprites...")
    
    with open(os.path.join(GRAPHICS_DIR, "soups.json")) as f:
        soups_json = json.load(f)
    
    soups_img = Image.open(os.path.join(GRAPHICS_DIR, "soups.png"))
    
    existing_frames = {f["filename"] for f in soups_json["textures"][0]["frames"]}
    
    # All ingredients that might appear in soups
    all_ingredients = ["tomato", "onion", "cucumber", "rice",
                       "olive", "feta_cheese", "hamburger_bun",
                       "soy_sauce", "frozen_peas", "frozen_carrots"]
    statuses = ["idle", "cooked", "done"]
    max_total = 3
    
    # Color map for ingredients in soup sprites
    SOUP_COLORS = {
        "onion": (255, 255, 0),
        "tomato": (255, 0, 0),
        "cucumber": (34, 139, 34),
        "rice": (255, 248, 220),
        "olive": OLIVE_COLOR,
        "feta_cheese": FETA_COLOR,
        "hamburger_bun": BUN_COLOR,
        "soy_sauce": SOY_SAUCE_BODY,
        "frozen_peas": FROZEN_PEAS_GREEN,
        "frozen_carrots": FROZEN_CARROTS_ORANGE,
    }
    
    STATUS_POT_COLOR = {
        "idle": (128, 128, 128, 255),
        "cooked": (128, 128, 128, 255),
        "done": (200, 200, 200, 255),
    }
    
    # Generate all combinations with up to max_total ingredients
    from itertools import combinations_with_replacement
    new_frames_needed = []
    for status in statuses:
        for total in range(1, max_total + 1):
            for combo in combinations_with_replacement(all_ingredients, total):
                # Build the frame name with counts for each ingredient
                from collections import Counter
                counts = Counter(combo)
                # Build name: soup_{status}_tomato_{N}_onion_{M}_cucumber_{K}_rice_{J}
                # For backward compat, only-tomato-onion combos use old naming
                has_new = any(counts.get(ing, 0) > 0 for ing in all_ingredients[2:])
                if not has_new:
                    # Old format for backward compat
                    name = f"soup_{status}_tomato_{counts.get('tomato', 0)}_onion_{counts.get('onion', 0)}.png"
                else:
                    parts = [f"soup_{status}"]
                    for ing in all_ingredients:
                        parts.append(f"{ing}_{counts.get(ing, 0)}")
                    name = "_".join(parts) + ".png"
                
                if name not in existing_frames:
                    new_frames_needed.append((name, status, combo))
    
    if not new_frames_needed:
        print("  All soup sprites already exist.")
        return
    
    old_w, old_h = soups_img.size
    frames_per_row = 12
    num_new = len(new_frames_needed)
    new_rows = (num_new + frames_per_row - 1) // frames_per_row
    new_h = old_h + new_rows * (TILE + 2)
    new_w = max(old_w, frames_per_row * (TILE + 2))
    
    new_img = Image.new("RGBA", (new_w, new_h), TRANSPARENT)
    new_img.paste(soups_img, (0, 0))
    draw = ImageDraw.Draw(new_img)
    
    for idx, (name, status, combo) in enumerate(new_frames_needed):
        row = idx // frames_per_row
        col = idx % frames_per_row
        fx = col * (TILE + 2) + 1
        fy = old_h + row * (TILE + 2) + 1
        
        pot_color = STATUS_POT_COLOR[status]
        
        if status == "done":
            draw.ellipse([fx+1, fy+3, fx+13, fy+13], fill=(200, 200, 200, 255), outline=(100, 100, 100, 255))
        else:
            draw.rectangle([fx+1, fy+5, fx+13, fy+13], fill=pot_color)
            draw.rectangle([fx+0, fy+4, fx+14, fy+6], fill=pot_color)
        
        total = len(combo)
        if total == 1:
            positions = [(fx+5, fy+7)]
        elif total == 2:
            positions = [(fx+3, fy+7), (fx+8, fy+7)]
        else:
            positions = [(fx+3, fy+7), (fx+8, fy+7), (fx+5, fy+10)]
        
        for i, ing in enumerate(combo[:3]):
            px, py = positions[i]
            color = SOUP_COLORS.get(ing, (200, 200, 200)) + (255,)
            draw.ellipse([px, py, px+4, py+3], fill=color)
        
        if status == "cooked":
            draw.line([fx+4, fy+1, fx+4, fy+3], fill=(200, 200, 200, 180))
            draw.line([fx+7, fy+0, fx+7, fy+2], fill=(200, 200, 200, 180))
            draw.line([fx+10, fy+1, fx+10, fy+3], fill=(200, 200, 200, 180))
        
        soups_json["textures"][0]["frames"].append({
            "filename": name,
            "frame": {"x": fx, "y": fy, "w": TILE, "h": TILE},
            "rotated": False,
            "trimmed": False,
            "spriteSourceSize": {"x": 0, "y": 0, "w": TILE, "h": TILE},
            "sourceSize": {"w": TILE, "h": TILE}
        })
    
    soups_json["textures"][0]["size"] = {"w": new_w, "h": new_h}
    
    new_img.save(os.path.join(GRAPHICS_DIR, "soups.png"))
    with open(os.path.join(GRAPHICS_DIR, "soups.json"), "w") as f:
        json.dump(soups_json, f, indent=2)
    
    print(f"  Added {len(new_frames_needed)} new soup sprites. New size: {new_w}x{new_h}")


def update_chef_sprites():
    """Add chef sprites holding new ingredients."""
    print("Updating chef sprites...")
    
    chefs_img = Image.open(os.path.join(GRAPHICS_DIR, "chefs.png"))
    with open(os.path.join(GRAPHICS_DIR, "chefs.json")) as f:
        chefs_json = json.load(f)
    
    directions = ["NORTH", "SOUTH", "EAST", "WEST"]
    
    # All items that chefs can hold (including original cucumber/rice)
    all_held_items = ["cucumber", "rice", "soup-cucumber", "soup-rice",
                      "olive", "feta_cheese", "hamburger_bun", "soy_sauce",
                      "frozen_peas", "frozen_carrots",
                      "soup-olive", "soup-feta_cheese", "soup-hamburger_bun",
                      "soup-soy_sauce", "soup-frozen_peas", "soup-frozen_carrots"]
    
    # Get base sprite positions for each direction
    base_frames = {}
    for d in directions:
        key = f"{d}.png"
        if key in chefs_json["frames"]:
            base_frames[d] = chefs_json["frames"][key]["frame"]
    
    old_w, old_h = chefs_img.size
    
    needed = []
    for d in directions:
        for item in all_held_items:
            key = f"{d}-{item}.png"
            if key not in chefs_json["frames"]:
                needed.append((d, item, key))
    
    if not needed:
        print("  All chef sprites already exist.")
        return
    
    new_w = old_w + (TILE + 2) * ((len(needed) + 3) // 4)
    new_h = max(old_h, 4 * (TILE + 2) + 2)
    
    new_img = Image.new("RGBA", (new_w, new_h), TRANSPARENT)
    new_img.paste(chefs_img, (0, 0))
    
    for idx, (direction, item, key) in enumerate(needed):
        col = idx // 4
        row = idx % 4
        fx = old_w + col * (TILE + 2) + 1
        fy = row * (TILE + 2) + 1
        
        bf = base_frames[direction]
        base_region = chefs_img.crop((bf["x"], bf["y"], bf["x"] + bf["w"], bf["y"] + bf["h"]))
        new_img.paste(base_region, (fx, fy))
        
        draw = ImageDraw.Draw(new_img)
        
        if direction == "SOUTH":
            ix, iy = fx + 5, fy + 10
        elif direction == "NORTH":
            ix, iy = fx + 5, fy + 1
        elif direction == "EAST":
            ix, iy = fx + 10, fy + 6
        elif direction == "WEST":
            ix, iy = fx + 1, fy + 6
        
        is_soup = item.startswith("soup-")
        base_item = item[5:] if is_soup else item
        
        if is_soup:
            # Draw a small bowl/pot with colored dot
            draw.ellipse([ix-1, iy, ix+5, iy+4], fill=(128, 128, 128, 255))
            color = INGREDIENT_COLORS.get(base_item, (200, 200, 200))
            draw.ellipse([ix, iy+1, ix+3, iy+3], fill=color + (255,))
        else:
            # Draw a small colored indicator for the ingredient
            color = INGREDIENT_COLORS.get(base_item, (200, 200, 200))
            draw.ellipse([ix, iy, ix+4, iy+3], fill=color + (255,))
        
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
