from flask import Flask, render_template, request
from collections import Counter

app = Flask(__name__)

# Lista expandida de receitas com ingredientes em comum, avaliação e número de pedidos
receitas = {
    "Bolo de Chocolate": {"ingredientes": ["chocolate", "açúcar", "farinha", "ovo", "manteiga"], "avaliacao": 4.8, "num_pedidos": 120},
    "Salada de Frutas": {"ingredientes": ["maçã", "banana", "laranja", "mel"], "avaliacao": 4.5, "num_pedidos": 80},
    "Sorvete de Baunilha": {"ingredientes": ["baunilha", "leite", "açúcar", "creme de leite"], "avaliacao": 4.7, "num_pedidos": 95},
    "Sopa de Legumes": {"ingredientes": ["cenoura", "batata", "cebola", "alho"], "avaliacao": 4.2, "num_pedidos": 60},
    "Sanduíche": {"ingredientes": ["pão", "queijo", "presunto", "alface", "manteiga"], "avaliacao": 4.0, "num_pedidos": 150},
    "Torta de Maçã": {"ingredientes": ["maçã", "canela", "farinha", "manteiga", "açúcar"], "avaliacao": 4.6, "num_pedidos": 110},
    "Brigadeiro": {"ingredientes": ["leite condensado", "chocolate", "manteiga", "açúcar"], "avaliacao": 4.9, "num_pedidos": 200},
    "Frango Grelhado": {"ingredientes": ["frango", "sal", "pimenta", "alho", "manteiga"], "avaliacao": 4.4, "num_pedidos": 130},
    "Pizza": {"ingredientes": ["queijo", "molho de tomate", "presunto", "azeitona", "orégano"], "avaliacao": 4.9, "num_pedidos": 220},
    "Lasanha": {"ingredientes": ["massa", "queijo", "carne", "molho de tomate", "orégano"], "avaliacao": 4.7, "num_pedidos": 170},
    "Suco de Laranja": {"ingredientes": ["laranja", "açúcar", "água"], "avaliacao": 4.3, "num_pedidos": 75},
    "Café Gelado": {"ingredientes": ["café", "gelo", "açúcar", "leite"], "avaliacao": 4.5, "num_pedidos": 85},
    "Chá Quente": {"ingredientes": ["chá", "água", "açúcar", "limão"], "avaliacao": 4.1, "num_pedidos": 55},
    "Pipoca Doce": {"ingredientes": ["milho", "açúcar", "manteiga"], "avaliacao": 4.2, "num_pedidos": 90},
    "Salada Verde": {"ingredientes": ["alface", "tomate", "pepino", "azeite", "sal"], "avaliacao": 4.3, "num_pedidos": 65},
    "Risoto de Frango": {"ingredientes": ["arroz", "frango", "caldo de galinha", "alho", "cebola"], "avaliacao": 4.6, "num_pedidos": 140},
    "Espaguete à Bolonhesa": {"ingredientes": ["massa", "carne", "molho de tomate", "alho", "cebola"], "avaliacao": 4.8, "num_pedidos": 200},
    "Tiramisu": {"ingredientes": ["café", "açúcar", "mascarpone", "ovos", "cacau"], "avaliacao": 4.7, "num_pedidos": 90},
    "Panqueca": {"ingredientes": ["farinha", "ovo", "leite", "manteiga", "açúcar"], "avaliacao": 4.5, "num_pedidos": 75},
    "Omelete": {"ingredientes": ["ovo", "queijo", "presunto", "cebola", "pimentão"], "avaliacao": 4.3, "num_pedidos": 100},
    "Cuscuz": {"ingredientes": ["milho", "água", "sal", "manteiga", "queijo"], "avaliacao": 4.4, "num_pedidos": 95},
    "Moqueca": {"ingredientes": ["peixe", "leite de coco", "pimentão", "tomate", "cebola"], "avaliacao": 4.6, "num_pedidos": 130},
    "Bruschetta": {"ingredientes": ["pão", "tomate", "manjericão", "azeite", "alho"], "avaliacao": 4.7, "num_pedidos": 80},
    "Taco": {"ingredientes": ["tortilha", "carne", "queijo", "alface", "tomate"], "avaliacao": 4.5, "num_pedidos": 110},
    "Churrasco": {"ingredientes": ["carne", "sal grosso", "alho", "pimenta", "azeite"], "avaliacao": 4.9, "num_pedidos": 300},
    "Pão de Queijo": {"ingredientes": ["polvilho", "queijo", "leite", "ovo", "manteiga"], "avaliacao": 4.8, "num_pedidos": 250},
    "Crepe": {"ingredientes": ["farinha", "ovo", "leite", "manteiga", "açúcar"], "avaliacao": 4.7, "num_pedidos": 85},
    "Hambúrguer": {"ingredientes": ["pão", "carne", "queijo", "alface", "tomate"], "avaliacao": 4.8, "num_pedidos": 210},
    "Empadão": {"ingredientes": ["farinha", "frango", "manteiga", "ovo", "cebola"], "avaliacao": 4.7, "num_pedidos": 120},
    "Ceviche": {"ingredientes": ["peixe", "limão", "cebola", "coentro", "pimenta"], "avaliacao": 4.5, "num_pedidos": 60},
    "Brownie": {"ingredientes": ["chocolate", "açúcar", "farinha", "manteiga", "ovo"], "avaliacao": 4.9, "num_pedidos": 180},
    "Pavê": {"ingredientes": ["biscoito", "leite condensado", "creme de leite", "chocolate", "ovo"], "avaliacao": 4.6, "num_pedidos": 140},
    "Escondidinho": {"ingredientes": ["batata", "carne", "queijo", "creme de leite", "alho"], "avaliacao": 4.7, "num_pedidos": 100},
}

def sugerir_receita(escolhas):
    ingredientes_escolhidos = []
    for escolha in escolhas:
        ingredientes_escolhidos.extend(receitas[escolha]["ingredientes"])
    
    ingredientes_contados = Counter(ingredientes_escolhidos)
    
    receitas_possiveis = {k: v for k, v in receitas.items() if k not in escolhas}
    
    similaridades = {}
    for receita, detalhes in receitas_possiveis.items():
        similaridade = sum(ingredientes_contados[ing] for ing in detalhes["ingredientes"])
        score = similaridade * detalhes["avaliacao"] * (1 + detalhes["num_pedidos"] / 100)
        similaridades[receita] = score
    
    melhor_receita = max(similaridades, key=similaridades.get)
    ingredientes_similares = [ing for ing in receitas[melhor_receita]["ingredientes"] if ing in ingredientes_contados]
    
    return melhor_receita, ingredientes_similares

@app.route('/', methods=['GET', 'POST'])
def index():
    sugestao = None
    escolhas_usuario = []
    ingredientes_similares = []
    
    if request.method == 'POST':
        escolhas_usuario = [request.form.get('pedido1'), request.form.get('pedido2'), request.form.get('pedido3')]
        escolhas_usuario = [escolha for escolha in escolhas_usuario if escolha]
        sugestao, ingredientes_similares = sugerir_receita(escolhas_usuario)
    
    return render_template('index.html', receitas=receitas, sugestao=sugestao, escolhas=escolhas_usuario, ingredientes_similares=ingredientes_similares)

if __name__ == '__main__':
    app.run(debug=True)
