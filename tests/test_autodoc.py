#!/usr/bin/env python

"""
Testing.
"""

import pytest
import os
from sphinx_testing import with_app

import sys
# sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__))))
sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__)), 'example_doc_python_source'))

expected = '''<p>This is test documentation</p>
<span class="target" id="module-autodoc_napoleon_typehints_example"></span><p>Small module to provide sourcecode for testing if everything works as needed</p>
<dl class="function">
<dt id="autodoc_napoleon_typehints_example.format_unit">
<code class="descclassname">autodoc_napoleon_typehints_example.</code><code class="descname">format_unit</code><span class="sig-paren">(</span><em>self</em>, <em>value</em>, <em>unit</em>, <em>test</em><span class="sig-paren">)</span><a class="headerlink" href="#autodoc_napoleon_typehints_example.format_unit" title="Permalink to this definition">¶</a></dt>
<dd><table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Return type:</th><td class="field-body"><code class="xref py py-class docutils literal"><span class="pre">str</span></code></td>
</tr>
</tbody>
</table>
<p>Formats the given value as a human readable string using the given units.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first last simple">
<li><strong>value</strong> (<code class="xref py py-class docutils literal"><span class="pre">Union</span></code>[<code class="xref py py-class docutils literal"><span class="pre">float</span></code>, <code class="xref py py-class docutils literal"><span class="pre">int</span></code>]) &#8211; a numeric value</li>
<li><strong>unit</strong> (<code class="xref py py-class docutils literal"><span class="pre">str</span></code>) &#8211; the unit for the value (kg, m, etc.)</li>
<li><strong>test</strong> (<code class="xref py py-class docutils literal"><span class="pre">Optional</span></code>[(typing.Iterable[+T_co],)]) &#8211; bla bla blathe unit for the value (kg, m, etc.)</li>
</ul>
</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="function">
<dt id="autodoc_napoleon_typehints_example.format_unit_google">
<code class="descclassname">autodoc_napoleon_typehints_example.</code><code class="descname">format_unit_google</code><span class="sig-paren">(</span><em>self</em>, <em>value</em>, <em>unit</em>, <em>test</em><span class="sig-paren">)</span><a class="headerlink" href="#autodoc_napoleon_typehints_example.format_unit_google" title="Permalink to this definition">¶</a></dt>
<dd><table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Return type:</th><td class="field-body"><code class="xref py py-class docutils literal"><span class="pre">str</span></code></td>
</tr>
</tbody>
</table>
<p>Formats the given value as a human readable string using the given units.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first simple">
<li><strong>value</strong> (<code class="xref py py-class docutils literal"><span class="pre">Union</span></code>[<code class="xref py py-class docutils literal"><span class="pre">float</span></code>, <code class="xref py py-class docutils literal"><span class="pre">int</span></code>]) &#8211; a numeric value</li>
<li><strong>unit</strong> (<code class="xref py py-class docutils literal"><span class="pre">str</span></code>) &#8211; the unit for the value (kg, m, etc.)</li>
<li><strong>test</strong> (<code class="xref py py-class docutils literal"><span class="pre">Optional</span></code>[(typing.Iterable[+T_co],)]) &#8211; bla bla blathe unit for the value (kg, m, etc.)</li>
</ul>
</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body"><p class="first last">This function returns something of
value: and does not overwrite this part.</p>
</td>
</tr>
</tbody>
</table>
</dd></dl>

<dl class="function">
<dt id="autodoc_napoleon_typehints_example.format_unit_numpy">
<code class="descclassname">autodoc_napoleon_typehints_example.</code><code class="descname">format_unit_numpy</code><span class="sig-paren">(</span><em>self</em>, <em>value</em>, <em>unit</em>, <em>test</em><span class="sig-paren">)</span><a class="headerlink" href="#autodoc_napoleon_typehints_example.format_unit_numpy" title="Permalink to this definition">¶</a></dt>
<dd><table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Return type:</th><td class="field-body"><code class="xref py py-class docutils literal"><span class="pre">str</span></code></td>
</tr>
</tbody>
</table>
<p>Formats the given value as a human readable string using the given units.</p>
<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><ul class="first simple">
<li><strong>value</strong> (<em>a numeric value</em>) &#8211; </li>
<li><strong>unit</strong> (<em>the unit for the value (kg, m, etc.)</em>) &#8211; </li>
<li><strong>test</strong> (<em>bla bla blathe unit for the value (kg, m, etc.)</em>) &#8211; </li>
</ul>
</td>
</tr>
<tr class="field-even field"><th class="field-name">Returns:</th><td class="field-body"><p class="first last"><ul class="simple">
<li><em>This function returns something of</em></li>
<li><strong>value</strong> (<em>and does not overwrite this part.</em>)</li>
</ul>
</p>
</td>
</tr>
</tbody>
</table>
</dd></dl>
'''


@pytest.fixture
def html():
    """This insane hack is to deal with the fact that the with_app decorator
    somehow eats the return value."""

    html_str = ''

    @with_app(buildername='html',
              srcdir=os.path.join(os.path.dirname(__file__), 'example_docs'),
              copy_srcdir_to_tmpdir=True)
    def build(app, status, warning):
        app.build()
        html = (app.outdir / 'index.html').read_text()
        nonlocal html_str
        html_str = html

    build()
    return html_str


def test_autodoc(html):
    with open('html_output.html', 'w') as f:
        f.write(html)

    start = "<p>This is test documentation</p>"
    start_ix = html.find(start)
    assert start_ix > -1, 'Start of actual code documentation is not where it should be... it wasnt found at all.'
    end = '</dd></dl>\n'
    end_ix = html.rfind(end) + len(end)
    assert end_ix > -1, 'End of actual code documentation is not where it should be... it wasnt found at all.'

    assert html[start_ix:end_ix] == expected
