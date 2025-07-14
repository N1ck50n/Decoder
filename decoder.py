import requests
from lxml import html

def fetch_html(googleDoc):
    response = requests.get(googleDoc)
    if response.status_code != 200:
        raise Exception("Failed to retrieve document. Check if it's published and public.")
    return response.content

def parse_table(data):
    tree = html.fromstring(data)
    rows = tree.xpath('//tr')
    return rows

def extract_grid(rows):
    gridData = []
    max_X = 0
    max_Y = 0

    for row in rows:
        cols = row.xpath('./td | ./th')
        if len(cols) != 3:
            continue
        try:
            x = int(cols[0].text_content().strip())
            char = cols[1].text_content().strip()
            y = int(cols[2].text_content().strip())
        except ValueError:
            continue
        gridData.append((char, x, y))
        max_X = max(max_X, x)
        max_Y = max(max_Y, y)

    return gridData, max_X, max_Y

def build_grid(gridData, max_X, max_Y):
    grid = [[' ' for _ in range(max_X + 1)] for _ in range(max_Y + 1)]
    for char, x, y in gridData:
        grid[y][x] = char
    return grid

def print_grid(grid):
    for row in reversed(grid):
        print(''.join(row))

def grid(googleDoc):
    data = fetch_html(googleDoc)
    rows = parse_table(data)
    gridData, max_X, max_Y = extract_grid(rows)
    grid_matrix = build_grid(gridData, max_X, max_Y)
    print_grid(grid_matrix)

grid("https://docs.google.com/document/d/e/2PACX-1vTER-wL5E8YC9pxDx43gk8eIds59GtUUk4nJo_ZWagbnrH0NFvMXIw6VWFLpf5tWTZIT9P9oLIoFJ6A/pub")
