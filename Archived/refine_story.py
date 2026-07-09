import os
import re

print("Refining Project Lumière copywriting, background atmosphere, and emotional pacing...")

# 1. Update index.html: Rewrite copy, update names, button texts, and timeline memories
html_path = "index.html"
if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Modify Audio Button Label
    content = content.replace("PLAY SYSTEM SCORE", "Play Music")

    # Modify Preloader Header text
    content = content.replace("Loading Memories...", "Preparing Something Beautiful...")

    # Modify Preloader Step 2 text
    content = content.replace(
        "Our love story deserves something truly special.",
        "Every Moment Has A Story..."
    )

    # Modify Hero brand and title details
    content = content.replace("EST. 2025", "Made Especially For You")
    content = content.replace("Happy Birthday", "To The Most Beautiful Soul")
    content = content.replace("My Love", "Happy Birthday Nirosha")

    # Modify Hero CTA text
    content = content.replace("Begin The Journey", "Touch My Heart ❤️")

    # Modify Chapter 1 (Story) copy
    content = content.replace("A Cinematic Convergence", "The Day My Heart Found Home")
    content = content.replace("Chapter I", "Chapter I — The Beginning Of Us")
    content = content.replace(
        """Every moment we have shared has felt like a scene crafted by a master filmmaker. The quiet evenings, the explosive laughter, and the subtle gestures of love that bind us closer with every passing season.""",
        """I still remember the exact moment you walked into my life. The world didn't stop, and there were no fireworks, but in that quiet, ordinary second, everything changed for me. Your laugh immediately felt like a familiar song, and your presence brought a calm I didn't know I was searching for."""
    )
    content = content.replace(
        """This experience is a digital monument to our journey together. A celebration of your light, your brilliance, and the effortless way you make the world feel more beautiful simply by being in it.""",
        """This space is a little home for our memories. It’s for the private jokes we share, the hurdles we’ve crossed together, and the quiet comfort of holding your hand at the end of a long day. I wanted to build something that shows you how deeply you are loved, not just today, but in every single moment."""
    )
    content = content.replace(
        """"In your smile, I find the script of my absolute happiest days.\"""",
        """"In your smile, I found the place where I always want to stay.\""""
    )
    content = content.replace("October 14, 2024", "Our First Selfie")
    content = content.replace("Paris, France", "The Day Everything Changed")

    # Modify Chapter 2 (Timeline) copy
    content = content.replace("Our Milestone Timeline", "Every Step With You")
    content = content.replace("Key frames from the reel of our beautiful journey.", "The moments that built the bridge to where we are today.")
    
    # Timeline card 1
    content = content.replace("The Spark", "Where It All Began")
    content = content.replace("Where it all began", "We Became Friends")
    content = content.replace(
        "The precise coordinates where our paths crossed, turning an ordinary afternoon into an unforgettable beginning.",
        "It started with simple conversations and endless laughter. We talked about everything and nothing at all, slowly building a safe space where we could completely be ourselves."
    )

    # Timeline card 2
    content = content.replace("The Growth", "The Shift")
    content = content.replace("Shared Ambitions", "Our First Chocolate")
    content = content.replace(
        "Building dreams together, encouraging each other’s wild creative ideas, and establishing an unbreakable partnership.",
        "That sweet, quiet afternoon where a simple gesture of sharing chocolate turned into something deeper. I looked at you and realized my thoughts were occupied by you, always."
    )

    # Timeline card 3
    content = content.replace("The Adventure", "The Realization")
    content = content.replace("Uncharted Horizons", "The Day I Realized I Love You")
    content = content.replace(
        "Chasing Sunsets across different borders, documenting every moment, finding absolute peace in our own little universe.",
        "There was no turning back. Your kindness, your beautiful heart, and the effortless way you make the world warmer showed me that my future belonged right next to yours."
    )

    # Modify Chapter 3 (Gallery) copy
    content = content.replace("A Curated Gallery", "Moments I'll Never Forget")
    content = content.replace("Captured fragments of timeless joy.", "Scattered frames of pure happiness.")
    content = content.replace("Captured Joy", "Your Beautiful Smile")
    content = content.replace("Candid", "My Favorite View")
    content = content.replace("Starlit Skyline", "That Rainy Evening")
    content = content.replace("Scenic", "Cozy Details")
    content = content.replace("Connected", "The Happiest Day")
    content = content.replace("Detail", "Our Private Universe")
    content = content.replace("Warm Horizons", "The Smile That Changed Everything")
    content = content.replace("Travel", "Unplanned Adventures")

    # Modify Chapter 4 (Letter) copy
    content = content.replace("To My Forever", "A Letter From My Heart")
    content = content.replace("Click the wax seal to unveil my personal note to you.", "Click the wax seal to unfold my personal note to you.")
    content = content.replace("Today and Always", "Today and Always, Nirosha")
    content = content.replace("My Dearest,", "My Dearest Nirosha,")
    content = content.replace(
        "As another wonderful year rolls around, I find myself looking back at all the microscopic and monumental details of our shared path. You have been my constant inspiration, my calmest sanctuary, and my greatest cheerleader.",
        "As another wonderful year rolls around, I find myself looking back at how incredibly lucky I am to have you in my life. You have been my constant inspiration, my calmest sanctuary, and my greatest source of joy. Your kindness is a gentle light that guides me on my darkest days, and your laugh is my absolute favorite sound in the world."
    )
    content = content.replace(
        "This experience is a digital monument to our journey together. A celebration of your light, your brilliance, and the effortless way you make the world feel more beautiful simply by being in it.",
        "I am so incredibly proud of the woman you are—the strength you carry, the warmth you give to everyone around you, and the beautiful dreams you work so hard to achieve."
    )
    content = content.replace(
        "May your year be filled with the same boundless warmth, stunning brilliance, and infinite joy you give so freely to those around you.",
        "On your birthday, my promise to you is simple: no matter where life leads us, I will walk by your side, holding your hand, and cheering you on. I promise to support your wildest ideas, to protect your peace, and to love you more with every single passing day."
    )
    content = content.replace("Forever yours,", "With all my love, always,")
    content = content.replace("Lumière", "Yours ❤️")

    # Modify Chapter 5 (Finale) copy
    content = content.replace("To Infinite Birthdays Together.", "No Matter Where Life Takes Us")
    content = content.replace(
        "Our cinematic narrative has only just started. Thank you for making everyday extraordinary.",
        "I'll Always Choose You."
    )
    content = content.replace("I love you, always.", "Happy Birthday Nirosha ❤️")
    content = content.replace("Replay Experience", "Relive Our Memories")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ Successfully personalized copywriting and tags inside index.html")
