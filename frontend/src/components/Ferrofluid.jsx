import { useEffect, useRef } from 'react';

const vertexShaderSource = `
attribute vec2 position;
void main() {
  gl_Position = vec4(position, 0.0, 1.0);
}
`;

const fragmentShaderSource = `
precision highp float;

uniform vec2 resolution;
uniform vec2 mouse;
uniform float time;
uniform vec3 color0;
uniform vec3 color1;
uniform vec3 color2;
uniform float speed;
uniform float scale;
uniform float turbulence;
uniform float fluidity;
uniform float rimWidth;
uniform float sharpness;
uniform float shimmer;
uniform float glow;
uniform float flowDirection;
uniform float mouseInteraction;
uniform float mouseStrength;
uniform float mouseRadius;

float hash(vec2 p) {
  return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453123);
}

float noise(vec2 p) {
  vec2 i = floor(p);
  vec2 f = fract(p);
  f = f * f * (3.0 - 2.0 * f);
  return mix(mix(hash(i), hash(i + vec2(1.0, 0.0)), f.x), mix(hash(i + vec2(0.0, 1.0)), hash(i + vec2(1.0, 1.0)), f.x), f.y);
}

void main() {
  vec2 uv = (gl_FragCoord.xy * 2.0 - resolution.xy) / min(resolution.x, resolution.y);
  vec2 p = uv / max(scale, 0.01);
  float t = time * speed;

  vec2 flow = vec2(sin(t * 0.15) * 0.25, flowDirection * t * 0.22);
  vec2 pointer = (mouse - uv) * mouseInteraction;
  float pointerDistance = length(pointer);
  float pointerForce = exp(-pointerDistance / max(mouseRadius, 0.01)) * mouseStrength;
  p += pointer * pointerForce * 0.35;

  float warp = 0.0;
  vec2 warped = p + flow;
  for (int i = 0; i < 4; i++) {
    float band = float(i) + 1.0;
    warp += sin(warped.y * (1.2 + band * 0.8) + t * (0.7 + band * 0.13)) * 0.12;
    warped += vec2(sin(warped.y * 2.2 + t * 0.8), cos(warped.x * 1.9 - t * 0.9)) * 0.05 * turbulence;
  }

  vec2 q = p + flow + vec2(warp * turbulence, warp * fluidity);
  float stream = sin(q.x * 3.8 + sin(q.y * 2.2 + t * 1.2) * 1.6) * 0.5 + 0.5;
  float ridges = sin(q.y * 5.5 - q.x * 2.8 + t * 1.4 + stream * 2.5) * 0.5 + 0.5;
  float noiseField = noise(q * 3.2 + vec2(t * 0.25, -t * 0.45));
  float fluid = smoothstep(0.15, 0.85, stream * 0.55 + ridges * 0.3 + noiseField * 0.2);

  float edge = abs(fluid - 0.5) * 2.0;
  float rim = pow(max(0.0, 1.0 - edge), max(sharpness, 0.1)) * rimWidth;
  float shine = pow(max(0.0, sin(q.x * 7.0 + q.y * 3.5 - t * 1.8)), 16.0) * shimmer;
  float halo = exp(-length(uv) * 0.8) * glow * 0.15;

  vec3 neonCyan = color0;
  vec3 neonViolet = color1;
  vec3 neonIndigo = color2;

  vec3 base = mix(neonCyan, neonViolet, smoothstep(0.15, 0.65, fluid));
  base = mix(base, neonIndigo, smoothstep(0.55, 0.95, fluid));
  
  vec3 result = base * (0.35 + fluid * 0.75) + (neonCyan + vec3(0.2, 0.6, 1.0)) * rim * 0.5 + vec3(shine * 0.6 + halo * 0.4);
  result *= 0.85 + 0.15 * smoothstep(1.8, 0.2, length(uv));

  gl_FragColor = vec4(result, 1.0);
}
`;

function parseColor(color, fallback) {
  const value = color?.replace('#', '');
  if (!value || !/^[0-9a-f]{6}$/i.test(value)) return fallback;
  return [
    parseInt(value.slice(0, 2), 16) / 255,
    parseInt(value.slice(2, 4), 16) / 255,
    parseInt(value.slice(4, 6), 16) / 255,
  ];
}

function createShader(gl, type, source) {
  const shader = gl.createShader(type);
  gl.shaderSource(shader, source);
  gl.compileShader(shader);
  if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
    gl.deleteShader(shader);
    return null;
  }
  return shader;
}

