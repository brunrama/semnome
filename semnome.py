import re
import spacy

class SemNome:

# Carregar modelo do spaCy uma única vez
    try:
        nlp = spacy.load("pt_core_news_sm")
    except OSError:
        raise RuntimeError(
            "O modelo pt_core_news_sm não está instalado. "
            "Execute: python -m spacy download pt_core_news_sm"
        )

    @staticmethod
    def elimina_cpf_nascimento(texto: str) -> str:
        """
        Substitui padrões de CPF e datas de nascimento por 'X'.
        """

        # --- CPF com pontos e hífen: 000.000.000-00 ou com X
        texto = re.sub(r'\b[\dX]{3}\.[\dX]{3}\.[\dX]{3}-[\dX]{2}\b',
                       lambda m: "X" * len(m.group()), texto)

        # --- CPF só com hífen: 000000000-00
        texto = re.sub(r'\b[\dX]{9}-[\dX]{2}\b',
                       lambda m: "X" * len(m.group()), texto)

        # --- CPF solto, mas antecedido por "cpf" em até 3 palavras
        padrao_cpf_solto = re.compile(r'\b(\d{11})\b')
        for m in padrao_cpf_solto.finditer(texto):
            inicio = max(0, texto.rfind(" ", 0, m.start()))
            contexto = texto[inicio:m.start()]
            if re.search(r'\bcpf\b', contexto, re.IGNORECASE):
                texto = texto.replace(m.group(), "X" * len(m.group()))

        # --- Data de nascimento NN/NN/NNNN antecedido por palavras-chave
        padrao_data = re.compile(r'\b\d{2}/\d{2}/\d{4}\b')
        for m in padrao_data.finditer(texto):
            inicio = max(0, texto.rfind(" ", 0, m.start() - 50))
            contexto = texto[inicio:m.start()]
            if re.search(r'(nascimento|nascido|aniversário)', contexto, re.IGNORECASE):
                texto = texto.replace(m.group(), "X" * len(m.group()))

        return texto

    @staticmethod
    def encodar_maiusculas(texto: str, lista1: list):
        """
        Substitui termos compostos da lista1 (com maiúsculas) por versão em minúsculas.
        Retorna lista2 (tudo minúsculo) + texto tratado.
        """
        lista2 = [t.lower() for t in lista1]

        for original, lower in zip(lista1, lista2):
            # substitui ignorando case
            texto = re.sub(re.escape(original), lower, texto, flags=re.IGNORECASE)

        return lista2, texto

    @staticmethod
    def sem_nome(texto: str) -> str:
        """
        Identifica nomes e substitui por iniciais se houver contexto de pessoa.
        """
        contexto_palavras = [
            "sra", "sr", "sr\\(a\\)", "beneficiário", "beneficiária", "beneficiário\\(a\\)",
            "senhor", "senhora", "senhor\\(a\\)", "cidadão", "cidadã", "paciente",
            "dependente", "usuário", "usuária", "usuário\\(a\\)", "cliente",
            "consumidor", "consumidora", "consumidor\\(a\\)", "reclamante", "segurado", "segurada"
        ]

         
        # - exige pelo menos 2 palavras de nome
        # - permite conectores múltiplos no meio
        # - aceita nomes totalmente em maiúsculas também
        padrao_nome = re.compile(
            r'\b(?:[A-ZÁÉÍÓÚÃÕÂÊÔ][a-záéíóúãõâêôç]+|[A-Z]{2,})'         # primeira palavra
            r'(?:\s+(?:de|da|do|dos|das)\s+(?:[A-ZÁÉÍÓÚÃÕÂÊÔ][a-záéíóúãõâêôç]+|[A-Z]{2,}))*'  # conectores + nomes
            r'(?:\s+(?:[A-ZÁÉÍÓÚÃÕÂÊÔ][a-záéíóúãõâêôç]+|[A-Z]{2,}))+'  # pelo menos mais um nome
        )

        for m in list(padrao_nome.finditer(texto)):
            nome = m.group()

            # contexto: até 5 palavras antes e depois
            inicio_ctx = max(0, m.start() - 100)
            fim_ctx = min(len(texto), m.end() + 100)
            contexto = texto[inicio_ctx:fim_ctx]

            if re.search(r'\b(?:' + "|".join(contexto_palavras) + r')\b', contexto, re.IGNORECASE):
                partes = nome.split()
                iniciais = []
                for p in partes:
                    if p.lower() in ["de", "da", "do", "dos", "das"]:
                        iniciais.append(p)  # mantém conector
                    else:
                        iniciais.append(p[0].upper() + ".")
                novo_nome = " ".join(iniciais)
                texto = texto.replace(nome, novo_nome, 1)

        return texto

    @classmethod
    def sem_nome_spacy(cls, texto: str) -> str:
        """
        Camada extra de confirmação usando spaCy:
        detecta entidades de pessoa e anonimiza com iniciais
        se ainda não foi feito pelo regex.
        """
        doc = cls.nlp(texto)
        for ent in doc.ents:
            if ent.label_ == "PER":
                nome = ent.text
                # ignora se já virou iniciais (C. S. etc.)
                if re.match(r'(?:[A-Z]\.)+(?:\s+(?:de|da|do|dos|das)\s+[A-Z]\.)*', nome):
                    continue
                # transforma em iniciais
                partes = nome.split()
                iniciais = []
                for p in partes:
                    if p.lower() in ["de", "da", "do", "dos", "das"]:
                        iniciais.append(p)
                    else:
                        iniciais.append(p[0].upper() + ".")
                novo_nome = " ".join(iniciais)
                texto = texto.replace(nome, novo_nome, 1)
        return texto

    @staticmethod
    def decodar_maiusculas(texto: str, lista1: list, lista2: list) -> str:
        """
        Reverte o encodamento: termos em lista2 voltam para lista1.
        """
        for original, lower in zip(lista1, lista2):
            texto = re.sub(re.escape(lower), original, texto, flags=re.IGNORECASE)
        return texto
