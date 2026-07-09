import { CONFIG } from './config.js';

// Cache registry object containing element references and query methods
export const DOM = {
    // Expose queryLive as a method of DOM to prevent runtime exceptions
    queryLive(selector) {
        try {
            return document.querySelector(selector);
        } catch (e) {
            return null;
        }
    },
    
    // Expose queryAllLive as a method of DOM
    queryAllLive(selector) {
        try {
            return document.querySelectorAll(selector);
        } catch (e) {
            return document.createDocumentFragment().childNodes;
        }
    }
};

export function initDOM() {
    let missingElementsCount = 0;

    for (const [key, selector] of Object.entries(CONFIG.selectors)) {
        try {
            const element = document.querySelector(selector);
            
            if (element) {
                DOM[key] = element;
            } else {
                DOM[key] = null;
                missingElementsCount++;
            }
        } catch (error) {
            console.error(`DOM Cache: Exception during query initialization for "${key}" ("${selector}"):`, error);
            DOM[key] = null;
        }
    }
}

// Keep standalone named exports to prevent module dependency failures
export function queryLive(selector) {
    return DOM.queryLive(selector);
}

export function queryAllLive(selector) {
    return DOM.queryAllLive(selector);
}

export function recacheItem(key) {
    const selector = CONFIG.selectors[key];
    if (selector) {
        DOM[key] = document.querySelector(selector);
    }
}