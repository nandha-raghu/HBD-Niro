import { CONFIG } from '../core/config.js';
import { STATE } from '../core/state.js';
import { DOM } from '../core/dom.js';

const TARGET_VOLUME = 0.5;
let playPromise = null;

function syncWidgetVisuals(isPlaying) {
    const widget = DOM.audioWidget;
    const btnText = DOM.audioBtn?.querySelector('.btn-text');

    if (!widget) return;

    if (isPlaying) {
        widget.classList.add('is-playing');
        if (btnText) btnText.textContent = "Mute Our Song";
        DOM.audioBtn?.setAttribute('aria-label', 'Mute musical score');
    } else {
        widget.classList.remove('is-playing');
        if (btnText) btnText.textContent = "Play Our Song ❤️";
        DOM.audioBtn?.setAttribute('aria-label', 'Play musical score');
    }
}

export function playScore() {
    const audio = DOM.audioSource;
    if (!audio) return;

    if (STATE.current.audioPlaying) return;

    audio.volume = 0;
    playPromise = audio.play();

    if (playPromise !== undefined) {
        playPromise.then(() => {
            STATE.set('audioPlaying', true);
            
            gsap.to(audio, {
                volume: TARGET_VOLUME,
                duration: 2.0,
                ease: "power2.out"
            });
        }).catch(error => {
            console.warn("Audio Autoplay Policy blocks gestureless playback.", error);
            STATE.set('audioPlaying', false);
        });
    }
}

export function pauseScore() {
    const audio = DOM.audioSource;
    if (!audio || !STATE.current.audioPlaying) return;

    gsap.to(audio, {
        volume: 0,
        duration: 1.5,
        ease: "power2.in",
        onComplete: () => {
            audio.pause();
            STATE.set('audioPlaying', false);
        }
    });
}

function handleToggleClick() {
    if (STATE.current.audioPlaying) {
        pauseScore();
    } else {
        playScore();
    }
}

export function initMusic() {
    const toggleBtn = DOM.audioBtn;

    if (!toggleBtn) return;

    STATE.subscribe('audioPlaying', syncWidgetVisuals);
    toggleBtn.addEventListener('click', handleToggleClick, { passive: true });
}