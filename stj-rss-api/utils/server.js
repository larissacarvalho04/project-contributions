const express = require("express");
const { extrairNoticias, extrairUltimaNoticia } = require("./services/rssService");
const { salvarNoS3, buscarNoticiasPorTermo } = require("./services/s3Service");

const app = express();
const PORT = 3000;

app.use(express.json());
app.use(express.static("../public"));

// Rotas

app.get("/api/consultar", async (req, res) => {            // Chama s3Service.js
  try {
    const { termo } = req.query;
    if (!termo) return res.status(400).json({ erro: "Parâmetro 'termo' obrigatório" });
    const resultados = await buscarNoticiasPorTermo(termo);
    res.json(resultados);
  } catch (erro) {
    res.status(500).json({ erro: "Erro ao buscar notícias" });
  }
});

app.post("/api/atualizar", async (req, res) => {
  try {
    const noticias = await extrairNoticias();
    await salvarNoS3(`noticias-${Date.now()}.json`, noticias);
    res.json({ mensagem: "Notícias atualizadas com sucesso!" });
  } catch (erro) {
    res.status(500).json({ erro: "Erro ao atualizar notícias" });
  }
});

app.get("/api/ultima-noticia", async (req, res) => {
  try {
    const noticia = await extrairUltimaNoticia();
    res.json(noticia);
  } catch (erro) {
    res.status(500).json({ erro: "Erro ao buscar última notícia" });
  }
});

app.listen(PORT, () => console.log(`Servidor rodando na porta ${PORT}`));