(function () {
  if (!window.Chart) return;
  const palette = ['#245c49', '#4b8b68', '#8db89c', '#d1a43b', '#6b8194', '#9a6e75'];
  const dataFrom = function (id) {
    const node = document.getElementById(id);
    return node ? JSON.parse(node.textContent) : [];
  };
  const categories = dataFrom('datos-categorias');
  const status = dataFrom('datos-estados');
  const categoryCanvas = document.getElementById('chart-categorias');
  const statusCanvas = document.getElementById('chart-estados');
  if (categoryCanvas && categories.length) {
    new window.Chart(categoryCanvas, {
      type: 'bar',
      data: {labels: categories.map(item => item.nombre), datasets: [{label: 'Ofertas publicadas', data: categories.map(item => item.total), backgroundColor: palette, borderRadius: 7}]},
      options: {responsive: true, maintainAspectRatio: false, plugins: {legend: {display: false}}, scales: {y: {beginAtZero: true, ticks: {precision: 0}}}}
    });
  }
  if (statusCanvas && status.length) {
    new window.Chart(statusCanvas, {
      type: 'doughnut',
      data: {labels: status.map(item => item.estado), datasets: [{data: status.map(item => item.total), backgroundColor: palette, borderWidth: 0}]},
      options: {responsive: true, maintainAspectRatio: false, plugins: {legend: {position: 'bottom'}}}
    });
  }
})();
