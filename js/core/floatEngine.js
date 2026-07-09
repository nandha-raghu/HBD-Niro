export class FloatEngine {
    constructor(selector, maxTilt = 8) {
        this.targets = document.querySelectorAll(selector);
        this.maxTilt = maxTilt;
        
        if (this.targets.length > 0) {
            this.init();
        }
    }

    init() {
        this.targets.forEach(element => {
            element.addEventListener('mousemove', (e) => this.handleMouseMove(e, element), { passive: true });
            element.addEventListener('mouseleave', () => this.handleMouseLeave(element), { passive: true });
            element.addEventListener('mouseenter', () => this.handleMouseEnter(element), { passive: true });
        });
    }

    handleMouseMove(e, element) {
        const rect = element.getBoundingClientRect();
        
        const mouseX = e.clientX - rect.left;
        const mouseY = e.clientY - rect.top;

        const percentX = (mouseX / rect.width) - 0.5;
        const percentY = (mouseY / rect.height) - 0.5;

        const rotateY = percentX * this.maxTilt;
        const rotateX = -percentY * this.maxTilt;

        const percentageX = (mouseX / rect.width) * 100;
        const percentageY = (mouseY / rect.height) * 100;
        element.style.setProperty('--mouse-x', `${percentageX}%`);
        element.style.setProperty('--mouse-y', `${percentageY}%`);

        gsap.to(element, {
            rotationX: rotateX,
            rotationY: rotateY,
            z: 15,
            transformPerspective: 1000,
            duration: 0.6,
            ease: "power2.out",
            overwrite: "auto"
        });
    }

    handleMouseLeave(element) {
        gsap.to(element, {
            rotationX: 0,
            rotationY: 0,
            z: 0,
            duration: 0.8,
            ease: "power3.out",
            overwrite: "auto"
        });
    }

    handleMouseEnter(element) {
        gsap.to(element, {
            z: 8,
            duration: 0.4,
            ease: "power2.out"
        });
    }
}