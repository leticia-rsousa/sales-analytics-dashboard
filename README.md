## Sales Analytics Dashboard
**Descrição Geral** 📄<br>
Este projeto apresenta um **dashboard interativo de análise de vendas**, desenvolvido com **Python, Streamlit e SQLite.** <br>
O sistema realiza **carregamento de dados, filtros dinâmicos, cálculo de KPIs, visualização gráfica**, além de **exportação de relatórios em CSV e PDF.** <br>
O projeto demonstra conceitos essenciais de **manipulação de dados, construção de dashboards, integração com banco SQLite, visualização interativa, geração de relatórios automatizados e boas práticas de organização em aplicações de dados.**

---
**Objetivo** 🎯 <br> 
O objetivo principal do projeto é construir uma **aplicação interativa para análise de vendas**, permitindo visualizar métricas importantes, explorar diferentes dimensões (região, produto, categoria), acompanhar tendências e gerar relatórios completos. <br>
A ferramenta pode ser utilizada em cenários como **monitoramento de performance comercial, análises gerenciais, acompanhamento diário de vendas ou apresentações executivas.**

---
**Tecnologias Utilizadas** 💻 <br>
* ***Python*** - linguagem principal.
* ***Pandas*** - manipulação e análise de dados.
* ***NumPy*** - geração e suporte aos dados simulados.
* ***Streamlit*** - construção do dashboard.
* ***Plotly Express*** - visualizações interativas.
* ***SQLite*** - banco de dados local.
* ***FPDF2*** - geração de relatórios em PDF.

---
**Arquitetura e Estrutura do Código** 🧱 <br><br>
***1. Script Principal (sales_analytics_dashboard.py)*** <br>
Responsável por:
* ***Criar e inicializar o banco de dados SQLite com dados fictícios.*** 
* ***Carregar os dados e armazenar em cache para melhor desempenho.***
* ***Criar filtros interativos na sidebar (data, região, categoria, produto).***
* ***Gerar KPIs essenciais:***
  * Receita Total
  * Quantidade Vendida
  * Ticket Médio
  * Total de Transações
* ***Renderizar gráficos interativos:***
  * Evolução diária da receita
  * Distribuição por categoria
  * Performance por região
  * Comparação por dia da semana
  * Dispersão (faturamento × quantidade)
* ***Criar tabela filtrada para consulta detalhada.*** 
* ***Disponibilizar download de CSV.***
* ***Gerar relatório PDF completo com top 15 vendas.***
* ***Aplicar tema visual customizado via CSS.***

---
**Conceitos e Funcionalidades Demonstradas** 🔍 <br><br>
✅ ***Manipulação e preparação de dados:*** <br>
Carregamento via SQLite, filtragem avançada, agrupamentos e métricas agregadas.

✅***Cache de dados (Streamlit):*** <br>
Utilização de @st.cache_data para melhorar desempenho da aplicação.

✅***Dashboard Interativo Completo:*** <br>
Com filtros, KPIs, tabelas, tabs e múltiplos gráficos.

✅***Visualização de dados avançada:*** <br>
Gráficos interativos com **Plotly.**

✅***Exportação Automática:*** <br>
Geração de arquivo CSV direto do DataFrame filtrado.

✅***Relatório PDF Executivo:*** <br>
PDF contendo:
* Título e timestamp
* KPIs
* Tabela com **Top 15 vendas por receita**
* Layout formatado com FPDF

✅***Tema Customizado:*** <br>
CSS aplicado diretamente ao Streamlit para aparência aprimorada.

---
**Como Executar o Projeto** ▶️ <br><br>
***1. Instale as dependências (recomendado via requirements.txt):*** <br>
```pip install -r requirements.txt```

***2. Execute o aplicativo Streamlit:*** <br>
```streamlit run sales_analytics_dashboard.py```

***3. Interaja com o dashboard:*** <br>
Use os filtros laterais, explore os gráficos e baixe relatórios CSV ou PDF.

***Exemplo de saída (KPIs):*** <br>
```
Receita Total: R$ 1.450.230
Quantidade Vendida: 18.320
Ticket Médio: R$ 79.20
Transações: 1120
```

---
**Conclusão** 📌 <br>
Este projeto demonstra como criar um ** dashboard profissional de análise de vendas** , combinando:
* Banco de dados SQLite
* Manipulação de dados com Pandas
* Visualizações avançadas com Plotly
* Interface interativa no Streamlit
* Exportação de relatórios executivos <br>
Ele oferece uma estrutura completa e reutilizável para qualquer aplicação de ** Sales Analytics** , podendo ser facilmente expandido para dados reais ou novas métricas.
