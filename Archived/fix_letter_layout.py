import os
import re

print("Applying premium layout repairs and seamless cinematic transitions...")

# 1. Update index.html: Refactor to clean, single-heart DOM and remove redundant definitions
html_path = "index.html"
if os.path.exists(html_path):
    # Complete pristine clean rewrite of index.html with single-heart correct structure
    clean_html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Project Lumière v2.0 — An immersive, high-end cinematic interactive journey celebrating a beautiful milestone.">
    <meta name="theme-color" content="#050505">
    <title>Project Lumière v2.0</title>

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">

    <!-- CSS Layered Stylesheet Architecture -->
    <link rel="stylesheet" href="css/base/variables.css">
    <link rel="stylesheet" href="css/base/reset.css">
    <link rel="stylesheet" href="css/base/typography.css">
    <link rel="stylesheet" href="css/layout/layout.css">
    <link rel="stylesheet" href="css/layout/grid.css">
    <link rel="stylesheet" href="css/components/buttons.css">
    <link rel="stylesheet" href="css/components/glass.css">
    <link rel="stylesheet" href="css/components/particles.css">
    <link rel="stylesheet" href="css/components/cards.css">
    <link rel="stylesheet" href="css/sections/loader.css">
    <link rel="stylesheet" href="css/sections/hero.css">
    <link rel="stylesheet" href="css/sections/story.css">
    <link rel="stylesheet" href="css/sections/timeline.css">
    <link rel="stylesheet" href="css/sections/gallery.css">
    <link rel="stylesheet" href="css/sections/letter.css">
    <link rel="stylesheet" href="css/sections/finale.css">
    <link rel="stylesheet" href="css/utilities/animations.css">
    <link rel="stylesheet" href="css/utilities/responsive.css">

    <!-- External Essential Scripts -->
    <script src="https://unpkg.com/lenis@1.1.13/dist/lenis.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
    <script src="https://unpkg.com/split-type"></script>
