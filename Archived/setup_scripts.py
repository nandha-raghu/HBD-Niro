import os

print("Preparing to write JavaScript modular system...")

files = {}

# js/core/config.js
files["js/core/config.js"] = """export const CONFIG = Object.freeze({
    debug: false,
    assets: {
        scoreUrl: 'assets/music/bg-score.mp3'
    },
    performance: {
        highRefreshTarget: 60,
        mobileParticleReduction: 0.5,
        resizeDebounceMs: 150
    },
    particles: {
        loader: {
            density: 50,
            colorGold: 'rgba(212, 175, 55, 0.65)',
            colorRoseGold: 'rgba(255, 95, 138, 0.45)',
            size: { min: 1, max: 3 },
            speed: { min: 0.3, max: 1.2 }
        },
        hero: {
            density: 80,
            colorGold: 'rgba(212, 175, 55, 0.35)',
            colorRoseGold: 'rgba(255, 95, 138, 0.25)',
            size: { min: 0.5, max: 2 },
            speed: { min: 0.1, max: 0.5 }
        },
        finale: {
            density: 100,
            colorGold: 'rgba(212, 175, 55, 0.55)',
            colorRoseGold: 'rgba(255, 95, 138, 0.45)',
            size: { min: 0.8, max: 2.5 },
            speed: { min: 0.2, max: 0.8 }
        }
    },
    preloader: {
        fakePreloadDurationMs: 4000,
        textFadeDurationSec: 1.2,
        transitionOverlapSec: 0.6
    },
    bezierFlight: {
        controlPointOffset: { x: -150, y: -250 },
        flightDurationSec: 2.5,
        flightEasing: "power4.inOut"
    },
    selectors: {
        noiseOverlay: '.noise-overlay',
        customCursor: '#custom-cursor',
        audioWidget: '#audio-widget',
        audioBtn: '#audio-toggle-btn',
        audioSource: '#ambient-score',
        
        loaderScreen: '#loader-screen',
        loaderHeart: '#intro-heart',
        loaderHeartContainer: '#intro-heart-container',
        progressBar: '#progress-bar',
        msgStep1: '#msg-step-1',
        msgStep2: '#msg-step-2',
        
        smoothWrapper: '#smooth-wrapper',
        smoothContent: '#smooth-content',
        
        heroSection: '#hero-section',
        heroTarget: '#hero-heart-target',
        heroTitle: '#hero-title',
        heroCta: '#hero-cta',
        heroScrollIndicator: '#hero-scroll-indicator',
        heroBrand: '.hero-brand-top',
        
        storySection: '#story-section',
        timelineSection: '#timeline-section',
        timelineProgress: '#timeline-progress-bar',
        timelineItems: '.timeline-item',
        
        gallerySection: '#gallery-section',
        galleryItems: '.gallery-item',
        lightbox: '#gallery-lightbox',
        lightboxImg: '#lightbox-display-img',
        lightboxCaption: '#lightbox-display-caption',
        lightboxClose: '#lightbox-close-btn',
        
        letterSection: '#letter-section',
        envelope: '#envelope',
        sealTrigger: '#seal-trigger',
        letterSheet: '#letter-sheet',
        envelopeFlap: '#envelope-flap',
        
        finaleSection: '#finale-section',
        replayBtn: '#replay-experience'
    }
});"""

# js/core/state.js
files["js/core/state.js"] = """class StateManager {
    constructor() {
        this._state = {
            isLoaded: false,
            audioPlaying: false,
            envelopeOpen: false,
            activeSection: 'loader',
            isMobile: false,
            windowWidth: 0,
            windowHeight: 0
        };
        this._listeners = new Map();
    }

    get current() {
        return Object.freeze({ ...this._state });
    }

    subscribe(key, callback) {
        if (!this._listeners.has(key)) {
            this._listeners.set(key, []);
        }
        this._listeners.get(key).push(callback);
    }

    set(key, newValue) {
        if (!(key in this._state)) {
            console.warn(`StateManager: Attempted to set unregistered state property: "${key}"`);
            return;
        }

        if (this._state[key] === newValue) return;

        const oldValue = this._state[key];
        this._state[key] = newValue;

        const subscribers = this._listeners.get(key);
        if (subscribers) {
            subscribers.forEach(callback => {
                try {
                    callback(newValue, oldValue);
                } catch (error) {
                    console.error(`StateManager: Error during subscriber execution for key "${key}":`, error);
                }
            });
        }

        window.dispatchEvent(new CustomEvent(`state:${key}`, {
            detail: { property: key, current: newValue, previous: oldValue }
        }));
    }
}

export const STATE = new StateManager();"""

