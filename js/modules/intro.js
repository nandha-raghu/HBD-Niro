import { CONFIG } from '../core/config.js';
import { STATE } from '../core/state.js';
import { DOM } from '../core/dom.js';
import { getElementCenterCoordinates, getQuadraticBezierPoint } from '../core/utils.js';
import { unlockScroll } from '../core/animationManager.js';
import { destroyPreload } from './preload.js';
import { revealHero } from './hero.js';

let startDelta = { x: 0, y: 0 };
let restingCoords = { x: 0, y: 0 };
let centerCoords = { x: 0, y: 0 };
let controlCoords = { x: 0, y: 0 };

/**
 * Configure start, end and curved path coordinates inside relative offset dimensions
 */
function recalculateFlightCoordinates() {
    const heartEl = DOM.introHeartContainer;
    if (!heartEl) return;

    // 1. Temporarily strip offsets so we can measure the heart's natural layout position under EST. 2025
    heartEl.style.transform = "none";
    heartEl.classList.remove('is-loader-state');

    // 2. Measure coordinates
    restingCoords = getElementCenterCoordinates(heartEl);
    centerCoords = {
        x: window.innerWidth / 2,
        y: window.innerHeight / 2
    };

    // 3. Compute offset delta needed to position the heart in the physical screen center initially
    startDelta = {
        x: centerCoords.x - restingCoords.x,
        y: centerCoords.y - restingCoords.y
    };

    // 4. Compute curved control coordinates using dynamic arcing
    controlCoords = {
        x: (centerCoords.x + restingCoords.x) / 2 + CONFIG.bezierFlight.controlPointOffset.x,
        y: Math.min(centerCoords.y, restingCoords.y) + CONFIG.bezierFlight.controlPointOffset.y
    };

    // 5. Restore loader centered layout state
    heartEl.classList.add('is-loader-state');
    heartEl.style.transform = `translate3d(${startDelta.x}px, ${startDelta.y}px, 0)`;
}

/**
 * Executes a 60 FPS Bézier return-to-resting-home curve
 */
function beginCinematicFlight() {
    const heartEl = DOM.introHeartContainer;
    if (!heartEl) return;

    // Halt heartbeat animation
    heartEl.classList.remove('is-beating');
    heartEl.style.animation = 'none';

    // Snappy, energetic flight timing (2.0s is the cinematic sweet spot)
    const flightDuration = 2.0; 
    const flightProgress = { t: 0 };

    // GSAP updates relative translations dynamically
    gsap.to(flightProgress, {
        t: 1,
        duration: flightDuration,
        ease: "power3.inOut", // Dynamic acceleration curve
        onUpdate: () => {
            const currentPos = getQuadraticBezierPoint(
                centerCoords,
                controlCoords,
                restingCoords,
                flightProgress.t
            );

            // Subtract resting coordinates to transition translate offsets back to 0,0,0
            const currentDeltaX = currentPos.x - restingCoords.x;
            const currentDeltaY = currentPos.y - restingCoords.y;

            heartEl.style.transform = `translate3d(${currentDeltaX}px, ${currentDeltaY}px, 0)`;
        },
        onComplete: () => {
            finalizeLandingSequence(heartEl);
        }
    });

    // CINEMATIC TRANSITION UPDATE:
    // Trigger preloader screen fade-out IMMEDIATELY on flight start 
    // so that the Hero background is revealed as the heart is in transit!
    destroyPreload();
}

function finalizeLandingSequence(heartElement) {
    // 1. Completely clear all coordinate displacements
    heartElement.style.transform = "translate3d(0, 0, 0)";
    heartElement.classList.remove('is-loader-state');

    // 2. Activate continuous, lightweight, responsive floating animation loop
    heartElement.classList.add('has-landed');

    // 3. Land with solid impact
    gsap.fromTo(heartElement, 
        { scale: 0.8 }, 
        { scale: 1, duration: 0.6, ease: "elastic.out(1, 0.4)" }
    );

    // 4. Reveal hero elements and unlock page interaction
    revealHero();
    unlockScroll();
}

export function initIntro() {
    // Measure coordinates and position heart in physical screen center on load
    recalculateFlightCoordinates();

    window.addEventListener('preload:complete', beginCinematicFlight);

    window.addEventListener('state:windowWidth', () => {
        if (!STATE.current.isLoaded) {
            recalculateFlightCoordinates();
        }
    });
}