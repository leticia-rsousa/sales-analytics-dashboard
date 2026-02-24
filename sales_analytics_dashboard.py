# Mini-Projeto 10 - Data App Para Dashboard Interativo de Sales Analytics em Python com Streamlit

# Importações principais
import sqlite3
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from datetime import datetime, date, timedelta

# Configuração inicial da aplicação Streamlit
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon=":100:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Inicialização do Banco --- #

def init_db(conn):
    """Cria a tabela tb_vendas e popula com dados fictícios caso esteja vazia."""

    cursor = conn.cursor()

    # Criação da tabela
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tb_vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            date TEXT,
            regiao TEXT,
            categoria TEXT,
            produto TEXT,
            faturamento REAL,
            quantidade INTEGER
        )
    """)
    conn.commit()

    # Verifica se já existe conteúdo
    cursor.execute("SELECT COUNT(*) FROM tb_vendas")
    if cursor.fetchone()[0] == 0:

        # Dados iniciais
        np.random.seed(42)
        start_date = date(2026, 1, 1)
        datas = [start_date + timedelta(days=i) for i in range(180)]

        regioes = ["Norte", "Nordeste", "Sul", "Sudeste", "Centro-Oeste"]
        categorias = ["Eletrônicos", "Roupas", "Alimentos", "Serviços"]

        dict_produtos = {
            "Eletrônicos": {"Smartphone": 1200, "Laptop": 3500, "Tablet": 800},
            "Roupas": {"Camiseta": 50, "Terno": 150, "Casaco": 300},
            "Alimentos": {"Congelados": 40, "Bebidas": 15, "Limpeza": 25},
            "Serviços": {"Consultoria": 1000, "Instalação": 400, "Suporte": 200}
        }

        rows = []

        # Geração dos registros
        for d in datas:
            vendas_diarias = np.random.randint(5, 15)

            for _ in range(vendas_diarias):
                r = np.random.choice(regioes)
                c = np.random.choice(categorias)
                p = np.random.choice(list(dict_produtos[c].keys()))
                preco_base = dict_produtos[c][p]
                quantidade = np.random.randint(1, 25)
                base_faturamento = preco_base * quantidade
                noise = np.random.uniform(-0.20, 0.20)
                faturamento = max(0, base_faturamento * (1 + noise))

                rows.append((d.isoformat(), r, c, p, round(faturamento, 2), quantidade))

        cursor.executemany(
            "INSERT INTO tb_vendas (date, regiao, categoria, produto, faturamento, quantidade) VALUES (?, ?, ?, ?, ?, ?)",
            rows,
        )
        conn.commit()


# --- Conexão com o Banco --- #

def cria_conexao(db_path="database.db"):
    """Retorna uma conexão SQLite para o arquivo informado."""
    return sqlite3.connect(db_path, check_same_thread=False)


# --- Carregamento de Dados com Cache --- #

@st.cache_data(ttl=600)
def carrega_dados():
    """Carrega o DataFrame da tabela tb_vendas, inicializando o BD se necessário."""
    conn = cria_conexao()
    init_db(conn)
    df = pd.read_sql_query("SELECT * FROM tb_vendas", conn, parse_dates=["date"])
    conn.close()
    return df


# --- Filtros da Sidebar --- #

def filtros_sidebar(df):
    """Cria filtros na sidebar e retorna o DataFrame filtrado."""

    st.sidebar.markdown(
        """
        <div style="background-color:#00CC96; padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 15px;">
            <h3 style="color:white; margin:0; font-weight:bold;">Sales Analytics Dashboard</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.header("🔍 Filtros")

    min_date = df["date"].min().date()
    max_date = df["date"].max().date()

    date_range = st.sidebar.date_input("Período de Análise", (min_date, max_date),
                                       min_value=min_date, max_value=max_date)

    all_regioes = sorted(df["regiao"].unique())
    selected_regioes = st.sidebar.multiselect("Regiões", all_regioes, default=all_regioes)

    all_categorias = sorted(df["categoria"].unique())
    selected_categorias = st.sidebar.multiselect("Categorias", all_categorias, default=all_categorias)

    all_produtos = sorted(df["produto"].unique())
    selected_produtos = st.sidebar.multiselect("Produtos", all_produtos, default=all_produtos)

    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = min_date, max_date

    df_filtrado = df[
        (df["date"].dt.date >= start_date) &
        (df["date"].dt.date <= end_date) &
        (df["regiao"].isin(selected_regioes)) &
        (df["categoria"].isin(selected_categorias)) &
        (df["produto"].isin(selected_produtos))
    ].copy()

    st.sidebar.markdown("---")
    with st.sidebar.expander("🆘 Suporte / Fale conosco", expanded=False):
        st.write("Se tiver dúvidas envie mensagem para suporte@datascienceacademy.com.br")

    st.sidebar.caption("Dashboard desenvolvido como projeto de Sales Analytics.")

    return df_filtrado

