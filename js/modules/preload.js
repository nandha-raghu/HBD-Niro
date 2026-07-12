import { CONFIG } from '../core/config.js';
import { STATE } from '../core/state.js';
import { DOM } from '../core/dom.js';
import { ParticleEngine } from '../core/particleEngine.js';
import { playScore } from './music.js';

let loaderParticles = null;

export function initPreload() {
    const canvas = DOM.queryLive('#loader-particle-canvas');
    if (DOM.loaderScreen && canvas) {
        loaderParticles = new ParticleEngine(canvas, 'loader');
    }
    
    // Intercept loading progress: Initialize the lock screen validation listeners first!
    initPasswordScreen();
}

/**
 * Handle password verification and input focus bindings
 */
function initPasswordScreen() {
    const overlay = document.querySelector('.password-overlay');
    const input = document.querySelector('.password-input');
    const submitBtn = document.querySelector('#password-submit');
    const errorMsg = document.querySelector('#password-error');
    const card = document.querySelector('.password-card');

    if (!overlay || !input || !submitBtn) return;

    // Auto-focus input box for friendly UX
    setTimeout(() => input.focus(), 500);

    const checkPassword = () => {
        const rawVal = input.value.trim().toLowerCase();
        
        // Accepted answers
        if (rawVal === "niro" || rawVal === "nirosha" || rawVal === "wife") {
            // Correct answerEntered!
            overlay.classList.add('is-unlocked');
            
            // 1. Play background song instantly (Allowed because of active click gesture!)
            playScore();
            
            // 2. Start preloader canvas particles
            if (loaderParticles) {
                loaderParticles.start();
            }
            
            // 3. Initiate progressive loading thoughts bar
            beginPreloadingProgress();
        } else {
            // Incorrect answer: Trigger 3D shake animation on card using GSAP
            errorMsg.classList.add('is-visible');
            input.value = ""; // Clear box
            
            gsap.fromTo(card, 
                { x: -10 },
                { x: 10, repeat: 5, yoyo: true, duration: 0.05, onComplete: () => {
                    gsap.set(card, { x: 0 }); // Reset alignment
                }}
            );
        }
    };

    // Bind triggers
    submitBtn.addEventListener('click', checkPassword, { passive: true });
    
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            checkPassword();
        }
    }, { passive: true });
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
                titleElement.textContent = "Preparing something beautiful...";
            } else if (progressClamped < 50) {
                titleElement.textContent = "Remembering when we first met...";
            } else if (progressClamped < 75) {
                titleElement.textContent = "Gathering our favorite laughs...";
            } else if (progressClamped < 92) {
                titleElement.textContent = "Finding our beautiful moments...";
            } else {
                titleElement.textContent = "Almost ready...";
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

    const proseEl = DOM.msgStep2?.querySelector('.heartfelt-prose');
    if (DOM.msgStep2 && proseEl) {
        gsap.set(proseEl, { y: 15, opacity: 0 });
        DOM.msgStep2.classList.add('active');

        // --- CLIMAX MOVEMENT 1: The Girl ---
        fadeTimeline.to(proseEl, {
            onStart: () => {
                proseEl.innerHTML = "The Girl<br><span style='color: var(--color-gold); font-size: 0.85em; font-style: italic; display: inline-block; margin-top: 8px;'>Who Stole My Heart...</span>";
            },
            opacity: 1,
            y: 0,
            duration: 1.2,
            ease: "power3.out"
        }, "+=0.2");
        
        fadeTimeline.to(proseEl, {
            opacity: 0,
            y: -10,
            duration: 0.8,
            ease: "power2.in"
        }, "+=3.8");

        // --- CLIMAX MOVEMENT 2: The Woman ---
        fadeTimeline.to(proseEl, {
            onStart: () => {
                proseEl.innerHTML = "The Woman<br><span style='color: var(--color-gold); font-size: 0.85em; font-style: italic; display: inline-block; margin-top: 8px;'>Who Changed My Life...</span>";
            },
            opacity: 1,
            y: 0,
            duration: 1.2,
            ease: "power3.out"
        }, "+=0.2");

        fadeTimeline.to(proseEl, {
            opacity: 0,
            y: -10,
            duration: 0.8,
            ease: "power2.in"
        }, "+=3.8");

        // --- CLIMAX MOVEMENT 3: The Love ---
        fadeTimeline.to(proseEl, {
            onStart: () => {
                proseEl.innerHTML = "The Love<br><span style='color: var(--color-rose-gold); font-size: 0.85em; font-style: italic; display: inline-block; margin-top: 8px;'>I'll Choose Forever...</span>";
            },
            opacity: 1,
            y: 0,
            duration: 1.4,
            ease: "power3.out"
        }, "+=0.2");

        fadeTimeline.to(proseEl, {
            opacity: 0,
            y: -10,
            duration: 1.0,
            ease: "power2.in"
        }, "+=4.2");
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
}