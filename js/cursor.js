(() => {
  const layer = document.createElement('div');
  layer.id = 'cursor-particles';
  document.body.appendChild(layer);

  let cx = 0, cy = 0;

  window.addEventListener('mousemove', e => {
    cx = e.clientX;
    cy = e.clientY;
    for (let i = 0; i < 4; i++) spawn();
  });

  function spawn() {
    const dot = document.createElement('div');
    dot.className = 'cursor-dot';

    const size = 3 + Math.random() * 6;
    dot.style.width = size + 'px';
    dot.style.height = size + 'px';

    const hue = Math.floor(Math.random() * 360);
    dot.style.background = `hsl(${hue}, 75%, 60%)`;

    layer.appendChild(dot);

    const sx = cx;
    const sy = cy;
    const driftX = (Math.random() - 0.5) * 70;
    const driftY = (Math.random() - 0.5) * 70;
    const duration = 350 + Math.random() * 250;
    const start = performance.now();

    requestAnimationFrame(function frame(t) {
      const p = (t - start) / duration;
      if (p >= 1) {
        dot.remove();
        return;
      }
      const x = sx + driftX * p;
      const y = sy + driftY * p;
      dot.style.transform = `translate(${x}px, ${y}px)`;
      dot.style.opacity = 1 - p;
      requestAnimationFrame(frame);
    });
  }
})();
