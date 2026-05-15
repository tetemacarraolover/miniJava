class MiniJavaTeste { // Teste para a sintaxe válida
    // Definindo a função
    static void minhaFuncao(){
        // Função que não precisa fazer nada pra análise sintática
    }
    public static void main(String[] args){
        int x = 10;    // imprime x e existe dentro do escopo alem de nao estar duplicada 
        System.out.println(x);

        //Chamada de função
        minhaFuncao();// chama funcao existente 
    }
}