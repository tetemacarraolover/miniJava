from lark import Lark, Transformer
from collections import ChainMap
import warnings

# Definindo a gramática para o subconjunto da linguagem Java
java_gramatica = r"""
    programa: declaracao_classe
    declaracao_classe: "class" IDENTIFICADOR "{" corpo_classe* "}"
    corpo_classe: "public"? "static" "void" IDENTIFICADOR "(" parametro? ")" "{" corpo_funcao* "}"
    parametro: "String" "[" "]" IDENTIFICADOR
    corpo_funcao: declaracao_variavel | estrutura_controle | expressao_stmt | comando_saida
    declaracao_variavel: tipo IDENTIFICADOR ";"
    estrutura_controle: "if" "(" expressao ")" "{" corpo_funcao* "}" ("else" "{" corpo_funcao* "}")?
    expressao_stmt: expressao ";"
    expressao: atribuicao
         | comparacao
    atribuicao: IDENTIFICADOR "=" expressao
    comparacao: soma (MAIOR soma)*
    soma: termo ((MAIS | MENOS) termo)*
    termo: fator ((MULT | DIV) fator)*

    MAIOR: ">"
    MAIS: "+"
    MENOS: "-"
    MULT: "*"
    DIV: "/"
    fator: chamada_funcao | IDENTIFICADOR | NUMERO | STRING | "(" expressao ")"
    chamada_funcao: IDENTIFICADOR "(" [argumentos] ")"
    argumentos: expressao ("," expressao)*
    comando_saida: "System" "." "out" "." "println" "(" expressao ")" ";"
    tipo: TIPO
    TIPO.2: "int" | "String" | "boolean" | "double" | "float"
    IDENTIFICADOR: /[a-zA-Z_][a-zA-Z0-9_]*/
    NUMERO: /\d+/
    STRING: ESCAPED_STRING
    %import common.ESCAPED_STRING
    %import common.WS
    %ignore WS
"""

# Criando o analisador sintático utilizando a gramática definida
analisador = Lark(java_gramatica, start='programa', parser='lalr')

# Criando uma classe para transformar a árvore de sintaxe em uma representação mais útil
class JavaTransformer(Transformer): # Transformador para converter a árvore de sintaxe em uma representação mais útil (AST)
    def programa(self, items):
        return {"programa": items}

    def declaracao_classe(self, items): # Representação da declaração de classe como um dicionário, exemplo: {"classe": "MinhaClasse", "corpo": [metodo1, metodo2, ...]}
        return {"classe": items[0], "corpo": items[1:]}

    def corpo_classe(self, items): # Representação da declaração de método como um dicionário
        method_name = items[0]

        #ignora parametro
        if len(items) > 1 and "Tree" in str(type(items[1])):
            body = items[2:]
        else:
            body = items[1:]

        return {
            "metodo": method_name,
            "corpo": body
    }
    def corpo_funcao(self, items): # Representação do corpo do método como um dicionário, exemplo: {"metodo": "minhaFuncao", "corpo": [declaracao_variavel, estrutura_controle, ...]}
        return items[0]

    def declaracao_variavel(self, items): # Representação da declaração de variável como um dicionário, exemplo: {"variavel": "x", "tipo": "int"}
        return {"tipo": items[0], "variavel": items[1]}

    def comando_saida(self, items): # Representação do comando de saída como um dicionário, exemplo: {"tipo": "saida", "expressao": ...}
        return {"tipo": "saida", "expressao": items[0]}

    def estrutura_controle(self, items): # Representação da estrutura de controle if-else como um dicionário, exemplo: {"tipo": "if", "condicao": ..., "corpo_if": [...], "corpo_else": [...]}
        controle = {"tipo": "if", "condicao": items[0], "corpo_if": items[1]}
        if len(items) > 2:
            controle["corpo_else"] = items[2]
        return controle

    def expressao_stmt(self, items): # Representação de uma expressão como um dicionário, exemplo: {"tipo": "expressao", "valor": ...}
        return items[0]

    def expressao(self, items):
        return items[0]

    def atribuicao(self, items): # Representação da atribuição como um dicionário, exemplo: {"tipo": "atribuicao", "variavel": "x", "valor": 5}
        return {
            "tipo": "atribuicao",
            "variavel": items[0],
            "valor": items[1]
        }

    def comparacao(self, items): # Representação da comparação como um dicionário, exemplo: {"tipo": "comparacao", "operador": ">", "esquerda": ..., "direita": ...}
        if len(items) == 1:
            return items[0]
        left = items[0]
        for operador, right in zip(items[1::2], items[2::2]):
            left = {"tipo": "comparacao", "operador": operador, "esquerda": left, "direita": right}
        return left

    def soma(self, items): # Representação da soma como um dicionário, exemplo: {"tipo": "soma", "operador": "+", "esquerda": ..., "direita": ...}
        if len(items) == 1:
            return items[0]
        left = items[0]
        for operador, right in zip(items[1::2], items[2::2]):
            left = {"tipo": "soma", "operador": operador, "esquerda": left, "direita": right}
        return left

    def termo(self, items): # Representação do termo como um dicionário, exemplo: {"tipo": "termo", "operador": "*", "esquerda": ..., "direita": ...}
        if len(items) == 1:
            return items[0]
        left = items[0]
        for operador, right in zip(items[1::2], items[2::2]):
            left = {"tipo": "termo", "operador": operador, "esquerda": left, "direita": right}
        return left

    def fator(self, items): # Representação do fator como um dicionário, exemplo: {"tipo": "fator", "valor": ...}
        return items[0]

    def chamada_funcao(self, items): # Representação da chamada de função como um dicionário, exemplo: {"tipo": "chamada_funcao", "funcao": "minhaFuncao", "argumentos": [...]}
        if len(items) == 2:
            return {"tipo": "chamada_funcao", "funcao": items[0], "argumentos": items[1]}
        return {"tipo": "chamada_funcao", "funcao": items[0], "argumentos": []}

    def argumentos(self, items): # Representação dos argumentos como uma lista, exemplo: [{"tipo": "expressao", "valor": ...}, {"tipo": "expressao", "valor": ...}, ...]
        return items

    def tipo(self, items): # Representação do tipo como uma string, exemplo: "int", "String", etc.
        return items[0]

    def IDENTIFICADOR(self, token): # Representação do identificador como uma string, exemplo: "x", "MinhaClasse", etc.
        return str(token)

    def NUMERO(self, token): # Representação do número como um inteiro, exemplo: 5, 10, etc.
        return int(token)

    def STRING(self, token): # Representação da string como uma string sem as aspas, exemplo: "Olá, mundo!" -> Olá, mundo!
        return str(token)[1:-1]

    

