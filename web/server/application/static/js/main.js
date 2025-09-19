async function renderAppsFromJSON(jsonPath) {
  try {
    const response = await fetch(jsonPath);
    if (!response.ok) throw new Error(`Error al cargar JSON: ${response.status}`);
    
    const apps = await response.json();
    const container = document.getElementById("list-apps");
    container.innerHTML = ""; // Limpia contenido previo

    // load all app find in the apps.json
    apps.forEach(app => {
      const col = document.createElement("div");
      col.className = "col-lg-6";

      col.innerHTML = `
        <a class="portfolio-item" href="${app.url}" target="_blank">
          <div class="caption">
            <div class="caption-content">
              <div class="h2">${app.title}</div>
            </div>
          </div>
          <img class="img-fluid" src="${app.image}" alt="..." />
        </a>
      `;

      container.appendChild(col);
    });
  } catch (err) {
    console.error("Error al renderizar apps:", err);
  }
}

// Ejecutar al cargar la página.
document.addEventListener("DOMContentLoaded", () => {
  renderAppsFromJSON("/static/js/data/apps.json"); // Ruta relativa al archivo JSON
});
