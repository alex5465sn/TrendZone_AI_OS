# -*- coding: utf-8 -*-
"""Conteudo textual de cada pagina do TrendZone AI OS (fonte: codigo atual)."""
from gerar_apresentacao import add_page, build_pdf

add_page(
    1, "Login", "/login",
    "Tela publica de autenticacao (nao aparece no menu lateral).",
    "Formulario simples de acesso ao sistema, com logotipo, campos de credenciais e link para criacao de conta.",
    [
        "Campo <b>Email</b>.",
        "Campo <b>Senha</b> (oculta).",
        "Botao <b>Entrar</b>  -  autentica e redireciona para o Painel (/dashboard). Mostra spinner de carregamento enquanto processa.",
        "Mensagem de erro em vermelho caso email/senha estejam incorretos ou vazios.",
        "Link <b>Registre-se</b>  -  leva para a tela de Registro.",
    ],
)

add_page(
    2, "Registro", "/register",
    "Tela publica de criacao de conta (nao aparece no menu lateral).",
    "Formulario de cadastro de novo usuario na plataforma.",
    [
        "Campo <b>Nome Completo</b>.",
        "Campo <b>Email</b>.",
        "Campo <b>Empresa (opcional)</b>.",
        "Campo <b>Senha</b> (minimo de 6 caracteres).",
        "Botao <b>Registrar</b>  -  cria a conta e redireciona para a tela de Login. Exibe spinner durante o processo.",
        "Validacoes: nome/email/senha obrigatorios; senha com no minimo 6 caracteres.",
        "Link <b>Faca login</b>  -  volta para a tela de Login.",
    ],
)

add_page(
    3, "Painel", "/dashboard",
    "Painel de Controle  -  visao geral do sistema ao entrar na plataforma.",
    "Tela inicial com indicadores gerais, personalizacao de widgets, produtos em destaque da Shopee e status de saude do sistema.",
    [
        "Numero da versao do sistema exibido no topo (ex: v2.0).",
        "Botao de icone <b>Personalizar painel</b> (engrenagem/regulagem)  -  abre menu com checkboxes para ligar/desligar cada widget da tela (Produtos Rastreados, Pipeline IA, Status do Sistema, Shopee API, Produtos em Destaque, Saude do Sistema). Preferencia salva no navegador.",
        "Cartao <b>Produtos Rastreados</b>  -  total de produtos no tracker.",
        "Cartao <b>Pipeline IA</b>  -  indicador do funil de vendas.",
        "Cartao <b>Status do Sistema</b>.",
        "Cartao <b>Shopee API</b>  -  mostra se ha produtos carregados ou se esta pronta para carregar.",
        "Bloco <b>Produtos em Destaque - Shopee</b>: botao <b>Carregar produtos</b> (busca produtos em tendencia na Shopee) e botao <b>Ver todos</b> (leva para a pagina Produtos). Tabela com Produto, Preco, Comissao, Vendas e botao <b>Oferta</b> (abre o link do produto em nova aba).",
        "Bloco <b>Saude do Sistema</b>  -  lista de indicadores de saude (status de cada integracao/servico).",
    ],
)

add_page(
    4, "Produtos", "/products",
    "Produtos Shopee.",
    "Busca de produtos em tempo real na Shopee para identificar oportunidades de afiliados.",
    [
        "Campo de busca por palavra-chave (ex: fone de ouvido, smartwatch, bolsas).",
        "Botao <b>Buscar</b>  -  pesquisa produtos na Shopee pela palavra-chave.",
        "Chips de <b>categorias</b>  -  atalhos que preenchem a busca automaticamente por categoria (eletronicos, moda, casa, etc.).",
        "Cartao <b>Produtos Encontrados</b>  -  contagem de resultados.",
        "Cartao <b>Maior Comissao</b>  -  maior percentual de comissao entre os resultados.",
        "Cartao <b>Melhor Avaliacao</b>  -  maior nota entre os resultados.",
        "Tabela de produtos (componente ShopeeProductTable) com botao para <b>adicionar</b> cada produto ao tracker interno (rastreamento de produtos).",
    ],
)

