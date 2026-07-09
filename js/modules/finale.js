import { CONFIG } from '../core/config.js';
import { STATE } from '../core/state.js';
import { DOM } from '../core/dom.js';
import { ParticleEngine } from '../core/particleEngine.js';
import { scrollToTop } from '../core/animationManager.js';
import { resetEnvelope } from './letter.js';

let finaleParticles = null;
let excitedPulse = null;

/**
 * Spawns a massive, beautiful celebration burst of stars and hearts from the giant heart's core
 */
function triggerFinaleFirework(cx, cy) {
    const sectionElement = DOM.queryLive(CONFIG.selectors.finaleSection);
    if (!sectionElement) return;

    const colors = ['#D4AF37', '#FF5F8A', '#FFFFFF', '#FF8EA4', '#E6C15C', '#F3E5AB'];
    const particleCount = 75;

    // Localized anchor
    const container = document.createElement('div');
    container.style.position = 'fixed';
    container.style.left = '0';
    container.style.top = '0';
    container.style.width = '100vw';
    container.style.height = '100vh';
    container.style.pointerEvents = 'none';
    container.style.zIndex = '99999';
    document.body.appendChild(container);

    for (let i = 0; i < particleCount; i++) {
        const piece = document.createElement('div');
        piece.style.position = 'absolute';
        piece.style.left = `${cx}px`;
        piece.style.top = `${cy}px`;
        piece.style.transform = 'translate(-50%, -50%)';
        piece.style.pointerEvents = 'none';

        // Mix 50% sparkles (dots) and 50% elegant mini vector hearts!
        const isHeart = Math.random() > 0.5;

        if (isHeart) {
            piece.style.width = '18px';
            piece.style.height = '16px';
            piece.innerHTML = `
                <svg viewBox="0 0 24 24" width="100%" height="100%">
                    <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" fill="${gsap.utils.random(colors)}" opacity="0.85" />
                </svg>
            `;
        } else {
            piece.style.width = `${gsap.utils.random(5, 10)}px`;
            piece.style.height = piece.style.width;
            piece.style.borderRadius = '50%';
            piece.style.backgroundColor = gsap.utils.random(colors);
        }

        container.appendChild(piece);

        // Calculate expansive celebration blast vectors (explosive physical circle)
        const angle = gsap.utils.random(0, Math.PI * 2);
        const force = gsap.utils.random(100, 380);
        const targetX = Math.cos(angle) * force;
        const targetY = Math.sin(angle) * force - gsap.utils.random(50, 150); // Skew upwards

        // Kinetic explosion timelines
        gsap.timeline({
            onComplete: () => piece.remove()
        })
        .to(piece, {
            x: targetX,
            y: targetY,
            rotation: "random(-360, 360)",
            scale: gsap.utils.random(0.5, 1.5),
            duration: gsap.utils.random(0.6, 1.2),
            ease: "power3.out"
        })
        .to(piece, {
            y: targetY + gsap.utils.random(150, 300), // Falling gravity curve
            opacity: 0,
            scale: 0.1,
            duration: gsap.utils.random(1.0, 1.6),
            ease: "power2.in",
            delay: -0.2
        });
    }

    // Clean up container
    setTimeout(() => container.remove(), 3500);
}

function setupFinaleScrollAnimations() {
    const sectionElement = DOM.queryLive(CONFIG.selectors.finaleSection);
    const heartDisplay = sectionElement?.querySelector('.finale-heart-display');
    const headline = sectionElement?.querySelector('.finale-headline');
    const prose = sectionElement?.querySelector('.finale-prose');
    const signature = sectionElement?.querySelector('.finale-signature');
    const actions = sectionElement?.querySelector('.finale-actions');

    if (!sectionElement) return;

    const revealTimeline = gsap.timeline({
        scrollTrigger: {
            trigger: sectionElement,
            start: "top 75%",
            once: true
        }
    });

    // Reveal giant glowing heart
    if (heartDisplay) {
        revealTimeline.fromTo(heartDisplay,
            { scale: 0.6, opacity: 0 },
            { scale: 1, opacity: 1, duration: 1.4, ease: "elastic.out(1, 0.4)" }
        );
    }

    // Character-by-character reveal for headline
    if (headline) {
        const split = new SplitType(headline, { types: 'lines, words, chars' });
        headline.classList.add('js-split-initialized');

        revealTimeline.from(split.chars, {
            y: "100%",
            opacity: 0,
            duration: 1.2,
            stagger: 0.02,
            ease: "power4.out"
        }, "-=0.8");
    }

    // Staggered reveals of prose, signatures, and buttons
    const elementsToReveal = [];
    if (prose) elementsToReveal.push(prose);
    if (signature) elementsToReveal.push(signature);
    if (actions) elementsToReveal.push(actions);

    if (elementsToReveal.length > 0) {
        revealTimeline.fromTo(elementsToReveal,
            { opacity: 0, y: 20 },
            { opacity: 1, y: 0, duration: 1.0, stagger: 0.25, ease: "power3.out" },
            "-=0.6"
        );
    }
}

