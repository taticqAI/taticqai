import streamlit as st
import os
import time
from google import genai

# Configuração da página web com layout moderno
st.set_page_config(
    page_title="Taticq | Análise de Desempenho de Alto Nível",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILIZAÇÃO CSS CUSTOMIZADA (Design Moderno & Profissional) ---
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #f0f2f6;
    }
    .taticq-header {
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #374151;
        text-align: center;
        margin-bottom: 25px;
    }
    .pricing-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        transition: transform 0.2s ease, border-color 0.2s ease;
        height: 100%;
    }
    .pricing-card:hover {
        transform: translateY(-5px);
        border-color: #58a6ff;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    .sidebar-metric {
        background: #21262d;
        padding: 12px;
        border-radius: 8px;
        border-left: 4px solid #238636;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Nova Chave da API do Gemini integrada
API_KEY_GEMINI = "AQ.Ab8RN6Lj-jBqcD6GFw6OrrAz_Q2_8ZK5m60ozcZjAbzZfBlWnQ"

# Gestão de Sessão para Créditos, Assinatura e Perfil do Utilizador
if "creditos_disponiveis" not in st.session_state:
    st.session_state.creditos_disponiveis = 10  
if "plano_ativo" not in st.session_state:
    st.session_state.plano_ativo = "Plano Starter (Trial)"
if "status_pagamento" not in st.session_state:
    st.session_state.status_pagamento = "Ativo (Modo Demonstração)"
if "nome_analista" not in st.session_state:
    st.session_state.nome_analista = "Analista Principal"
if "clube_atual" not in st.session_state:
    st.session_state.clube_atual = "Clube Exemplo FC"
if "categoria_atual" not in st.session_state:
    st.session_state.categoria_atual = "Profissional"

# --- BARRA LATERAL (LOGO AJUSTADA, PERFIL E MENU) ---
logo_path = "logo.png" if os.path.exists("logo.png") else "Logo da Taticq.png"

if os.path.exists(logo_path):
    st.sidebar.image(logo_path, width=150)
else:
    st.sidebar.markdown("### ⚽ Taticq")

st.sidebar.markdown("---")
st.sidebar.markdown("### 👤 Perfil do Analista & Clube")

with st.sidebar.form("form_perfil"):
    nome_input = st.text_input("Seu Nome:", value=st.session_state.nome_analista)
    clube_input = st.text_input("Clube:", value=st.session_state.clube_atual)
    categoria_input = st.selectbox(
        "Categoria:",
        ["Sub-13", "Sub-15", "Sub-17", "Sub-20", "Profissional"],
        index=["Sub-13", "Sub-15", "Sub-17", "Sub-20", "Profissional"].index(st.session_state.categoria_atual)
    )
    atualizar_perfil = st.form_submit_button("Guardar Perfil")
    
    if atualizar_perfil:
        st.session_state.nome_analista = nome_input
        st.session_state.clube_atual = clube_input
        st.session_state.categoria_atual = categoria_input
        st.sidebar.success("Perfil atualizado com sucesso!")

st.sidebar.markdown("---")
opcao = st.sidebar.radio(
    "Navegação do Sistema:",
    ["📤 Carregar & Analisar Jogo", "💳 Planos & Assinaturas (SaaS)", "📂 Histórico de Relatórios"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("#### 📊 Estado da Conta")
st.sidebar.markdown(f"""
<div class="sidebar-metric">
    <b>Clube:</b> {st.session_state.clube_atual} ({st.session_state.categoria_atual})<br>
    <b>Plano:</b> {st.session_state.plano_ativo}<br>
    <b>Créditos:</b> {st.session_state.creditos_disponiveis} disponíveis
</div>
""", unsafe_allow_html=True)

# --- CABEÇALHO VISUAL PRINCIPAL ---
st.markdown("""
    <div class="taticq-header">
        <h1>Taticq</h1>
        <p style="color: #9ca3af; font-size: 1.1rem; margin-top: 5px;">Performance Intelligence & Análise de Desempenho de Alto Nível</p>
    </div>
""", unsafe_allow_html=True)

# --- SECÇÃO 1: CARREGAR JOGO & ANALISAR ---
if opcao == "📤 Carregar & Analisar Jogo":
    col_main, col_side = st.columns([2, 1])
    
    with col_main:
        st.subheader("🎬 Motor de Processamento de Vídeo e Tracking Avançado")
        st.write(f"Bem-vindo, **{st.session_state.nome_analista}**. A analisar para o **{st.session_state.clube_atual}** na categoria **{st.session_state.categoria_atual}**.")
        
        # Seletor do Foco da Análise Tática
        foco_analise = st.selectbox(
            "🎯 Selecione o Foco Principal da Análise Tática:",
            [
                "Ação Ofensiva (Organização, Construção e Finalização)",
                "Ação Defensiva (Bloco, Pressão e Recuperação)",
                "Transição Ofensiva (Contra-ataque e Aceleração)",
                "Transição Defensiva (Reorganização e Retirada de Espaço)",
                "Bolas Paradas (Pontapés de canto, livres e laterais)",
                "Análise Geral Completa (Todas as Fases do Jogo)"
            ]
        )
        
        video_file = st.file_uploader("Arraste ou selecione o ficheiro de vídeo da partida (.mp4, .mov)", type=["mp4", "mov"])
        
        if video_file is not None:
            with open("jogo.mp4", "wb") as f:
                f.write(video_file.getbuffer())
                
            st.success("✔ Vídeo sincronizado com sucesso no servidor do Taticq!")
            st.video(video_file)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚀 Processar e Gerar Relatório Tático Profissional por Dorsal", type="primary"):
                if st.session_state.creditos_disponiveis <= 0:
                    st.error("⚠️ Limite de créditos esgotado! Vá à aba 'Planos & Assinaturas' para fazer o upgrade.")
                else:
                    with st.spinner(f"⏳ A cruzar base de dados avançada de dorsais para o {st.session_state.clube_atual} ({st.session_state.categoria_atual}) com foco em: {foco_analise}..."):
                        try:
                            st.session_state.creditos_disponiveis -= 1
                            
                            # Lê automaticamente o ficheiro rico de dados de tracking local (`dados_jogada.csv`)
                            dados_extras = ""
                            if os.path.exists("dados_jogada.csv"):
                                with open("dados_jogada.csv", "r", encoding="utf-8") as f_csv:
                                    dados_extras = f_csv.read()
                            
                            client = genai.Client(api_key=API_KEY_GEMINI)
                            
                            prompt_analista = f"""
                            Atua como o motor de inteligência analítica líder de mercado do 'Taticq', um sistema de Análise de Desempenho de Alto Nível para o Futebol Profissional.
                            
                            CONTEXTO DA EQUIPA:
                            - Analista Responsável: {st.session_state.nome_analista}
                            - Clube: {st.session_state.clube_atual}
                            - Escalão / Categoria: {st.session_state.categoria_atual}
                            
                            BASE DE DADOS DE TRACKING AVANÇADA (dados_jogada.csv):
                            {dados_extras if dados_extras else "Nenhum dado auxiliar detetado."}
                            
                            FOCO TÁTICO SELECIONADO: '{foco_analise}'.
                            
                            Elabora um relatório executivo exaustivo, altamente detalhado e estruturado para a comissão técnica do {st.session_state.clube_atual}, adaptando rigorosamente a exigência metodológica e o vocabulário à categoria '{st.session_state.categoria_atual}'. O relatório DEVE cruzar as colunas da base de dados (Momentos, Setores, Números de Camisa/Dorsais, Ações Técnicas, Zonas do Campo e Velocidades em km/h) para cobrir:
                            1. RESUMO EXECUTIVO DO ESCALÃO ({st.session_state.categoria_atual}) E DO FOCO: Comportamentos coletivos estruturais associados a '{foco_analise}'.
                            2. DESEMPENHO INDIVIDUAL E SETORIAL POR NÚMERO DE CAMISA (DORSAL): Análise fina baseada nos dorsais presentes no CSV (ex: rendimento do Camisa 10, Camisa 9, Camisa 8, etc.), avaliando intensidade de pressão, zonas de atuação e velocidade de execução.
                            3. ANÁLISE CRÍTICA DE ALTA PRECISÃO POR MOMENTO-CHAVE: Fato observado com base exata nas métricas do tracking, interpretação tática funcional e causa/efeito comportamental.
                            4. RECOMENDAÇÕES DE CORREÇÃO TÁTICA E EXERCÍCIOS DE TREINO: Propostas metodológicas concretas e estruturadas para o microciclo semanal direcionadas aos setores e dorsais específicos que necessitam de evolução.
                            """
                            
                            resposta = client.models.generate_content(
                                model='gemini-3.6-flash',
                                contents=prompt_analista
                            )
                            
                            texto_relatorio = resposta.text
                            
                            st.markdown("---")
                            st.subheader(f"📋 Relatório Tático Profissional | {st.session_state.clube_atual} ({st.session_state.categoria_atual}) - Foco: {foco_analise}")
                            st.markdown(texto_relatorio)
                            
                            with open('relatorio_tatico_taticq.txt', 'w', encoding='utf-8') as f_out:
                                f_out.write(texto_relatorio)
                            
                            st.download_button(
                                label="📥 Descarregar Relatório Completo (.txt)",
                                data=texto_relatorio,
                                file_name=f"relatorio_tatico_profissional_{st.session_state.clube_atual}_{st.session_state.categoria_atual}.txt",
                                mime="text/plain"
                            )
                            
                        except Exception as e:
                            st.error(f"Ocorreu um erro ao comunicar com a IA do Taticq: {e}")

    with col_side:
        st.markdown("### 💡 Dicas de Utilização")
        st.info(
            f"**Painel Ativo para:** {st.session_state.clube_atual}\n\n"
            f"• **Categoria:** {st.session_state.categoria_atual}\n"
            "• **Banco de Dados Completo:** O sistema cruza momentos, dorsais, zonas e velocidades do `dados_jogada.csv`.\n"
            "• Selecione o foco correto antes de enviar o vídeo."
        )

# --- SECÇÃO 2: PLANOS E PAGAMENTOS (SAAS) ---
elif opcao == "💳 Planos & Assinaturas (SaaS)":
    st.subheader("💳 Escolha o Plano Ideal para a sua Equipa")
    st.write("Escale a análise de desempenho do seu clube com o ecossistema profissional do Taticq.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="pricing-card">
            <h3>Starter</h3>
            <h2 style="color: #58a6ff;">R$ 299,90<span style="font-size:0.9rem; color:#8b949e;">/mês</span></h2>
            <p style="color: #8b949e; font-size: 0.9rem;">Para analistas independentes e formação.</p>
            <hr style="border-color: #30363d;">
            <p>✅ <b>10 Créditos</b> mensais</p>
            <p>✅ Relatórios táticos detalhados</p>
            <p>✅ Suporte por E-mail</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("[🔗 Assinar Starter via Stripe](https://buy.stripe.com/test_starter_link_exemplo)", unsafe_allow_html=True)
        if st.button("Ativar Modo Teste (Starter)"):
            st.session_state.plano_ativo = "Plano Starter"
            st.session_state.creditos_disponiveis = 10
            st.session_state.status_pagamento = "Ativo (Stripe)"
            st.success("Plano Starter ativado com sucesso!")
            
    with col2:
        st.markdown("""
        <div class="pricing-card" style="border: 2px solid #238636;">
            <div style="background: #238636; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; display:inline-block; margin-bottom:8px;">MAIS POPULAR</div>
            <h3>Pro 🌟</h3>
            <h2 style="color: #58a6ff;">R$ 499,90<span style="font-size:0.9rem; color:#8b949e;">/mês</span></h2>
            <p style="color: #8b949e; font-size: 0.9rem;">Perfeito para equipas profissionais.</p>
            <hr style="border-color: #30363d;">
            <p>✅ <b>25 Créditos</b> mensais</p>
            <p>✅ Relatórios avançados</p>
            <p>✅ Histórico ilimitado</p>
            <p>✅ Suporte Prioritário</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("[🔗 Assinar Pro via Stripe](https://buy.stripe.com/test_pro_link_exemplo)", unsafe_allow_html=True)
        if st.button("Ativar Modo Teste (Pro)"):
            st.session_state.plano_ativo = "Plano Pro"
            st.session_state.creditos_disponiveis = 25
            st.session_state.status_pagamento = "Ativo (Stripe)"
            st.success("Plano Pro ativado com sucesso!")
            
    with col3:
        st.markdown("""
        <div class="pricing-card">
            <h3>Elite Club</h3>
            <h2 style="color: #58a6ff;">R$ 699,90<span style="font-size:0.9rem; color:#8b949e;">/mês</span></h2>
            <p style="color: #8b949e; font-size: 0.9rem;">Para clubes de elite e scouting.</p>
            <hr style="border-color: #30363d;">
            <p>✅ <b>60 Créditos</b> mensais</p>
            <p>✅ Análise multijogador em tempo real</p>
            <p>✅ Relatórios customizados</p>
            <p>✅ Suporte Dedicado 24/7</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("[🔗 Assinar Elite via Stripe](https://buy.stripe.com/test_elite_link_exemplo)", unsafe_allow_html=True)
        if st.button("Ativar Modo Teste (Elite)"):
            st.session_state.plano_ativo = "Plano Elite Club"
            st.session_state.creditos_disponiveis = 60
            st.session_state.status_pagamento = "Ativo (Stripe)"
            st.success("Plano Elite Club ativado com sucesso!")

# --- SECÇÃO 3: HISTÓRICO DE RELATÓRIOS ---
elif opcao == "📂 Histórico de Relatórios":
    st.subheader("📂 Arquivo de Relatórios Analíticos")
    st.write("Consulte, analise e descarregue os relatórios gerados anteriormente na sua conta.")
    
    if os.path.exists('relatorio_tatico_taticq.txt'):
        with open('relatorio_tatico_taticq.txt', 'r', encoding='utf-8') as f:
            conteudo_antigo = f.read()
            
        st.text_area("Último Relatório Emitido:", conteudo_antigo, height=450)
        
        st.download_button(
            label="📥 Descarregar Documento Completo (.txt)",
            data=conteudo_antigo,
            file_name="relatorio_tatico_taticq_historico.txt",
            mime="text/plain"
        )
    else:
        st.info("ℹ️ Ainda não existem relatórios gravados no sistema nesta sessão.")