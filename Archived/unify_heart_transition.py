import os
import re

print("Unifying and locking heart dimensions for a 100% seamless transition...")

# 1. Update css/sections/loader.css to lock dimensions to 80x72
loader_css_path = "css/sections/loader.css"
if os.path.exists(loader_css_path):
    with open(loader_css_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Define locked, centered loader-heart wrapper styles (prevents transform conflict)
    new_loader_heart_style = """.loader-heart-wrapper {
    position: fixed;
    top: 50%;
    left: 50%;
    width: 80px;
    height: 72px;
    margin-left: -40px !important;
    margin-top: -36px !important;
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
    transform-origin: center;
    will-change: transform, opacity;
}"""

    # Replace the loader-heart wrapper block
    content = re.sub(r"\.loader-heart-wrapper\s*\{[^}]+\}", new_loader_heart_style, content)

    with open(loader_css_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ Successfully unified preloader heart size in loader.css")
else:
    print("✗ loader.css not found!")

# 2. Update css/sections/hero.css to match loader dimensions perfectly
hero_css_path = "css/sections/hero.css"
if os.path.exists(hero_css_path):
    with open(hero_css_path, "r", encoding="utf-8") as f:
        content = f.read()

    new_hero_target_style = """.hero-heart-destination {
    position: relative;
    width: 80px;
    height: 72px;
    margin: var(--space-md) auto;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: transform 0.8s var(--ease-out-expo);
}"""

    content = re.sub(r"\.hero-heart-destination\s*\{[^}]+\}", new_hero_target_style, content)

    with open(hero_css_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ Successfully unified hero target size in hero.css")
else:
    print("✗ hero.css not found!")

# 3. Update js/modules/intro.js to compute coordinate transitions flawlessly
intro_js_path = "js/modules/intro.js"
if os.path.exists(intro_js_path):
    repaired_intro_code = """import { CONFIG } from '../core/config.js';
import { STATE } from '../core/state.js';
import { DOM } from '../core/dom.js';
import { getElementCenterCoordinates, getQuadraticBezierPoint } from '../core/utils.js';
import { unlockScroll } from '../core/animationManager.js';
import { destroyPreload } from './preload.js';
import { revealHero } from './hero.js';

let originCoords = { x: 0, y: 0 };
let destinationCoords = { x: 0, y: 0 };
let controlCoords = { x: 0, y: 0 };

function recalculateFlightCoordinates() {
    // Start directly from the physical center of the screen
    originCoords = {
        x: window.innerWidth / 2,
        y: window.innerHeight / 2
    };

    // Landing target center in Hero
    destinationCoords = getElementCenterCoordinates(DOM.heroTarget);

    // Dynamic control arc curve
    controlCoords = {
        x: (originCoords.x + destinationCoords.x) / 2 + CONFIG.bezierFlight.controlPointOffset.x,
        y: Math.min(originCoords.y, destinationCoords.y) + CONFIG.bezierFlight.controlPointOffset.y
    };
}

function beginCinematicFlight() {
    recalculateFlightCoordinates();

    const heartEl = DOM.introHeartContainer;
    if (!heartEl) return;

    // Halt preloader beats and prepare element styles
    heartEl.classList.remove('is-beating');
    heartEl.style.animation = 'none';
    heartEl.style.position = 'fixed';
    heartEl.style.top = '0';
    heartEl.style.left = '0';
    heartEl.style.margin = '0';
    heartEl.style.zIndex = '99999';
    heartEl.style.transformOrigin = 'center center';

    const flightProgress = { t: 0 };

    gsap.to(flightProgress, {
        t: 1,
        duration: CONFIG.bezierFlight.flightDurationSec,
        ease: CONFIG.bezierFlight.flightEasing,
        onUpdate: () => {
            const currentPos = getQuadraticBezierPoint(
                originCoords,
                controlCoords,
                destinationCoords,
                flightProgress.t
            );

            // Deduct half dimensions (40px, 36px) to position relative to element center
            const offsetX = currentPos.x - 40;
            const offsetY = currentPos.y - 36;

            heartEl.style.transform = `translate3d(${offsetX}px, ${offsetY}px, 0)`;
        },
        onComplete: () => {
            finalizeLandingSequence(heartEl);
        }
    });

    gsap.to('#loader-particle-canvas', {
        opacity: 0,
        duration: 1.5,
        ease: "power2.out"
    });
}

function finalizeLandingSequence(heartElement) {
    if (DOM.heroTarget) {
        // Shift DOM parent nodes cleanly
        DOM.heroTarget.appendChild(heartElement);

        // Reset fixed coordinates back to Hero-relative positioning
        heartElement.style.position = 'relative';
        heartElement.style.top = 'auto';
        heartElement.style.left = 'auto';
        heartElement.style.margin = '0 auto';
        heartElement.style.transform = 'translate3d(0, 0, 0)';
        heartElement.style.zIndex = '1';

        // Start hero ambient float
        DOM.heroTarget.classList.add('has-landed');
        
        // Solidify with elastic compression impact
        gsap.fromTo(heartElement, 
            { scale: 0.9 }, 
            { scale: 1, duration: 0.6, ease: "elastic.out(1, 0.4)" }
        );
    }

    revealHero();
    unlockScroll();
    destroyPreload();
}

export function initIntro() {
    window.addEventListener('preload:complete', beginCinematicFlight);

    window.addEventListener('state:windowWidth', () => {
        if (!STATE.current.isLoaded) {
            recalculateFlightCoordinates();
        }
    });
}"""

    with open(intro_js_path, "w", encoding="utf-8") as f:
        f.write(repaired_intro_code)
    print("✓ Successfully updated js/modules/intro.js coordinates solver")
else:
    print("✗ intro.js not found!")

print("\\nSeamless heart transitions complete!")