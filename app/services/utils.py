# == Validações ==


import re
from datetime import datetime


def validar_numeros(numeros: str) -> (bool, str):
    """
    O método verifica se o valor contém apenas números e se o tamanho é igual a 6.
    """
    if len(numeros) != 6:
        return False, "O código deve ter exatamente 6 dígitos."

    if not bool(re.match("^[0-9]+$", numeros)):
        if any(char.isalpha() for char in numeros):  # Verifica se contém letras
            return False, "O código deve conter apenas números, e você informou letras."
        if ' ' in numeros:  # Verifica se contém espaços
            return False, "O código deve conter apenas números, mas você está enviando espaços."
        return False, "O código deve conter apenas números."

    return True, ""


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

    :return: A boolean value indicating whether the status is valid. Returns True if the status is valid (i.e., it follows
             the required pattern and only contains safe characters). Returns False otherwise.

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


# == Verificação de Dados Recebidos ==
def verificar_asterisco(valor):
    """
    Verifica se o valor é um asterisco, indicando que todos os valores devem ser considerados.
    """
    return re.match(r"^[*]?$", valor)


def valores_por_virgula(valor):
    """
    Verifica se o valor contém vários valores separados por vírgula.
    Retorna uma lista dos valores separados ou None se não houver vírgula.
    """
    if "," in valor:
        return valor.split(",")
    return None


def dois_caracteres_uppercase(lista_valores):
    """
    Verifica se cada string na lista tem exatamente 2 caracteres em UPPERCASE.
    Retorna True se todos os valores satisfazem os critérios, False caso contrário.
    """
    for valor in lista_valores:
        if not (valor.isupper() and len(valor) == 2):
            return False
    return True