# js/core/dom.js
files["js/core/dom.js"] = """import { CONFIG } from './config.js';

export const DOM = {};

export function initDOM() {
    let missingElementsCount = 0;

    for (const [key, selector] of Object.entries(CONFIG.selectors)) {
        try {
            const element = document.querySelector(selector);
            
            if (element) {
                DOM[key] = element;
            } else {
                DOM[key] = null;
                missingElementsCount++;
            }
        } catch (error) {
            console.error(`DOM Cache: Exception during query initialization for "${key}" ("${selector}"):`, error);
            DOM[key] = null;
        }
    }
}

export function queryLive(selector) {
    try {
        return document.querySelector(selector);
    } catch (e) {
        return null;
    }
}

export function queryAllLive(selector) {
    try {
        return document.querySelectorAll(selector);
    } catch (e) {
        return document.createDocumentFragment().childNodes;
    }
}

export function recacheItem(key) {
    const selector = CONFIG.selectors[key];
    if (selector) {
        DOM[key] = document.querySelector(selector);
    }
}"""

# js/core/events.js
files["js/core/events.js"] = """import { CONFIG } from './config.js';
import { STATE } from './state.js';

const pointerCoords = { x: 0, y: 0, targetX: 0, targetY: 0 };

export function debounce(func, delay) {
    let timeoutId;
    return function (...args) {
        const context = this;
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => {
            func.apply(context, args);
        }, delay);
    };
}

function recordViewportDimensions() {
    const width = window.innerWidth;
    const height = window.innerHeight;
    const isMobile = width <= 768;

    STATE.set('windowWidth', width);
    STATE.set('windowHeight', height);
    STATE.set('isMobile', isMobile);
}

function handlePointerMovement(event) {
    let rawX, rawY;

    if (event.touches && event.touches.length > 0) {
        rawX = event.touches[0].clientX;
        rawY = event.touches[0].clientY;
    } else {
        rawX = event.clientX;
        rawY = event.clientY;
    }

    pointerCoords.targetX = rawX;
    pointerCoords.targetY = rawY;

    window.dispatchEvent(new CustomEvent('pointer:move', {
        detail: { x: rawX, y: rawY }
    }));
}

export function initEvents() {
    recordViewportDimensions();

    window.addEventListener('resize', debounce(() => {
        recordViewportDimensions();
    }, CONFIG.performance.resizeDebounceMs), { passive: true });

    if (window.matchMedia('(pointer: fine)').matches) {
        window.addEventListener('mousemove', handlePointerMovement, { passive: true });
    } else {
        window.addEventListener('touchmove', handlePointerMovement, { passive: true });
    }

    document.addEventListener('mouseover', (e) => {
        const target = e.target.closest('a, button, [role="button"], .gallery-item, .wax-seal-btn');
        if (target) {
            window.dispatchEvent(new CustomEvent('pointer:enter-interactive'));
        }
    }, { passive: true });

    document.addEventListener('mouseout', (e) => {
        const target = e.target.closest('a, button, [role="button"], .gallery-item, .wax-seal-btn');
        if (target) {
            window.dispatchEvent(new CustomEvent('pointer:leave-interactive'));
        }
    }, { passive: true });
}

export function getPointerPosition() {
    return pointerCoords;
}"""

