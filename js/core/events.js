import { CONFIG } from './config.js';
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

function spawnFloatingHeart(x, y) {
    const heart = document.createElement('div');
    heart.style.position = 'fixed';
    heart.style.left = `${x}px`;
    heart.style.top = `${y}px`;
    heart.style.width = '20px';
    heart.style.height = '18px';
    heart.style.pointerEvents = 'none';
    heart.style.zIndex = '999999';
    heart.style.transform = 'translate(-50%, -50%)';
    
    heart.innerHTML = `
        <svg viewBox="0 0 24 24" width="100%" height="100%">
            <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" fill="#FF5F8A" opacity="0.75" />
        </svg>
    `;
    document.body.appendChild(heart);
    
    gsap.to(heart, {
        y: -130,
        x: 'random(-45, 45)',
        rotation: 'random(-40, 40)',
        scale: 'random(0.9, 1.6)',
        opacity: 0,
        duration: gsap.utils.random(1.2, 1.8),
        ease: "power2.out",
        onComplete: () => heart.remove()
    });
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
    window.addEventListener('click', (e) => {
        if (e.target.closest('.lightbox-close, #lightbox-display-img')) return;
        spawnFloatingHeart(e.clientX, e.clientY);
    }, { passive: true });

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
        if (!e.target || typeof e.target.closest !== 'function') return;
        const target = e.target.closest('a, button, [role="button"], .gallery-item, .wax-seal-btn');
        if (target) {
            window.dispatchEvent(new CustomEvent('pointer:enter-interactive'));
        }
    }, { passive: true });

    document.addEventListener('mouseout', (e) => {
        if (!e.target || typeof e.target.closest !== 'function') return;
        const target = e.target.closest('a, button, [role="button"], .gallery-item, .wax-seal-btn');
        if (target) {
            window.dispatchEvent(new CustomEvent('pointer:leave-interactive'));
        }
    }, { passive: true });
}

export function getPointerPosition() {
    return pointerCoords;
}