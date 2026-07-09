export function lerp(start, end, amt) {
    return (1 - amt) * start + amt * end;
}

export function clamp(val, min, max) {
    return Math.min(Math.max(val, min), max);
}

export function mapRange(value, inMin, inMax, outMin, outMax) {
    return ((value - inMin) * (outMax - outMin)) / (inMax - inMin) + outMin;
}

export function getElementCenterCoordinates(element) {
    if (!element) return { x: 0, y: 0 };

    const rect = element.getBoundingClientRect();
    const scrollX = window.scrollX || window.pageXOffset;
    const scrollY = window.scrollY || window.pageYOffset;

    return {
        x: rect.left + rect.width / 2 + scrollX,
        y: rect.top + rect.height / 2 + scrollY
    };
}

export function getQuadraticBezierPoint(p0, p1, p2, t) {
    const term1_coefficient = (1 - t) ** 2;
    const term2_coefficient = 2 * (1 - t) * t;
    const term3_coefficient = t ** 2;

    return {
        x: term1_coefficient * p0.x + term2_coefficient * p1.x + term3_coefficient * p2.x,
        y: term1_coefficient * p0.y + term2_coefficient * p1.y + term3_coefficient * p2.y
    };
}