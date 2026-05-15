class TesteFuncaoInexistente{ // Teste quando declaramos duas variáveis com o mesmo nome no mesmo escopo
    static void minhaFuncao(){

    }
    public static void main(String[] args){
        int x = 10;
        int x = 20; // Erro semântico: variável 'x' duplicada
        System.out.println(x);

        //Chamada de função
        minhaFuncao();
    }
}class TesteFuncaoInexistente { // Teste para chamada de função

    public static void main(String[] args){
        int x = 10;
        System.out.println(x);

        //Chamada de função
        minhaFuncao(); //Erro, função 'minhaFuncao' não foi declarada, ou seja, inexistente
    }
}