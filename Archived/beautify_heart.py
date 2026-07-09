import os
import re

print("Beautifying heart vectors across index.html...")

html_path = "index.html"
if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Standardize and beautify the Intro Heart (Change ViewBox and replace Path)
    old_intro_heart_svg = """<svg class="interactive-heart" id="intro-heart" viewBox="0 0 100 90" xmlns="http://www.w3.org/2000/svg">
                    <defs>
                        <linearGradient id="gold-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stop-color="#FF5F8A" />
                            <stop offset="50%" stop-color="#D4AF37" />
                            <stop offset="100%" stop-color="#FF5F8A" />
                        </linearGradient>
                        <filter id="luxury-glow" x="-20%" y="-20%" width="140%" height="140%">
                            <feGaussianBlur stdDeviation="6" result="blur" />
                            <feComposite in="SourceGraphic" in2="blur" operator="over" />
                        </filter>
                    </defs>
                    <path d="M12 4.435C2.106-2.19 0 7.435 0 14.331c0 14.168 15.698 28.536 34.024 43.19C42.863 64.636 47 68.3 50 71c3-2.7 7.137-6.364 15.976-13.479C84.302 42.867 100 28.499 100 14.331c0-6.896-2.106-16.521-12-10.096C76.2 11.83 60.1 19.333 50 22.408 39.9 19.333 23.8 11.83 12 4.435z" fill="url(#gold-gradient)" filter="url(#luxury-glow)" />
                </svg>"""

    new_intro_heart_svg = """<svg class="interactive-heart" id="intro-heart" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <defs>
                        <linearGradient id="gold-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stop-color="#FF5F8A" />
                            <stop offset="50%" stop-color="#D4AF37" />
                            <stop offset="100%" stop-color="#FF5F8A" />
                        </linearGradient>
                        <filter id="luxury-glow" x="-20%" y="-20%" width="140%" height="140%">
                            <feGaussianBlur stdDeviation="3" result="blur" />
                            <feComposite in="SourceGraphic" in2="blur" operator="over" />
                        </filter>
                    </defs>
                    <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" fill="url(#gold-gradient)" filter="url(#luxury-glow)" />
                </svg>"""

    content = content.replace(old_intro_heart_svg, new_intro_heart_svg)

    # In case there was some slight spacing variance, let's also do a direct path replace safety check:
    content = content.replace(
        'd="M12 4.435C2.106-2.19 0 7.435 0 14.331c0 14.168 15.698 28.536 34.024 43.19C42.863 64.636 47 68.3 50 71c3-2.7 7.137-6.364 15.976-13.479C84.302 42.867 100 28.499 100 14.331c0-6.896-2.106-16.521-12-10.096C76.2 11.83 60.1 19.333 50 22.408 39.9 19.333 23.8 11.83 12 4.435z"',
        'd="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"'
    )


    # 2. Standardize and beautify the Finale Heart
    old_finale_heart_svg = """<svg class="glowing-heart-svg" viewBox="0 0 100 90" xmlns="http://www.w3.org/2000/svg" aria-label="Pulsating Gold Heart Icon">
                            <path d="M12 4.435C2.106-2.19 0 7.435 0 14.331c0 14.168 15.698 28.536 34.024 43.19C42.863 64.636 47 68.3 50 71c3-2.7 7.137-6.364 15.976-13.479C84.302 42.867 100 28.499 100 14.331c0-6.896-2.106-16.521-12-10.096C76.2 11.83 60.1 19.333 50 22.408 39.9 19.333 23.8 11.83 12 4.435z" fill="url(#gold-gradient)" />
                        </svg>"""

    new_finale_heart_svg = """<svg class="glowing-heart-svg" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-label="Pulsating Gold Heart Icon">
                            <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" fill="url(#gold-gradient)" />
                        </svg>"""

    content = content.replace(old_finale_heart_svg, new_finale_heart_svg)

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ Successfully replaced both vectors with the beautiful classic heart model inside index.html")
else:
    print("✗ index.html not found!")

# Clean up helper scripts
try:
    for helper in ["seamless_heart.py", "align_heart.py", "fix_intro.py", "repair_dom.py", "repair_layout.py"]:
        if os.path.exists(helper):
            os.remove(helper)
except Exception:
    pass

print("\\nHeart beautification process completed successfully!")