else:
    print("✗ index.html not found!")


# 2. Update css/sections/story.css with a warm, floating dawn-light leak backdrop
story_css_path = "css/sections/story.css"
if os.path.exists(story_css_path):
    with open(story_css_path, "r", encoding="utf-8") as f:
        content = f.read()

    ambient_story_bg = """.story-viewport {
    background: radial-gradient(circle at 80% 20%, rgba(255, 95, 138, 0.04) 0%, var(--color-bg) 60%),
                radial-gradient(circle at 20% 80%, rgba(212, 175, 55, 0.03) 0%, var(--color-bg) 70%);
    padding: var(--space-xxl) 0;
}"""
    content = re.sub(r"\.story-viewport\s*\{[^}]+\}", ambient_story_bg, content)
    with open(story_css_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ Embedded warm emotional dawn-light leak backdrop in story.css")


# 3. Update css/sections/timeline.css with deep cosmic nebula layers
timeline_css_path = "css/sections/timeline.css"
if os.path.exists(timeline_css_path):
    with open(timeline_css_path, "r", encoding="utf-8") as f:
        content = f.read()

    ambient_timeline_bg = """.timeline-viewport {
    background: radial-gradient(circle at 50% 50%, rgba(142, 142, 142, 0.02) 0%, var(--color-bg-secondary) 100%),
                radial-gradient(circle at 10% 20%, rgba(212, 175, 55, 0.02) 0%, transparent 50%),
                radial-gradient(circle at 90% 80%, rgba(255, 95, 138, 0.02) 0%, transparent 50%);
    padding: var(--space-xxl) 0;
}"""
    content = re.sub(r"\.timeline-viewport\s*\{[^}]+\}", ambient_timeline_bg, content)
    with open(timeline_css_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ Embedded elegant starlight nebula depth inside timeline.css")


# 4. Update css/sections/gallery.css with soft spotlights and vignette framing
gallery_css_path = "css/sections/gallery.css"
if os.path.exists(gallery_css_path):
    with open(gallery_css_path, "r", encoding="utf-8") as f:
        content = f.read()

    ambient_gallery_bg = """.gallery-viewport {
    background: radial-gradient(ellipse at center, rgba(5, 5, 5, 0) 40%, rgba(0, 0, 0, 0.95) 100%),
                radial-gradient(circle at 50% 30%, rgba(212, 175, 55, 0.02) 0%, var(--color-bg) 60%);
    padding: var(--space-xxl) 0;
}"""
    content = re.sub(r"\.gallery-viewport\s*\{[^}]+\}", ambient_gallery_bg, content)
    with open(gallery_css_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ Embedded elegant focal spotlight vignette inside gallery.css")


# 5. Update css/sections/letter.css with candlelight warm glows
letter_css_path = "css/sections/letter.css"
if os.path.exists(letter_css_path):
    with open(letter_css_path, "r", encoding="utf-8") as f:
        content = f.read()

    ambient_letter_bg = """.letter-viewport {
    background: radial-gradient(circle at 50% 10%, rgba(212, 175, 55, 0.04) 0%, var(--color-bg-secondary) 80%);
    padding: var(--space-xxl) 0;
}"""
    content = re.sub(r"\.letter-viewport\s*\{[^}]+\}", ambient_letter_bg, content)
    with open(letter_css_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ Embedded warm romantic candlelight atmosphere inside letter.css")


# 6. Update css/sections/finale.css with cinematic cosmic sunrise galaxy backdrops
finale_css_path = "css/sections/finale.css"
if os.path.exists(finale_css_path):
    with open(finale_css_path, "r", encoding="utf-8") as f:
        content = f.read()

    ambient_finale_bg = """.finale-viewport {
    position: relative;
    background: radial-gradient(circle at 50% 120%, rgba(255, 95, 138, 0.12) 0%, rgba(212, 175, 55, 0.06) 40%, var(--color-bg) 80%);
    min-height: 100vh;
    padding: var(--space-xxl) 0;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    text-align: center;
}"""
    content = re.sub(r"\.finale-viewport\s*\{[^}]+\}", ambient_finale_bg, content)
    with open(finale_css_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ Embedded beautiful sunrise galaxy glow inside finale.css")


# 7. Update js/modules/preload.js: Handle the fading text sequence steps dynamically
preload_js_path = "js/modules/preload.js"
if os.path.exists(preload_path):
    repaired_preload_code = """import { CONFIG } from '../core/config.js';
import { STATE } from '../core/state.js';
import { DOM } from '../core/dom.js';
import { ParticleEngine } from '../core/particleEngine.js';

let loaderParticles = null;

export function initPreload() {
    const canvas = DOM.queryLive('#loader-particle-canvas');
    if (DOM.loaderScreen && canvas) {
        loaderParticles = new ParticleEngine(canvas, 'loader');
        loaderParticles.start();
    }
    beginPreloadingProgress();
}

function beginPreloadingProgress() {
    let currentProgress = 0;
    const duration = CONFIG.preloader.fakePreloadDurationMs;
    const intervalMs = 30;
    const totalSteps = duration / intervalMs;
    const progressIncrement = 100 / totalSteps;

    if (DOM.introHeartContainer) {
        DOM.introHeartContainer.classList.add('is-beating');
    }

    const titleElement = DOM.msgStep1?.querySelector('.loader-title');

    const progressTimer = setInterval(() => {
        currentProgress += progressIncrement;
        const progressClamped = Math.min(100, currentProgress);

        if (DOM.progressBar) {
            DOM.progressBar.style.transform = `scaleX(${progressClamped / 100})`;
        }

        // Dynamic, high-anticipation loader string updates based on progress percent
        if (titleElement) {
            if (progressClamped < 25) {
                titleElement.textContent = "Preparing Something Beautiful...";
            } else if (progressClamped < 55) {
                titleElement.textContent = "Collecting Our Memories...";
            } else if (progressClamped < 80) {
                titleElement.textContent = "Every Moment Has A Story...";
            } else {
                titleElement.textContent = "Almost Ready...";
            }
        }

        if (DOM.introHeartContainer && progressClamped > 40) {
            const beatDuration = gsap.utils.mapRange(40, 100, 1.4, 0.6, progressClamped);
            DOM.introHeartContainer.style.animationDuration = `${beatDuration}s`;
        }

        if (progressClamped >= 100) {
            clearInterval(progressTimer);
            handlePreloadComplete();
        }
    }, intervalMs);
}

function handlePreloadComplete() {
    const fadeTimeline = gsap.timeline({
        onComplete: () => {
            window.dispatchEvent(new CustomEvent('preload:complete'));
        }
    });

    if (DOM.msgStep1) {
        fadeTimeline.to(DOM.msgStep1, {
            opacity: 0,
            y: -15,
            duration: 0.8,
            ease: "power2.inOut"
        });
    }

    if (DOM.msgStep2) {
        fadeTimeline.to(DOM.msgStep2, {
            onStart: () => {
                if (DOM.msgStep1) DOM.msgStep1.classList.remove('active');
                
                // Final loading climax text
                const proseEl = DOM.msgStep2.querySelector('.cinematic-prose');
                if (proseEl) proseEl.textContent = "Happy Birthday ❤️";
                
                DOM.msgStep2.classList.add('active');
            },
            opacity: 1,
            y: 0,
            duration: CONFIG.preloader.textFadeDurationSec,
            ease: "power3.out"
        }, `+=${CONFIG.preloader.transitionOverlapSec}`);

        fadeTimeline.to(DOM.msgStep2, {
            opacity: 0,
            y: -10,
            duration: 0.8,
            ease: "power2.in"
        }, "+=1.8");
    }
}

export function destroyPreload() {
    if (loaderParticles) {
        loaderParticles.stop();
        loaderParticles = null;
    }

    if (DOM.loaderScreen) {
        DOM.loaderScreen.classList.add('is-loaded');
        setTimeout(() => {
            DOM.loaderScreen.remove();
        }, 1200);
    }
}"""
    with open(preload_path, "w", encoding="utf-8") as f:
        f.write(repaired_preload_code)
    print("✓ Injected dynamic preloader sequence into preload.js")


# 8. Update js/modules/music.js and js/modules/hero.js text bindings to match "Play Music"
music_path = "js/modules/music.js"
if os.path.exists(music_path):
    with open(music_path, "r", encoding="utf-8") as f:
        content = f.read()

    content = content.replace("PLAY SYSTEM SCORE", "Play Music")
    content = content.replace("MUTE SYSTEM SCORE", "Mute Music")

    with open(music_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ Updated button text parameters inside music.js")

print("\\nEmotional experience refinement complete!")