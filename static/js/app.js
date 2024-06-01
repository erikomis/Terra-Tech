
// function downloadApp() {
//   const filename = "terra-tech.1.6.0.apk"; // Nome do arquivo a ser baixado
//   const loadingIndicator = document.getElementById("loadingIndicator");
//   const downloadBtn = document.getElementById("downloadBtn");

//   // Desabilitar o botão de download enquanto estiver processando o download
//   downloadBtn.disabled = true;
//   downloadBtn.style.cursor = "not-allowed";

//   // Mostrar o indicador de carregamento
//   loadingIndicator.style.display = "inline-block";

//   fetch(`/download/${filename}`)
//     .then((response) => {
//       if (!response.ok) {
//         throw new Error("Network response was not ok");
//       }
//       return response.blob();
//     })
//     .then((blob) => {
//       const url = window.URL.createObjectURL(blob);
//       const a = document.createElement("a");
//       a.style.display = "none";
//       a.href = url;
//       a.download = filename;
//       document.body.appendChild(a);
//       a.click();
//       window.URL.revokeObjectURL(url);

//       // Ocultar o indicador de carregamento após o download
//       loadingIndicator.style.display = "none";

//       // Habilitar o botão de download novamente
//       downloadBtn.disabled = false;
//       downloadBtn.style.cursor = "pointer";
//     })
//     .catch((err) => {
//       console.error("Download failed:", err);
//       // Ocultar o indicador de carregamento em caso de erro
//       loadingIndicator.style.display = "none";
//       // Habilitar o botão de download novamente em caso de erro
//       downloadBtn.disabled = false;
//       downloadBtn.style.cursor = "pointer";
//     });
// }


function downloadApp() {
  const filename = "terra-tech.apk"; // Nome do arquivo a ser baixado
  const loadingIndicator = document.getElementById("loadingIndicator");
  const downloadBtn = document.getElementById("downloadBtn");
  const errorMessage = document.getElementById("errorMessage"); // Elemento para mostrar mensagens de erro
  const TIMEOUT_DURATION = 30000; // 30 segundos de timeout

  // Desabilitar o botão de download enquanto estiver processando o download
  downloadBtn.disabled = true;
  downloadBtn.style.cursor = "not-allowed";

  // Mostrar o indicador de carregamento
  loadingIndicator.style.display = "inline-block";
  errorMessage.style.display = "none"; // Ocultar mensagem de erro

  const controller = new AbortController();
  const signal = controller.signal;

  const timeout = setTimeout(() => {
    controller.abort();
    errorMessage.textContent = "Tempo de espera excedido. Por favor, tente novamente.";
    errorMessage.style.display = "block";
    // Ocultar o indicador de carregamento em caso de timeout
    loadingIndicator.style.display = "none";
    // Habilitar o botão de download novamente em caso de timeout
    downloadBtn.disabled = false;
    downloadBtn.style.cursor = "pointer";
  }, TIMEOUT_DURATION);

  fetch(`/download/`, { signal })
    .then((response) => {
      console.log(timeout);
      console.log(signal);
      console.log(response);
      clearTimeout(timeout); // Limpar o timeout se a resposta for recebida a tempo
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
      downloadBtn.style.cursor = "pointer";
    })
    .catch((err) => {
      if (err.name === 'AbortError') {
        console.error("Download aborted due to timeout");
      } else {
        console.error("Download failed:", err);
        errorMessage.textContent = "Falha no download. Por favor, tente novamente.";
        errorMessage.style.display = "block";
      }
      // Ocultar o indicador de carregamento em caso de erro
      loadingIndicator.style.display = "none";
      // Habilitar o botão de download novamente em caso de erro
      downloadBtn.disabled = false;
      downloadBtn.style.cursor = "pointer";
    });
}
