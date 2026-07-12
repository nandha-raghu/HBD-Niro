import { CONFIG } from '../core/config.js';
import { STATE } from '../core/state.js';
import { DOM } from '../core/dom.js';
import { ParticleEngine } from '../core/particleEngine.js';
import { playScore } from './music.js';

let loaderParticles = null;
let currentQuizStep = 0;

// The Three-Question Romantic Verification data
const QUIZ_STEPS = [
    {
        type: "intro",
        title: "Before We Begin...",
        subtitle: "Before I show you this little surprise,<br>let's see how well you know your husband. 😊",
        buttonText: "I'm Ready ❤️"
    },
    {
        type: "question",
        number: 1,
        title: "Question 1",
        question: "Who is your favourite person? 😉",
        expected: "nandha",
        placeholder: "Type your answer here...",
        buttonText: "Continue ❤️"
    },
    {
        type: "question",
        number: 2,
        title: "Question 2",
        question: "Who loves you more than anything in this world? ❤️",
        expected: "nandha",
        placeholder: "Type your answer here...",
        buttonText: "Continue ❤️"
    },
    {
        type: "question",
        number: 3,
        title: "Question 3",
        question: "Who stole your heart? 😜",
        expected: "nandha",
        placeholder: "Type your answer here...",
        buttonText: "Continue ❤️"
    },
    {
        type: "success",
        title: "Perfect!",
        prose: "You know me well...<br><br>Now it's my turn to remind you<br>how much I love you. ❤️"
    }
];

// Romantic hint library (shown randomly on incorrect answers)
const HINTS = [
    "<span style='color:#FF5F8A; font-weight:500; font-size:14px; display:block; margin-bottom:6px;'>💛</span><strong>Close...</strong><br>Try remembering one of our favourite memories.",
    "<span style='color:#FF5F8A; font-weight:500; font-size:14px; display:block; margin-bottom:6px;'>😊</span><strong>Hint:</strong><br>It's someone who loves you endlessly.",
    "<span style='color:#FF5F8A; font-weight:500; font-size:14px; display:block; margin-bottom:6px;'>❤️</span><strong>Think about us...</strong><br>You'll get it.",
    "<span style='color:#FF5F8A; font-weight:500; font-size:14px; display:block; margin-bottom:6px;'>🥰</span><strong>Almost there...</strong><br>Your heart already knows the answer.",
    "<span style='color:#FF5F8A; font-weight:500; font-size:14px; display:block; margin-bottom:6px;'>💕</span><strong>One more try...</strong><br>I'm waiting for you on the next screen."
];

/**
 * Synthesizes a warm, arpeggiated A-major high chime using Web Audio API on correct answers
 */
function playSuccessChime() {
    try {
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        if (!AudioContext) return;
        const ctx = new AudioContext();
        const now = ctx.currentTime;
        
        // Note 1: E5 (659.25 Hz)
        const osc1 = ctx.createOscillator();
        const gain1 = ctx.createGain();
        osc1.type = 'sine';
        osc1.frequency.setValueAtTime(659.25, now);
        gain1.gain.setValueAtTime(0.08, now);
        gain1.gain.exponentialRampToValueAtTime(0.001, now + 1.2);
        osc1.connect(gain1);
        gain1.connect(ctx.destination);
        
        // Note 2: A5 (880.00 Hz) - arpeggiated delay swell for luxurious feel
        const osc2 = ctx.createOscillator();
        const gain2 = ctx.createGain();
        osc2.type = 'sine';
        osc2.frequency.setValueAtTime(880.00, now + 0.08);
        gain2.gain.setValueAtTime(0.12, now + 0.08);
        gain2.gain.exponentialRampToValueAtTime(0.001, now + 1.4);
        osc2.connect(gain2);
        gain2.connect(ctx.destination);
        
        osc1.start(now);
        osc1.stop(now + 1.3);
        osc2.start(now + 0.08);
        osc2.stop(now + 1.5);
    } catch (e) {
        // Safe bypass on legacy or blocked mobile devices
    }
}

export function initPreload() {
    const canvas = DOM.queryLive('#loader-particle-canvas');
    if (DOM.loaderScreen && canvas) {
        loaderParticles = new ParticleEngine(canvas, 'loader');
    }
    
    // Launch the 3-question mini-game!
    initPasswordScreen();
}

/**
 * Compiles and renders the current step of the verification card
 */
