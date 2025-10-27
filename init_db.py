import sqlite3

DATABASE = 'saep_db.db'

def init_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Criar tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            nome TEXT NOT NULL,
            email TEXT
        )
    ''')
    
    # Criar tabela de produtos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            preco REAL NOT NULL,
            quantidade INTEGER NOT NULL,
            estoque_minimo INTEGER NOT NULL
        )
    ''')
    
    # Criar tabela de movimentações
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movimentacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER NOT NULL,
            tipo TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            data_movimentacao DATE NOT NULL,
            FOREIGN KEY (produto_id) REFERENCES produtos (id)
        )
    ''')
    
    # Inserir usuários
    usuarios = [
        ('admin', 'admin123', 'Administrador do Sistema', 'admin@saep.com'),
        ('joao', 'senha123', 'João Silva', 'joao@saep.com'),
        ('maria', 'senha456', 'Maria Santos', 'maria@saep.com')
    ]
    
    cursor.executemany(
        'INSERT OR IGNORE INTO usuarios (username, password, nome, email) VALUES (?, ?, ?, ?)',
        usuarios
    )
    
    # Inserir produtos
    produtos = [
        ('Notebook Dell', 'Notebook Dell Inspiron 15, 8GB RAM, 256GB SSD', 3500.00, 15, 5),
        ('Mouse Logitech', 'Mouse sem fio Logitech M280', 89.90, 50, 10),
        ('Teclado Mecânico', 'Teclado mecânico RGB Redragon', 299.00, 25, 8),
        ('Monitor LG 24"', 'Monitor LG 24" Full HD IPS', 899.00, 12, 3),
        ('Webcam HD', 'Webcam Full HD 1080p com microfone', 199.00, 30, 10)
    ]
    
    cursor.executemany(
        'INSERT OR IGNORE INTO produtos (nome, descricao, preco, quantidade, estoque_minimo) VALUES (?, ?, ?, ?, ?)',
        produtos
    )
    
    # Inserir movimentações
    movimentacoes = [
        (1, 'entrada', 10, '2025-01-15'),
        (1, 'saida', 5, '2025-01-20'),
        (2, 'entrada', 30, '2025-01-10'),
        (2, 'saida', 10, '2025-01-25'),
        (3, 'entrada', 20, '2025-01-12'),
        (4, 'saida', 3, '2025-01-18')
    ]
    
    cursor.executemany(
        'INSERT OR IGNORE INTO movimentacoes (produto_id, tipo, quantidade, data_movimentacao) VALUES (?, ?, ?, ?)',
        movimentacoes
    )
    
    conn.commit()
    conn.close()
    
    print('Banco de dados "saep_db" criado e populado com sucesso!')
    print('\nUsuários cadastrados:')
    print('- Username: admin | Senha: admin123')
    print('- Username: joao | Senha: senha123')
    print('- Username: maria | Senha: senha456')

if __name__ == '__main__':
    init_database()
