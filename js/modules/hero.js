import { CONFIG } from "../core/config.js";
import { STATE } from "../core/state.js";
import { DOM } from "../core/dom.js";
import { ParticleEngine } from "../core/particleEngine.js";
import { getScroller } from "../core/animationManager.js";
import { playScore } from "./music.js";

let heroParticles = null;

export function revealHero() {
  const revealTimeline = gsap.timeline();

  STATE.set("isLoaded", true);

  if (DOM.heroBrand) {
    DOM.heroBrand.classList.add("is-visible");
  }

  if (DOM.heroTitle) {
    const splitText = new SplitType(DOM.heroTitle, {
      types: "lines, words, chars",
    });
    DOM.heroTitle.classList.add("js-split-initialized");

    revealTimeline.from(
      splitText.chars,
      {
        y: "100%",
        opacity: 0,
        duration: 1.4,
        stagger: 0.02,
        ease: "power4.out",
      },
      0.2,
    );
  }

  if (DOM.heroCta) {
    // CINEMATIC DELAY: Hold on the title and heart for 5.0s before showing the button
    revealTimeline.to(
      DOM.heroCta,
      {
        onStart: () => {
          DOM.heroCta.classList.add("is-visible");
        },
        opacity: 1,
        y: 0,
        duration: 1.2,
        ease: "power3.out",
      },
      "+=5.0",
    );
  }

  if (DOM.heroScrollIndicator) {
    revealTimeline.to(
      DOM.heroScrollIndicator,
      {
        onStart: () => {
          DOM.heroScrollIndicator.classList.add("is-visible");
        },
        opacity: 0.6,
        duration: 1.0,
        ease: "power2.out",
      },
      "-=0.2",
    );
  }

  if (DOM.audioWidget) {
    DOM.audioWidget.classList.add("is-visible");
  }
}

export function initHero() {
  // 4. Bind interactive mouse-reactive volumetric background glow
  window.addEventListener("pointer:move", (e) => {
    const { x, y } = e.detail;
    const glow = DOM.queryLive("#hero-glow");
    if (glow) {
      // Translate volumetric glow coordinates smoothly with lagging trail coordinates
      gsap.to(glow, {
        x: x - window.innerWidth / 2,
        y: y - window.innerHeight / 2,
        duration: 2.0,
        ease: "power2.out",
        overwrite: "auto",
      });
    }
  });

  const canvasElement = DOM.queryLive("#hero-particle-canvas");
  if (canvasElement) {
    heroParticles = new ParticleEngine(canvasElement, "hero");
    heroParticles.start();
  }

  window.addEventListener("canvas:hero:play", () => {
    if (heroParticles) heroParticles.start();
  });

  window.addEventListener("canvas:hero:pause", () => {
    if (heroParticles) heroParticles.stop();
  });

  const actionBtn = DOM.queryLive("#hero-action-btn");
  if (actionBtn) {
    actionBtn.addEventListener("click", () => {
      const lenis = getScroller();
      const storyEl = DOM.queryLive(CONFIG.selectors.storySection);
      if (lenis && storyEl) {
        lenis.scrollTo(storyEl, {
          offset: 0,
          duration: 1.6,
          easing: (t) => (t === 1 ? 1 : 1 - Math.pow(2, -10 * t)),
        });
      }
      playScore();
    });
  }
}
