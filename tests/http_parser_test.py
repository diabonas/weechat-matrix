import html.entities

from hypothesis import given
from hypothesis.strategies import sampled_from

from matrix.colors import MatrixHtmlParser

try:
    # python 3
    html_entities = [(name, char, ord(char))
                     for name, char in html.entities.html5.items()
                     if not name.endswith(';')]
except AttributeError:
    # python 2
    html_entities = [(name, unichr(codepoint), codepoint)
                     for name, codepoint
                     in html.entities.name2codepoint.items()]


@given(sampled_from(html_entities))
def test_html_named_entity_parsing(entitydef):
    name = entitydef[0]
    character = entitydef[1]
    parser = MatrixHtmlParser()
    assert parser.unescape('&{};'.format(name)) == character


@given(sampled_from(html_entities))
def test_html_numeric_reference_parsing(entitydef):
    character = entitydef[1]
    num = entitydef[2]
    parser = MatrixHtmlParser()
    assert parser.unescape('&#{};'.format(num)) == character


def test_parsing_of_escaped_brackets():
    p = MatrixHtmlParser()
    p.feed('<pre><code>&lt;faketag&gt;</code></pre>')
    s = p.get_substrings()
    print(s)
    assert s[0].text == '<faketag>' and len(s) == 1