add_page(
    5, "Scout IA", "/scout",
    "Analise inteligente de produtos da Shopee com scoring automatico  -  a pagina mais completa do sistema.",
    "Motor de descoberta e divulgacao de produtos: busca, pontuacao por IA, geracao de posts, geracao de video, publicacao no Facebook e agendamento automatico de publicacoes.",
    [
        "Campo de busca por palavra-chave + botao <b>Analisar</b>  -  busca ate 50 produtos na Shopee e calcula o Score IA de cada um (combina vendas, avaliacao, comissao e desconto ativo), mostrando os 10 melhores.",
        "Cartao <b>Agendamento Automatico de Posts</b>: botao <b>Gerar agendamento agora</b>  -  a IA agenda automaticamente cerca de 5 posts por dia em horarios de pico, sempre escolhendo produtos diferentes dos usados nos ultimos 30 dias. Lista os proximos posts pendentes com botao <b>Cancelar</b> em cada um.",
        "Botoes de <b>categorias</b> (selecao multipla) + botao <b>Encontrar Produtos Campeoes</b>  -  a IA varre todas as categorias selecionadas (ou todas, se nenhuma marcada) em busca dos produtos com melhor pontuacao, mostrando os 20 melhores.",
        "Cada card de produto mostra: imagem, nome, selo de decisao (<b>PROMOVER</b>/<b>TESTAR</b>/<b>OBSERVAR</b>/<b>DESCARTAR</b> conforme o Score), Score IA, percentual de Comissao, numero de Vendas e preco.",
        "Botao <b>Ver</b>  -  abre o link da oferta na Shopee em nova aba.",
        "Botao <b>Analisar (TCIE)</b>  -  roda a analise comercial inteligente (Testador de Comercializacao e Inteligencia Economica): calcula lucro liquido estimado, margem, ROI, preco ideal e preco minimo viavel, com decisao final (ESCALAR/TESTAR/AJUSTAR/MATAR).",
        "Botao <b>Gerar Post</b>  -  cria automaticamente um texto de divulgacao para Facebook (com link de rastreamento proprio) e abre um alerta com o texto pronto.",
        "Dentro do alerta de post gerado: botao <b>Copiar</b> (copia o texto), botao <b>Postar no Facebook</b> (publica diretamente na pagina configurada  -  pergunta confirmacao se o produto ja foi postado antes), botao <b>Gerar Video</b> (cria um video automatico do produto a partir da imagem, preco e desconto), botao <b>Postar Video no Facebook</b> (aparece apos gerar o video) e botao <b>Agendar</b> (pede data/hora e cria um agendamento de publicacao).",
        "Botao <b>Adicionar</b>  -  adiciona o produto ao tracker interno (Produtos).",
    ],
    notas="Se a publicacao automatica no Facebook nao estiver configurada (FACEBOOK_PAGE_ID/FACEBOOK_PAGE_TOKEN no servidor), o sistema avisa e desabilita os botoes de postagem direta.",
)

add_page(
    6, "Analises", "/analytics",
    "Analises & Metricas.",
    "Painel de graficos e indicadores consolidados sobre os produtos rastreados.",
    [
        "Cartao <b>Score Medio</b> dos produtos.",
        "Cartao <b>Comissao Total</b> acumulada.",
        "Cartao <b>Avaliacao Media</b> dos produtos.",
        "Grafico de pizza <b>Distribuicao de Scores</b> (faixas 0-39, 40-59, 60-79, 80-100).",
        "Grafico de barras <b>Distribuicao de Comissoes</b> (faixas de 0-5% ate 20%+).",
        "Grafico de barras <b>Top 10 Produtos por Score</b> (comparando score e comissao).",
        "Grafico de linha <b>Vendas por Avaliacao</b> (faixas de nota de 0-2.9 ate 4.5-5.0).",
    ],
)

add_page(
    7, "Oportunidades", "/opportunities",
    "Oportunidades de Venda.",
    "A IA analisa os produtos monitorados e sugere conteudo de divulgacao pronto; o usuario revisa, copia ou salva e publica manualmente onde preferir.",
    [
        "Aba <b>Sugestoes da IA</b>: lista de oportunidades geradas automaticamente, cada uma com selo de decisao (PROMOVER/TESTAR), Score, titulo e legenda sugeridos, hashtags, publico-alvo e canal sugerido.",
        "Botao <b>Copiar</b>  -  copia o conteudo completo (titulo, legenda, hashtags e link) para a area de transferencia.",
        "Botao <b>Salvar</b>  -  salva a sugestao como uma campanha em rascunho (aba Campanhas Salvas).",
        "Aba <b>Campanhas Salvas</b>: lista das campanhas ja salvas, com selo de status (rascunho/publicada).",
        "Botao <b>Marcar publicada</b>  -  muda o status da campanha para publicada.",
        "Botao <b>Remover</b>  -  exclui a campanha salva.",
        "Aviso quando nao ha oportunidades ou campanhas disponiveis.",
    ],
)

