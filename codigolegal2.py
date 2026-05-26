from lark import Lark, Transformer, v_args

# Definindo a gramática para o subconjunto da linguagem Java
java_gramatica = """
    programa: declaracao_classe
    declaracao_classe: "class" IDENTIFICADOR "{" corpo_classe* "}"   # Declaração de classe, exemplo: class MinhaClasse { ... }
    corpo_classe: "public"? "static" "void" IDENTIFICADOR "(" ("String[]" IDENTIFICADOR)? ")" "{" corpo_funcao* "}"   # Declaração de método exemplo: publicstatic void main() { ... }
    corpo_funcao: declaracao_variavel | estrutura_controle | expressao | comando_saida  # Corpo do método exemplo: int x; if (x > 0) { ... } x = 5; System.out.println(x);
    declaracao_variavel: tipo IDENTIFICADOR ";" # Declaração de variável, exemplo: int x;
    estrutura_controle: "if" "(" expressao ")" "{" corpo_funcao* "}" ("else" "{" corpo_funcao* "}")?  # Estrutura de controle if-else, exemplo: if (x > 0) { ... } else { ... }
    expressao: IDENTIFICADOR "=" expressao ";" | IDENTIFICADOR "(" ")" ";" | IDENTIFICADOR | NUMERO   # Expressão de atribuição, chamada de método, acesso a variável ou número, exemplo: x = 5; minhaFuncao(); x;
    comando_saida: "System.out.println" "(" expressao ")" ";"  # Comando de saída, exemplo: System.out.println(x);
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
        return {"metodo": items[2], "corpo": items[3:]} # Representação do corpo da classe como um dicionário, exemplo: {"metodo": "main", "corpo": [declaracao_variavel, estrutura_controle, ...]}
    
    def corpo_funcao(self, items):
        return items[0] # Representação do corpo do método como um dicionário, exemplo: {"metodo": "minhaFuncao", "corpo": [declaracao_variavel, estrutura_controle, ...]}
    
    def declaracao_variavel(self, items):
        return {"variavel": items[1], "tipo": items[0]} # Representação da declaração de variável como um dicionário, exemplo: {"variavel": "x", "tipo": "int"}
    
    def comando_saida(self, items):
        return {"tipo": "saida", "expressao": items[0]} # Representação do comando de saída como um dicionário, exemplo: {"tipo": "saida", "expressao": "x"}
    
    def estrutura_controle(self, items):
        controle = {"tipo": "if", "condicao": items[0], "corpo_if": items[1]} # Representação da estrutura de controle if como um dicionário, exemplo: {"tipo": "if", "condicao": "x > 0", "corpo_if": [declaracao_variavel, expressao, ...]}
        if len(items) > 2:
            controle["corpo_else"] = items[2]
        return controle
    
    def expressao(self, items):
        if len(items) == 3 and items[1] == "=":
            return {"tipo": "atribuicao", "variavel": items[0], "valor": items[2]} # Representação de expressão de atribuição como um dicionário, exemplo: {"tipo": "atribuicao", "variavel": "x", "valor": 5}
        elif len(items) == 2 and isinstance(items[1], list):
            return {"tipo": "chamada_funcao", "funcao": items[0], "argumentos": []} # Representação de chamada de função como um dicionário, exemplo: {"tipo": "chamada_funcao", "funcao": "minhaFuncao", "argumentos": []}
        elif len(items) == 1 and isinstance(items[0], str):
            return {"tipo": "variavel", "nome": items[0]} # Representação de acesso a variável como um dicionário, exemplo: {"tipo": "variavel", "nome": "x"}
        elif len(items) == 1 and isinstance(items[0], int):
            return {"tipo": "numero", "valor": items[0]} # Representação de número como um dicionário, exemplo: {"tipo": "numero", "valor": 123}
    def tipo(self, items):
        return items[0]
    def IDENTIFICADOR(self, token):
            return str(token)
    def NUMERO(self, token):
        return int(token)
    