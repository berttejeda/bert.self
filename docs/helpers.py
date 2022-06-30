def render_cheat_page():

  cheat_html = """
    <div id="container">
    <div class="example-page">
    <div>
    <h1>bash</h1>
    </div>
    <div id="main">
    <div class="c1">
    <div id="lovely-things-list">
    <input class="search" placeholder="Search My Bash Notes" />
    <ul class="sort-by">
    <li class="sort btn" data-sort="name">Sort by name</li>
    <li class="sort btn" data-sort="category">Sort by category</li>
    </ul>
    <ul class="filter">
    <li class="btn" id="filter-none">Show all</li>
    <li class="btn" id="filter-games">Only show games</li>
    <li class="btn" id="filter-beverages">Only show beverages</li>
    </ul>
    <ul class="list">
    </ul>
    </div>
    </div>
    </div>
    </div>    
  """