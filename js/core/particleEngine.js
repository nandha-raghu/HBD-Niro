import { CONFIG } from './config.js';
import { STATE } from './state.js';

class ParticleInstance {
    constructor(width, height, settings) {
        this.canvasWidth = width;
        this.canvasHeight = height;
        this.settings = settings;

        this.reset();
        this.y = Math.random() * this.canvasHeight;
    }

    reset() {
        this.x = Math.random() * this.canvasWidth;
        this.y = this.canvasHeight + Math.random() * 20;
        
        this.size = Math.random() * (this.settings.size.max - this.settings.size.min) + this.settings.size.min;
        this.speedY = Math.random() * (this.settings.speed.max - this.settings.speed.min) + this.settings.speed.min;
        
        this.swaySpeed = Math.random() * 0.02 + 0.005;
        this.swayAmount = Math.random() * 1.5 + 0.5;
        this.swayAngle = Math.random() * Math.PI * 2;

        this.alpha = Math.random() * 0.4 + 0.1;
        this.color = Math.random() > 0.45 ? this.settings.colorGold : this.settings.colorRoseGold;
    }

    update() {
        this.y -= this.speedY;
        
        this.swayAngle += this.swaySpeed;
        this.x += Math.sin(this.swayAngle) * (this.swayAmount * 0.1);
        this.alpha = Math.sin(this.swayAngle) * 0.15 + 0.4;

        if (this.y < -10 || this.x < -10 || this.x > this.canvasWidth + 10) {
            this.reset();
        }
    }

    draw(ctx) {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fillStyle = this.color.replace(')', `, ${this.alpha})`).replace('rgb', 'rgba');
        ctx.fill();
    }
}

export class ParticleEngine {
    constructor(canvasElement, configKey) {
        this.canvas = canvasElement;
        if (!this.canvas) return;

        this.ctx = this.canvas.getContext('2d');
        this.settings = CONFIG.particles[configKey];
        this.particles = [];
        this.isRunning = false;
        this.rafId = null;

        this.init();
    }

    init() {
        this.resize();
        this.populate();

        window.addEventListener('state:windowWidth', () => this.resize());
    }

    resize() {
        if (!this.canvas) return;

        this.width = this.canvas.clientWidth;
        this.height = this.canvas.clientHeight;

        const scale = window.devicePixelRatio || 1;
        this.canvas.width = this.width * scale;
        this.canvas.height = this.height * scale;
        this.ctx.scale(scale, scale);

        this.particles.forEach(p => {
            p.canvasWidth = this.width;
            p.canvasHeight = this.height;
        });
    }

    populate() {
        this.particles = [];
        let count = this.settings.density;

        if (STATE.current.isMobile) {
            count = Math.floor(count * CONFIG.performance.mobileParticleReduction);
        }

        for (let i = 0; i < count; i++) {
            this.particles.push(new ParticleInstance(this.width, this.height, this.settings));
        }
    }

    start() {
        if (this.isRunning) return;
        this.isRunning = true;
        this.tick();
    }

    stop() {
        this.isRunning = false;
        if (this.rafId) {
            cancelAnimationFrame(this.rafId);
            this.rafId = null;
        }
    }

    tick() {
        if (!this.isRunning) return;

        this.ctx.clearRect(0, 0, this.width, this.height);

        this.particles.forEach(p => {
            p.update();
            p.draw(this.ctx);
        });

        this.rafId = requestAnimationFrame(() => this.tick());
    }
}