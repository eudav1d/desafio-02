"""Testes de EXEMPLO do Desafio 02. Rode com:  python -m unittest

Passar aqui não garante passar nos testes de correção, que são outros
e incluem casos de borda e entradas grandes (limite de 2 segundos).
"""
import unittest
from pathlib import Path

from despacho import despachar

PASTA = Path(__file__).resolve().parent.parent / "exemplos"


class TestExemplos(unittest.TestCase):
    def test_fila_simples(self):
        self.assertEqual(despachar(["CHEGA P1", "CHEGA P2", "SAI", "SAI"]), ["P1", "P2"])

    def test_cancela(self):
        self.assertEqual(despachar(["CHEGA P1", "CHEGA P2", "CANCELA P1", "SAI"]), ["P2"])

    def test_desfaz_saida(self):
        log = ["CHEGA P1", "CHEGA P2", "SAI", "DESFAZ", "CHEGA P3", "SAI", "SAI"]
        self.assertEqual(despachar(log), ["P1", "P2"])

    def test_log_do_sistema_antigo(self):
        log = (PASTA / "log-antigo.txt").read_text(encoding="utf-8").splitlines()
        esperado = [
            linha.strip()
            for linha in (PASTA / "log-antigo.saida.txt").read_text(encoding="utf-8").splitlines()
            if linha.strip() and not linha.startswith("#")
        ]
        self.assertEqual(despachar(log), esperado)


if __name__ == "__main__":
    unittest.main()
