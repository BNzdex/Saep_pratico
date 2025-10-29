import sqlite3

DATABASE = 'saep.db'

def init_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            nome TEXT NOT NULL,
            email TEXT
        )
    ''')
    
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
    
    usuarios = [
        ('admin', 'admin123', 'Administrador do Sistema', 'admin@saep.com'),
        ('joao', 'senha123', 'João Silva', 'joao@saep.com'),
        ('maria', 'senha456', 'Maria Santos', 'maria@saep.com')
    ]
    
    cursor.executemany(
        'INSERT OR IGNORE INTO usuarios (username, password, nome, email) VALUES (?, ?, ?, ?)',
        usuarios
    )
    
    produtos = [
    ('Furadeira Bosch', 'Furadeira elétrica Bosch 650W com mandril de 13mm', 480.00, 20, 5),
    ('Parafusadeira DeWalt', 'Parafusadeira a bateria DeWalt 12V com carregador', 650.00, 15, 4),
    ('Chave de Fenda Philips', 'Chave de fenda Philips 5mm com cabo emborrachado', 25.00, 100, 20),
    ('Martelo de Unha', 'Martelo de unha 27mm com cabo de madeira', 45.00, 40, 10),
    ('Trena 5m', 'Trena metálica de 5 metros com trava automática', 35.00, 60, 15)
    ]

    
    cursor.executemany(
        'INSERT OR IGNORE INTO produtos (nome, descricao, preco, quantidade, estoque_minimo) VALUES (?, ?, ?, ?, ?)',
        produtos
    )
    
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
