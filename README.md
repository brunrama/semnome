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


