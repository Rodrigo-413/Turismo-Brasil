class CidadeController {
    constructor(cidadeNome) {
        this.cidade = cidadeNome;
        this.pontos = [];
        this.categorias = [];
        this.categoriaAtual = 'todos';
        this.estatisticas = { total_pontos: 0, total_categorias: 0 };
        this.modalAberto = null;
    }

    //Detectar cidade automaticamente pela página
    detectarCidade() {
        const url = window.location.pathname;
        const pagina = url.split('/').pop();
        
        const cidadesMap = {
            'sao_paulo-sp.html': 'São Paulo',
            'campinas.html': 'Campinas', 
            'camposjordao.html': 'Campos do Jordão',
            'ubatuba.html': 'Ubatuba'
        };
        
        return cidadesMap[pagina] || 'São Paulo';
    }

    //Inicializar automaticamente
    async inicializar() {
        // Se cidade não foi passada, detectar automaticamente
        if (!this.cidade) {
            this.cidade = this.detectarCidade();
        }
        
        await this.carregarCategorias();
        await this.carregarEstatisticas();
        await this.carregarPontos('todos');
        this.atualizarEstatisticasUI();
        this.atualizarTituloPagina();
    }

    //Atualizar título da página com dados dinâmicos
    atualizarTituloPagina() {
        const titulo = document.querySelector('.titulo-cidade');
        const subtitulo = document.querySelector('.subtitulo-cidade');
        
        if (titulo) {
            titulo.textContent = this.cidade.toUpperCase();
        }
        
        // Atualizar subtítulo baseado na cidade
        if (subtitulo) {
            const subtitulosMap = {
                'São Paulo': 'Terra da garoa',
                'Campinas': 'Princesa d\'Oeste', 
                'Campos do Jordão': 'Suíça Brasileira',
                'Ubatuba': 'Capital do Surf'
            };
            subtitulo.textContent = subtitulosMap[this.cidade] || '';
        }
    }

    fecharModal() {
        if (this.modalAberto) {
            this.modalAberto.remove();
            this.modalAberto = null;
        }
    }

    async carregarCategorias() {
        try {
            const response = await fetch(`http://127.0.0.1:5000/categorias/${this.cidade}`);
            this.categorias = await response.json();
            this.exibirCategorias();
            
        } catch (error) {
            console.error('Erro ao carregar categorias:', error);
        }
    }

    async carregarEstatisticas() {
        try {
            const response = await fetch(`http://127.0.0.1:5000/estatisticas/${this.cidade}`);
            this.estatisticas = await response.json();
            
        } catch (error) {
            console.error('Erro ao carregar estatísticas:', error);
        }
    }

    exibirCategorias() {
        const container = document.getElementById('botoes-categoria');
        
        if (this.categorias.length === 0) {
            container.innerHTML = '<p class="sem-categorias">Nenhuma categoria disponível para esta cidade</p>';
            return;
        }

        let html = `
            <button class="botao-categoria ativo" onclick="cidadeCtrl.filtrarPorCategoria('todos')">
                🎯 Todos (${this.estatisticas.total_pontos})
            </button>
        `;

        html += this.categorias.map(cat => `
            <button class="botao-categoria" onclick="cidadeCtrl.filtrarPorCategoria('${cat.nome}')">
                ${cat.icone || '📍'} ${cat.nome} (${cat.total_pontos})
            </button>
        `).join('');

        container.innerHTML = html;
    }

    async carregarPontos(categoria = 'todos') {
        try {
            this.fecharModal();
            
            let url;
            if (categoria === 'todos') {
                url = `http://127.0.0.1:5000/pontos-turisticos/${this.cidade}`;
            } else {
                url = `http://127.0.0.1:5000/pontos-turisticos/${this.cidade}/${categoria}`;
            }

            const response = await fetch(url);
            this.pontos = await response.json();
            
            this.categoriaAtual = categoria;
            this.exibirPontos();
            
        } catch (error) {
            console.error('Erro ao carregar pontos:', error);
        }
    }

    exibirPontos() {
        const container = document.getElementById('pontos-container');
        
        if (this.pontos.length === 0) {
            const mensagem = this.categoriaAtual === 'todos' 
                ? `Nenhum ponto turístico cadastrado em ${this.cidade}`
                : `Nenhum ponto turístico na categoria ${this.categoriaAtual} em ${this.cidade}`;
                
            container.innerHTML = `
                <div class="sem-resultados">
                    <h3>${mensagem}</h3>
                    <p>Seja o primeiro a cadastrar um local!</p>
                    <a href="inscricao.html" class="btn-inscrever">Inscrever Local</a>
                </div>
            `;
            return;
        }

        container.innerHTML = this.pontos.map(ponto => this.criarCardPonto(ponto)).join('');
    }

    criarCardPonto(ponto) {
        return `
            <div class="card-ponto" data-categoria="${ponto.categoria_nome.toLowerCase()}">
                <div class="card-header">
                    <h3 class="ponto-nome">${ponto.nome}</h3>
                    <span class="categoria-badge">
                        ${ponto.icone || '📍'} ${ponto.categoria_nome}
                    </span>
                </div>
                
                <div class="card-body">
                    <div class="info-item">
                        <span class="icon">📍</span>
                        <span class="text">${ponto.endereco}</span>
                    </div>
                    
                    ${ponto.ponto_referencia ? `
                    <div class="info-item">
                        <span class="icon">🎯</span>
                        <span class="text">Perto de: ${ponto.ponto_referencia}</span>
                    </div>
                    ` : ''}
                    
                    <div class="info-item">
                        <span class="icon">🎭</span>
                        <span class="text">${ponto.tipo_turismo}</span>
                    </div>
                    
                    ${ponto.dias_funcionamento ? `
                    <div class="info-item">
                        <span class="icon">📅</span>
                        <span class="text">Funciona: ${ponto.dias_funcionamento}</span>
                    </div>
                    ` : ''}
                    
                    <div class="info-preco">
                        ${ponto.preco_minimo > 0 ? `
                            <span class="preco">R$ ${parseFloat(ponto.preco_minimo).toFixed(2)}</span>
                        ` : '<span class="gratis">Grátis</span>'}
                        
                        ${ponto.necessita_ingresso ? 
                            '<span class="ingresso">Com ingresso</span>' : 
                            '<span class="ingresso">Entrada livre</span>'
                        }
                    </div>
                </div>
                
                <div class="card-footer">
                    <button class="btn-ver-mais" onclick="cidadeCtrl.verDetalhes(${ponto.id})">
                        Ver Detalhes
                    </button>
                    <button class="btn-rota" onclick="cidadeCtrl.traçarRota('${ponto.endereco}')">
                        🗺️ Traçar Rota
                    </button>
                </div>
            </div>
        `;
    }

    filtrarPorCategoria(categoria) {
        this.fecharModal();
        
        this.carregarPontos(categoria);
        
        document.querySelectorAll('.botao-categoria').forEach(btn => {
            btn.classList.remove('ativo');
        });
        event.target.classList.add('ativo');
        
        document.getElementById('categoria-atual').textContent = 
            categoria === 'todos' ? 'Todos' : categoria;
    }

    atualizarEstatisticasUI() {
        document.getElementById('total-pontos').textContent = this.estatisticas.total_pontos;
        document.getElementById('total-categorias').textContent = this.estatisticas.total_categorias;
        document.getElementById('categoria-atual').textContent = 'Todos';
    }

    verDetalhes(pontoId) {
        this.fecharModal();
        
        const ponto = this.pontos.find(p => p.id === pontoId);
        if (ponto) {
            this.abrirModalDetalhes(ponto);
        }
    }

    abrirModalDetalhes(ponto) {
        const modalHTML = `
            <div class="modal-overlay">
                <div class="modal-content">
                    <button class="btn-fechar-modal" onclick="cidadeCtrl.fecharModal()">×</button>
                    <h2>${ponto.nome}</h2>
                    <div class="modal-info">
                        <p><strong>📍 Endereço:</strong> ${ponto.endereco}</p>
                        ${ponto.ponto_referencia ? `<p><strong>🎯 Ponto de Referência:</strong> ${ponto.ponto_referencia}</p>` : ''}
                        <p><strong>🎭 Tipo de Turismo:</strong> ${ponto.tipo_turismo}</p>
                        <p><strong>🏷️ Categoria:</strong> ${ponto.categoria_nome}</p>
                        ${ponto.dias_funcionamento ? `<p><strong>📅 Funcionamento:</strong> ${ponto.dias_funcionamento}</p>` : ''}
                        <p><strong>💰 Preço:</strong> ${ponto.preco_minimo > 0 ? `R$ ${parseFloat(ponto.preco_minimo).toFixed(2)}` : 'Grátis'}</p>
                        <p><strong>🎫 Ingresso:</strong> ${ponto.necessita_ingresso ? 'Necessário' : 'Não necessário'}</p>
                    </div>
                    <button class="btn-rota-grande" onclick="cidadeCtrl.traçarRota('${ponto.endereco}')">
                        🗺️ Traçar Rota no Maps
                    </button>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        this.modalAberto = document.querySelector('.modal-overlay:last-child');
        
        this.modalAberto.addEventListener('click', (e) => {
            if (e.target === this.modalAberto) {
                this.fecharModal();
            }
        });
        
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.modalAberto) {
                this.fecharModal();
            }
        });
    }

    traçarRota(endereco) {
        const enderecoCodificado = encodeURIComponent(endereco);
        window.open(`https://www.google.com/maps/dir/?api=1&destination=${enderecoCodificado}`, '_blank');
    }
}

//Funciona para qualquer cidade
const cidadeCtrl = new CidadeController();