def analisar_codigo(codigo): # Função para analisar o código Java e detectar erros de sintaxe, retornando a AST se o código for válido ou None se houver erros de sintaxe
    try:
        arvore = analisador.parse(codigo)
        ast = JavaTransformer().transform(arvore)
        print("Código Java válido.")
        return ast
    except Exception as e:
        print(f"Erro de sintaxe: {e}")
        return None
# Exemplo de uso do analisador para um código Java válido e para um código Java com erros de sintaxe para testar a função analisar_codigo e verificar se o analisador está funcionando corretamente.
codigo_java = """
class MinhaClasse {
    public static void main(String[] args) {
        int x;
        x = 5;
        if (x > 0) {
            System.out.println(x);
        } else {
            System.out.println("x é menor ou igual a 0");
        }
    }
}
"""
analisar_codigo(codigo_java)
class AnalisadorSemantico:

    def __init__(self):

        self.tabela_variaveis = ChainMap({})
        self.tabela_classe = {}

    def analisador_semantico(self, no):

        #metodo
        if "metodo" in no:

            print(f"entrando no método: {no['metodo']}")

            #criacao escopo
            self.tabela_variaveis = self.tabela_variaveis.new_child()

            #percorre comandos do metodo
            for comando in no["corpo"]:
                self.analisador_semantico(comando)

            #warning variavel nao utilizada
            for nome, info in self.tabela_variaveis.maps[0].items():

                if info["usada"] == False:

                    warnings.warn(
                        f"variável '{nome}' não utilizada"
                    )

            #saida do escopo
            self.tabela_variaveis = self.tabela_variaveis.parents

            print(f"saindo do método: {no['metodo']}")

        #variavel
        elif "variavel" in no and no["tipo"] != "atribuicao":

            nome = no["variavel"]

            #variavel duplicada
            if nome in self.tabela_variaveis.maps[0]:

                print("Erro: Variável duplicada")

            else:

                #warning variavel global
                if nome in self.tabela_variaveis:

                    warnings.warn(
                        f"Atenção a variável '{nome}' está sendo ocultada"
                    )

                self.tabela_variaveis[nome] = {
                    "tipo": no["tipo"],
                    "usada": False
                }

                print(f"variavel '{nome}' declarada")

        #atribuicao
        elif no.get("tipo") == "atribuicao":

            nome = no["variavel"]

            #variavel nao declarada
            if nome not in self.tabela_variaveis:

                print("Erro: variavel não declarada")

            else:

                #marca variavel como usada
                self.tabela_variaveis[nome]["usada"] = True

                print("variavel declarada")

        #funcoes
        elif no.get("tipo") == "chamada_funcao":

            funcao = no["funcao"]

            #funcao inexistente
            if funcao not in self.tabela_classe:

                print("Erro: função inexistente")

            else:

                print(f"função '{funcao}' encontrada")

        #classe
        elif "classe" in no:

            for item in no["corpo"]:
                self.analisador_semantico(item)
#gera AST
ast = analisar_codigo(codigo_java)

#executa analise semantica
if ast:
    analisador_semantico = AnalisadorSemantico()

    #percorre programa
    for item in ast["programa"]:
        analisador_semantico.analisador_semantico(item)