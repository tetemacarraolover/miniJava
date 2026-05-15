class TesteFuncaoInexistente { // Teste para chamada de função

    public static void main(String[] args){
        int x = 10;
        System.out.println(x);

        //Chamada de função
        minhaFuncao(); //Erro, função 'minhaFuncao' não foi declarada, ou seja, inexistente
    }
}