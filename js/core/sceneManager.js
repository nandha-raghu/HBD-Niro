import { CONFIG } from './config.js';
import { STATE } from './state.js';
import { getScroller } from './animationManager.js';

function initSideNavigation() {
    const navContainer = document.querySelector('.side-navigation');
    const dots = document.querySelectorAll('.nav-dot');
    if (!navContainer || dots.length === 0) return;

    STATE.subscribe('activeSection', (activeSectionId) => {
        if (activeSectionId !== 'loader') {
            navContainer.classList.add('is-visible');
        } else {
            navContainer.classList.remove('is-visible');
        }

        dots.forEach(dot => {
            const target = dot.getAttribute('data-target');
            if (target === `#${activeSectionId}-section`) {
                dot.classList.add('active');
            } else {
                dot.classList.remove('active');
            }
        });
    });

    dots.forEach(dot => {
        dot.addEventListener('click', () => {
            const targetSelector = dot.getAttribute('data-target');
            const targetElement = document.querySelector(targetSelector);
            const lenis = getScroller();

            if (lenis && targetElement) {
                lenis.scrollTo(targetElement, {
                    offset: 0,
                    duration: 1.6,
                    easing: (t) => (t === 1 ? 1 : 1 - Math.pow(2, -10 * t))
                });
            }
        }, { passive: true });
    });
}

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
    initSideNavigation();

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
}