add_page(
    8, "Prospeccao", "/prospects",
    "Prospeccao de Nichos.",
    "A IA analisa os produtos cadastrados, agrupa por nicho de mercado e classifica cada um em quente, morno ou frio, com dossie e sugestao de abordagem  -  alem de permitir agendar prospeccoes automaticas.",
    [
        "Aba <b>Nichos Prospectados</b>: campo de filtro por nicho + botao <b>Buscar</b> (icone de lupa)  -  roda a prospeccao e lista os nichos encontrados.",
        "Cada card de nicho traz: selo de temperatura (quente/morno/frio, com icones de chama/sol/floco de neve), quantidade de produtos, preco medio, comissao media, total de vendas, texto de abordagem sugerida pela IA e canal de divulgacao sugerido.",
        "Botao <b>Marcar contatado</b>  -  atualiza o status do nicho para contatado (some depois de marcado).",
        "Botao <b>Remover</b>  -  exclui o registro do nicho prospectado.",
        "Aba <b>Agendamentos</b>: botao <b>Novo Agendamento</b>  -  abre dialogo para a IA prospectar automaticamente em um horario definido.",
        "Dialogo <b>Novo Agendamento</b>: campos Nicho, Horario (HH:MM) e Quantidade de leads; botoes Cancelar/Criar.",
        "Cada agendamento exibe nicho, cidade (se houver), horario, dias configurados, quantidade e data da ultima execucao, alem de botao <b>Remover</b>.",
    ],
)

add_page(
    9, "Vendas & Comissoes", "/sales",
    "Acompanhamento financeiro das vendas realizadas pelos links de afiliado.",
    "Painel financeiro com sincronizacao direta com a Shopee e rastreamento de desempenho por campanha.",
    [
        "Aba <b>Painel Financeiro</b>: botao <b>Sincronizar com Shopee</b>  -  busca as vendas/conversoes mais recentes diretamente na API da Shopee.",
        "Cartoes de resumo: <b>Total de Vendas</b>, <b>Comissao Total</b>, <b>Pendente</b> (valor e quantidade aguardando confirmacao) e <b>Disponivel para Saque</b> (valor ja confirmado).",
        "Tabela <b>Historico de Vendas</b>: numero do pedido, status (confirmada/pendente/cancelada, com cores), data da compra, dispositivo usado, comissao total e comissao liquida.",
        "Aba <b>Rastreamento de Campanhas</b>: lista de campanhas com link de rastreamento proprio, mostrando status, canal, link gerado, cliques, conversoes e receita.",
    ],
)

add_page(
    10, "Contas de Afiliado", "/accounts",
    "Contas de Afiliado.",
    "Central de conexao das contas de afiliado de cada marketplace (Shopee, Mercado Livre, Amazon, AliExpress, Magalu, TikTok Shop), usadas para rastrear vendas e gerar links proprios.",
    [
        "Lista de <b>contas conectadas</b>, cada uma com selo de status (Conectada/erro) e informacao se o token de acesso esta armazenado.",
        "Botao <b>Desconectar</b> em cada conta conectada (pede confirmacao antes de remover).",
        "Tabela <b>Marketplaces disponiveis</b>: nome do marketplace, status (conectada ou nao) e botao <b>Conectar</b> (se ainda nao conectado) ou <b>Atualizar</b> (se ja conectado, para trocar as credenciais).",
        "Dialogo de <b>Conectar/Atualizar</b>: campos App ID e Secret (senha oculta) da conta de afiliado; botoes Cancelar/Conectar. As credenciais sao armazenadas de forma criptografada.",
        "Dialogo de confirmacao de <b>Desconexao</b>: aviso de que as vendas ja registradas permanecem no historico mesmo apos desconectar.",
        "Link direto para o Portal do Afiliado Shopee, com instrucao de onde encontrar as credenciais (Open API -> Application).",
    ],
)

