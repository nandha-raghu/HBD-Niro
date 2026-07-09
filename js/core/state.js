class StateManager {
    constructor() {
        this._state = {
            isLoaded: false,
            audioPlaying: false,
            envelopeOpen: false,
            activeSection: 'loader',
            isMobile: false,
            windowWidth: 0,
            windowHeight: 0
        };
        this._listeners = new Map();
    }

    get current() {
        return Object.freeze({ ...this._state });
    }

    subscribe(key, callback) {
        if (!this._listeners.has(key)) {
            this._listeners.set(key, []);
        }
        this._listeners.get(key).push(callback);
    }

    set(key, newValue) {
        if (!(key in this._state)) {
            console.warn(`StateManager: Attempted to set unregistered state property: "${key}"`);
            return;
        }

        if (this._state[key] === newValue) return;

        const oldValue = this._state[key];
        this._state[key] = newValue;

        const subscribers = this._listeners.get(key);
        if (subscribers) {
            subscribers.forEach(callback => {
                try {
                    callback(newValue, oldValue);
                } catch (error) {
                    console.error(`StateManager: Error during subscriber execution for key "${key}":`, error);
                }
            });
        }

        window.dispatchEvent(new CustomEvent(`state:${key}`, {
            detail: { property: key, current: newValue, previous: oldValue }
        }));
    }
}

export const STATE = new StateManager();