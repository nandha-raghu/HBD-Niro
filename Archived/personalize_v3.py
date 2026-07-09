import os
import re

print("Executing Project Lumière Ultimate Personalization Sweep...")

# 1. Update index.html (Metadata, Headers, Intimate Copywriting, and Asset Targets)
html_path = "index.html"
if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Browser Title & Meta
    content = content.replace("<title>Project Lumière v2.0</title>", "<title>Happy Birthday Nirosha ❤️</title>")
    content = content.replace(
        '<meta name="description" content="Project Lumière v2.0 — An immersive, high-end cinematic interactive journey celebrating a beautiful milestone.">',
        '<meta name="description" content="A heartfelt birthday surprise made with love for Niro.">'
    )

    # Audio Control Labels
    content = content.replace("PLAY SYSTEM SCORE", "Play Our Song ❤️")
    content = content.replace("Play Music", "Play Our Song ❤️")

    # Preloader Headers and Labels
    content = content.replace("PROJECT LUMIÈRE", "A Gift From My Heart")
    content = content.replace("class=\"cinematic-prose font-serif\"", "class=\"heartfelt-prose font-serif\"")
    content = content.replace("Every Moment Has A Story...", "Finding Every Beautiful Moment...")

    # Hero brand and title details
    content = content.replace("Made Especially For You", "Every Memory With You Is My Favourite Story")
    
    # Chapter 1 (Story) Clean up presentation markers and AI terms
    content = content.replace("Chapter I — The Beginning Of Us", "Our Story")
    content = content.replace("A Cinematic Convergence", "Where My Heart Found Home")
    content = content.replace("Where My Heart Found Home", "The Day My World Changed")

    # Timeline Section
    content = content.replace("Chapter II", "Beautiful Memories")

    # Gallery Section
    content = content.replace("Chapter III", "Moments That Matter")

    # Letter Section
    content = content.replace("Chapter IV", "A Letter From My Heart")
    content = content.replace("A Letter From My Heart", "To My Forever")
    content = content.replace("To My Forever", "A Letter From My Heart") # Align exact sequence
    
    # Personal memory injection inside the letter
    old_letter_body = """As another wonderful year rolls around, I find myself looking back at how incredibly lucky I am to have you in my life. You have been my constant inspiration, my calmest sanctuary, and my greatest source of joy. Your kindness is a gentle light that guides me on my darkest days, and your laugh is my absolute favorite sound in the world."""
    
    new_letter_body = """As another wonderful year rolls around, I find myself looking back at how incredibly lucky I am to have you in my life. You have been my constant inspiration, my calmest sanctuary, and my greatest source of joy. I still smile thinking about our first laugh together—that silly, uncontrollable moment where we couldn't even remember what we were laughing at, but we knew we didn't want it to end. Your kindness is a gentle light that guides me on my darkest days, and your laugh is my favorite sound in the world."""
    
    content = content.replace(old_letter_body, new_letter_body)

    # Gallery Captions - Intimate & Handcrafted replacement
    content = content.replace("Your Beautiful Smile", "The Smile I Fell In Love With")
    content = content.replace("My Favorite View", "Forever my favourite smile")
    content = content.replace("That Rainy Evening", "The Day My World Changed")
    content = content.replace("Cozy Details", "One more beautiful moment")
    content = content.replace("The Happiest Day", "The Happiest Version Of Me")
    content = content.replace("Our Private Universe", "My favourite memory")
    content = content.replace("The Smile That Changed Everything", "The Little Moments I Treasure")
    content = content.replace("Unplanned Adventures", "Every moment with you matters")

    # Finale Text Blocks
    content = content.replace("No Matter Where Life Takes Us", "No Matter Where Life Takes Us")
    content = content.replace("I'll Always Choose You.", "Every day with you is the greatest gift I've ever received.")
    content = content.replace("Happy Birthday Nirosha ❤️", "Happy Birthday Nirosha ❤️")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ Refactored index.html (personal memories, tags, metadata, and browser titles)")
else:
    print("✗ index.html not found!")


# 2. Update css/sections/loader.css (Support rebuilt class name for prose)
loader_css_path = "css/sections/loader.css"
if os.path.exists(loader_css_path):
    with open(loader_css_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Rename cinematic prose to heartfelt prose
    content = content.replace(".cinematic-prose", ".heartfelt-prose")

    with open(loader_css_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ Successfully updated CSS class indicators inside loader.css")
else:
    print("✗ loader.css not found!")


# 3. Update js/modules/preload.js (Dynamic loader message values)
preload_path = "js/modules/preload.js"
if os.path.exists(preload_path):
    with open(preload_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace progressive message updates
    content = content.replace("Every Moment Has A Story...", "Finding Every Beautiful Moment...")
    content = content.replace(".cinematic-prose", ".heartfelt-prose")

    with open(preload_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ Configured progressive loaders inside preload.js")
else:
    print("✗ preload.js not found!")


# 4. Update js/modules/music.js (Widget text updates)
music_path = "js/modules/music.js"
if os.path.exists(music_path):
    with open(music_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Modify string constants inside player toggler
    content = content.replace('"MUTE SYSTEM SCORE"', '"Mute Our Song"')
    content = content.replace('"PLAY SYSTEM SCORE"', '"Play Our Song ❤️"')
    content = content.replace('"Mute Music"', '"Mute Our Song"')
    content = content.replace('"Play Music"', '"Play Our Song ❤️"')

    with open(music_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ Configured unmuting copy indicators inside music.js")
else:
    print("✗ music.js not found!")

print("\\nRefinement sweep completed! Your workspace is pristine, beautiful, and completely custom-tailored for Nirosha.")