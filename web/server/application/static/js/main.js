async function renderAppsFromJSON(jsonPath) {
  try {
    const response = await fetch(jsonPath);
    if (!response.ok) throw new Error(`Error al cargar JSON: ${response.status}`);
    
    const apps = await response.json();
    const container = document.getElementById("list-apps");
    container.innerHTML = ""; // Limpia contenido previo

    // Cargar todas las apps desde apps.json
    apps.forEach(app => {
      const col = document.createElement("div");
      col.className = "col-lg-6";

      // Crear el enlace
      const link = document.createElement("a");
      link.className = "portfolio-item";
      link.href = app.url;
      link.target = "_blank";
      link.rel = "noopener noreferrer"; // Seguridad adicional

      // Crear el contenedor de texto
      const caption = document.createElement("div");
      caption.className = "caption";

      const captionContent = document.createElement("div");
      captionContent.className = "caption-content";

      const title = document.createElement("h2"); // Semántica mejorada
      title.textContent = app.title;

      // Crear imagen
      const image = document.createElement("img");
      image.className = "img-fluid";
      image.src = app.image;
      image.alt = `Captura de ${app.title}`; // Mejora de accesibilidad

      // Ensamblar estructura
      captionContent.appendChild(title);
      caption.appendChild(captionContent);
      link.appendChild(caption);
      link.appendChild(image);
      col.appendChild(link);
      container.appendChild(col);
    });
  } catch (err) {
    console.error("Error al renderizar apps:", err);
  }
}

// Ejecutar al cargar la página.
document.addEventListener("DOMContentLoaded", () => {
  renderAppsFromJSON("/data/apps.json"); // Ruta relativa al archivo JSON
});
