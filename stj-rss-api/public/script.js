async function buscarNoticias() {
  const termo = document.getElementById("termo").value.trim();
  if (!termo) return alert("Digite um termo para buscar!");

  try {
    const resposta = await fetch(`/api/consultar?termo=${encodeURIComponent(termo)}`);
    const noticias = await resposta.json();
    const resultadoDiv = document.getElementById("resultado");

    resultadoDiv.innerHTML = noticias.length === 0 
      ? "<p>Nenhuma notícia encontrada.</p>"
      : noticias.map(noticia => `
          <div class="card-noticia">
            <h3>${noticia.title}</h3>
            <p>${noticia.contentSnippet}</p>
            <p><strong>Data:</strong> ${noticia.pubDate}</p>
            <a href="${noticia.link}" target="_blank">Ler mais</a>
          </div>
        `).join("");
  } catch (erro) {
    alert("Erro ao buscar notícias.");
  }
}

async function atualizarNoticias() {
  try {
    const resposta = await fetch("/api/atualizar", { method: "POST" });
    const mensagem = await resposta.json();
    alert(mensagem.mensagem);
  } catch (erro) {
    alert("Erro ao atualizar notícias.");
  }
}

async function mostrarUltimaNoticia() {
  try {
    const resposta = await fetch("/api/ultima-noticia");
    const noticia = await resposta.json();
    document.getElementById("resultado").innerHTML = `
      <div class="card-noticia">
        <h3>${noticia.title}</h3>
        <p>${noticia.contentSnippet}</p>
        <p><strong>Data:</strong> ${noticia.pubDate}</p>
        <a href="${noticia.link}" target="_blank">Ler mais</a>
      </div>
    `;
  } catch (erro) {
    alert("Erro ao carregar última notícia.");
  }
}

document.getElementById("termo").addEventListener("keypress", (evento) => {
  if (evento.key === "Enter") buscarNoticias();
});