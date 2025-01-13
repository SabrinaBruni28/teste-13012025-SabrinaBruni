import requests
from bs4 import BeautifulSoup
import calculadora_desafio1 as c

def defineClasse(classe: str):
    """
    retorna o nome da classe que corresponde no site.
    """
    if (classe == "Residencial"):
        return "Residencial Normal (Consumo R$/kWh)"
    elif (classe == "Industrial"):
        return "Rural - Normal (Consumo R$/kWh)"
    else:
        return "Demais classes (Consumo R$/kWh)"

def defineBandeira(bandeira: str):
    """
    retorna a coluna da bandeira na tabela do site.
    """
    if (bandeira == "BANDEIRA VERDE"):
        return 1
    if (bandeira == "BANDEIRA AMARELA"):
        return 2
    elif (bandeira == "BANDEIRA VERMELHA 1"):
        return 3
    elif (bandeira == "BANDEIRA VERMELHA 2"):
        return 4

def calculadora(consumo: list, classe: str, bandeira: str) -> tuple:
    """
    retorna uma tupla de floats contendo economia anual, economia mensal, desconto aplicado e cobertura.
    """
    economia_anual = 0
    economia_mensal = 0
    desconto_aplicado = 0
    cobertura = 0
    tarifa = 0

    # Desenvolva seu código aqui #

    # URL da página que contém as tarifas
    url = "https://www.cemig.com.br/atendimento/valores-de-tarifas-e-servicos/"

    # Requisição para a página
    response = requests.get(url)

    # Requisição foi bem-sucedida
    if response.status_code == 200:
        # Analisa o conteúdo da página
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Encontra a tabela de informações
        tarifas_section = soup.find_all("table", class_="table table-bordered")
        
        # De acordo com o html do site, pesquisa em cada tag de informação da tabela
        for tarifa_elemento in tarifas_section:
            # Encontra as tags tbody dentro das tabelas
            tbody = tarifa_elemento.find("tbody")
            if tbody:
                # Encontra as tags de tr dentro das tags tbody
                tr_elementos = tbody.find_all("tr")
                for tr in tr_elementos:
                    # Encontra as tags td dentro das tags tr
                    td_elementos = tr.find_all("td")
                    if td_elementos:
                        # Na tag tr recupera o primeiro elemento, que é a classe
                        classe_coluna = td_elementos[0].text.strip()

                        # Verifica se a classe é a classe que estamos procurando
                        if defineClasse(classe) in classe_coluna:
                            # Recupera o valor da tarifa de acordo com a coluna da bandeira
                            valor_coluna = td_elementos[defineBandeira(bandeira)].text
                            # Extrai o valor da tarifa e converte para float
                            try:
                                tarifa = float(valor_coluna.replace(",", ".").replace("R$", "").strip())
                                break  # Para o loop ao encontrar a tarifa correta
                            except ValueError:
                                print(f"Erro ao converter valor de tarifa: {valor_coluna}")
                                tarifa = 0
                if tarifa:
                    break  # Para o loop externo se a tarifa já foi encontrada

    if tarifa == 0:
        raise ValueError("Tarifa não encontrada ou inválida.")

    # Calcula os valores pedidos com a calculadora do desafio 1
    economia_anual, economia_mensal, desconto_aplicado, cobertura = c.calculadora(consumo, tarifa, classe)

    return (
        round(economia_anual, 2),
        round(economia_mensal, 2),
        round(desconto_aplicado, 2),
        round(cobertura, 2),
    )


if __name__ == "__main__":
    print("Testando...")

    assert calculadora([1518, 1071, 968], "Industrial", "BANDEIRA VERMELHA 2") == (
        1349.86,
        112.49,
        0.12,
        0.90,
    ) 

    assert calculadora([1000, 1054, 1100], "Residencial", "BANDEIRA VERMELHA 1") == (
        1725.61,
        143.8,
        0.18,
        0.90
    )

    assert calculadora([973, 629, 726], "Comercial", "BANDEIRA AMARELA") == (
        1097.6,
        91.47,
        0.16,
        0.90
    )

    assert calculadora([15000, 14000, 16000], "Industrial", "BANDEIRA VERMELHA 1") == (
        21656.81,
        1804.73,
        0.15,
        0.95
    )

    assert calculadora([12000, 11000, 11400], "Residencial", "BANDEIRA VERDE") == (
        22997.8,
        1916.48,
        0.22,
        0.95
    )

    assert calculadora([17500, 16000, 16400], "Comercial", "BANDEIRA AMARELA") == (
        27938.08,
        2328.17,
        0.18,
        0.95
    )

    assert calculadora([30000, 29000, 29500], "Industrial", "BANDEIRA VERMELHA 1") == (
        53262.07,
        4438.51,
        0.18,
        0.99
    )

    assert calculadora([22000, 21000, 21400], "Residencial", "BANDEIRA AMARELA") == (
        52186.84,
        4348.9,
        0.25,
        0.99
    )

    assert calculadora([25500, 23000, 21400], "Comercial", "BANDEIRA VERDE") == (
        48697.35,
        4058.11,
        0.22,
        0.99
    )

    print("Todos os testes passaram!")
    