# Catálogo de materiais da Biblioteca

## Modelo adotado

- Google Drive é o repositório oficial dos PDFs.
- Os arquivos são compartilhados individualmente como **Qualquer pessoa com o link — Leitor**.
- O GitHub mantém somente metadados e URLs dos arquivos.
- A página `biblioteca.html` lê `dados/catalogo_materiais.json` e `dados/estrutura.json`.
- Não há upload de PDFs pelo site, nem Apps Script ou autenticação Google nesta versão.

## Como adicionar um material

1. Envie o PDF para a pasta adequada no Google Drive.
2. No Drive, abra **Compartilhar** e altere o acesso geral para **Qualquer pessoa com o link — Leitor**.
3. Copie o link do arquivo.
4. Abra `dados/catalogo_materiais.json` no GitHub e clique em editar.
5. Acrescente um objeto dentro do array `materiais`, usando o modelo:

```json
{
  "titulo": "Título do material",
  "disciplina": "Nome exato da disciplina conforme dados/estrutura.json",
  "disciplina_id": "id-da-disciplina",
  "categoria": "Texto de estudo",
  "descricao": "Descrição breve do conteúdo.",
  "assunto": "Assunto curricular, se aplicável",
  "arquivos": [
    "https://drive.google.com/file/d/ID_DO_ARQUIVO/view"
  ]
}
```

6. Salve a alteração no GitHub.
7. Aguarde a publicação do GitHub Pages e atualize a Biblioteca.

## Regras importantes

- `disciplina` deve corresponder ao nome em `dados/estrutura.json`; a página usa esse nome para vincular o material à disciplina.
- `disciplina_id` é mantido para futura associação curricular mais robusta.
- `arquivos` deve ser uma lista de URLs HTTPS do Google Drive. Um material pode ter mais de um PDF.
- Não inserir PDFs no repositório GitHub.
- Não usar links de pastas compartilhadas no lugar de links de arquivos.
- Não incluir senhas, tokens, documentos pessoais ou arquivos que não devam ser acessíveis a qualquer pessoa que obtenha o link.
- O link público permite acesso a quem o possuir e pode ser compartilhado por terceiros.
- Manter `documentos.json` apenas como legado vazio; a Biblioteca não deve mais depender dele.

## Limitações da primeira versão

- O cadastro é manual no JSON.
- A atualização automática do catálogo a partir do Drive não está implementada.
- A página exibe os PDFs cadastrados no catálogo; não percorre o Drive.
- A associação por `disciplina_id`, unidade e assunto poderá ser refinada em etapa posterior.
