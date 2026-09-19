document.addEventListener('DOMContentLoaded', () => {

  // Lógica para las pestañas de convocatorias
  const tabBtns = document.querySelectorAll('.tab-btn');
  const tabPanels = document.querySelectorAll('.tab-panel');

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      // Remover clase activa de todos los botones y paneles
      tabBtns.forEach(b => b.classList.remove('active'));
      tabPanels.forEach(p => p.classList.remove('active'));
      
      // Agregar clase activa al botón presionado y a su panel correspondiente
      btn.classList.add('active');
      const targetPanel = document.getElementById(btn.dataset.tab);
      if (targetPanel) {
        targetPanel.classList.add('active');
      }
    });
  });

  // Lógica para los chips/filtros de la red de emprendimientos
  const chips = document.querySelectorAll('.chip');
  chips.forEach(chip => {
    chip.addEventListener('click', () => {
      // Remover estado activo de todos y ponerlo en el que se hizo clic
      chips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
    });
  });

});