# js/core/utils.js
files["js/core/utils.js"] = """export function lerp(start, end, amt) {
    return (1 - amt) * start + amt * end;
}

export function clamp(val, min, max) {
    return Math.min(Math.max(val, min), max);
}

export function mapRange(value, inMin, inMax, outMin, outMax) {
    return ((value - inMin) * (outMax - outMin)) / (inMax - inMin) + outMin;
}

export function getElementCenterCoordinates(element) {
    if (!element) return { x: 0, y: 0 };

    const rect = element.getBoundingClientRect();
    const scrollX = window.scrollX || window.pageXOffset;
    const scrollY = window.scrollY || window.pageYOffset;

    return {
        x: rect.left + rect.width / 2 + scrollX,
        y: rect.top + rect.height / 2 + scrollY
    };
}

export function getQuadraticBezierPoint(p0, p1, p2, t) {
    const term1_coefficient = (1 - t) ** 2;
    const term2_coefficient = 2 * (1 - t) * t;
    const term3_coefficient = t ** 2;

    return {
        x: term1_coefficient * p0.x + term2_coefficient * p1.x + term3_coefficient * p2.x,
        y: term1_coefficient * p0.y + term2_coefficient * p1.y + term3_coefficient * p2.y
    };
}"""

# js/core/animationManager.js
files["js/core/animationManager.js"] = """import { STATE } from './state.js';
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
            dotElement.style.transform = `translate3d(${cursorInterp.dotX}px, ${cursorInterp.dotY}px, 0)`;
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
}"""

# js/core/particleEngine.js
files["js/core/particleEngine.js"] = """import { CONFIG } from './config.js';
import { STATE } from './state.js';

class ParticleInstance {
    constructor(width, height, settings) {
        this.canvasWidth = width;
        this.canvasHeight = height;
        this.settings = settings;

        this.reset();
        this.y = Math.random() * this.canvasHeight;
    }

    reset() {
        this.x = Math.random() * this.canvasWidth;
        this.y = this.canvasHeight + Math.random() * 20;
        
        this.size = Math.random() * (this.settings.size.max - this.settings.size.min) + this.settings.size.min;
        this.speedY = Math.random() * (this.settings.speed.max - this.settings.speed.min) + this.settings.speed.min;
        
        this.swaySpeed = Math.random() * 0.02 + 0.005;
        this.swayAmount = Math.random() * 1.5 + 0.5;
        this.swayAngle = Math.random() * Math.PI * 2;

        this.alpha = Math.random() * 0.4 + 0.1;
        this.color = Math.random() > 0.45 ? this.settings.colorGold : this.settings.colorRoseGold;
    }

    update() {
        this.y -= this.speedY;
        
        this.swayAngle += this.swaySpeed;
        this.x += Math.sin(this.swayAngle) * (this.swayAmount * 0.1);
        this.alpha = Math.sin(this.swayAngle) * 0.15 + 0.4;

        if (this.y < -10 || this.x < -10 || this.x > this.canvasWidth + 10) {
            this.reset();
        }
    }

    draw(ctx) {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fillStyle = this.color.replace(')', `, ${this.alpha})`).replace('rgb', 'rgba');
        ctx.fill();
    }
}

export class ParticleEngine {
    constructor(canvasElement, configKey) {
        this.canvas = canvasElement;
        if (!this.canvas) return;

        this.ctx = this.canvas.getContext('2d');
        this.settings = CONFIG.particles[configKey];
        this.particles = [];
        this.isRunning = false;
        this.rafId = null;

        this.init();
    }

    init() {
        this.resize();
        this.populate();

        window.addEventListener('state:windowWidth', () => this.resize());
    }

    resize() {
        if (!this.canvas) return;

        this.width = this.canvas.clientWidth;
        this.height = this.canvas.clientHeight;

        const scale = window.devicePixelRatio || 1;
        this.canvas.width = this.width * scale;
        this.canvas.height = this.height * scale;
        this.ctx.scale(scale, scale);

        this.particles.forEach(p => {
            p.canvasWidth = this.width;
            p.canvasHeight = this.height;
        });
    }

    populate() {
        this.particles = [];
        let count = this.settings.density;

        if (STATE.current.isMobile) {
            count = Math.floor(count * CONFIG.performance.mobileParticleReduction);
        }

        for (let i = 0; i < count; i++) {
            this.particles.push(new ParticleInstance(this.width, this.height, this.settings));
        }
    }

    start() {
        if (this.isRunning) return;
        this.isRunning = true;
        this.tick();
    }

    stop() {
        this.isRunning = false;
        if (this.rafId) {
            cancelAnimationFrame(this.rafId);
            this.rafId = null;
        }
    }

    tick() {
        if (!this.isRunning) return;

        this.ctx.clearRect(0, 0, this.width, this.height);

        this.particles.forEach(p => {
            p.update();
            p.draw(this.ctx);
        });

        this.rafId = requestAnimationFrame(() => this.tick());
    }
}"""

