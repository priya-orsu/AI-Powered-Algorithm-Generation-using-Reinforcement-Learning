import React, { useEffect, useRef } from 'react';

export default function StarfieldGravity({
  starCount = 180,
  maxStarRadius = 2.4,
  gravityRadius = 160,
  gravityStrength = 0.8,
  constellationDistance = 110,
  speedMultiplier = 0.5,
  colors = ['#06b6d4', '#8b5cf6', '#3b82f6', '#ec4899', '#ffffff'],
}) {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationFrameId;
    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    const mouse = {
      x: width / 2,
      y: height / 2,
      targetX: width / 2,
      targetY: height / 2,
      active: false,
      radius: gravityRadius,
    };

    const handleMouseMove = (e) => {
      mouse.targetX = e.clientX;
      mouse.targetY = e.clientY;
      mouse.active = true;
    };

    const handleMouseLeave = () => {
      mouse.active = false;
    };

    const handleResize = () => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
      initStars();
    };

    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('mouseleave', handleMouseLeave);
    window.addEventListener('resize', handleResize);

    // Particle Class representing stars in deep space
    class Star {
      constructor() {
        this.reset(true);
      }

      reset(initial = false) {
        this.x = Math.random() * width;
        this.y = Math.random() * height;
        this.z = Math.random() * 3 + 0.5; // Depth layer: 0.5 (far) to 3.5 (near)
        
        this.baseRadius = (Math.random() * maxStarRadius + 0.6) * (this.z / 2);
        this.radius = this.baseRadius;
        
        // Base orbital drift velocity
        this.vx = (Math.random() - 0.5) * 0.4 * speedMultiplier * this.z;
        this.vy = (Math.random() - 0.5) * 0.4 * speedMultiplier * this.z;
        
        // Dynamic velocity added by mouse gravity
        this.dx = 0;
        this.dy = 0;
        
        this.color = colors[Math.floor(Math.random() * colors.length)];
        this.alpha = Math.random() * 0.7 + 0.3;
        this.twinkleSpeed = Math.random() * 0.03 + 0.01;
        this.twinkleAngle = Math.random() * Math.PI * 2;
      }

      update() {
        // Smooth mouse position easing
        mouse.x += (mouse.targetX - mouse.x) * 0.1;
        mouse.y += (mouse.targetY - mouse.y) * 0.1;

        // Gravitational warping physics
        if (mouse.active) {
          const dx = mouse.x - this.x;
          const dy = mouse.y - this.y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < mouse.radius && dist > 0) {
            const force = (1 - dist / mouse.radius) * gravityStrength * (this.z / 2);
            const angle = Math.atan2(dy, dx);

            // Gravitational pull towards cursor with tangential swirl
            const pullX = Math.cos(angle) * force * 1.5;
            const pullY = Math.sin(angle) * force * 1.5;
            const swirlX = -Math.sin(angle) * force * 0.8;
            const swirlY = Math.cos(angle) * force * 0.8;

            this.dx += (pullX + swirlX) * 0.2;
            this.dy += (pullY + swirlY) * 0.2;
          }
        }

        // Apply damping velocity
        this.dx *= 0.92;
        this.dy *= 0.92;

        // Position update
        this.x += this.vx + this.dx;
        this.y += this.vy + this.dy;

        // Twinkle effect
        this.twinkleAngle += this.twinkleSpeed;
        const twinkle = Math.sin(this.twinkleAngle) * 0.3;
        this.currentAlpha = Math.min(1, Math.max(0.1, this.alpha + twinkle));

        // Screen boundary wrap-around
        if (this.x < -20) this.x = width + 20;
        if (this.x > width + 20) this.x = -20;
        if (this.y < -20) this.y = height + 20;
        if (this.y > height + 20) this.y = -20;
      }

      draw(ctx) {
        ctx.save();
        ctx.globalAlpha = this.currentAlpha;
        
        // Draw star core
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = this.color;
        ctx.shadowBlur = this.z > 2 ? 12 : 6;
        ctx.shadowColor = this.color;
        ctx.fill();

        // Draw soft outer halo for foreground stars
        if (this.z > 2.2) {
          ctx.beginPath();
          ctx.arc(this.x, this.y, this.radius * 2.5, 0, Math.PI * 2);
          ctx.fillStyle = this.color;
          ctx.globalAlpha = this.currentAlpha * 0.2;
          ctx.fill();
        }

        ctx.restore();
      }
    }

    // Shooting Star Class for dynamic meteor trails
    class ShootingStar {
      constructor() {
        this.reset();
      }

      reset() {
        this.x = Math.random() * width * 1.5 - width * 0.25;
        this.y = Math.random() * height * 0.5 - height * 0.25;
        this.length = Math.random() * 120 + 80;
        this.speed = Math.random() * 12 + 8;
        this.size = Math.random() * 1.5 + 0.8;
        this.angle = Math.PI / 4 + (Math.random() - 0.5) * 0.2; // ~45 deg downward slope
        this.vx = Math.cos(this.angle) * this.speed;
        this.vy = Math.sin(this.angle) * this.speed;
        this.active = false;
        this.waitTime = Math.random() * 300 + 100;
        this.color = colors[Math.floor(Math.random() * colors.length)];
      }

      update() {
        if (!this.active) {
          this.waitTime--;
          if (this.waitTime <= 0) {
            this.active = true;
          }
          return;
        }

        this.x += this.vx;
        this.y += this.vy;

        if (this.x > width + 200 || this.y > height + 200) {
          this.reset();
        }
      }

      draw(ctx) {
        if (!this.active) return;

        const tailX = this.x - Math.cos(this.angle) * this.length;
        const tailY = this.y - Math.sin(this.angle) * this.length;

        const gradient = ctx.createLinearGradient(this.x, this.y, tailX, tailY);
        gradient.addColorStop(0, '#ffffff');
        gradient.addColorStop(0.3, this.color);
        gradient.addColorStop(1, 'transparent');

        ctx.save();
        ctx.beginPath();
        ctx.moveTo(this.x, this.y);
        ctx.lineTo(tailX, tailY);
        ctx.strokeStyle = gradient;
        ctx.lineWidth = this.size;
        ctx.lineCap = 'round';
        ctx.shadowBlur = 10;
        ctx.shadowColor = this.color;
        ctx.stroke();
        ctx.restore();
      }
    }

    let stars = [];
    const shootingStars = [new ShootingStar(), new ShootingStar()];

    function initStars() {
      stars = [];
      const calculatedCount = Math.floor((width * height) / 8000); // Responsive star count
      const finalCount = Math.max(120, Math.min(240, calculatedCount));
      for (let i = 0; i < finalCount; i++) {
        stars.push(new Star());
      }
    }

    initStars();

    // Draw deep ambient gradient nebula background
    function drawNebulaBackground() {
      // Dark cosmic space gradient
      const bgGrad = ctx.createRadialGradient(
        width / 2, height / 2, 100,
        width / 2, height / 2, Math.max(width, height)
      );
      bgGrad.addColorStop(0, '#0a0f1d');
      bgGrad.addColorStop(0.6, '#060a14');
      bgGrad.addColorStop(1, '#020408');

      ctx.fillStyle = bgGrad;
      ctx.fillRect(0, 0, width, height);

      // Ambient glowing energy nebula nodes
      ctx.save();
      ctx.globalCompositeOperation = 'screen';

      // Nebula 1 (Cyan Glow top-left)
      const g1 = ctx.createRadialGradient(width * 0.2, height * 0.25, 0, width * 0.2, height * 0.25, width * 0.45);
      g1.addColorStop(0, 'rgba(6, 182, 212, 0.12)');
      g1.addColorStop(0.6, 'rgba(139, 92, 246, 0.05)');
      g1.addColorStop(1, 'transparent');
      ctx.fillStyle = g1;
      ctx.fillRect(0, 0, width, height);

      // Nebula 2 (Purple Glow bottom-right)
      const g2 = ctx.createRadialGradient(width * 0.8, height * 0.75, 0, width * 0.8, height * 0.75, width * 0.5);
      g2.addColorStop(0, 'rgba(139, 92, 246, 0.14)');
      g2.addColorStop(0.5, 'rgba(59, 130, 246, 0.06)');
      g2.addColorStop(1, 'transparent');
      ctx.fillStyle = g2;
      ctx.fillRect(0, 0, width, height);

      // Mouse Gravitational Glow Pulse
      if (mouse.active) {
        const mouseGlow = ctx.createRadialGradient(mouse.x, mouse.y, 0, mouse.x, mouse.y, mouse.radius * 1.5);
        mouseGlow.addColorStop(0, 'rgba(6, 182, 212, 0.18)');
        mouseGlow.addColorStop(0.5, 'rgba(139, 92, 246, 0.08)');
        mouseGlow.addColorStop(1, 'transparent');
        ctx.fillStyle = mouseGlow;
        ctx.fillRect(0, 0, width, height);
      }

      ctx.restore();
    }

    // Draw dynamic constellation connections between nearby stars
    function drawConstellations() {
      ctx.save();
      for (let i = 0; i < stars.length; i++) {
        for (let j = i + 1; j < stars.length; j++) {
          const s1 = stars[i];
          const s2 = stars[j];
          
          // Only draw constellation lines between medium/foreground stars
          if (s1.z < 1.2 || s2.z < 1.2) continue;

          const dx = s1.x - s2.x;
          const dy = s1.y - s2.y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < constellationDistance) {
            const alpha = (1 - dist / constellationDistance) * 0.25 * Math.min(s1.currentAlpha, s2.currentAlpha);
            ctx.beginPath();
            ctx.moveTo(s1.x, s1.y);
            ctx.lineTo(s2.x, s2.y);
            ctx.strokeStyle = s1.color;
            ctx.globalAlpha = alpha;
            ctx.lineWidth = 0.75;
            ctx.stroke();
          }
        }
      }
      ctx.restore();
    }

    // Main Animation Rendering Loop
    function render() {
      ctx.clearRect(0, 0, width, height);

      drawNebulaBackground();
      drawConstellations();

      // Update and render stars
      for (let i = 0; i < stars.length; i++) {
        stars[i].update();
        stars[i].draw(ctx);
      }

      // Update and render shooting stars
      for (let i = 0; i < shootingStars.length; i++) {
        shootingStars[i].update();
        shootingStars[i].draw(ctx);
      }

      animationFrameId = requestAnimationFrame(render);
    }

    render();

    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseleave', handleMouseLeave);
      window.removeEventListener('resize', handleResize);
      cancelAnimationFrame(animationFrameId);
    };
  }, [starCount, maxStarRadius, gravityRadius, gravityStrength, constellationDistance, speedMultiplier, colors]);

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 w-full h-full pointer-events-none z-0"
      style={{ background: '#030712' }}
    />
  );
}
