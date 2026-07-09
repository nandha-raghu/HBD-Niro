import { CONFIG } from '../core/config.js';
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
}