add_page(
    11, "Funil de Vendas", "/funnel",
    "Kanban para gerenciar o ciclo de vida dos seus produtos.",
    "Quadro estilo Kanban com colunas (estagios) por onde os produtos avancam, do primeiro contato ate a venda.",
    [
        "Botao <b>Sincronizar com IA</b>  -  a IA cria automaticamente cards no funil a partir dos dados existentes (produtos, prospeccoes, etc.).",
        "Selo de <b>oportunidades paradas</b>  -  alerta quantos cards estao parados ha muito tempo em um estagio (radar de estagnacao).",
        "Botao de icone <b>+</b> em cada coluna  -  abre o dialogo para criar um novo card diretamente naquele estagio.",
        "Cards podem ser <b>arrastados</b> (drag and drop) entre colunas para mudar de estagio.",
        "Cada card mostra titulo, descricao resumida, selo de prioridade (Alta/Media/Baixa), receita estimada (se informada) e canal (se informado); botao de icone <b>excluir</b> em cada card.",
        "Dialogo <b>Novo Card</b>: campos Titulo, Descricao, Prioridade (Alta/Media/Baixa), Receita Estimada (R$), Canal (ex: Pinterest, WhatsApp, Shopee Video) e Notas; botoes Cancelar/Criar.",
    ],
)

add_page(
    12, "Descoberta", "/discovery",
    "Descoberta de Produtos  -  estrategia 'Loophole': encontrar produtos emergentes com alta comissao e baixa concorrencia.",
    "Quatro modos de descoberta de produtos, organizados em abas.",
    [
        "Aba <b>Emergentes</b>  -  produtos novos ganhando tracao, marcados com o selo EMERGENTE.",
        "Aba <b>Trending</b>  -  produtos em alta no momento, marcados com o selo TRENDING.",
        "Aba <b>Alta Comissao</b>  -  produtos com os maiores percentuais de comissao, marcados com o selo ALTA COMISSAO.",
        "Aba <b>Recomendacoes IA</b>  -  combina tres blocos gerados pela IA: Emergentes, Top Performers e Alta Comissao, todos na mesma tela.",
        "Cada card de produto mostra imagem, nome, preco, percentual de comissao, avaliacao (estrelas), numero de vendas, Score (quando aplicavel) e Indice de Oportunidade  -  OI (quando aplicavel).",
    ],
)

add_page(
    13, "Conteudo IA", "/content-strategy",
    "Estrategias de Conteudo  -  gere scripts prontos para video, post e blog otimizados por plataforma.",
    "Gerador de estrategias de conteudo por produto e por plataforma de divulgacao, com fluxo de producao (rascunho, em producao, publicado).",
    [
        "Botao <b>Gerar Estrategias</b>  -  abre dialogo para escolher o produto e as plataformas.",
        "Dialogo <b>Gerar Estrategias de Conteudo</b>: selecao do Produto e chips de selecao multipla de plataformas (Shopee Video, Pinterest, WhatsApp, Facebook, Instagram, TikTok, Blog-SEO); botoes Cancelar/Gerar.",
        "Chips de <b>filtro por plataforma</b> na listagem: Todos, Shopee Video, Pinterest, WhatsApp, Facebook, Instagram, TikTok, Blog-SEO.",
        "Cada estrategia aparece como um item expansivel (accordion) com selo de plataforma, titulo e selo de status (Rascunho/Em Producao/Publicado/Arquivado).",
        "Ao expandir, mostra: <b>Script/Roteiro</b> (com botao para copiar), <b>Hashtags</b>, <b>CTA</b> (chamada para acao) e <b>Melhores Horarios</b> para publicar  -  cada bloco aparece apenas se a IA gerou aquele conteudo.",
        "Botoes de mudanca de status: <b>Em Producao</b> e <b>Publicado</b> (avancam o status da estrategia) e botao de <b>excluir</b>.",
        "Estado vazio: mensagem convidando a clicar em 'Gerar Estrategias' para comecar.",
    ],
)

