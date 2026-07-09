import { CONFIG } from './config.js';
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
}