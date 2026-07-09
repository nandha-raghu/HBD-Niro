import { CONFIG } from '../core/config.js';
import { DOM } from '../core/dom.js';
import { FloatEngine } from '../core/floatEngine.js';

let galleryTilt = null;

/**
 * Configure staggered scroll reveals and adaptive mood lighting for the gallery
 */
function setupGalleryScrollAnimations() {
    const sectionElement = DOM.queryLive(CONFIG.selectors.gallerySection);
    const galleryGrid = DOM.queryLive('#masonry-gallery');
    const items = DOM.queryAllLive(CONFIG.selectors.galleryItems);

    if (!sectionElement || !galleryGrid || items.length === 0) return;

    // 1. Staggered fade and slide-up card entry
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

    // 2. Chromatic Mood Lighting: Adapt background gradient based on which card is hovered
    // Mapped luxury mood colors for each photo index
    const moodColors = [
        "rgba(255, 95, 138, 0.05)",  // Blush Rose-Pink for Photo 1
        "rgba(212, 175, 55, 0.045)", // Champagne Amber for Photo 2
        "rgba(112, 102, 224, 0.05)", // Nostalgic Violet for Photo 3
        "rgba(255, 122, 89, 0.04)"   // Sunset Coral for Photo 4
    ];

    const defaultSpotlight = "rgba(212, 175, 55, 0.035)"; // Base luxury gold

    items.forEach((item, index) => {
        const targetColor = moodColors[index] || defaultSpotlight;

        item.addEventListener('mouseenter', () => {
            // Smoothly morph the viewport radial spotlight color
            gsap.to(sectionElement, {
                background: `radial-gradient(ellipse at center, rgba(5, 5, 5, 0) 25%, rgba(0, 0, 0, 0.98) 100%), radial-gradient(circle at 50% 35%, ${targetColor} 0%, var(--color-bg) 70%)`,
                duration: 1.0,
                ease: "power2.out",
                overwrite: "auto"
            });
        }, { passive: true });

        item.addEventListener('mouseleave', () => {
            // Smoothly restore base luxury gold spotlight
            gsap.to(sectionElement, {
                background: `radial-gradient(ellipse at center, rgba(5, 5, 5, 0) 25%, rgba(0, 0, 0, 0.98) 100%), radial-gradient(circle at 50% 35%, ${defaultSpotlight} 0%, var(--color-bg) 70%)`,
                duration: 1.2,
                ease: "power2.inOut",
                overwrite: "auto"
            });
        }, { passive: true });
    });
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
        
        // CINEMATIC AUDIO DIM: Dim music to focus entirely on the memory
        const audio = document.querySelector('#ambient-score');
        if (audio && !audio.paused) {
            gsap.to(audio, { volume: 0.15, duration: 1.0, ease: "power1.out" });
        }

        setTimeout(() => closeBtn?.focus(), 100);
    };

    const closeLightbox = () => {
        lightbox.classList.remove('is-open');
        lightbox.setAttribute('aria-hidden', 'true');
        
        // CINEMATIC AUDIO RESTORE: Restore music back to comfort levels
        const audio = document.querySelector('#ambient-score');
        if (audio && !audio.paused) {
            gsap.to(audio, { volume: 0.5, duration: 1.2, ease: "power1.inOut" });
        }

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
}