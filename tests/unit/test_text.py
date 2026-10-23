from liberty_find.text import content_hash, html_to_text, posting_id


def test_html_to_text_handles_escaped_and_double_escaped_html() -> None:
    raw = (
        "&lt;p&gt;Ol&amp;aacute;&amp;nbsp;mundo&lt;/p&gt;"
        "&lt;ul&gt;&lt;li&gt;Python&lt;/li&gt;&lt;/ul&gt;"
    )
    assert html_to_text(raw, escaped=True) == "Olá mundo\n- Python"


def test_html_to_text_plain_html() -> None:
    assert html_to_text("<h2>Título</h2><p>Linha  com   espaços</p>") == "Título\nLinha com espaços"


def test_html_to_text_empty() -> None:
    assert html_to_text("", escaped=True) == ""


def test_content_hash_is_stable_and_ignores_outer_whitespace() -> None:
    assert content_hash(" Vaga ", "texto\n") == content_hash("Vaga", "texto")
    assert content_hash("Vaga", "texto") != content_hash("Vaga", "outro texto")
    assert len(content_hash("a", "b")) == 64


def test_posting_id() -> None:
    assert posting_id("greenhouse", "exemplo", "1001") == "greenhouse:exemplo:1001"
