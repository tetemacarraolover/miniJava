class TesteVariavelNaoDeclarada {
    static void minhaFuncao(){
    }
    public static void main(String[] args) {
        // Erro semântico: a variável 'z' está quer ser usada, mas nunca foi declarada.
        System.out.println(z);

        //Chamada de função
        minhaFuncao();
    }
}