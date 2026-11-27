/**
 * Biblioteca privada — Direito UFPR
 * Executa como o usuário implantador e deve ser implantada com acesso MYSELF.
 * Nenhum token OAuth é enviado ao navegador.
 */

const CONFIG = {
  ROOT_FOLDER_PROPERTY: 'ROOT_FOLDER_ID',
  MAX_FILES: 3000,
  MAX_DEPTH: 8
};

function doGet() {
  return HtmlService.createHtmlOutputFromFile('Index')
    .setTitle('Biblioteca privada — Direito UFPR')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

function getCatalog() {
  const rootId = PropertiesService.getScriptProperties()
    .getProperty(CONFIG.ROOT_FOLDER_PROPERTY);

  if (!rootId) {
    throw new Error('A pasta-raiz ainda não foi configurada no projeto Apps Script.');
  }

  const root = DriveApp.getFolderById(rootId);
  const items = [];
  percorrerPasta_(root, [], items, 0);

  items.sort((a, b) =>
    a.caminho.localeCompare(b.caminho, 'pt-BR', { sensitivity: 'base' }) ||
    a.nome.localeCompare(b.nome, 'pt-BR', { sensitivity: 'base' })
  );

  return {
    pastaRaiz: root.getName(),
    total: items.length,
    materiais: items
  };
}

function percorrerPasta_(pasta, caminhoAtual, saida, profundidade) {
  if (profundidade > CONFIG.MAX_DEPTH) return;

  const caminho = caminhoAtual.concat(pasta.getName());
  const arquivos = pasta.getFiles();

  while (arquivos.hasNext()) {
    const arquivo = arquivos.next();
    if (arquivo.isTrashed()) continue;

    const mime = arquivo.getMimeType();
    const nome = arquivo.getName();
    const ehPdf = mime === MimeType.PDF || /\.pdf$/i.test(nome);
    if (!ehPdf) continue;

    if (saida.length >= CONFIG.MAX_FILES) {
      throw new Error('O catálogo excedeu o limite de segurança de ' +
        CONFIG.MAX_FILES + ' PDFs. Divida o acervo ou ajuste o limite.');
    }

    saida.push({
      id: arquivo.getId(),
      nome: nome,
      caminho: caminho.slice(1).join(' / '),
      disciplinaPasta: caminho[1] || '',
      unidadePasta: caminho[2] || '',
      assuntoPasta: caminho[3] || '',
      url: arquivo.getUrl(),
      atualizadoEm: arquivo.getLastUpdated().toISOString(),
      mimeType: mime
    });
  }

  const subpastas = pasta.getFolders();
  while (subpastas.hasNext()) {
    percorrerPasta_(subpastas.next(), caminho, saida, profundidade + 1);
  }
}
