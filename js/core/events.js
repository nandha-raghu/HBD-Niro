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