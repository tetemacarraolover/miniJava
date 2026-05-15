class TesteErroEscopo { // Teste para erros semânticos de escopo
    static void minhaFuncao(){ // Aqui vem o erro semântico :0
        System.out.println(y) // A função tenta imprimir 'y', mas 'y' não existe neste escopo (ele pertence ao main).
    }
    public static void main(String[] args){
        int y = 5;
        
        //Chamada de função
        minhaFuncao(); 
    }
}