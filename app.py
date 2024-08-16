from flask import Flask, render_template, request
from collections import Counter

app = Flask(__name__)

# Lista de receitas, ingredientes, avaliação e número de pedidos
receitas = {
    "Bolo de Chocolate": {"ingredientes": ["chocolate", "açúcar", "farinha", "ovo"], "avaliacao": 4.8, "num_pedidos": 120},
    "Salada de Frutas": {"ingredientes": ["maçã", "banana", "laranja", "mel"], "avaliacao": 4.5, "num_pedidos": 80},
    "Sorvete de Baunilha": {"ingredientes": ["baunilha", "leite", "açúcar"], "avaliacao": 4.7, "num_pedidos": 95},
    "Sopa de Legumes": {"ingredientes": ["cenoura", "batata", "cebola", "alho"], "avaliacao": 4.2, "num_pedidos": 60},
    "Sanduíche": {"ingredientes": ["pão", "queijo", "presunto", "alface"], "avaliacao": 4.0, "num_pedidos": 150},
    "Torta de Maçã": {"ingredientes": ["maçã", "canela", "farinha", "manteiga"], "avaliacao": 4.6, "num_pedidos": 110},
    "Brigadeiro": {"ingredientes": ["leite condensado", "chocolate", "manteiga"], "avaliacao": 4.9, "num_pedidos": 200},
    "Frango Grelhado": {"ingredientes": ["frango", "sal", "pimenta", "alho"], "avaliacao": 4.4, "num_pedidos": 130},
    "Pizza": {"ingredientes": ["queijo", "molho de tomate", "presunto", "azeitona"], "avaliacao": 4.9, "num_pedidos": 220},
    "Lasanha": {"ingredientes": ["massa", "queijo", "carne", "molho de tomate"], "avaliacao": 4.7, "num_pedidos": 170},
    "Suco de Laranja": {"ingredientes": ["laranja", "açúcar", "água"], "avaliacao": 4.3, "num_pedidos": 75},
    "Café Gelado": {"ingredientes": ["café", "gelo", "açúcar"], "avaliacao": 4.5, "num_pedidos": 85},
    "Chá Quente": {"ingredientes": ["chá", "água", "açúcar"], "avaliacao": 4.1, "num_pedidos": 55},
    "Pipoca Doce": {"ingredientes": ["milho", "açúcar", "manteiga"], "avaliacao": 4.2, "num_pedidos": 90},
    "Salada Verde": {"ingredientes": ["alface", "tomate", "pepino", "azeite"], "avaliacao": 4.3, "num_pedidos": 65},
}

# Função para sugerir receita baseada na similaridade, avaliação e número de pedidos
def sugerir_receita(escolhas):
    ingredientes_escolhidos = []
    for escolha in escolhas:
        ingredientes_escolhidos.extend(receitas[escolha]["ingredientes"])
    
    ingredientes_contados = Counter(ingredientes_escolhidos)
    
    # Filtrar receitas que não foram escolhidas
    receitas_possiveis = {k: v for k, v in receitas.items() if k not in escolhas}
    
    # Calcular similaridade e outros fatores
    similaridades = {}
    for receita, detalhes in receitas_possiveis.items():
        similaridade = sum(ingredientes_contados[ing] for ing in detalhes["ingredientes"])
        # Ajuste da similaridade com base na avaliação e no número de pedidos
        score = similaridade * detalhes["avaliacao"] * (1 + detalhes["num_pedidos"] / 100)
        similaridades[receita] = score
    
    # Retornar a receita com maior pontuação
    return max(similaridades, key=similaridades.get)

@app.route('/', methods=['GET', 'POST'])
def index():
    sugestao = None
    escolhas_usuario = []
    
    if request.method == 'POST':
        escolhas_usuario = [request.form.get('pedido1'), request.form.get('pedido2'), request.form.get('pedido3')]
        escolhas_usuario = [escolha for escolha in escolhas_usuario if escolha]
        sugestao = sugerir_receita(escolhas_usuario)
    
    return render_template('index.html', receitas=receitas, sugestao=sugestao, escolhas=escolhas_usuario)

if __name__ == '__main__':
    app.run(debug=True)
