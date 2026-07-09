import { CONFIG } from '../core/config.js';
import { STATE } from '../core/state.js';
import { DOM } from '../core/dom.js';
import { ParticleEngine } from '../core/particleEngine.js';
import { scrollToTop } from '../core/animationManager.js';
import { resetEnvelope } from './letter.js';

let finaleParticles = null;

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

    if (heartDisplay) {
        revealTimeline.fromTo(heartDisplay,
            { scale: 0.6, opacity: 0 },
            { scale: 1, opacity: 1, duration: 1.4, ease: "elastic.out(1, 0.4)" }
        );
    }

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

    setupFinaleScrollAnimations();

    if (DOM.replayBtn) {
        DOM.replayBtn.addEventListener('click', runReplayExperience, { passive: true });
    }
}