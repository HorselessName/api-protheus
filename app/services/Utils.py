# == Validações ==


import re
from datetime import datetime


def validar_filial(filial: str) -> (bool, str):
    """
    Valida se a filial ou filiais fornecidas estão no formato correto.
    - Filiais devem ser strings de 6 dígitos, podendo ser várias separadas por vírgula.
    """
    # Divide a string de filial pelas vírgulas, criando uma lista de filiais.
    filiais = filial.split(',')

    # Loop para validar cada filial na lista
    for f in filiais:
        # Reutiliza o método validar_numeros para cada filial
        valido, mensagem = validar_numeros(f)
        if not valido:
            return False, mensagem

    # Se todas as filiais passaram na validação
    return True, ""


def validar_numeros(numeros: str) -> (bool, str):
    """
    Verifica se o valor contém apenas números de 6 dígitos. Pode ser um único número ou múltiplos números separados por vírgula.
    """
    print("##### Validando Números: ", numeros)

    # Primeiro, verifica se há múltiplos valores separados por vírgula
    valores = valores_por_virgula(numeros) or [numeros]

    for valor in valores:
        # Verifica se cada valor tem exatamente 6 dígitos e contém apenas números
        if len(valor) != 6 or not bool(re.match("^[0-9]+$", valor)):
            if any(char.isalpha() for char in valor):  # Verifica se contém letras
                return False, "Cada código deve conter apenas números, e você informou letras."
            if ' ' in valor:  # Verifica se contém espaços
                return False, "Cada código deve conter apenas números, mas você está enviando espaços."
            return False, "Cada código deve ter exatamente 6 dígitos e conter apenas números."

    return True, ""


def valores_por_virgula(valor: str) -> list:
    """
    Verifica se o valor contém vários valores separados por vírgula.
    Retorna uma lista dos valores separados.
    """
    return valor.split(",") if "," in valor else [valor]


def validar_caracteres(texto: str, nome_campo: str = None) -> (bool, str):
    """
    Valida se o texto fornecido não contém espaços ou caracteres especiais.
    Retorna um booleano indicando se a validação foi bem-sucedida e o texto validado ou uma mensagem de erro.

    Abro Exceção para as vírgulas pois uso elas pra lidar com valores que vem de uma lista.
    """
    if " " in texto or not re.match("^[a-zA-Z0-9,]*$", texto):
        if nome_campo:
            return False, f"O {nome_campo} não deve conter espaços ou caracteres especiais."
        else:
            return False, "O texto não deve conter espaços ou caracteres especiais."
    return True, texto.upper()


# == Tratativas de Strings ==

def format_sql_query(query):
    """
    Formata para uma string SQL legível uma consulta de SQL gerada pelo SQLAlchemy.
    """
    try:
        # Gerar a string SQL bruta
        raw_sql = str(query.statement.compile(compile_kwargs={"literal_binds": True}))

        # Formatar a string SQL para melhor legibilidade
        formatted_sql = (raw_sql
                         .replace("\\n", "\n")
                         .replace("\\t", "\t")
                         .replace('\"', ""))

        # Retornar a SQL formatada
        return formatted_sql

    except Exception as e:
        # Tratar exceções gerais, como uma consulta SQL vazia ou erros de formatação
        print(f"Erro ao formatar a consulta SQL: {e}")
        return "Erro ao gerar a consulta SQL."


def validar_status(status: str) -> bool:
    """
    This function validates the status provided by the user. The status should follow the pattern 'A,B,C' (without
    spaces) and should only contain safe characters. The function returns True if the status is valid,
    and False otherwise.

    :param status: A string representing the status to be validated. The status should be a comma-separated string
                   without spaces, containing only the characters 'A', 'E', 'C', and 'D'. Each character can only appear
                   once in the status string.

    :return: A boolean value indicating whether the status is valid. Returns True if the status is valid (i.e.,
    it follows the required pattern and only contains safe characters). Returns False otherwise.

    Usage:
    >>> validar_status('A,B,C')
    False
    >>> validar_status('A,E,C,D')
    True
    >>> validar_status('A,B,C,D,D')
    False
    >>> validar_status('A,D,C,E')
    True
    """

    print("\n----- Utils: Validando Status -----\n")

    caracteres_validos = ['A', 'C', 'D', 'E', 'S', 'V']
    caracteres_status = status.split(',')

    if (all(caractere in caracteres_validos for caractere in caracteres_status) and
            len(set(caracteres_status)) == len(caracteres_status) and
            1 <= len(caracteres_status) <= 4):
        return True
    else:
        return False


def validar_data_between(data: str) -> bool | tuple[bool, str]:
    """
    Verifica e valida se a data recebida é "ANOMESDIA,ANOMESDIA" e se o intervalo é válido.
    Converte somente valores no formato "YYYYMMDD,YYYYMMDD" (Ex: 20240115,20240130)
    """

    print("\n----- Utils: Validando Data Between -----\n")

    try:
        data_inicio, data_fim = data.split(',')
        data_inicio = datetime.strptime(data_inicio, '%Y%m%d')
        data_fim = datetime.strptime(data_fim, '%Y%m%d')

        # Se a data de início for maior, geramos um Throw Error.
        if data_inicio > data_fim:
            raise ValueError("Data inicial não pode ser maior ou igual à data final.")

        return True, data

    # Se o formato de data foi passado de forma errada, vai dar um Except e retornar um False.
    except (ValueError, AttributeError) as erro_data:
        return False, f"Data inicial deve ser menor que a final, formato correto é 'ANOMESDIA,ANOMESDIA', {erro_data}"
    pass


def verificar_asterisco(valor):
    """
    Verifica se o valor é um asterisco, indicando que todos os valores devem ser considerados.
    """
    return re.match(r"^[*]?$", valor)


def dois_caracteres_uppercase(lista_valores):
    """
    Verifica se cada string na lista tem exatamente 2 caracteres em UPPERCASE.
    Retorna True se todos os valores satisfazem os critérios, False caso contrário.
    """
    for valor in lista_valores:
        if not (valor.isupper() and len(valor) == 2):
            return False
    return True


def horario_atual():
    from datetime import datetime
    import pytz

    fuso_horario = pytz.timezone('America/Sao_Paulo')
    agora = datetime.now(fuso_horario)
    data_formatada = agora.strftime('%Y%m%d %H:%M')

    return data_formatada