</head>
<body>

    <div class="noise-overlay" aria-hidden="true"></div>

    <div class="custom-cursor" id="custom-cursor" aria-hidden="true">
        <div class="cursor-dot"></div>
        <div class="cursor-ring"></div>
    </div>

    <div class="audio-widget-container" id="audio-widget" aria-label="Audio Controls" role="region">
        <button class="audio-btn" id="audio-toggle-btn" aria-label="Toggle musical score">
            <span class="music-bars" aria-hidden="true">
                <span class="bar"></span>
                <span class="bar"></span>
                <span class="bar"></span>
                <span class="bar"></span>
            </span>
            <span class="btn-text">Play Our Song ❤️</span>
        </button>
        <audio id="ambient-score" loop preload="auto">
            <source src="assets/music/bg-score.mp3" type="audio/mpeg">
        </audio>
    </div>

    <!-- PRELOADER SCREEN (No heart element here, keeps rendering light and fast) -->
    <section class="loader-overlay" id="loader-screen" role="dialog" aria-modal="true" aria-label="Experience Preloader">
        <canvas class="loader-particles" id="loader-particle-canvas"></canvas>
        
        <div class="loader-content">
            <div class="loader-text-sequence" id="loader-sequence">
                <div class="loader-message active" id="msg-step-1">
                    <span class="sub-label">A Gift From My Heart</span>
                    <h2 class="loader-title">Preparing Something Beautiful...</h2>
                    <div class="gold-progress-line"><span class="progress-fill" id="progress-bar"></span></div>
                </div>
                <div class="loader-message" id="msg-step-2">
                    <p class="heartfelt-prose font-serif">Happy Birthday Nirosha ❤️</p>
                </div>
            </div>
        </div>
    </section>

    <main id="smooth-wrapper">
        <div id="smooth-content">

            <!-- HERO SECTION -->
            <section class="section hero-viewport" id="hero-section" aria-label="Hero Scene">
                <div class="ambient-glow" id="hero-glow" aria-hidden="true"></div>
                <canvas class="ambient-particles" id="hero-particle-canvas"></canvas>

                <div class="container hero-container">
                    <div class="hero-brand-top">
                        <span class="brand-line">Every Memory With You Is My Favourite Story</span>
                    </div>

                    <!-- THE SINGLE UNIFIED CINEMATIC HEART (Belongs here natively!) -->
                    <div class="hero-heart-destination is-loader-state" id="intro-heart-container">
                        <svg class="interactive-heart" id="intro-heart" viewBox="0 0 100 90" xmlns="http://www.w3.org/2000/svg">
                            <defs>
                                <linearGradient id="gold-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                                    <stop offset="0%" stop-color="#FF5F8A" />
                                    <stop offset="50%" stop-color="#D4AF37" />
                                    <stop offset="100%" stop-color="#FF5F8A" />
                                </linearGradient>
                                <filter id="luxury-glow" x="-20%" y="-20%" width="140%" height="140%">
                                    <feGaussianBlur stdDeviation="6" result="blur" />
                                    <feComposite in="SourceGraphic" in2="blur" operator="over" />
                                </filter>
                            </defs>
                            <path d="M12 4.435C2.106-2.19 0 7.435 0 14.331c0 14.168 15.698 28.536 34.024 43.19C42.863 64.636 47 68.3 50 71c3-2.7 7.137-6.364 15.976-13.479C84.302 42.867 100 28.499 100 14.331c0-6.896-2.106-16.521-12-10.096C76.2 11.83 60.1 19.333 50 22.408 39.9 19.333 23.8 11.83 12 4.435z" fill="url(#gold-gradient)" filter="url(#luxury-glow)" />
                        </svg>
                    </div>

                    <div class="hero-typography">
                        <h1 class="hero-title" id="hero-title">
                            <span class="line-small font-sans">Happy Birthday</span>
                            <span class="line-large font-serif">My Love</span>
                        </h1>
                    </div>

                    <div class="hero-cta-group" id="hero-cta">
                        <button class="btn btn-luxury" id="hero-action-btn" aria-label="Enter the experience">
                            <span class="btn-background-shimmer"></span>
                            <span class="btn-text">Begin The Journey</span>
                            <svg class="btn-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <line x1="12" y1="5" x2="12" y2="19"></line>
                                <polyline points="19 12 12 19 5 12"></polyline>
                            </svg>
                        </button>
                    </div>

                    <div class="scroll-indicator" id="hero-scroll-indicator" aria-hidden="true">
                        <div class="mouse-icon">
                            <div class="wheel"></div>
                        </div>
                        <span class="scroll-text">Scroll to reveal</span>
                    </div>
                </div>
            </section>

            <!-- STORY SECTION -->
            <section class="section story-viewport" id="story-section" aria-label="Our Story Narrative">
                <div class="container story-container">
                    <div class="grid grid-2-col">
                        <div class="story-text-column">
                            <span class="section-badge">Our Story</span>
                            <h2 class="section-title split-text font-serif">The Day My World Changed</h2>
                            <p class="story-paragraph text-muted">
                                Every moment we have shared has felt like a scene crafted by a master filmmaker. The quiet evenings, the explosive laughter, and the subtle gestures of love that bind us closer with every passing season.
                            </p>
                            <p class="story-paragraph text-muted">
                                This space is a little home for our memories. It’s for the private jokes we share, the hurdles we’ve crossed together, and the quiet comfort of holding your hand at the end of a long day. I wanted to build something that shows you how deeply you are loved, not just today, but in every single moment.
                            </p>
                            <blockquote class="luxury-quote font-serif">
                                "In your smile, I found the place where I always want to stay."
                            </blockquote>
                        </div>
                        <div class="story-media-column">
                            <div class="media-frame-wrapper glass-panel">
                                <div class="media-frame-inner">
                                    <img src="assets/images/story-1.jpg" alt="A beautiful shared memory of us" class="lazy-image" loading="lazy">
                                    <div class="media-overlay"></div>
                                </div>
                                <div class="floating-caption glass-label">
                                    <span class="caption-date">Our First Selfie</span>
                                    <span class="caption-location">The Day Everything Changed</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- TIMELINE SECTION -->
            <section class="section timeline-viewport" id="timeline-section" aria-label="Interactive Narrative Timeline">
                <div class="container timeline-container">
                    <div class="timeline-header">
                        <span class="section-badge">Beautiful Memories</span>
                        <h2 class="section-title text-center font-serif">Every Step With You</h2>
                        <p class="section-subtitle text-center text-muted">The moments that built the bridge to where we are today.</p>
                    </div>

                    <div class="timeline-track-wrapper">
                        <div class="timeline-axis-line">
                            <div class="timeline-axis-progress" id="timeline-progress-bar"></div>
                        </div>

                        <div class="timeline-item timeline-left">
                            <div class="timeline-marker" aria-hidden="true"></div>
                            <div class="timeline-card glass-panel">
                                <span class="card-year font-serif">Where It All Began</span>
                                <h3 class="card-title">We Became Friends</h3>
                                <p class="card-desc text-muted">It started with simple conversations and endless laughter. We talked about everything and nothing at all, slowly building a safe space where we could completely be ourselves.</p>
                                <div class="card-media">
                                    <img src="assets/images/timeline-1.jpg" alt="First encounter space" class="lazy-image" loading="lazy">
                                </div>
                            </div>
                        </div>

                        <div class="timeline-item timeline-right">
                            <div class="timeline-marker" aria-hidden="true"></div>
                            <div class="timeline-card glass-panel">
                                <span class="card-year font-serif">The Shift</span>
                                <h3 class="card-title">Our First Chocolate</h3>
                                <p class="card-desc text-muted">That sweet, quiet afternoon where a simple gesture of sharing chocolate turned into something deeper. I looked at you and realized my thoughts were occupied by you, always.</p>
                                <div class="card-media">
                                    <img src="assets/images/timeline-2.jpg" alt="Collaborative and support moments" class="lazy-image" loading="lazy">
                                </div>
                            </div>
                        </div>

                        <div class="timeline-item timeline-left">
                            <div class="timeline-marker" aria-hidden="true"></div>
                            <div class="timeline-card glass-panel">
                                <span class="card-year font-serif">The Realization</span>
                                <h3 class="card-title">The Day I Realized I Love You</h3>
                                <p class="card-desc text-muted">There was no turning back. Your kindness, your beautiful heart, and the effortless way you make the world warmer showed me that my future belonged right next to yours.</p>
                                <div class="card-media">
                                    <img src="assets/images/timeline-3.jpg" alt="Our travels together" class="lazy-image" loading="lazy">
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- GALLERY SECTION -->
            <section class="section gallery-viewport" id="gallery-section" aria-label="Curated Memory Gallery">
                <div class="container gallery-container">
                    <div class="gallery-header">
                        <span class="section-badge">Moments That Matter</span>
                        <h2 class="section-title text-center font-serif">Moments I'll Never Forget</h2>
                        <p class="section-subtitle text-center text-muted">Scattered frames of pure happiness.</p>
                    </div>

                    <div class="gallery-grid" id="masonry-gallery">
                        <div class="gallery-item item-portrait" role="button" aria-haspopup="dialog" aria-label="Open photo lightbox 1">
                            <div class="gallery-card-inner glass-panel">
                                <img src="assets/images/gallery-1.jpg" alt="Laughing candid portrait" class="gallery-img lazy-image" loading="lazy">
                                <div class="gallery-item-info">
                                    <h4 class="gallery-item-title font-serif">The Smile I Fell In Love With</h4>
                                    <p class="gallery-item-category">Forever my favourite smile</p>
                                </div>
                            </div>
                        </div>

                        <div class="gallery-item item-landscape" role="button" aria-haspopup="dialog" aria-label="Open photo lightbox 2">
                            <div class="gallery-card-inner glass-panel">
                                <img src="assets/images/gallery-2.jpg" alt="Watching the skyline together" class="gallery-img lazy-image" loading="lazy">
                                <div class="gallery-item-info">
                                    <h4 class="gallery-item-title font-serif">The Day My World Changed</h4>
                                    <p class="gallery-item-category">One more beautiful moment</p>
                                </div>
                            </div>
                        </div>

                        <div class="gallery-item item-square" role="button" aria-haspopup="dialog" aria-label="Open photo lightbox 3">
                            <div class="gallery-card-inner glass-panel">
                                <img src="assets/images/gallery-3.jpg" alt="Warm holding hands details" class="gallery-img lazy-image" loading="lazy">
                                <div class="gallery-item-info">
                                    <h4 class="gallery-item-title font-serif">The Happiest Version Of Me</h4>
                                    <p class="gallery-item-category">My favourite memory</p>
                                </div>
                            </div>
                        </div>

                        <div class="gallery-item item-portrait" role="button" aria-haspopup="dialog" aria-label="Open photo lightbox 4">
                            <div class="gallery-card-inner glass-panel">
                                <img src="assets/images/gallery-4.jpg" alt="Our sunny beach walk" class="gallery-img lazy-image" loading="lazy">
                                <div class="gallery-item-info">
                                    <h4 class="gallery-item-title font-serif">The Little Moments I Treasure</h4>
                                    <p class="gallery-item-category">Every moment with you matters</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- INTERACTIVE LETTER SECTION -->
            <section class="section letter-viewport" id="letter-section" aria-label="Personal Letter Screen">
                <div class="container letter-container">
                    <div class="letter-header">
                        <span class="section-badge">A Letter From My Heart</span>
                        <h2 class="section-title text-center font-serif">To My Forever</h2>
                        <p class="section-subtitle text-center text-muted">Click the wax seal to unfold my personal note to you.</p>
                    </div>

                    <div class="envelope-arena">
                        <div class="envelope-wrapper" id="envelope">
                            <div class="envelope-back" aria-hidden="true"></div>
                            
                            <div class="letter-paper" id="letter-sheet" role="article" aria-label="Personal note paper">
                                <div class="letter-paper-content">
                                    <p class="letter-date font-sans">Today and Always</p>
                                    <h3 class="letter-salutation font-serif">My Dearest,</h3>
                                    <p class="letter-body-prose font-serif">
                                        As another wonderful year rolls around, I find myself looking back at how incredibly lucky I am to have you in my life. You have been my constant inspiration, my calmest sanctuary, and my greatest source of joy. I still smile thinking about our first laugh together—that silly, uncontrollable moment where we couldn't even remember what we were laughing at, but we knew we didn't want it to end. Your kindness is a gentle light that guides me on my darkest days, and your laugh is my favorite sound in the world.
                                    </p>
                                    <p class="letter-body-prose font-serif">
                                        I am so incredibly proud of the woman you are—the strength you carry, the warmth you give to everyone around you, and the beautiful dreams you work so hard to achieve.
                                    </p>
                                    <p class="letter-body-prose font-serif">
                                        On your birthday, my promise to you is simple: no matter where life leads us, I will walk by your side, holding your hand, and cheering you on. I promise to support your wildest ideas, to protect your peace, and to love you more with every single passing day.
                                    </p>
                                    <p class="letter-sign-off font-serif">With all my love, always,</p>
                                    <span class="signature font-serif">Yours ❤️</span>
                                </div>
                            </div>

                            <div class="envelope-front-sides" aria-hidden="true"></div>
                            <div class="envelope-front-bottom" aria-hidden="true"></div>
                            <div class="envelope-flap" id="envelope-flap" aria-hidden="true"></div>

                            <button class="wax-seal-btn" id="seal-trigger" aria-label="Open letter seal" aria-expanded="false">
                                <div class="seal-inner">
                                    <span class="seal-monogram">L</span>
                                </div>
                            </button>
                        </div>
                    </div>
                </div>
            </section>

            <!-- FINALE SECTION -->
            <section class="section finale-viewport" id="finale-section" aria-label="Cinematic Finale">
                <div class="ambient-glow finale-glow" aria-hidden="true"></div>
                <canvas class="ambient-particles" id="finale-particle-canvas"></canvas>

                <div class="container finale-container">
                    <div class="finale-heart-display">
                        <svg class="glowing-heart-svg" viewBox="0 0 100 90" xmlns="http://www.w3.org/2000/svg" aria-label="Pulsating Gold Heart Icon">
                            <path d="M12 4.435C2.106-2.19 0 7.435 0 14.331c0 14.168 15.698 28.536 34.024 43.19C42.863 64.636 47 68.3 50 71c3-2.7 7.137-6.364 15.976-13.479C84.302 42.867 100 28.499 100 14.331c0-6.896-2.106-16.521-12-10.096C76.2 11.83 60.1 19.333 50 22.408 39.9 19.333 23.8 11.83 12 4.435z" fill="url(#gold-gradient)" />
                        </svg>
                    </div>

                    <div class="finale-text-block">
                        <h2 class="finale-headline font-serif">No Matter Where Life Takes Us</h2>
                        <p class="finale-prose font-sans text-muted">Every day with you is the greatest gift I've ever received.</p>
                        <span class="finale-signature font-serif">Happy Birthday Nirosha ❤️</span>
                    </div>

                    <div class="finale-actions">
                        <button class="btn btn-muted-outline" id="replay-experience" aria-label="Replay experience from beginning">Relive Our Memories</button>
                    </div>
                </div>
            </section>

        </div>
    </main>

    <div class="lightbox" id="gallery-lightbox" role="dialog" aria-modal="true" aria-hidden="true" aria-label="Image Zoom View">
        <button class="lightbox-close" id="lightbox-close-btn" aria-label="Close image zoom view">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
        </button>
        <div class="lightbox-content">
            <img src="" alt="Zoomed memory photo" class="lightbox-img" id="lightbox-display-img">
            <p class="lightbox-caption" id="lightbox-display-caption"></p>
        </div>
    </div>

    <script type="module" src="js/app.js"></script>