# js/core/floatEngine.js
files["js/core/floatEngine.js"] = """export class FloatEngine {
    constructor(selector, maxTilt = 8) {
        this.targets = document.querySelectorAll(selector);
        this.maxTilt = maxTilt;
        
        if (this.targets.length > 0) {
            this.init();
        }
    }

    init() {
        this.targets.forEach(element => {
            element.addEventListener('mousemove', (e) => this.handleMouseMove(e, element), { passive: true });
            element.addEventListener('mouseleave', () => this.handleMouseLeave(element), { passive: true });
            element.addEventListener('mouseenter', () => this.handleMouseEnter(element), { passive: true });
        });
    }

    handleMouseMove(e, element) {
        const rect = element.getBoundingClientRect();
        
        const mouseX = e.clientX - rect.left;
        const mouseY = e.clientY - rect.top;

        const percentX = (mouseX / rect.width) - 0.5;
        const percentY = (mouseY / rect.height) - 0.5;

        const rotateY = percentX * this.maxTilt;
        const rotateX = -percentY * this.maxTilt;

        const percentageX = (mouseX / rect.width) * 100;
        const percentageY = (mouseY / rect.height) * 100;
        element.style.setProperty('--mouse-x', `${percentageX}%`);
        element.style.setProperty('--mouse-y', `${percentageY}%`);

        gsap.to(element, {
            rotationX: rotateX,
            rotationY: rotateY,
            z: 15,
            transformPerspective: 1000,
            duration: 0.6,
            ease: "power2.out",
            overwrite: "auto"
        });
    }

    handleMouseLeave(element) {
        gsap.to(element, {
            rotationX: 0,
            rotationY: 0,
            z: 0,
            duration: 0.8,
            ease: "power3.out",
            overwrite: "auto"
        });
    }

    handleMouseEnter(element) {
        gsap.to(element, {
            z: 8,
            duration: 0.4,
            ease: "power2.out"
        });
    }
}"""

# js/core/sceneManager.js
files["js/core/sceneManager.js"] = """import { CONFIG } from './config.js';
import { STATE } from './state.js';

function registerSectionObservers() {
    const sectionIds = ['hero', 'story', 'timeline', 'gallery', 'letter', 'finale'];

    sectionIds.forEach(id => {
        const selector = CONFIG.selectors[`${id}Section`];
        const element = document.querySelector(selector);

        if (!element) return;

        ScrollTrigger.create({
            trigger: element,
            start: 'top 60%',
            end: 'bottom 40%',
            onEnter: () => handleSectionIntersection(id, 'forward'),
            onEnterBack: () => handleSectionIntersection(id, 'backward')
        });
    });
}

function handleSectionIntersection(sectionId, direction) {
    STATE.set('activeSection', sectionId);

    window.dispatchEvent(new CustomEvent('scene:intersection', {
        detail: { activeSection: sectionId, direction: direction }
    }));
}

export function initSceneManager() {
    registerSectionObservers();

    window.addEventListener('scene:intersection', (e) => {
        const { activeSection } = e.detail;

        if (activeSection === 'hero') {
            window.dispatchEvent(new CustomEvent('canvas:hero:play'));
            window.dispatchEvent(new CustomEvent('canvas:finale:pause'));
        } else if (activeSection === 'finale') {
            window.dispatchEvent(new CustomEvent('canvas:hero:pause'));
            window.dispatchEvent(new CustomEvent('canvas:finale:play'));
        } else {
            window.dispatchEvent(new CustomEvent('canvas:hero:pause'));
            window.dispatchEvent(new CustomEvent('canvas:finale:pause'));
        }
    });
}"""

