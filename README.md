# semnome
Classe Python desenvolvida para anonimizar informações sensíveis específicas (nome de pessoas, CPF e datas de nascimento) em textos técnicos ou administrativos, com o objetivo de criar uma camada extra de anonimização em workflows que envolvam a manipulação de strings.   

O foco está em **nomes de pessoas**, **datas de nascimento** e **CPFs**.

---

## ✨ Funcionalidades

- 🔒 **Anonimização de CPF**
- 🎂 **Anonimização de Data de Nascimento**
- 👤 **Anonimização de Nomes**
- 🔠 **Codificação / Decodificação de Maiúsculas**
- 🧠 **Camada Extra (opcional) com SpaCy**

---
**Detalhamento do funcionamento:**

A classe encapsula 5 funções específicas e pensadas para uso sequencial, de forma a gerar um tratamento consistente na anonimização de nomes próprios.
Diversas ferramentas de anonimização são baseadas em REGEX e acabam resultando em anonimizações "falso positivas", ou seja, quando o código acaba anonimizando uma expressão que parece nome próprio, mas não o é. No exemplo "então ele disse à Central de Adentimento que gostaria de (...)", pode haver anonimização indevida de "Central de Atendimento".
Mesmo utilizando modelos de processamento natural de linguagem (NLP), a exemplo do SpaCY, algumas ocorrências podem ser falseamente anonimizadas, o que acaba gerando diferentes perdas de conteúdo da string como um todo. 
Para eliminar tais efeitos, a classe "SemNome" estabelece 5 camadas a serem aplicadas de forma progressiva e incremental, a saber:

*ENTRADA DA STRING PARA TRATAMENTO*
(...)

(1) Primeira Camada (CPF):
Apenas anonnimização de CPF e data de nascimento, utilizando reconhecimento de seu padrão via REGEX (CPF) e REGEX + contexto (para eliminar apenas aquelas datas com contexto de nascimento e manter outras datas que podem não ser datas de nascimento).

(2) Segunda Camada (remover expressões chave - colocando-as em minusculas):
Aqui, a função recebe uma lista Python com inumeras expressões com maiusculas e minusculas que podem ser propositalmente colocadas em minusculas para criar maior segurança contra a sua anonimização. Tal lista pode contemplar centenas, milhares de expressões como "Constituição Federal", "Código de Defesa do Consumidor", "Formulário do Cliente", e quaisquer outras que sejam afetas ao ambiente de trabalho do qual se refere a string. Todas elas são colocadas em minusculas. 

(3) Terceira Camada (reconhecimento de nomes com NLP)
Aqui, as expressões remanescentes da segunda camada que possuam maiuscula-minuscula são submetidas a um modelo de processamento de linguagem natural - NLP (SpaCY), qie irá identificar quais estão em conexto de nomes e convertê-los em nomes abreviados 

(4) Quarta Camada (reconhecimento de nomes com REGEX + contexto)
Aqui, são eliminadas expressões no formato (i) maiuscula-minuscula ou (ii) todas em maiusculas que estejam proximas de expressões-chave que possuem contexto de nome, tais como "senhor" "senhora", "Sr", "cliente", etc.

(5) Quinta Camada (reversão das minusculas da 2ª camada)
Aqui, todas as palavras em minusculas que foram revertidas na segunda camada são "decodadas" e voltam a adquirir seu formato original.

(...)
*SAÍDA DA STRING TRATADA*

---

📦 Instalação
Clone o repositório:
git clone https://github.com/seu-usuario/semnome.git
cd semnome
(Ou copie o arquivo semnome.py para o seu projeto.)
Dependências opcionais (para SpaCy):
pip install spacy
python -m spacy download pt_core_news_sm
________________________________________
🚀 Exemplo de Uso

if __name__ == "__main__":
    engine = SemNome()

    texto = """
    O consumidor Carlos Santos de Aguiar, nascido em 12/05/1985, residente no Rio de Janeiro,
    apresentou seu CPF 123.456.789-00. A cliente Julia Vilela Sodré também compareceu.
    Outro registro: CPF 123456789-11 informado manualmente.
    """

    print("=== Texto original ===")
    print(texto)

    # 1) Eliminar CPF e nascimento
    t1 = engine.elimina_cpf_nascimento(texto)
    print("\n=== Após elimina_cpf_nascimento ===")
    print(t1)

    # 2) Encodar maiúsculas
    lista1 = ["Rio de Janeiro", "CPF"]  
    # Aqui pode ser feita a importação de vários termos preestabelecidos com Maiusculas-Minusculas que você não deseja que sejam confundidos com nomes de pessoas.
    lista2, t2 = engine.encodar_maiusculas(t1, lista1)
    print("\n=== Após encodar_maiusculas ===")
    print(t2)

    # 3) Reconhecer nomes com spaCy
    t3 = engine.sem_nome_spacy(t2)
    print("\n=== Após sem_nome_spacy ===")
    print(t3)

    # 4) Remover nomes
    t4 = engine.sem_nome(t3)
    print("\n=== Após sem_nome ===")
    print(t4)        

    # 5) Decodar maiúsculas
    t5 = engine.decodar_maiusculas(t4, lista1, lista2)
    print("\n=== Texto final ===")
    print(t5)
________________________________________
📜 Licença
Distribuído sob a licença MIT.
Sinta-se livre para usar, modificar e contribuir!
________________________________________
🙌 Contribuições
Pull requests são bem-vindos!
Se encontrar algum caso de nome/CPF/Data não anonimizado corretamente, abra uma issue descrevendo o exemplo.


