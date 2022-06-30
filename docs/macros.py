from urllib.parse import urlparse, urljoin
import html
import os
import io

def render_cheat(markdown_file):

  cheats_length = 0
  if os.path.exists(markdown_file) and not os.path.isdir(markdown_file):
    try:
        with io.open(markdown_file, "r", encoding="utf-8") as n:
            cheats = n.readlines()
    except UnicodeDecodeError:
        try:
            with io.open(markdown_file, "r") as n:
                cheats = n.readlines()
        except Exception:
            return 'Error'
    cheats_length = len(cheats)

    topics = [(i, n) for i, n in enumerate(cheats) if n.startswith('# ')]
    cheats_html_list = []
    for index, line in enumerate(topics):
        # Find the corresponding line index
        s_line_index = topics[index][0]
        cheat_topic = cheats[s_line_index]
        # Find the next corresponding line index
        s_next_line_index = cheats_length if index + 1 > len(topics) - 1 else topics[index + 1][0]
        # Grab the topic headers
        header_list = ['# %s' % header.strip() for header in cheat_topic.split('# ') if header]
        headers = ' '.join(sorted(set(header_list), key=header_list.index))
        # Get the topic's body
        body = ''.join([l for l in cheats[s_line_index + 1:s_next_line_index] if l])
        # utf-8 encoding
        try:
            headers = str(headers.encode('utf-8').decode('utf8'))
            body = str(body.encode('utf-8').decode('utf8'))
        except UnicodeEncodeError:
            try:
                body = str(body.encode('utf-8'))
            except Exception:
                continue
        try:
            cheat_html = f"""
            <tr><td>{headers}</td>
            <td>
            <pre class="cheat_note">
            {body}
            </pre>      
            </td></tr>            
            """
            cheats_html_list.append(cheat_html)
        except Exception:
            # logger.error('Failed to process topic ... skipping')
            continue
    return ''.join(cheats_html_list)

def render_cheat_page(markdown_file):

  cheat_items = render_cheat(markdown_file)

  cheat_html = f"""
  <table class="table stripe row-border table-bordered table-fluid" id="cheatData">
  <thead>
  <tr><th>Keywords</th><th>Description</th></tr>
  </thead>
  <tbody>

  {cheat_items}   

  </tbody>
  </table>   
  """
  

  return cheat_html

def declare_variables(variables, macro):
    @macro
    def code_from_file(fn: str, flavor: str = ""):
        """
        Load code from a file and save as a preformatted code block.
        If a flavor is specified, it's passed in as a hint for syntax highlighters.

        Example usage in markdown:

            {{code_from_file("code/myfile.py", "python")}}

        """
        docs_dir = os.path.abspath(__file__ + "../../..")
        fn = os.path.abspath(os.path.join(docs_dir, fn))
        if not os.path.exists(fn):
            return f"""<b>File not found: {fn}</b>"""
        with open(fn, "r") as f:
            return (
                f"""<div class="highlight parent"><pre><code class="from-file {flavor}">{html.escape(f.read())}</code></pre></div>"""
            )

    @macro
    def external_markdown(fn: str):
        """
        Load markdown from files external to the mkdocs root path.
        Example usage in markdown:

            {{external_markdown("../../README.md")}}

        """
        docs_dir = variables.get("docs_dir", "docs")
        fn = os.path.abspath(os.path.join(docs_dir, fn))
        if not os.path.exists(fn):
            return f"""<b>File not found: {fn}</b>"""
        with open(fn, "r") as f:
            return f.read()

def is_absolute(url):
    return bool(urlparse(url).netloc)

def define_env(env):
    "Hook function"

    @env.macro
    def test_fn(x:float):
        "Test function"
        return x * 4 / 3

    @env.macro
    def cheat_page(markdown_file:str):

        body_html = render_cheat_page(markdown_file)

        # return "<p>You will be processing %s</p>" % markdown_file
        return body_html

    @env.macro
    def say_hello(s:str):
        "Test procedure"
        return "<i>Hello %s</i>" % s

    @env.macro
    def video_as_gif(url):
        if not is_absolute(url):
            url = urljoin(env.conf['site_url'], url)
        return f'<p><video autoplay muted loop playsinline style="width: 100%"> <source src="{url}" type="video/mp4"></video></p>'

    @env.macro
    def video(url):
        if not is_absolute(url):
            url = urljoin(env.conf['site_url'], url)
        return f'<p><video controls style="width: 100%"> <source src="{url}" type="video/mp4"></video></p>'

    @env.macro
    def screenshot(url, width='400px'):
        if not is_absolute(url):
            url = urljoin(env.conf['site_url'], url)
        return f'<p><svg style="width: {width};" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 282 158"> <g id="flipper__screen"> <rect width="282" height="158" x="0" y="0" fill="#c6c5c3" rx="18"></rect> <rect width="278" height="154" x="2" y="2" fill="#d9d8d6" rx="15"></rect> <rect width="276" height="152" x="3" y="3" fill="#e5e5e5" rx="15"></rect> <rect width="266" height="142" x="8" y="8" fill="#ff8b29" rx="10"></rect> <foreignObject width="256" height="128" x="13" y="15"> <img src="{url}" style="image-rendering: pixelated; width: 256px;"/> </foreignObject></g></svg></p>'

    @env.macro
    def altium(id):
        return f'<script src="https://viewer.altium.com/client/static/js/embed.js"></script><div class="altium-ecad-viewer" data-project-src="{id}" style="height: 500px; overflow: hidden; max-width: 1280px;"></div>'