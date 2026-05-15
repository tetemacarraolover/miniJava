class TesteVariavelDuplicada{ // Teste quando declaramos duas variáveis com o mesmo nome no mesmo escopo
    static void minhaFuncao(){

    }
    public static void main(String[] args){
        int x = 10;
        int x = 20; // Erro semântico: variável 'x' duplicada
        System.out.println(x);

        //Chamada de função
        minhaFuncao();
    }
}