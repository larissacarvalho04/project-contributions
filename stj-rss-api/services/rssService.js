const Parser = require("rss-parser");
const parser = new Parser();

async function extrairNoticias() {
  const feed = await parser.parseURL("https://stj.jus.br/portal/arquivo-de-noticias/rss.xml");
  return feed.items.map((item) => ({
    title: item.title,
    contentSnippet: item.contentSnippet,
    link: item.link,
    pubDate: item.pubDate,
  }));
}

async function extrairUltimaNoticia() {
  const noticias = await extrairNoticias();
  return noticias[0]; 
}

module.exports = { extrairNoticias, extrairUltimaNoticia };