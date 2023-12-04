# == Validações ==


import re


def validar_filial(filial: str) -> (bool, str):
    # Verifica se há caracteres que não são dígitos
    if not bool(re.match("^[0-9]+$", filial)):
        if any(char.isalpha() for char in filial):  # Verifica se contém letras
            return False, "A filial deve conter apenas números, e você informou letras."
        if ' ' in filial:  # Verifica se contém espaços
            return False, "A filial deve conter apenas números, mas você está enviando espaços."
        return False, "A filial deve conter apenas números."
    return True, ""


def validar_setor(setor: str) -> (bool, str):
    if " " in setor or not re.match("^[a-zA-Z0-9]*$", setor):
        return False, "O setor não deve conter espaços ou caracteres especiais."
    return True, setor.upper()


def validar_equipamento(equipamento: str) -> (bool, str):
    if not bool(re.match("^[a-zA-Z0-9]+$", equipamento)):
        return False, "O equipamento não deve conter caracteres especiais ou espaços."
    return True, equipamento.upper()


def validar_grupo(grupo: str) -> (bool, str):
    if not re.match("^[a-zA-Z0-9]+$", grupo):
        return False, "O grupo não deve conter espaços ou caracteres especiais."
    return True, grupo.upper()


# == Tratativas de Strings ==

def format_sql_query(query):
    try:
        # Gerar a string SQL bruta
        raw_sql = str(query.statement.compile(compile_kwargs={"literal_binds": True}))

        # Formatar a string SQL para melhor legibilidade
        formatted_sql = raw_sql.replace("\\n", "\n").replace("\\t", "\t").replace('\\"', '"')

        # Retornar a SQL formatada
        return formatted_sql

    except Exception as e:
        # Tratar exceções gerais, como uma consulta SQL vazia ou erros de formatação
        print(f"Erro ao formatar a consulta SQL: {e}")
        return "Erro ao gerar a consulta SQL."