export default function Ferrofluid({
  colors = ['#06b6d4', '#8b5cf6', '#3b82f6'],
  speed = 0.6,
  scale = 1.1,
  turbulence = 1.3,
  fluidity = 0.4,
  rimWidth = 0.35,
  sharpness = 2.5,
  shimmer = 1.2,
  glow = 2.5,
  flowDirection = 'down',
  opacity = 0.6,
  mouseInteraction = true,
  mouseStrength = 1.2,
  mouseRadius = 0.35,
}) {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const gl = canvas?.getContext('webgl', { alpha: true, antialias: false });
    if (!gl) return undefined;

    const vertexShader = createShader(gl, gl.VERTEX_SHADER, vertexShaderSource);
    const fragmentShader = createShader(gl, gl.FRAGMENT_SHADER, fragmentShaderSource);
    if (!vertexShader || !fragmentShader) return undefined;

    const program = gl.createProgram();
    gl.attachShader(program, vertexShader);
    gl.attachShader(program, fragmentShader);
    gl.linkProgram(program);
    if (!gl.getProgramParameter(program, gl.LINK_STATUS)) return undefined;

    const buffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, -1, 1, 1, -1, 1, 1]), gl.STATIC_DRAW);

    const uniforms = Object.fromEntries([
      'resolution', 'mouse', 'time', 'color0', 'color1', 'color2', 'speed', 'scale', 'turbulence', 'fluidity',
      'rimWidth', 'sharpness', 'shimmer', 'glow', 'flowDirection', 'mouseInteraction', 'mouseStrength', 'mouseRadius'
    ].map((name) => [name, gl.getUniformLocation(program, name)]));
    const parsedColors = colors.slice(0, 3).map((color) => parseColor(color, [0.02, 0.71, 0.83]));
    while (parsedColors.length < 3) parsedColors.push([0.55, 0.36, 0.96]);
    const pointer = { x: 0, y: 0 };
    let animationFrame;
    let startTime = performance.now();

    const resize = () => {
      const width = Math.max(1, Math.floor(canvas.clientWidth * Math.min(window.devicePixelRatio || 1, 2)));
      const height = Math.max(1, Math.floor(canvas.clientHeight * Math.min(window.devicePixelRatio || 1, 2)));
      if (canvas.width !== width || canvas.height !== height) {
        canvas.width = width;
        canvas.height = height;
      }
      gl.viewport(0, 0, width, height);
    };

    const updatePointer = (event) => {
      pointer.x = (event.clientX / window.innerWidth) * 2 - 1;
      pointer.y = 1 - (event.clientY / window.innerHeight) * 2;
    };

    const render = (now) => {
      resize();
      gl.useProgram(program);
      gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
      const position = gl.getAttribLocation(program, 'position');
      gl.enableVertexAttribArray(position);
      gl.vertexAttribPointer(position, 2, gl.FLOAT, false, 0, 0);
      gl.uniform2f(uniforms.resolution, canvas.width, canvas.height);
      gl.uniform2f(uniforms.mouse, pointer.x, pointer.y);
      gl.uniform1f(uniforms.time, (now - startTime) / 1000);
      gl.uniform3fv(uniforms.color0, parsedColors[0]);
      gl.uniform3fv(uniforms.color1, parsedColors[1]);
      gl.uniform3fv(uniforms.color2, parsedColors[2]);
      gl.uniform1f(uniforms.speed, speed);
      gl.uniform1f(uniforms.scale, scale);
      gl.uniform1f(uniforms.turbulence, turbulence);
      gl.uniform1f(uniforms.fluidity, fluidity);
      gl.uniform1f(uniforms.rimWidth, rimWidth);
      gl.uniform1f(uniforms.sharpness, sharpness);
      gl.uniform1f(uniforms.shimmer, shimmer);
      gl.uniform1f(uniforms.glow, glow);
      gl.uniform1f(uniforms.flowDirection, flowDirection === 'down' ? 1 : -1);
      gl.uniform1f(uniforms.mouseInteraction, mouseInteraction ? 1 : 0);
      gl.uniform1f(uniforms.mouseStrength, mouseStrength);
      gl.uniform1f(uniforms.mouseRadius, mouseRadius);
      gl.clearColor(0, 0, 0, 0);
      gl.clear(gl.COLOR_BUFFER_BIT);
      gl.drawArrays(gl.TRIANGLES, 0, 6);
      animationFrame = requestAnimationFrame(render);
    };

    const observer = new ResizeObserver(resize);
    observer.observe(canvas);
    if (mouseInteraction) window.addEventListener('pointermove', updatePointer);
    render(startTime);

    return () => {
      cancelAnimationFrame(animationFrame);
      observer.disconnect();
      window.removeEventListener('pointermove', updatePointer);
      gl.deleteBuffer(buffer);
      gl.deleteProgram(program);
      gl.deleteShader(vertexShader);
      gl.deleteShader(fragmentShader);
    };
  }, [colors.join(','), flowDirection, fluidity, glow, mouseInteraction, mouseRadius, mouseStrength, opacity, rimWidth,
    scale, sharpness, shimmer, speed, turbulence]);

  return <canvas ref={canvasRef} aria-hidden="true" className="ferrofluid-background" style={{ opacity }} />;
}