add_page(
    14, "Follow-ups", "/follow-ups",
    "Follow-ups & Radar  -  nunca perca uma oportunidade: acompanhe cada acao pendente.",
    "Lista de lembretes e tarefas de acompanhamento (follow-ups) criados manualmente ou pelas automacoes.",
    [
        "Botao <b>Novo Follow-up</b>  -  abre dialogo de criacao.",
        "Alerta de aviso quando ha follow-ups atrasados, informando quantos precisam de acao.",
        "Cada card mostra: selo de prioridade (Alta/Media/Baixa), selo de status (concluido em verde), mensagem, data limite (com indicacao de quantos dias em atraso, se aplicavel).",
        "Botao de icone <b>concluir</b> (marca como feito, desaparece do card apos concluido) e botao de icone <b>excluir</b>.",
        "Dialogo <b>Novo Follow-up</b>: campos Mensagem (varias linhas), Data limite (data e hora) e Prioridade (Alta/Media/Baixa); botoes Cancelar/Criar.",
        "Estado vazio: 'Nenhum follow-up registrado.'",
    ],
)

add_page(
    15, "Canais & SubIDs", "/channels",
    "Canais & SubID Tracking  -  rastreie performance por canal com SubIDs unicos.",
    "Ferramenta de rastreamento de desempenho de links de afiliado organizados por canal e SubID (identificador de sub-campanha).",
    [
        "Botao <b>Novo Tracking</b>  -  abre dialogo de criacao.",
        "Secao <b>Resumo por Canal</b>: um card por canal (Shopee Video, Pinterest, WhatsApp, Facebook, Instagram, TikTok, Blog, Telegram) com barra de progresso da receita total, alem de cliques, conversoes e CTR (taxa de cliques).",
        "Tabela <b>Links de Rastreamento</b>: Canal, SubID, Cliques, Conversoes, Receita, CTR e botao de icone <b>excluir</b> em cada linha.",
        "Dialogo <b>Novo Tracking de Canal</b>: selecao do Canal, campo SubID (ex: Pin_12345, WA_grupo1) e campo URL de Rastreamento; botoes Cancelar/Criar.",
    ],
)

add_page(
    16, "Calendario Sazonal", "/seasonal",
    "Planeje campanhas com antecedencia para datas estrategicas.",
    "Calendario de datas comemorativas, sazonais e de marketplace, com contagem regressiva para planejar campanhas.",
    [
        "Botao <b>Carregar Datas Padrao</b>  -  preenche automaticamente o calendario com datas comemorativas brasileiras e datas Shopee.",
        "Botao <b>Novo Evento</b>  -  abre dialogo para cadastrar um evento manualmente.",
        "Cada card de evento mostra: selo de categoria (comemorativa/sazonal/marketplace), selo de status, indicador 'EM PREPARACAO' quando aplicavel, nome do evento, data, contagem regressiva 'Faltam N dias' com barra de progresso colorida conforme a urgencia (vermelho ≤7 dias, laranja ≤30 dias, azul ≤60 dias, verde acima disso), nichos relevantes.",
        "Botao de icone <b>Ativar</b>  -  muda o evento para status ativo.",
        "Botao de icone <b>excluir</b>.",
        "Dialogo <b>Novo Evento Sazonal</b>: campos Nome do evento, Data, Categoria (ex: comemorativa, sazonal, marketplace), Nichos relevantes e Notas de estrategia; botoes Cancelar/Criar.",
        "Estado vazio traz tambem o botao 'Carregar Calendario Padrao (Datas BR + Shopee)'.",
    ],
)

add_page(
    17, "Automacoes", "/automation",
    'Regras de Automacao  -  motor QUANDO / SE / ENTAO ("nada morre no silencio").',
    "Motor de regras que automatiza acoes na plataforma (criar follow-ups, mudar status, notificar) com base em gatilhos, alem de um modo em que a propria IA decide as acoes necessarias.",
    [
        "Botao <b>Deixar a IA Decidir</b>  -  a IA avalia toda a base e executa sozinha as acoes que julgar necessarias, avisando quantas acoes foram tomadas (ou que nao ha nada pendente).",
        "Botao <b>Executar Regras</b>  -  roda manualmente todas as regras de automacao cadastradas e ativas.",
        "Botao <b>Nova Regra Manual</b>  -  abre dialogo para criar uma regra personalizada.",
        "Cada regra aparece em um card com nome, interruptor para ativar/desativar, descricao do gatilho (QUANDO), da acao (ENTAO) e contador de quantas vezes ja disparou; botao de icone <b>excluir</b>.",
        "Dialogo <b>Nova Regra de Automacao</b>: campo Nome da regra, selecao do gatilho (QUANDO), campo de dias (quando o gatilho envolve tempo parado), selecao da acao (ENTAO) e campos que aparecem conforme a acao escolhida  -  Mensagem e Prioridade (para criar follow-up ou notificar), Novo status (para mudar status do prospect) ou Nova temperatura (Quente/Morno/Frio); botoes Cancelar/Criar.",
    ],
)

