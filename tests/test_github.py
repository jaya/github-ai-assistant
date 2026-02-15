from __future__ import annotations

import os

import pytest


@pytest.mark.langsmith
def test_username(ask) -> None:  # noqa: ANN001
    expected = os.getenv("GITHUB_LOGIN")
    response = ask("qual meu user name")
    assert expected in response


@pytest.mark.langsmith
def test_closed_pr(ask) -> None:  # noqa: ANN001
    response = ask("me mostra um PR fechado no repo jaya/sports-program")
    r = response.lower()
    assert any(x in r for x in ["closed", "merged", "fechado", "mesclado"])


@pytest.mark.langsmith
def test_pr_details(ask) -> None:  # noqa: ANN001
    response = ask("me mostra os detalhes do PR #105 no repo jaya/sports-program")
    assert "105" in response


@pytest.mark.langsmith
def test_closed_issue(ask) -> None:  # noqa: ANN001
    response = ask("me mostra uma issue fechada no repo jaya/sports-program")
    assert any(x in response.lower() for x in ["closed", "fechada", "fechado"])


@pytest.mark.langsmith
def test_repo_info(ask) -> None:  # noqa: ANN001
    response = ask("me dá informações sobre o repo jaya/sports-program")
    assert "sports-program" in response.lower()


@pytest.mark.langsmith
def test_file_contents(ask) -> None:  # noqa: ANN001
    response = ask("me mostra o conteúdo do README do repo jaya/sports-program")
    assert "readme" in response.lower()


@pytest.mark.langsmith
def test_multi_turn_memory(ask) -> None:  # noqa: ANN001
    expected = os.getenv("GITHUB_LOGIN")
    ask("qual meu user name")
    response = ask("qual foi o user name que vc me disse na pergunta anterior?")
    assert expected in response


@pytest.mark.langsmith
def test_nonexistent_repo(ask) -> None:  # noqa: ANN001
    response = ask("liste issues do repo jaya/repo-que-nao-existe-xyz").lower()
    assert any(
        x in response
        for x in [
            "not found",
            "não encontr",
            "404",
            "não existe",
            "não consegui",
        ]
    )


@pytest.mark.langsmith
def test_contributors(ask) -> None:  # noqa: ANN001
    response = ask("quem é o top contributor do repo jaya/sports-program?")
    assert "contributor" in response.lower() or "ivanqueiroz" in response.lower()