/**
 * Configure hover pounding effects and explosive click triggers on the giant heart
 */
function initInteractiveHeart() {
    const sectionElement = DOM.queryLive(CONFIG.selectors.finaleSection);
    const heartDisplay = sectionElement?.querySelector('.finale-heart-display');
    const heartSvg = sectionElement?.querySelector('.glowing-heart-svg');

    if (!heartDisplay || !heartSvg) return;

    // 1. Mouse Enter: Accelerate and brighten heartbeat pulse
    heartDisplay.addEventListener('mouseenter', () => {
        // Double-rate custom pulsing beats
        excitedPulse = gsap.to(heartSvg, {
            scale: 1.15,
            filter: "drop-shadow(0 0 45px rgba(255, 95, 138, 0.95)) drop-shadow(0 0 20px rgba(212, 175, 55, 0.5))",
            duration: 0.35,
            repeat: -1,
            yoyo: true,
            ease: "sine.inOut"
        });
        
        // Elastic slight lift on container
        gsap.to(heartDisplay, {
            scale: 1.1,
            duration: 0.4,
            ease: "back.out(1.5)"
        });
    }, { passive: true });

    // 2. Mouse Leave: Restore normal slow ambient beating
    heartDisplay.addEventListener('mouseleave', () => {
        if (excitedPulse) {
            excitedPulse.kill();
            excitedPulse = null;
        }

        // Restore baseline slow pulse
        gsap.to(heartSvg, {
            scale: 1.0,
            filter: "drop-shadow(0 0 35px rgba(212, 175, 55, 0.6))",
            duration: 0.6,
            ease: "power2.out"
        });

        gsap.to(heartDisplay, {
            scale: 1.0,
            duration: 0.6,
            ease: "power3.out"
        });
    }, { passive: true });

    // 3. Mouse Click: Trigger elastic impact and massive fireworks blast
    heartDisplay.addEventListener('click', (e) => {
        // Physical click feedback pop
        const clickTimeline = gsap.timeline();
        clickTimeline.to(heartDisplay, { scale: 0.9, duration: 0.1, ease: "power1.in" });
        clickTimeline.to(heartDisplay, { scale: 1.18, duration: 0.5, ease: "elastic.out(1, 0.3)" });

        // Calculate absolute center of the clicked heart
        const rect = heartDisplay.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;

        // Erupt the celebration fireworks!
        triggerFinaleFirework(centerX, centerY);
    }, { passive: true });
}

function runReplayExperience() {
    scrollToTop(false);
    setTimeout(() => {
        resetEnvelope();
    }, 1000);
}

export function initFinale() {
    const canvasElement = DOM.queryLive('#finale-particle-canvas');
    if (canvasElement) {
        finaleParticles = new ParticleEngine(canvasElement, 'finale');
    }

    window.addEventListener('canvas:finale:play', () => {
        if (finaleParticles) finaleParticles.start();
    });

    window.addEventListener('canvas:finale:pause', () => {
        if (finaleParticles) finaleParticles.stop();
    });

    // Setup entry and click triggers
    setupFinaleScrollAnimations();
    initInteractiveHeart();

    if (DOM.replayBtn) {
        DOM.replayBtn.addEventListener('click', runReplayExperience, { passive: true });
    }
}