add_page(
    18, "Grupos de Divulgacao", "/divulgation-groups",
    "Gere o texto com IA e publique manualmente nos seus grupos de WhatsApp e Facebook.",
    "Ferramenta que gera textos de divulgacao com IA e organiza os grupos de WhatsApp/Facebook onde o usuario publica manualmente (a plataforma nao publica sozinha nesses grupos por limitacao das proprias redes).",
    [
        "Botao <b>Cadastrar Grupo</b>  -  abre dialogo para registrar um novo grupo.",
        "Fluxo guiado em 3 passos: 1) Gere seu texto com IA, 2) Escolha o grupo e copie, 3) Cole e publique.",
        "Passo 1: selecao do Produto, selecao do Tom do texto (Oferta direta/Storytelling/Humor/Urgencia) e botao <b>Gerar texto com IA</b>; a previa do texto aparece com botao <b>Copiar texto</b>.",
        "Passo 2: campo de busca de grupo por nome ou categoria; chips de filtro por plataforma (Todos/WhatsApp/Facebook).",
        "Cada card de grupo mostra icone da plataforma, nome, categoria, melhor horario sugerido para postar, e botoes de icone <b>editar</b> e <b>excluir</b>.",
        "Botoes <b>Copiar</b> e <b>Publicar</b> em cada grupo (ficam desabilitados ate que um texto seja gerado): no WhatsApp, 'Publicar' abre o link direto do grupo (wa.me) ja com o texto preenchido; no Facebook, copia o texto e abre o grupo em nova aba para colar manualmente.",
        "Dialogo <b>Cadastrar/Editar Grupo de Divulgacao</b>: campos Nome do grupo, Plataforma (WhatsApp/Facebook), Categoria, Link do grupo (opcional), Melhor horario (ex: 19h-21h) e Numero de membros (opcional); botoes Cancelar/Salvar.",
    ],
)

add_page(
    19, "Log de Auditoria", "/audit-log",
    "Historico de todas as acoes realizadas na plataforma.",
    "Tela somente leitura que registra tudo o que acontece no sistema, para fins de rastreabilidade.",
    [
        "Selecao <b>Filtrar por entidade</b>  -  permite ver apenas os registros de um tipo especifico (Todas ou um tipo dinamico conforme os dados existentes).",
        "Tabela com Data, Entidade, Acao (selo colorido: CREATE em verde, UPDATE em azul, DELETE em vermelho, MOVE em laranja, TRIGGER em roxo) e Descricao detalhada do evento.",
        "Mensagem informativa quando nao ha registros.",
    ],
)

add_page(
    20, "Vocabulario", "/vocabulary",
    "Personalize os termos usados na plataforma para o seu segmento (ex: Lead/Paciente/Comprador).",
    "Permite trocar a terminologia exibida em toda a plataforma para se adequar ao nicho de negocio do usuario (ex: uma clinica pode preferir 'Paciente' em vez de 'Lead').",
    [
        "Chips de <b>presets</b> prontos  -  aplicam um conjunto de termos de uma so vez para nichos comuns.",
        "Campos editaveis: Nome do Nicho, Termo para 'Lead', Termo para 'Prospect', Termo para 'Cliente', Termo para 'Oportunidade', Termo para 'Quente' e Termo para 'Frio'.",
        "Botao <b>Salvar Vocabulario</b>  -  grava as personalizacoes para uso em toda a plataforma.",
    ],
)

add_page(
    21, "WhatsApp", "/whatsapp",
    "Conexao com o WhatsApp via WAHA (self-hosted). Escaneie o QR Code para conectar seu numero.",
    "Central de conexao e conversa via WhatsApp, integrada a um servidor proprio (WAHA).",
    [
        "Aviso automatico caso o servidor WAHA esteja inacessivel.",
        "Cartao de status da sessao (conectado/desconectado), numero de telefone conectado e ultimo erro registrado (se houver).",
        "Botao <b>Conectar / Gerar QR Code</b>  -  inicia a sessao e exibe o QR Code para ser escaneado no celular.",
        "Botao <b>Desconectar</b>  -  encerra a sessao do WhatsApp conectado.",
        "Layout de duas colunas: lista de <b>Conversas</b> (clicavel, a esquerda) e painel de <b>Mensagens</b> (a direita) com bolhas de chat diferenciando mensagens enviadas e recebidas  -  mensagens respondidas automaticamente pelo agente de IA sao identificadas com uma legenda propria.",
        "Campo de mensagem + botao <b>Enviar</b>  -  envia uma mensagem manualmente pela conversa selecionada.",
        "A tela atualiza status e conversas automaticamente a cada 8 segundos.",
    ],
)

