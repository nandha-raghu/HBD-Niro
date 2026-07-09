import { CONFIG } from '../core/config.js';
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
}