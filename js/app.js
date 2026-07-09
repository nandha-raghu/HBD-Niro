import { initDOM } from './core/dom.js';
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
}