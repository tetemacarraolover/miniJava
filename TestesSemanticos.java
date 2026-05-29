public class TestesSemanticos {

    // Função válida
    public static void funcaoValida() {
    }
    //  Variável fora do escopo
 
    public static void testeErroEscopo() {
        System.out.println(y);
        // Erro semântico:
        // variavel 'y' não existe neste escopo
    }

    // Função inexistente
    // =========================
    public static void testeFuncaoInexistente() {
        minhaFuncao();
        // Erro semântico:
        // função não declarada
    }
   
    // Tipo incompatível
    public static void testeTipoIncompativel() {
        float x = "hello world";
        // Erro semântico:
        // tipos incompatíveis
    }

    //  Variável duplicada

    public static void testeVariavelDuplicada() {
        int x = 10;
        int x = 20;

        // Erro semântico:
        // variável duplicada no mesmo escopo
    }

  
    // Variável nao declarada
    public static void testeVariavelNaoDeclarada() {
        System.out.println(z);

        // Erro semântico:
        // variável 'z' não declarada
    }


    //  Terceiro escopo
    public static void testeEscopoInterno() {

        int limite = 100;

        class Validador {

            void validar(int valor) {

                if (valor > limite) {
                    System.out.println(valor);
                }

                System.out.println(x);
                // Erro semântico:
                // variável 'x' não existe neste escopo
            }
        }

        Validador v = new Validador();
        v.validar(150);
    }


    // main
    public static void main(String[] args) {

        funcaoValida();

        testeErroEscopo();
        testeFuncaoInexistente();
        testeTipoIncompativel();
        testeVariavelDuplicada();
        testeVariavelNaoDeclarada();
        testeEscopoInterno();
    }
}