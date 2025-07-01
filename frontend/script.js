// Exemplo: Mostrar nome dos arquivos selecionados
document.getElementById("file").addEventListener("change", function () {
  const files = Array.from(this.files).map(file => file.name).join(", ");
  alert("Files selected: " + files);
});