# js/modules/preload.js
files["js/modules/preload.js"] = """import { CONFIG } from '../core/config.js';
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

    const progressTimer = setInterval(() => {
        currentProgress += progressIncrement;
        const progressClamped = Math.min(100, currentProgress);

        if (DOM.progressBar) {
            DOM.progressBar.style.transform = `scaleX(${progressClamped / 100})`;
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
        }, "+=2.0");
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

# js/modules/intro.js
files["js/modules/intro.js"] = """import { CONFIG } from '../core/config.js';
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
    originCoords = getElementCenterCoordinates(DOM.introHeartContainer);
    destinationCoords = getElementCenterCoordinates(DOM.heroTarget);
    controlCoords = {
        x: (originCoords.x + destinationCoords.x) / 2 + CONFIG.bezierFlight.controlPointOffset.x,
        y: Math.min(originCoords.y, destinationCoords.y) + CONFIG.bezierFlight.controlPointOffset.y
    };
}

function beginCinematicFlight() {
    recalculateFlightCoordinates();

    const heartEl = DOM.introHeartContainer;
    if (!heartEl) return;

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

            const offsetX = currentPos.x - (heartEl.offsetWidth / 2);
            const offsetY = currentPos.y - (heartEl.offsetHeight / 2);

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
        DOM.heroTarget.appendChild(heartElement);

        heartElement.style.position = 'relative';
        heartElement.style.top = 'auto';
        heartElement.style.left = 'auto';
        heartElement.style.transform = 'translate3d(0, 0, 0)';
        heartElement.style.zIndex = '1';

        DOM.heroTarget.classList.add('has-landed');
        
        gsap.fromTo(heartElement, 
            { scale: 0.8 }, 
            { scale: 1, duration: 0.6, ease: "elastic.out(1, 0.3)" }
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

# js/modules/hero.js
files["js/modules/hero.js"] = """import { CONFIG } from '../core/config.js';
import { STATE } from '../core/state.js';
import { DOM } from '../core/dom.js';
import { ParticleEngine } from '../core/particleEngine.js';
import { getScroller } from '../core/animationManager.js';
import { playScore } from './music.js';

let heroParticles = null;

export function revealHero() {
    const revealTimeline = gsap.timeline();

    STATE.set('isLoaded', true);

    if (DOM.heroBrand) {
        DOM.heroBrand.classList.add('is-visible');
    }

    if (DOM.heroTitle) {
        const splitText = new SplitType(DOM.heroTitle, { types: 'lines, words, chars' });
        DOM.heroTitle.classList.add('js-split-initialized');

        revealTimeline.from(splitText.chars, {
            y: "100%",
            opacity: 0,
            duration: 1.4,
            stagger: 0.02,
            ease: "power4.out"
        }, 0.2);
    }

    if (DOM.heroCta) {
        revealTimeline.to(DOM.heroCta, {
            onStart: () => {
                DOM.heroCta.classList.add('is-visible');
            },
            opacity: 1,
            y: 0,
            duration: 1.2,
            ease: "power3.out"
        }, "-=0.6");
    }

    if (DOM.heroScrollIndicator) {
        revealTimeline.to(DOM.heroScrollIndicator, {
            onStart: () => {
                DOM.heroScrollIndicator.classList.add('is-visible');
            },
            opacity: 0.6,
            duration: 1.0,
            ease: "power2.out"
        }, "-=0.4");
    }

    if (DOM.audioWidget) {
        DOM.audioWidget.classList.add('is-visible');
    }
}

export function initHero() {
    const canvasElement = DOM.queryLive('#hero-particle-canvas');
    if (canvasElement) {
        heroParticles = new ParticleEngine(canvasElement, 'hero');
        heroParticles.start();
    }

    window.addEventListener('canvas:hero:play', () => {
        if (heroParticles) heroParticles.start();
    });

    window.addEventListener('canvas:hero:pause', () => {
        if (heroParticles) heroParticles.stop();
    });

    const actionBtn = DOM.queryLive('#hero-action-btn');
    if (actionBtn) {
        actionBtn.addEventListener('click', () => {
            const lenis = getScroller();
            const storyEl = DOM.queryLive(CONFIG.selectors.storySection);
            if (lenis && storyEl) {
                lenis.scrollTo(storyEl, {
                    offset: 0,
                    duration: 1.6,
                    easing: (t) => (t === 1 ? 1 : 1 - Math.pow(2, -10 * t))
                });
            }
            playScore();
        });
    }
}"""

# js/modules/story.js
files["js/modules/story.js"] = """import { CONFIG } from '../core/config.js';
import { DOM } from '../core/dom.js';
import { FloatEngine } from '../core/floatEngine.js';

let storyTilt = null;

function setupStoryScrollAnimations() {
    const sectionElement = DOM.queryLive(CONFIG.selectors.storySection);
    if (!sectionElement) return;

    const badge = sectionElement.querySelector('.section-badge');
    const title = sectionElement.querySelector('.section-title');
    const paragraphs = sectionElement.querySelectorAll('.story-paragraph');
    const quote = sectionElement.querySelector('.luxury-quote');
    const mediaFrame = sectionElement.querySelector('.media-frame-wrapper');
    const image = sectionElement.querySelector('.media-frame-inner img');

    const revealTimeline = gsap.timeline({
        scrollTrigger: {
            trigger: sectionElement,
            start: "top 75%",
            once: true
        }
    });

    if (badge) {
        revealTimeline.fromTo(badge, 
            { opacity: 0, y: 15 },
            { opacity: 1, y: 0, duration: 1.0, ease: "power3.out" }
        );
    }

    if (title) {
        const split = new SplitType(title, { types: 'lines, words, chars' });
        title.classList.add('js-split-initialized');

        revealTimeline.from(split.chars, {
            y: "110%",
            opacity: 0,
            duration: 1.2,
            stagger: 0.015,
            ease: "power4.out"
        }, "-=0.8");
    }

    const textElements = [...paragraphs];
    if (quote) textElements.push(quote);

    if (textElements.length > 0) {
        revealTimeline.fromTo(textElements,
            { opacity: 0, y: 20 },
            { opacity: 1, y: 0, duration: 1.0, stagger: 0.15, ease: "power3.out" },
            "-=0.8"
        );
    }

    if (mediaFrame) {
        revealTimeline.fromTo(mediaFrame,
            { opacity: 0, scale: 0.95, y: 40 },
            { 
                opacity: 1, 
                scale: 1, 
                y: 0, 
                duration: 1.4, 
                ease: "power3.out",
                onComplete: () => {
                    if (image) image.classList.add('loaded');
                }
            },
            "-=1.0"
        );

        gsap.to(mediaFrame, {
            y: -50,
            ease: "none",
            scrollTrigger: {
                trigger: sectionElement,
                start: "top bottom",
                end: "bottom top",
                scrub: true
            }
        });
    }
}

export function initStory() {
    setupStoryScrollAnimations();
    storyTilt = new FloatEngine('.media-frame-wrapper', 10);
}"""

# js/modules/timeline.js
files["js/modules/timeline.js"] = """import { CONFIG } from '../core/config.js';
import { DOM } from '../core/dom.js';
import { FloatEngine } from '../core/floatEngine.js';

let timelineTilt = null;

function setupTimelineAnimations() {
    const sectionElement = DOM.queryLive(CONFIG.selectors.timelineSection);
    const trackWrapper = DOM.queryLive('.timeline-track-wrapper');
    const progressBar = DOM.queryLive(CONFIG.selectors.timelineProgress);
    const items = DOM.queryAllLive(CONFIG.selectors.timelineItems);

    if (!sectionElement || !trackWrapper) return;

    if (progressBar) {
        gsap.to(progressBar, {
            scaleY: 1,
            ease: "none",
            scrollTrigger: {
                trigger: trackWrapper,
                start: "top 35%",
                end: "bottom 65%",
                scrub: true
            }
        });
    }

    items.forEach(item => {
        const card = item.querySelector('.timeline-card');
        const image = item.querySelector('.card-media img');
        const isRightAligned = item.classList.contains('timeline-right');
        const slideOffset = isRightAligned ? 50 : -50;

        const cardTimeline = gsap.timeline({
            scrollTrigger: {
                trigger: item,
                start: "top 80%",
                once: true
            }
        });

        if (card) {
            cardTimeline.fromTo(card,
                { opacity: 0, x: slideOffset, y: 15 },
                { 
                    opacity: 1, 
                    x: 0, 
                    y: 0, 
                    duration: 1.2, 
                    ease: "power3.out",
                    onComplete: () => {
                        if (image) image.classList.add('loaded');
                    }
                }
            );
        }

        ScrollTrigger.create({
            trigger: item,
            start: "top 55%",
            end: "bottom 45%",
            onEnter: () => item.classList.add('is-active'),
            onEnterBack: () => item.classList.add('is-active'),
            onLeave: () => item.classList.remove('is-active'),
            onLeaveBack: () => item.classList.remove('is-active')
        });
    });
}

export function initTimeline() {
    setupTimelineAnimations();
    timelineTilt = new FloatEngine('.timeline-card', 6);
}"""

# js/modules/gallery.js
files["js/modules/gallery.js"] = """import { CONFIG } from '../core/config.js';
import { DOM } from '../core/dom.js';
import { FloatEngine } from '../core/floatEngine.js';

let galleryTilt = null;

function setupGalleryScrollAnimations() {
    const sectionElement = DOM.queryLive(CONFIG.selectors.gallerySection);
    const galleryGrid = DOM.queryLive('#masonry-gallery');
    const items = DOM.queryAllLive(CONFIG.selectors.galleryItems);

    if (!sectionElement || !galleryGrid || items.length === 0) return;

    gsap.fromTo(items,
        { opacity: 0, y: 30 },
        {
            opacity: 1,
            y: 0,
            duration: 1.2,
            stagger: 0.12,
            ease: "power3.out",
            scrollTrigger: {
                trigger: galleryGrid,
                start: "top 80%",
                once: true
            },
            onComplete: () => {
                items.forEach(item => {
                    const img = item.querySelector('.gallery-img');
                    if (img) img.classList.add('loaded');
                });
            }
        }
    );
}

function initLightboxController() {
    const lightbox = DOM.lightbox;
    const lightboxImg = DOM.lightboxImg;
    const lightboxCaption = DOM.lightboxCaption;
    const closeBtn = DOM.lightboxClose;
    const items = DOM.queryAllLive(CONFIG.selectors.galleryItems);

    if (!lightbox || !lightboxImg || !lightboxCaption || items.length === 0) return;

    const openLightbox = (element) => {
        const img = element.querySelector('.gallery-img');
        const titleText = element.querySelector('.gallery-item-title')?.textContent || '';
        const categoryText = element.querySelector('.gallery-item-category')?.textContent || '';

        if (!img) return;

        lightboxImg.src = img.src;
        lightboxCaption.textContent = `${titleText} — ${categoryText}`;

        lightbox.classList.add('is-open');
        lightbox.setAttribute('aria-hidden', 'false');

        setTimeout(() => closeBtn?.focus(), 100);
    };

    const closeLightbox = () => {
        lightbox.classList.remove('is-open');
        lightbox.setAttribute('aria-hidden', 'true');
        
        setTimeout(() => {
            lightboxImg.src = '';
            lightboxCaption.textContent = '';
        }, 600);
    };

    items.forEach(item => {
        item.addEventListener('click', () => openLightbox(item), { passive: true });
    });

    closeBtn?.addEventListener('click', closeLightbox, { passive: true });

    lightbox.addEventListener('click', (e) => {
        if (e.target === lightbox) {
            closeLightbox();
        }
    }, { passive: true });

    window.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && lightbox.classList.contains('is-open')) {
            closeLightbox();
        }
    }, { passive: true });
}

export function initGallery() {
    setupGalleryScrollAnimations();
    initLightboxController();
    galleryTilt = new FloatEngine('.gallery-card-inner', 8);
}"""

# js/modules/letter.js
files["js/modules/letter.js"] = """import { CONFIG } from '../core/config.js';
import { STATE } from '../core/state.js';
import { DOM } from '../core/dom.js';

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

    openTimeline.to(seal, {
        scale: 0.8,
        opacity: 0,
        duration: 0.4,
        ease: "power2.in"
    });

    openTimeline.to(flap, {
        rotationX: 180,
        duration: 0.8,
        ease: "power3.inOut",
        onStart: () => {
            envelope.classList.add('is-open');
        },
        onComplete: () => {
            flap.style.zIndex = '1';
            paper.style.zIndex = '10';
        }
    }, "-=0.1");

    openTimeline.to(paper, {
        yPercent: -80,
        boxShadow: "0 30px 80px rgba(0, 0, 0, 0.85)",
        duration: 1.3,
        ease: "power3.inOut"
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
}"""

# js/modules/finale.js
files["js/modules/finale.js"] = """import { CONFIG } from '../core/config.js';
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
}"""

# js/modules/music.js
files["js/modules/music.js"] = """import { CONFIG } from '../core/config.js';
import { STATE } from '../core/state.js';
import { DOM } from '../core/dom.js';

const TARGET_VOLUME = 0.5;
let playPromise = null;

function syncWidgetVisuals(isPlaying) {
    const widget = DOM.audioWidget;
    const btnText = DOM.audioBtn?.querySelector('.btn-text');

    if (!widget) return;

    if (isPlaying) {
        widget.classList.add('is-playing');
        if (btnText) btnText.textContent = "MUTE SYSTEM SCORE";
        DOM.audioBtn?.setAttribute('aria-label', 'Mute musical score');
    } else {
        widget.classList.remove('is-playing');
        if (btnText) btnText.textContent = "PLAY SYSTEM SCORE";
        DOM.audioBtn?.setAttribute('aria-label', 'Play musical score');
    }
}

export function playScore() {
    const audio = DOM.audioSource;
    if (!audio) return;

    if (STATE.current.audioPlaying) return;

    audio.volume = 0;
    playPromise = audio.play();

    if (playPromise !== undefined) {
        playPromise.then(() => {
            STATE.set('audioPlaying', true);
            
            gsap.to(audio, {
                volume: TARGET_VOLUME,
                duration: 2.0,
                ease: "power2.out"
            });
        }).catch(error => {
            console.warn("Audio Autoplay Policy blocks gestureless playback.", error);
            STATE.set('audioPlaying', false);
        });
    }
}

export function pauseScore() {
    const audio = DOM.audioSource;
    if (!audio || !STATE.current.audioPlaying) return;

    gsap.to(audio, {
        volume: 0,
        duration: 1.5,
        ease: "power2.in",
        onComplete: () => {
            audio.pause();
            STATE.set('audioPlaying', false);
        }
    });
}

function handleToggleClick() {
    if (STATE.current.audioPlaying) {
        pauseScore();
    } else {
        playScore();
    }
}

export function initMusic() {
    const toggleBtn = DOM.audioBtn;

    if (!toggleBtn) return;

    STATE.subscribe('audioPlaying', syncWidgetVisuals);
    toggleBtn.addEventListener('click', handleToggleClick, { passive: true });
}"""

# js/app.js
files["js/app.js"] = """import { initDOM } from './core/dom.js';
import { initEvents } from './core/events.js';
import { initAnimationManager, scrollToTop } from './core/animationManager.js';
import { initSceneManager } from './core/sceneManager.js';

import { initPreload } from './modules/preload.js';
import { initIntro } from './modules/intro.js';
import { initHero } from './modules/hero.js';
import { initStory } from './modules/story.js';
import { initTimeline } from './modules/timeline.js';
import { initGallery } from './modules/gallery.js';
import { initLetter } from './modules/letter.js';
import { initFinale } from './modules/finale.js';
import { initMusic } from './modules/music.js';

function initializeApplication() {
    try {
        scrollToTop(true);
        gsap.registerPlugin(ScrollTrigger);

        initDOM();
        initEvents();
        initAnimationManager();
        initSceneManager();

        initIntro();
        initHero();
        initStory();
        initTimeline();
        initGallery();
        initLetter();
        initFinale();
        initMusic();

        initPreload();

    } catch (criticalError) {
        console.error("Application Boot Failure:", criticalError);
    }
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeApplication);
} else {
    initializeApplication();
}"""

print("\\nWriting files to disk...")
for filepath, content in files.items():
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"Generated file: {filepath}")

# Clean up setup scripts to keep the directory pristine
try:
    if os.path.exists("setup_styles.py"):
        os.remove("setup_styles.py")
        print("\\nPurged setup_styles.py template.")
except Exception as e:
    pass

print("\\nSetup part 2 (Scripts) completed successfully. Your workspace is fully set up.")