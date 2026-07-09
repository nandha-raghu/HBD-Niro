import { CONFIG } from '../core/config.js';
import { STATE } from '../core/state.js';
import { DOM } from '../core/dom.js';

/**
 * Spawns a premium GPU-accelerated confetti burst originating from the seal center
 */
function triggerConfettiPopper() {
    const envelopeArena = document.querySelector('.envelope-arena');
    if (!envelopeArena) return;

    // Aesthetically calibrated luxury colors
    const colors = ['#D4AF37', '#FF5F8A', '#FFFFFF', '#FF8EA4', '#E6C15C', '#F3E5AB'];
    const confettiCount = 110;

    // Create a localized anchor layer
    const popperContainer = document.createElement('div');
    popperContainer.style.position = 'absolute';
    popperContainer.style.top = '50%';
    popperContainer.style.left = '50%';
    popperContainer.style.width = '0px';
    popperContainer.style.height = '0px';
    popperContainer.style.pointerEvents = 'none';
    popperContainer.style.zIndex = '999';
    envelopeArena.appendChild(popperContainer);

    for (let i = 0; i < confettiCount; i++) {
        const piece = document.createElement('div');
        piece.style.position = 'absolute';
        
        // Randomize dimensions
        piece.style.width = `${gsap.utils.random(6, 12)}px`;
        piece.style.height = `${gsap.utils.random(4, 10)}px`;
        piece.style.backgroundColor = gsap.utils.random(colors);
        piece.style.transformOrigin = 'center center';
        piece.style.opacity = 1;
        
        // Asymmetric mixture of squares, circles, and rounded rectangles
        piece.style.borderRadius = gsap.utils.random(['0%', '50%', '3px']);
        
        popperContainer.appendChild(piece);

        // Vector Physics math variables
        const angle = gsap.utils.random(0, Math.PI * 2);
        const velocity = gsap.utils.random(90, 310);
        
        // Calculate arc coordinates
        const targetX = Math.cos(angle) * velocity;
        const targetY = Math.sin(angle) * velocity - gsap.utils.random(120, 240); // Skew upwards to simulate upward popper push

        // Run hardware composite animation segments
        gsap.timeline({
            onComplete: () => piece.remove()
        })
        .to(piece, {
            x: targetX,
            y: targetY,
            rotation: "random(360, 1080)",
            rotationX: "random(180, 720)",
            rotationY: "random(180, 720)",
            scale: gsap.utils.random(0.6, 1.4),
            duration: gsap.utils.random(0.7, 1.4),
            ease: "power2.out"
        })
        // Combine soft gravity drop segment
        .to(piece, {
            y: targetY + gsap.utils.random(200, 380),
            opacity: 0,
            scale: 0.3,
            duration: gsap.utils.random(1.2, 2.0),
            ease: "power1.in",
            delay: -0.3
        });
    }

    // Clean up container cleanly
    setTimeout(() => popperContainer.remove(), 4000);
}

function setupLetterScrollAnimations() {
    const sectionElement = DOM.queryLive(CONFIG.selectors.letterSection);
    const envelopeArena = DOM.queryLive('.envelope-arena');

    if (!sectionElement || !envelopeArena) return;

    gsap.fromTo(envelopeArena,
        { opacity: 0, y: 50, scale: 0.95 },
        {
            opacity: 1,
            y: 0,
            scale: 1,
            duration: 1.4,
            ease: "power3.out",
            scrollTrigger: {
                trigger: sectionElement,
                start: "top 75%",
                once: true
            }
        }
    );
}

function openEnvelope() {
    const envelope = DOM.envelope;
    const seal = DOM.sealTrigger;
    const flap = DOM.envelopeFlap;
    const paper = DOM.letterSheet;

    if (!envelope || !seal || !flap || !paper) return;

    if (STATE.current.envelopeOpen) return;
    STATE.set('envelopeOpen', true);
    seal.setAttribute('aria-expanded', 'true');

    const openTimeline = gsap.timeline();

    // Step 1: Pop and fade the wax seal medallion and launch confetti poppers!
    openTimeline.to(seal, {
        scale: 0.7,
        opacity: 0,
        duration: 0.45,
        ease: "power2.in",
        onStart: () => {
            triggerConfettiPopper(); // Launches physical confetti burst instantly
        }
    });

    // Step 2: Unfold envelope flap
    openTimeline.to(flap, {
        rotationX: 180,
        duration: 0.85,
        ease: "power3.inOut",
        onStart: () => {
            envelope.classList.add('is-open');
        },
        onComplete: () => {
            flap.style.zIndex = '1';
            paper.style.zIndex = '10';
        }
    }, "-=0.15");

    // Step 3: Slide parchment letter up elegantly to resting anchored focal height (-52%)
    openTimeline.to(paper, {
        yPercent: -52,
        boxShadow: "0 30px 100px rgba(0, 0, 0, 0.95)",
        duration: 1.3,
        ease: "power3.inOut",
        force3D: false, // Maintain crisp vector fonts onWindows/Mac layers
        clearProps: "willChange"
    }, "+=0.1");
}

export function resetEnvelope() {
    const envelope = DOM.envelope;
    const seal = DOM.sealTrigger;
    const flap = DOM.envelopeFlap;
    const paper = DOM.letterSheet;

    if (!envelope || !seal || !flap || !paper) return;

    STATE.set('envelopeOpen', false);
    seal.setAttribute('aria-expanded', 'false');

    const resetTimeline = gsap.timeline();

    resetTimeline.to(paper, {
        yPercent: 0,
        boxShadow: "0 4px 20px rgba(0, 0, 0, 0.3)",
        duration: 0.8,
        ease: "power2.inOut",
        onComplete: () => {
            flap.style.zIndex = '5';
            paper.style.zIndex = '2';
            envelope.classList.remove('is-open');
        }
    });

    resetTimeline.to(flap, {
        rotationX: 0,
        duration: 0.6,
        ease: "power2.inOut"
    });

    resetTimeline.to(seal, {
        scale: 1,
        opacity: 1,
        duration: 0.4,
        ease: "power2.out"
    }, "-=0.1");
}

export function initLetter() {
    setupLetterScrollAnimations();
    DOM.sealTrigger?.addEventListener('click', openEnvelope, { passive: true });
}