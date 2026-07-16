class ExecutiveReport:

    @staticmethod
    def build(product: dict):

        score = product["score"]

        if score >= 80:
            prioridade = "ALTA"
        elif score >= 60:
            prioridade = "MÉDIA"
        else:
            prioridade = "BAIXA"

        motivos = []

        if product["commission"] >= 10:
            motivos.append("Comissão acima da média")

        if product["rating"] >= 4.5:
            motivos.append("Excelente avaliação")

        if product["sales"] >= 1000:
            motivos.append("Grande volume de vendas")

        if product["price"] <= 150:
            motivos.append("Preço competitivo")

        return {

            "produto": product["name"],

            "score": score,

            "acao": product["decision"],

            "prioridade": prioridade,

            "comissao": product["commission"],

            "avaliacao": product["rating"],

            "vendas": product["sales"],

            "motivos": motivos,

        }