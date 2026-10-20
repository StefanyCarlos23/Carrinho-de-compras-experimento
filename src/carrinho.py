from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


class Carrinho:
    FRETE = Decimal("20.00")
    LIMITE_FRETE_GRATIS = Decimal("150.00")
    LIMITE_DESCONTO_10 = Decimal("200.00")
    LIMITE_DESCONTO_15 = Decimal("500.00")
    CENTAVO = Decimal("0.01")

    def __init__(self):
        self._itens = {}

    def adicionar_item(self, nome, preco, quantidade=1):
        try:
            valor = Decimal(str(preco))
        except (InvalidOperation, TypeError, ValueError):
            raise ValueError("O preço deve ser um número não negativo.") from None

        if not valor.is_finite() or valor < 0:
            raise ValueError("O preço deve ser um número não negativo.")
        if isinstance(quantidade, bool) or not isinstance(quantidade, int) or quantidade <= 0:
            raise ValueError("A quantidade deve ser um inteiro positivo.")

        if nome in self._itens:
            self._itens[nome]["quantidade"] += quantidade
        else:
            self._itens[nome] = {
                "nome": nome,
                "preco": float(valor),
                "quantidade": quantidade,
            }

    def remover_item(self, nome):
        if nome not in self._itens:
            raise ValueError(f"Item não encontrado: {nome}")
        del self._itens[nome]

    def show(self):
        return [item.copy() for item in self._itens.values()]

    def total(self):
        subtotal = sum(
            (Decimal(str(item["preco"])) * item["quantidade"] for item in self._itens.values()),
            Decimal("0.00"),
        )

        if subtotal == 0:
            return 0.00

        if subtotal >= self.LIMITE_DESCONTO_15:
            desconto = Decimal("0.15")
        elif subtotal >= self.LIMITE_DESCONTO_10:
            desconto = Decimal("0.10")
        else:
            desconto = Decimal("0.00")

        valor_com_desconto = (subtotal * (Decimal("1.00") - desconto)).quantize(
            self.CENTAVO, rounding=ROUND_HALF_UP
        )
        frete = Decimal("0.00") if valor_com_desconto >= self.LIMITE_FRETE_GRATIS else self.FRETE
        return float((valor_com_desconto + frete).quantize(self.CENTAVO, rounding=ROUND_HALF_UP))
