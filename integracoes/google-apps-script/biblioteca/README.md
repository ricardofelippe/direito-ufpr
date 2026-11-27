# Biblioteca privada — Google Apps Script

## Objetivo

Servir uma interface privada de consulta aos PDFs de uma pasta do Google Drive. O projeto não compartilha arquivos, não altera permissões e não faz upload, substituição ou exclusão. A implantação deve permanecer restrita ao usuário implantador.

## Arquitetura

- Google Drive: repositório oficial dos arquivos.
- Apps Script: consulta a pasta privada sob a identidade do usuário implantador.
- Interface HTML: busca e lista PDFs; abre cada arquivo no Google Drive.
- GitHub Pages: continua hospedando o restante do sistema. Não recebe tokens OAuth, IDs de arquivos privados nem uma cópia pública do catálogo.

## Instalação inicial

1. Entre na conta Google que possui acesso ao acervo.
2. Abra https://script.google.com/ e crie um projeto independente chamado **Biblioteca privada — Direito UFPR**.
3. No editor, crie um arquivo de script chamado `Code.gs` e copie o conteúdo deste repositório.
4. Crie um arquivo HTML chamado `Index` e copie o conteúdo de `Index.html`.
5. Em Configurações do projeto, habilite a exibição do arquivo de manifesto `appsscript.json`; substitua o manifesto pelo deste diretório.
6. Identifique a pasta-raiz do acervo no Drive. Copie somente o ID que aparece entre `/folders/` e o próximo separador na URL.
7. No editor, selecione a função `configurarPastaRaiz`, informe o ID da pasta e execute uma única vez. Autorize o acesso solicitado. O ID fica em Propriedades do script, não no HTML nem no repositório.
8. Execute `getCatalog` no editor e confirme que a lista retornada corresponde aos PDFs do acervo.
9. Selecione **Implantar → Nova implantação → App da Web**.
10. Configure **Executar como: Eu** e **Quem pode acessar: Somente eu**. Não selecione acesso para qualquer pessoa.
11. Implante, copie a URL terminada em `/exec` e guarde-a. Não publique a URL em páginas ou repositórios públicos.
12. Teste a URL em uma janela autenticada na conta autorizada. Teste também em uma janela sem essa conta: o acesso deve ser negado.

## Estrutura esperada

A rotina percorre a pasta-raiz e suas subpastas, em até oito níveis, listando arquivos PDF. A primeira pasta abaixo da raiz é exibida como agrupamento principal; os níveis seguintes aparecem como caminho. Assim, a organização existente no Drive é preservada sem impor nomes de pastas ainda não confirmados.

## Segurança

- Implantação privada: `access: MYSELF`.
- Execução como usuário implantador: `executeAs: USER_DEPLOYING`.
- Escopo de leitura do Drive; nenhuma permissão de escrita é solicitada.
- Nenhum token OAuth é transmitido ao navegador.
- Não usar links de compartilhamento público nem alterar permissões dos arquivos.
- A interface não faz upload, edição, movimentação, exclusão ou compartilhamento.
- Não armazenar a URL privada da implantação em arquivo público do GitHub.

## Limitações e validações pendentes

- A pasta-raiz e a estrutura real de subpastas ainda precisam ser confirmadas pelo usuário.
- A rotina lista PDFs; outros tipos de documento não são exibidos nesta primeira versão.
- A associação curricular por IDs de disciplina/unidade/assunto ainda não foi automatizada. Nesta primeira etapa, a classificação visual usa os nomes e caminhos das pastas do Drive.
- A integração com a página pública GitHub Pages não é feita por iframe ou endpoint público. O acesso inicial ocorre pela URL privada do Apps Script.
- Validar o comportamento com o acervo real antes de considerar a Biblioteca pronta para uso contínuo.
