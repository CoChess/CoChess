#!/bin/bash

echo "📦 Instalando dependências do projeto..."

# Se ainda não estiver no ambiente virtual, crie-o e ative
if [ ! -d venv ]; then
    echo "🔧 Configurando o ambiente virtual..."
    python3 -m venv venv || { echo "❌ Erro ao criar ambiente virtual."; exit 1; }
fi

# Ativa o ambiente virtual
source venv/bin/activate || { echo "❌ Erro ao ativar ambiente virtual."; exit 1; }

# Instala as dependências dentro do venv
pip install -r requirements.txt || { echo "❌ Erro ao instalar dependências."; exit 1; }

# Executa o script de criação do banco
echo "🛠️  Criando o banco de dados SQLite..."
python app/database/init_db.py || { echo "❌ Erro ao criar banco de dados."; exit 1; }

# Inicia a aplicação
echo "🚀 Iniciando o servidor Flask..."
python run.py
