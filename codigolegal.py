from lark import Lark, Transformer, v_args
from collections import ChainMap
# O objetivo é implementar um analisador (léxico, sintático e semântico) para um subconjunto dasintaxe uma linguagem 
# moderna de programação, no caso, Java.
# O analisador deve ser capaz de identificar erros léxicos, sintáticos e semânticos, e fornecer mensagens de erro claras e informativas para o usuário.
# O analisador deve ser implementado em Python, utilizando a biblioteca Lark para a análise
# O analisador deve ser capaz de processar arquivos de código-fonte Java e gerar uma representação interna da estrutura do código, como uma árvore de sintaxe abstrata (AST).
# O analisador deve ser capaz de lidar com as seguintes construções da linguagem Java:
# - Declaração de classes e interfaces
# - Declaração de métodos e variáveis
# - Estruturas de controle de fluxo (if, else, while, for)
# - Expressões aritméticas e lógicas
# - Chamadas de métodos e acesso a membros de classe
# - Comentários e espaços em branco
# O analisador deve detectar erros semânticos: isso depende da correta manutenção da
# tabela de símbolos para validar a visibilidade de cada nome de variável nos diversos
# escopos estáticos do código-fonte → sugere-se a classe ChainMap de Python.
# ● Os erros produzidos pelo analisador devem corresponder à saída de um compilador ou
# interpretador oficial para a linguagem escolhida → deve-se identificar as mesmas
# situações, mas não é necessário gerar as mesmas mensagens de erro, embora seja recomendado que as mensagens sejam claras e informativas.
# # O analisador deve ser capaz de identificar e relatar os seguintes tipos de erros:
# - Erros léxicos: caracteres inválidos, tokens não reconhecidos, etc.
# - Erros sintáticos: construção de código inválida, falta de elementos obrigatórios,
#   etc.
# - Erros semânticos: uso de variáveis não declaradas, tipos incompatíveis
# O analisador deve ser projetado de forma modular, permitindo a fácil extensão e manutenção do código.
# O código deve ser bem documentado, com comentários explicando a lógica e a estrutura do
# código, e deve seguir as melhores práticas de programação em Python.
# O código deve ser testado com uma variedade de casos de teste, incluindo casos válidos e casos com erros léxicos, sintáticos e semânticos, para garantir a robustez e a precisão do analisador.
# A seguir, apresento um exemplo de implementação de um analisador léxico e sintático para um subconjunto da linguagem Java utilizando a biblioteca Lark.


# Definindo a gramática para o subconjunto da linguagem Java
java_gramatica = """
    programa: declaracao_classe
    declaracao_classe: "class" IDENTIFICADOR "{" corpo_classe* "}"   # Declaração de classe, exemplo: class MinhaClasse { ... }
    corpo_classe: "static" "void" IDENTIFICADOR "(" ")" "{" corpo_funcao* "}"   # Declaração de método exemplo: static void main() { ... }
    corpo_funcao: declaracao_variavel | estrutura_controle | expressao    # Corpo do método exemplo: int x; if (x > 0) { ... } x = 5;
    declaracao_variavel: tipo IDENTIFICADOR ";" # Declaração de variável, exemplo: int x;
    estrutura_controle: "if" "(" expressao ")" "{" corpo_funcao* "}" ("else" "{" corpo_funcao* "}")?  # Estrutura de controle if-else, exemplo: if (x > 0) { ... } else { ... }
    expressao: IDENTIFICADOR "=" expressao | IDENTIFICADOR "(" ")" | IDENTIFICADOR | NUMERO   # Expressão de atribuição, chamada de método, acesso a variável ou número, exemplo: x = 5; minhaFuncao(); x;
    tipo: "int" | "String" | "boolean"  | "double" | "float"  # Tipos de dados, exemplo: int, String, boolean, double
    IDENTIFICADOR: /[a-zA-Z_][a-zA-ZA-Z0-9_]*/  # O que aceitamos como identificador, exemplo: minhaVariavel, minhaFuncao
    NUMERO: /\d+/ # O que aceitamos como número, exemplo: 123
    %import common.WS
    %ignore WS
"""


# Criando o analisador sintático utilizando a gramática definida
analisador = Lark(java_gramatica, start='programa')
# Criando uma classe para transformar a árvore de sintaxe em uma representação mais útil
class JavaTransformer(Transformer):
    def programa(self, items):
        return {"programa": items} # Representação do programa como um dicionário, exemplo: {"programa": [classe1, classe2, ...]}
    
    def declaracao_classe(self, items):
        return {"classe": items[0], "corpo": items[1:]} # Representação da declaração de classe como um dicionário, exemplo: {"classe": "MinhaClasse", "corpo": [metodo1, metodo2, ...]}
    
    def corpo_classe(self, items):
        return {"metodo": items[2], "corpo": items[3:]}
    
    def corpo_funcao(self, items):
        return items[0] # Representação do corpo do método como um dicionário, exemplo: {"metodo": "minhaFuncao", "corpo": [declaracao_variavel, estrutura_controle, ...]}
    
    def declaracao_variavel(self, items):
        return {"variavel": items[1], "tipo": items[0]} # Representação da declaração de variável como um dicionário, exemplo: {"variavel": "x", "tipo": "int"}
    
    def estrutura_controle(self, items):
        controle = {"tipo": "if", "condicao": items[0], "corpo_if": items[1]}
        if len(items) > 2:
            controle["corpo_else"] = items[2]
        return controle
    
    
    def expressao(self, items):
        if len(items) == 3:
            return {"atribuicao": {"variavel": items[0], "valor": items[2]}}
        elif len(items) == 2:
            return {"chamada_metodo": {"metodo": items[0]}}
        else:
            return {"variavel_ou_numero": items[0]}
    def tipo(self, items):
        return items[0]
    def IDENTIFICADOR(self, token):
        return str(token)
    def NUMERO(self, token):
        return int(token)
# Função para analisar o código-fonte Java e gerar a representação interna da estrutura do código (AST)
def analisar_codigo(codigo):
    try:
        arvore = analisador.parse(codigo)
        transformer = JavaTransformer()
        ast = transformer.transform(arvore)
        return ast
    except Exception as e:
        print(f"Erro ao analisar o código: {e}")
        return None
# Exemplo de uso
codigo_java = """
class MinhaClasse {
    static void main() {
        int x;
        x = 5;
        if (x > 0) {
            System.out.println("x é positivo");
        } else {
            System.out.println("x é negativo ou zero");
        }
    }
}
"""
ast = analisar_codigo(codigo_java)
print(ast)



