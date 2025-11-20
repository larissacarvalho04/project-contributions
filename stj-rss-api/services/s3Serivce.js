const AWS = require("aws-sdk");
const { streamToString } = require("../utils/streamToString");

const s3 = new AWS.S3({
  region: process.env.AWS_REGION,
});

const BUCKET_NAME = process.env.S3_BUCKET_NAME;

async function salvarNoS3(nomeArquivo, dados) {
  try {
    await s3
      .putObject({
        Bucket: BUCKET_NAME,
        Key: nomeArquivo,
        Body: JSON.stringify(dados, null, 2), 
        ContentType: "application/json",
      })
      .promise();

    return {
      mensagem: "Arquivo salvo no S3 com sucesso!",
      nomeArquivo: nomeArquivo,
    };
  } catch (erro) {
    console.error("Erro ao salvar no S3:", erro);
    throw new Error("Falha ao salvar arquivo no S3");
  }
}

async function buscarNoticiasPorTermo(termo) {
  try {
    const objetos = await s3
      .listObjectsV2({ Bucket: BUCKET_NAME })    //listObjectsV2: Método do AWS SDK para listar arquivos em um bucket S3.
      .promise();

    const resultados = [];
    for (const objeto of objetos.Contents) {
      const dados = await s3
        .getObject({
          Bucket: BUCKET_NAME,
          Key: objeto.Key,
        })
        .promise();

      const conteudo = await streamToString(dados.Body);
      const noticias = JSON.parse(conteudo);

      noticias
        .filter((noticia) => {
          const termoLower = termo.toLowerCase();
          return (
            noticia.title.toLowerCase().includes(termoLower) ||
            (noticia.contentSnippet &&
              noticia.contentSnippet.toLowerCase().includes(termoLower))
          );
        })
        .forEach((noticia) => resultados.push(noticia));
    }

    return resultados;
  } catch (erro) {
    console.error("Erro ao buscar no S3:", erro);
    throw new Error("Falha ao consultar notícias no S3");
  }
}

module.exports = {
  salvarNoS3,
  buscarNoticiasPorTermo,
};