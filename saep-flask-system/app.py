from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'bernardo_incrivel'

DATABASE = 'saep_db.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Você precisa estar logado para acessar esta página.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Por favor, preencha todos os campos.', 'error')
            return render_template('login.html')
        
        conn = get_db()
        user = conn.execute('SELECT * FROM usuarios WHERE username = ? AND password = ?', 
                           (username, password)).fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['nome'] = user['nome']
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Usuário ou senha incorretos. Tente novamente.', 'error')
            return render_template('login.html')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', nome=session.get('nome'))

@app.route('/produtos', methods=['GET', 'POST'])
@login_required
def produtos():
    conn = get_db()
    
    search = request.args.get('search', '')
    
    if search:
        produtos = conn.execute(
            'SELECT * FROM produtos WHERE nome LIKE ? OR descricao LIKE ?',
            (f'%{search}%', f'%{search}%')
        ).fetchall()
    else:
        produtos = conn.execute('SELECT * FROM produtos').fetchall()
    
    conn.close()
    
    return render_template('produtos.html', produtos=produtos, search=search)

@app.route('/produtos/adicionar', methods=['POST'])
@login_required
def adicionar_produto():
    nome = request.form.get('nome')
    descricao = request.form.get('descricao')
    preco = request.form.get('preco')
    quantidade = request.form.get('quantidade')
    estoque_minimo = request.form.get('estoque_minimo')
    
    if not nome or not preco or not quantidade or not estoque_minimo:
        flash('Todos os campos obrigatórios devem ser preenchidos.', 'error')
        return redirect(url_for('produtos'))
    
    try:
        preco = float(preco)
        quantidade = int(quantidade)
        estoque_minimo = int(estoque_minimo)
        
        if preco < 0 or quantidade < 0 or estoque_minimo < 0:
            flash('Os valores não podem ser negativos.', 'error')
            return redirect(url_for('produtos'))
    except ValueError:
        flash('Valores inválidos. Verifique os campos numéricos.', 'error')
        return redirect(url_for('produtos'))
    
    conn = get_db()
    conn.execute(
        'INSERT INTO produtos (nome, descricao, preco, quantidade, estoque_minimo) VALUES (?, ?, ?, ?, ?)',
        (nome, descricao, preco, quantidade, estoque_minimo)
    )
    conn.commit()
    conn.close()
    
    flash('Produto adicionado com sucesso!', 'success')
    return redirect(url_for('produtos'))

@app.route('/produtos/editar/<int:id>', methods=['POST'])
@login_required
def editar_produto(id):
    nome = request.form.get('nome')
    descricao = request.form.get('descricao')
    preco = request.form.get('preco')
    quantidade = request.form.get('quantidade')
    estoque_minimo = request.form.get('estoque_minimo')
    
    if not nome or not preco or not quantidade or not estoque_minimo:
        flash('Todos os campos obrigatórios devem ser preenchidos.', 'error')
        return redirect(url_for('produtos'))
    
    try:
        preco = float(preco)
        quantidade = int(quantidade)
        estoque_minimo = int(estoque_minimo)
        
        if preco < 0 or quantidade < 0 or estoque_minimo < 0:
            flash('Os valores não podem ser negativos.', 'error')
            return redirect(url_for('produtos'))
    except ValueError:
        flash('Valores inválidos. Verifique os campos numéricos.', 'error')
        return redirect(url_for('produtos'))
    
    conn = get_db()
    conn.execute(
        'UPDATE produtos SET nome = ?, descricao = ?, preco = ?, quantidade = ?, estoque_minimo = ? WHERE id = ?',
        (nome, descricao, preco, quantidade, estoque_minimo, id)
    )
    conn.commit()
    conn.close()
    
    flash('Produto atualizado com sucesso!', 'success')
    return redirect(url_for('produtos'))

@app.route('/produtos/excluir/<int:id>')
@login_required
def excluir_produto(id):
    conn = get_db()
    conn.execute('DELETE FROM produtos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    flash('Produto excluído com sucesso!', 'success')
    return redirect(url_for('produtos'))

@app.route('/estoque')
@login_required
def estoque():
    conn = get_db()
    produtos = conn.execute('SELECT * FROM produtos').fetchall()
    conn.close()
    
    produtos_list = list(produtos)
    n = len(produtos_list)
    for i in range(n):
        for j in range(0, n - i - 1):
            if produtos_list[j]['nome'].lower() > produtos_list[j + 1]['nome'].lower():
                produtos_list[j], produtos_list[j + 1] = produtos_list[j + 1], produtos_list[j]
    
    return render_template('estoque.html', produtos=produtos_list)

@app.route('/estoque/movimentar', methods=['POST'])
@login_required
def movimentar_estoque():
    produto_id = request.form.get('produto_id')
    tipo_movimentacao = request.form.get('tipo_movimentacao')
    quantidade = request.form.get('quantidade')
    data_movimentacao = request.form.get('data_movimentacao')
    
    if not produto_id or not tipo_movimentacao or not quantidade or not data_movimentacao:
        flash('Todos os campos devem ser preenchidos.', 'error')
        return redirect(url_for('estoque'))
    
    try:
        quantidade = int(quantidade)
        if quantidade <= 0:
            flash('A quantidade deve ser maior que zero.', 'error')
            return redirect(url_for('estoque'))
    except ValueError:
        flash('Quantidade inválida.', 'error')
        return redirect(url_for('estoque'))
    
    conn = get_db()
    produto = conn.execute('SELECT * FROM produtos WHERE id = ?', (produto_id,)).fetchone()
    
    if not produto:
        flash('Produto não encontrado.', 'error')
        conn.close()
        return redirect(url_for('estoque'))
    
    nova_quantidade = produto['quantidade']
    
    if tipo_movimentacao == 'entrada':
        nova_quantidade += quantidade
    elif tipo_movimentacao == 'saida':
        if produto['quantidade'] < quantidade:
            flash('Quantidade insuficiente em estoque.', 'error')
            conn.close()
            return redirect(url_for('estoque'))
        nova_quantidade -= quantidade
    
    conn.execute('UPDATE produtos SET quantidade = ? WHERE id = ?', (nova_quantidade, produto_id))
    
    conn.execute(
        'INSERT INTO movimentacoes (produto_id, tipo, quantidade, data_movimentacao) VALUES (?, ?, ?, ?)',
        (produto_id, tipo_movimentacao, quantidade, data_movimentacao)
    )
    
    conn.commit()
    
    if tipo_movimentacao == 'saida' and nova_quantidade < produto['estoque_minimo']:
        flash(f'ALERTA: O produto "{produto["nome"]}" está abaixo do estoque mínimo! Quantidade atual: {nova_quantidade}, Mínimo: {produto["estoque_minimo"]}', 'warning')
    else:
        flash('Movimentação realizada com sucesso!', 'success')
    
    conn.close()
    return redirect(url_for('estoque'))

if __name__ == '__main__':
    app.run(debug=True)