</body>
</html>"""

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(clean_html_content)
    print("✓ Recreated index.html with pristine Single-Heart DOM structure and updated titles.")


# 2. Update css/sections/letter.css (Disable viewport clipping and add safe vertical margins)
letter_css_path = "css/sections/letter.css"
if os.path.exists(letter_css_path):
    with open(letter_css_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Apply visible overflow to viewport so sliding paper is not cropped by section boundaries
    new_viewport_style = """.letter-viewport {
    background-color: var(--color-bg-secondary);
    padding: var(--space-xxl) 0;
    overflow: visible !important; /* Prevent browser from clipping sliding letter paper */
}"""

    # Add generous margin above envelope arena so it slides up into perfectly clean space
    new_arena_style = """.envelope-arena {
    position: relative;
    width: 100%;
    max-width: 500px;
    height: 380px;
    margin: 150px auto 50px auto; /* Increased top margin prevents overlap with headers */
    perspective: 1500px;
}"""

    content = re.sub(r"\.letter-viewport\s*\{[^}]+\}", new_viewport_style, content)
    content = re.sub(r"\.envelope-arena\s*\{[^}]+\}", new_arena_style, content)

    with open(letter_css_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ Repaired css/sections/letter.css viewport boundaries and margins.")
else:
    print("✗ letter.css not found!")

print("\\nRefactoring complete! Verify your files and reload.")