add_page(
    22, "Agente de IA", "/ai-agent",
    "Configure o agente que pode responder automaticamente as conversas do WhatsApp.",
    "Configuracao e teste do assistente de IA que pode atender clientes automaticamente pelo WhatsApp.",
    [
        "Aviso quando o provedor de IA selecionado nao tem chave de API configurada no servidor.",
        "Interruptor <b>Agente Ativo</b>  -  liga/desliga o agente de IA.",
        "Interruptor <b>Responder automaticamente no WhatsApp</b>  -  permite que o agente responda sozinho as mensagens recebidas.",
        "Selecao do <b>Provedor de IA</b> e do <b>Modelo</b> (a lista de modelos muda conforme o provedor escolhido).",
        "Campo <b>Prompt de Sistema (personalidade do agente)</b>  -  define como o agente deve se comportar e responder.",
        "Botao <b>Salvar Configuracao</b>.",
        "Bloco <b>Testar Agente</b>: chips de perguntas rapidas prontas (ex: calculo de margem, restricoes de politica da Shopee, sugestao de cupom) que preenchem o campo de teste ao clicar.",
        "Campo <b>Mensagem de teste</b> + botao <b>Testar</b>  -  envia a mensagem de teste para o agente (sem enviar de verdade pelo WhatsApp) e mostra a resposta gerada logo abaixo.",
    ],
)

add_page(
    23, "Inspetor", "/inspector",
    "Inspetor da Plataforma  -  funcionalidade restrita a administradores.",
    "Ferramenta de diagnostico tecnico que varre codigo, importacoes, banco de dados, logs e configuracoes do sistema em busca de problemas, corrigindo automaticamente o que for possivel.",
    [
        "Botao <b>Executar Inspecao Completa</b>  -  dispara a varredura completa (exige permissao de administrador).",
        "Quatro cartoes de estatistica apos a inspecao: contagem de Erros, Avisos e Verificacoes realizadas, com icone de status.",
        "Lista <b>Relatorio Detalhado</b>: cada item mostra icone/selo de severidade (erro/aviso/informacao), arquivo e linha correspondente, selo <b>CORRIGIDO</b> quando o proprio sistema corrigiu automaticamente o problema, alem da mensagem e detalhe da correcao aplicada.",
    ],
)

add_page(
    24, "Configuracoes", "/settings",
    "Ajuste as preferencias do Scout IA e do bot de divulgacao.",
    "Tela de preferencias gerais do usuario, guardadas localmente no navegador.",
    [
        "Painel <b>Categorias favoritas para o Scout IA</b>: lista de checkboxes com todas as categorias de produto disponiveis, usada para filtrar buscas automaticas no Scout IA.",
        "Painel <b>Metas e divulgacao</b>: campo numerico Meta de vendas mensais (R$) e campo Nome da pagina do Facebook (usado como referencia nos textos gerados automaticamente pelo bot).",
        "Botao <b>Salvar Configuracoes</b>  -  grava as preferencias e exibe confirmacao temporaria de sucesso.",
    ],
)

add_page(
    25, "Admin", "/admin",
    "Painel Administrativo  -  visivel apenas para usuarios com permissao de administrador.",
    "Area de gestao de usuarios e visao geral do sistema, restrita a administradores.",
    [
        "Quatro cartoes de estatistica: Total de Usuarios, Administradores, Produtos e Status (Online/Offline).",
        "Tabela <b>Usuarios do Sistema</b>: Nome, Email, Papel/Role (selo em vermelho quando ADMIN), Plano, Status (Ativo/Inativo) e coluna de Acoes com botao <b>Editar</b> por usuario.",
    ],
    notas="No codigo atual, o botao 'Editar' da tabela de usuarios ainda nao possui uma acao funcional associada (elemento visual presente, sem fluxo de edicao implementado).",
)

if __name__ == "__main__":
    build_pdf()
