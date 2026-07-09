export const CONFIG = Object.freeze({
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
        fakePreloadDurationMs: 8000,
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
        introHeartContainer: '#intro-heart-container',
        progressBar: '#progress-bar',
        msgStep1: '#msg-step-1',
        msgStep2: '#msg-step-2',
        
        smoothWrapper: '#smooth-wrapper',
        smoothContent: '#smooth-content',
        
        heroSection: '#hero-section',
        heroTarget: '#intro-heart-container',
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
});