# --- KPIs --- #

def renderiza_cards_kpis(df):
    """Calcula e retorna os KPIs principais e os exibe em cards."""

    total_faturamento = df["faturamento"].sum()
    total_qty = df["quantidade"].sum()
    avg_ticket = total_faturamento / total_qty if total_qty > 0 else 0
    delta_rev = np.random.uniform(-5, 15)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Receita Total</h3>
            <h2>R$ {total_faturamento:,.0f}</h2>
            <div class="delta" style="color:{'#4CAF50' if delta_rev > 0 else '#FF5252'}">
                {delta_rev:+.1f}% vs meta
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Vendas (Qtd)</h3>
            <h2>{total_qty:,.0f}</h2>
            <div class="delta">Unidades vendidas</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Ticket Médio</h3>
            <h2>R$ {avg_ticket:,.2f}</h2>
            <div class="delta">Por transação</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        transactions = df.shape[0]
        st.markdown(f"""
        <div class="metric-card">
            <h3>Transações</h3>
            <h2>{transactions}</h2>
            <div class="delta">Volume total</div>
        </div>
        """, unsafe_allow_html=True)

    return total_faturamento, total_qty, avg_ticket


# --- PDF --- #

def gera_pdf_report(df_filtrado, total_faturamento, total_quantidade, avg_ticket):
    """Gera relatório PDF completo usando FPDF."""

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Relatorio Executivo de Vendas", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 8, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_fill_color(240, 240, 240)
    pdf.rect(10, 35, 190, 25, 'F')
    pdf.set_y(40)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(60, 8, "Receita Total", align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.cell(60, 8, "Quantidade", align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.cell(60, 8, "Ticket Medio", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font("Helvetica", "", 12)
    pdf.cell(60, 8, f"R$ {total_faturamento:,.2f}", align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.cell(60, 8, f"{total_quantidade:,}", align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.cell(60, 8, f"R$ {avg_ticket:,.2f}", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.ln(15)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Top 15 Vendas (por receita):", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    col_widths = [30, 30, 30, 40, 25, 30]
    headers = ["Data", "Regiao", "Categoria", "Produto", "Qtd", "Receita"]

    pdf.set_font("Helvetica", "B", 9)
    for i, h in enumerate(headers):
        pdf.cell(col_widths[i], 8, h, 1, align='C', new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.ln()

    df_top = df_filtrado.sort_values("faturamento", ascending=False).head(15)
    pdf.set_font("Helvetica", "", 9)

    for _, row in df_top.iterrows():
        data = [
            str(row['date'].date()),
            row['regiao'],
            row['categoria'],
            row['produto'][:20],
            str(row['quantidade']),
            f"R$ {row['faturamento']:,.2f}"
        ]

        for i, d in enumerate(data):
            safe_txt = str(d).encode("latin-1", "replace").decode("latin-1")
            pdf.cell(col_widths[i], 7, safe_txt, 1,
                     align=('C' if i == 4 else 'L'),
                     new_x=XPos.RIGHT, new_y=YPos.TOP)

        pdf.ln()

    result = pdf.output()
    return result.encode("latin-1") if isinstance(result, str) else bytes(result)


# --- Tema Customizado --- #

def set_custom_theme():
    """Define estilo visual customizado via CSS."""

    card_bg_color = "#262730"
    text_color = "#FAFAFA"
    gold_color = "#E1C16E"
    dark_text = "#1E1E1E"

    css = f"""
    <style>
        [data-testid="stMultiSelect"] div[data-baseweb="select"] > div:first-child {{
            min-height: 100px !important;
            overflow-y: auto !important;
        }}

        .metric-card {{
            background-color: {card_bg_color};
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #444;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
            text-align: center;
            margin-bottom: 10px;
        }}

        .metric-card h3 {{
            margin: 0;
            font-size: 1.2rem;
            color: #AAA;
        }}

        .metric-card h2 {{
            margin: 10px 0 0 0;
            font-size: 2rem;
            color: {text_color};
        }}

        .metric-card .delta {{
            font-size: 0.9rem;
            margin-top: 5px;
        }}

        [data-baseweb="tag"] {{
            background-color: {gold_color} !important;
            color: {dark_text} !important;
        }}

        [data-baseweb="tag"] svg {{
            color: {dark_text} !important;
        }}

        [data-baseweb="tag"] svg:hover {{
            color: #FF0000 !important;
        }}
    </style>
    """

    st.markdown(css, unsafe_allow_html=True)


# --- Função Principal --- #

def sales_analytics_mp10():
    """Fluxo principal da aplicação."""

    set_custom_theme()
    df = carrega_dados()
    df_filtrado = filtros_sidebar(df)

    st.title("Sales Analytics Dashboard")
    st.title("📊 Data App Para Dashboard Interativo de Sales Analytics")
    st.subheader("Com Banco de Dados SQLite e Streamlit")
    st.markdown("---")

    if df_filtrado.empty:
        st.warning("⚠️ Nenhum dado encontrado com os filtros selecionados.")
        return

    total_faturamento, total_qty, avg_ticket = renderiza_cards_kpis(df_filtrado)

    st.markdown("---")

    tab1, tab2 = st.tabs(["📈 Visão Gráfica", "📄 Dados Detalhados & Exportação (CSV e PDF)"])

    # --- Aba 1 --- #
    with tab1:
        col_left, col_right = st.columns([2, 1])

        with col_left:
            st.subheader("Evolução da Receita Diária")
            daily_rev = df_filtrado.groupby("date")[["faturamento"]].sum().reset_index()
            fig_line = px.line(daily_rev, x="date", y="faturamento",
                               template="plotly_dark", height=400)
            fig_line.update_traces(fill='tozeroy', line=dict(color='#00CC96', width=3))
            st.plotly_chart(fig_line, use_container_width=True)

        with col_right:
            st.subheader("Mix de Categorias")
            cat_rev = df_filtrado.groupby("categoria")[["faturamento"]].sum().reset_index()
            fig_pie = px.pie(cat_rev, values="faturamento", names="categoria",
                             hole=0.4, template="plotly_dark", height=400)
            st.plotly_chart(fig_pie, use_container_width=True)

        c_a, c_b = st.columns(2)

        with c_a:
            st.subheader("Performance Regional")
            fig_bar = px.bar(
                df_filtrado.groupby("regiao")[["faturamento"]].sum().reset_index(),
                x="regiao", y="faturamento", color="regiao",
                template="plotly_dark", text_auto='.2s'
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        with c_b:
            st.subheader("Análise Dia da Semana")

            dias_pt_map = {
                0: "Segunda-feira", 1: "Terça-feira", 2: "Quarta-feira",
                3: "Quinta-feira", 4: "Sexta-feira", 5: "Sábado", 6: "Domingo"
            }

            dias_pt_ordem = [
                "Segunda-feira", "Terça-feira", "Quarta-feira",
                "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"
            ]

            df_filtrado["weekday_num"] = df_filtrado["date"].dt.dayofweek
            df_filtrado["dia_semana"] = df_filtrado["weekday_num"].map(dias_pt_map)

            wd_rev = df_filtrado.groupby("dia_semana")[["faturamento"]].mean() \
                .reindex(dias_pt_ordem).reset_index()

            fig_heat = px.bar(
                wd_rev, x="dia_semana", y="faturamento",
                title="Receita Média x Dia",
                template="plotly_dark"
            )
            st.plotly_chart(fig_heat, use_container_width=True)

        st.subheader("Dispersão: Quantidade x Faturamento x Produto")
        fig_scat = px.scatter(
            df_filtrado, x="quantidade", y="faturamento", color="categoria",
            size="faturamento", hover_data=["produto"],
            template="plotly_dark", height=500
        )
        st.plotly_chart(fig_scat, use_container_width=True)

    # --- Aba 2 --- #
    with tab2:
        st.subheader("Visualização Tabular")
        st.dataframe(df_filtrado, use_container_width=True, height=400)

        st.markdown("### 📥 Área de Exportação")
        c_exp1, c_exp2 = st.columns(2)

        with c_exp1:
            csv = df_filtrado.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="💾 Baixar CSV (Excel)",
                data=csv,
                file_name="dados_filtrados.csv",
                mime="text/csv",
                use_container_width=True
            )

        with c_exp2:
            if st.button("📄 Gerar Relatório PDF", use_container_width=True):
                with st.spinner("Renderizando PDF..."):
                    pdf_bytes = gera_pdf_report(df_filtrado, total_faturamento, total_qty, avg_ticket)
                    st.download_button(
                        label="⬇️ Clique aqui para Salvar PDF",
                        data=pdf_bytes,
                        file_name=f"Relatorio_Vendas_{date.today()}.pdf",
                        mime="application/pdf",
                        key="pdf-download-final"
                    )

    st.markdown("---")

    with st.expander("ℹ️ Sobre Esta Data App", expanded=False):
        st.info("Dashboard para análise de vendas com KPIs, gráficos interativos e exportação de relatórios.")
        st.markdown("""
        **Tecnologias Integradas:**
        - Python + Streamlit + SQLite  
        - Plotly Express  
        - Geração de PDF com FPDF  
        - Cache de dados com @st.cache_data  
        """)


# --- Execução --- #

if __name__ == "__main__":
    sales_analytics_mp10()
