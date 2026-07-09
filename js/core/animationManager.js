import { STATE } from './state.js';
import { DOM } from './dom.js';
import { lerp } from './utils.js';
import { getPointerPosition } from './events.js';

let lenisInstance = null;
const cursorInterp = { dotX: 0, dotY: 0, ringX: 0, ringY: 0 };

function initSmoothScroll() {
    lenisInstance = new Lenis({
        duration: 1.4,
        easing: (t) => (t === 1 ? 1 : 1 - Math.pow(2, -10 * t)),
        orientation: 'vertical',
        gestureOrientation: 'vertical',
        smoothWheel: true,
        wheelMultiplier: 1.0,
        touchMultiplier: 1.2,
        infinite: false
    });

    lenisInstance.on('scroll', ScrollTrigger.update);

    gsap.ticker.add((time) => {
        lenisInstance.raf(time * 1000);
    });

    gsap.ticker.lagSmoothing(0);

    lenisInstance.on('scroll', (e) => {
        if (e.scroll > 50) {
            STATE.set('activeSection', 'scrolling');
        } else {
            STATE.set('activeSection', 'hero');
        }
    });
}

// Spawns clean, GPU-accelerated gold stardust trailing behind the cursor
function spawnStardustSparkle(x, y) {
    // Throttle spawning rate to maintain 60 FPS performance
    if (Math.random() > 0.3) return;

    const sparkle = document.createElement('div');
    sparkle.style.position = 'fixed';
    sparkle.style.left = `${x}px`;
    sparkle.style.top = `${y}px`;
    sparkle.style.width = '4px';
    sparkle.style.height = '4px';
    sparkle.style.borderRadius = '50%';
    sparkle.style.pointerEvents = 'none';
    sparkle.style.zIndex = '999999';
    
    // Mix warm gold and rose gold sparks
    const colors = ['#D4AF37', '#FF5F8A', '#FFF', '#FF8EA4'];
    sparkle.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
    
    document.body.appendChild(sparkle);

    // Dynamic drifting vectors
    gsap.to(sparkle, {
        x: 'random(-15, 15)',
        y: 'random(-10, 25)', // Fall slightly due to gravity
        opacity: 0,
        scale: 0.1,
        duration: gsap.utils.random(0.6, 1.2),
        ease: "power2.out",
        onComplete: () => sparkle.remove()
    });
}

function updateCustomCursorTick() {
    const coords = getPointerPosition();

    cursorInterp.dotX = lerp(cursorInterp.dotX, coords.targetX, 0.35);
    cursorInterp.dotY = lerp(cursorInterp.dotY, coords.targetY, 0.35);
    cursorInterp.ringX = lerp(cursorInterp.ringX, coords.targetX, 0.12);
    cursorInterp.ringY = lerp(cursorInterp.ringY, coords.targetY, 0.12);

    if (DOM.customCursor) {
        const dotElement = DOM.customCursor.querySelector('.cursor-dot');
        const ringElement = DOM.customCursor.querySelector('.cursor-ring');

        if (dotElement) {
            dotElement.style.transform = `translate3d(${cursorInterp.dotX}px, ${cursorInterp.dotY}px, 0)`;\n        spawnStardustSparkle(cursorInterp.dotX, cursorInterp.dotY);
        }
        if (ringElement) {
            ringElement.style.transform = `translate3d(${cursorInterp.ringX}px, ${cursorInterp.ringY}px, 0)`;
        }
    }
}

export function initAnimationManager() {
    initSmoothScroll();
    lockScroll();
    gsap.ticker.add(updateCustomCursorTick);

    window.addEventListener('pointer:enter-interactive', () => {
        if (DOM.customCursor) DOM.customCursor.classList.add('active');
    });

    window.addEventListener('pointer:leave-interactive', () => {
        if (DOM.customCursor) DOM.customCursor.classList.remove('active');
    });
}

export function lockScroll() {
    if (lenisInstance) {
        lenisInstance.stop();
    }
    document.documentElement.classList.add('lenis-clean-scroll');
}

export function unlockScroll() {
    if (lenisInstance) {
        lenisInstance.start();
    }
    document.documentElement.classList.remove('lenis-clean-scroll');
}

export function scrollToTop(immediate = true) {
    if (lenisInstance) {
        lenisInstance.scrollTo(0, { immediate });
    }
}

export function getScroller() {
    return lenisInstance;
}