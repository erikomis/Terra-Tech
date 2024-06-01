
function downloadApp() {
  const filename = "terra-tech.1.6.0.apk"; // Nome do arquivo a ser baixado
  const loadingIndicator = document.getElementById("loadingIndicator");
  const downloadBtn = document.getElementById("downloadBtn");

  // Desabilitar o botão de download enquanto estiver processando o download
  downloadBtn.disabled = true;
  downloadBtn.style.cursor = "not-allowed";

  // Mostrar o indicador de carregamento
  loadingIndicator.style.display = "inline-block";

  fetch(`/download/${filename}`)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.blob();
    })
    .then((blob) => {
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.style.display = "none";
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);

      // Ocultar o indicador de carregamento após o download
      loadingIndicator.style.display = "none";

      // Habilitar o botão de download novamente
      downloadBtn.disabled = false;
    })
    .catch((err) => {
      console.error("Download failed:", err);
      // Ocultar o indicador de carregamento em caso de erro
      loadingIndicator.style.display = "none";
      // Habilitar o botão de download novamente em caso de erro
      downloadBtn.disabled = false;
    });
}
