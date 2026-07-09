import { CONFIG } from '../core/config.js';
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
}