function renderQuizStep(stepIndex, isInitial = false) {
    const cardContainer = document.querySelector('#password-card-container');
    if (!cardContainer) return;

    const data = QUIZ_STEPS[stepIndex];
    let cardContent = "";

    // 1. Compile card templates based on state type
    if (data.type === "intro") {
        cardContent = `
            <div class="password-card-inner">
                <div class="password-heart-icon">
                    <svg viewBox="0 0 24 24" width="36" height="32" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" fill="#FF5F8A" />
                    </svg>
                </div>
                <h2 class="password-title font-serif">${data.title}</h2>
                <p class="password-question font-sans" style="text-transform:none; font-size:13px; line-height:1.7;">${data.subtitle}</p>
                <button class="btn btn-luxury" id="quiz-btn">
                    <span class="btn-background-shimmer"></span>
                    <span class="btn-text">${data.buttonText}</span>
                </button>
            </div>
        `;
    } else if (data.type === "question") {
        cardContent = `
            <div class="password-card-inner">
                <div class="password-heart-icon">
                    <svg viewBox="0 0 24 24" width="36" height="32" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" fill="#FF5F8A" />
                    </svg>
                </div>
                <h2 class="password-title font-serif" style="font-size:12px; color:var(--color-gold);">${data.title}</h2>
                <p class="password-question font-sans" style="text-transform:none; font-size:16px; line-height:1.5; color:var(--color-white); font-weight:500;">${data.question}</p>
                <input type="text" id="password-input" class="password-input" placeholder="${data.placeholder}" autocomplete="off" spellcheck="false">
                <button class="btn btn-luxury" id="quiz-btn" disabled style="opacity:0.4;">
                    <span class="btn-background-shimmer"></span>
                    <span class="btn-text">${data.buttonText}</span>
                </button>
                <p class="password-error" id="quiz-error"></p>
            </div>
        `;
    } else if (data.type === "success") {
        cardContent = `
            <div class="password-card-inner">
                <div class="password-heart-icon" style="transform: scale(1.4); margin-bottom: 24px;">
                    <svg viewBox="0 0 24 24" width="36" height="32" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" fill="#FF5F8A" />
                    </svg>
                </div>
                <h2 class="password-title font-serif" style="font-size:24px; color:var(--color-gold); margin-bottom:20px;">${data.title}</h2>
                <p class="password-question font-sans" style="text-transform:none; font-size:15px; line-height:1.8; color:var(--color-white); font-weight:500;">${data.prose}</p>
            </div>
        `;
    }

    // 2. Animate transitions using high-performance GSAP scaling
    if (isInitial) {
        cardContainer.innerHTML = cardContent;
        bindQuizEvents();
        gsap.fromTo(cardContainer, { opacity: 0, scale: 0.9 }, { opacity: 1, scale: 1, duration: 1.0, ease: "power4.out" });
    } else {
        const inner = cardContainer.querySelector('.password-card-inner');
        gsap.to(inner, {
            opacity: 0,
            scale: 0.93,
            y: -15,
            duration: 0.45,
            ease: "power2.in",
            onComplete: () => {
                cardContainer.innerHTML = cardContent;
                bindQuizEvents();
                const newInner = cardContainer.querySelector('.password-card-inner');
                gsap.fromTo(newInner, 
                    { opacity: 0, scale: 0.95, y: 25 },
                    { opacity: 1, scale: 1, y: 0, duration: 0.65, ease: "power3.out" }
                );
            }
        });
    }
}

/**
 * Binds active events, text listeners, and heart cursors to the newly injected card nodes
 */
function bindQuizEvents() {
    const data = QUIZ_STEPS[currentQuizStep];
    
    // --- ROTATED CRITICAL REPAIR ---
    // If the card is in the success state, handle the triggers first
    // before the button checking returns, preventing the card from freezing!
    if (data.type === "success") {
        const overlay = document.querySelector('.password-overlay');
        
        // Play the score music instantly under user gesture!
        playScore();

        // Hold success screen for exactly 3.2s, then transition into preloader
        setTimeout(() => {
            if (overlay) {
                overlay.classList.add('is-unlocked');
            }
            if (loaderParticles) {
                loaderParticles.start();
            }
            beginPreloadingProgress();
        }, 3200);
        return; // Safe early exit for success state
    }

    const btn = document.querySelector('#quiz-btn');
    const input = document.querySelector('#password-input');
    const errorEl = document.querySelector('#quiz-error');
    const heartIcon = document.querySelector('.password-heart-icon');
    const card = document.querySelector('.password-card');

    if (!btn) return;

    // A. Focus text box automatically
    if (input) {
        setTimeout(() => input.focus(), 600);

        // B. Heart Cursor Hover Bindings
        input.addEventListener('focus', () => {
            document.querySelector('#custom-cursor')?.classList.add('cursor-heart');
        }, { passive: true });

        input.addEventListener('blur', () => {
            document.querySelector('#custom-cursor')?.classList.remove('cursor-heart');
        }, { passive: true });

        input.addEventListener('mouseenter', () => {
            document.querySelector('#custom-cursor')?.classList.add('cursor-heart');
        }, { passive: true });

        input.addEventListener('mouseleave', () => {
            if (document.activeElement !== input) {
                document.querySelector('#custom-cursor')?.classList.remove('cursor-heart');
            }
        }, { passive: true });

        // C. Character listener: Enable action button only when typing
        input.addEventListener('input', () => {
            const rawVal = input.value.trim();
            if (rawVal.length > 0) {
                btn.removeAttribute('disabled');
                btn.style.opacity = '1';
                if (errorEl) errorEl.classList.remove('is-visible');
            } else {
                btn.setAttribute('disabled', 'true');
                btn.style.opacity = '0.4';
            }
        }, { passive: true });

        // D. Enter key trigger
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && input.value.trim().length > 0) {
                processAnswer();
            }
        }, { passive: true });
    }

    const processAnswer = () => {
        if (data.type === "intro") {
            currentQuizStep++;
            renderQuizStep(currentQuizStep);
        } else if (data.type === "question") {
            const rawVal = input.value.trim().toLowerCase();
            
            if (rawVal === data.expected) {
                playSuccessChime();
                card.classList.add('success-glow');
                gsap.fromTo(heartIcon, { scale: 1 }, { scale: 1.4, duration: 0.4, yoyo: true, repeat: 1, ease: "back.out" });

                setTimeout(() => {
                    card.classList.remove('success-glow');
                    currentQuizStep++;
                    renderQuizStep(currentQuizStep);
                }, 800);
            } else {
                const randomHint = HINTS[Math.floor(Math.random() * HINTS.length)];
                if (errorEl) {
                    errorEl.innerHTML = randomHint;
                    errorEl.classList.add('is-visible');
                }
            }
        }
    };

    btn.addEventListener('click', processAnswer, { passive: true });
}

function initPasswordScreen() {
    renderQuizStep(currentQuizStep, true);
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