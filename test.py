from bs4 import BeautifulSoup

# Example HTML content
html_content = '''
<div id="content">
    <h2>Animate Breath</h2>
    (<a href="/rulebooks/supplementals-35--5/draconomicon--92/">Draconomicon</a>)
    <br>
    <br>
    <a href="/spells/schools/transmutation/">Transmutation</a>
    <br>
    <strong>Level:</strong>
    <a href="/classes/sorcerer/spells-level-7/">Sorcerer 7</a>,
    <a href="/classes/wizard/spells-level-7/">Wizard 7</a>,
    <br>
    <strong>Components:</strong>
    <abbr title="Somatic">S</abbr>,
    <abbr title="Meta Breath">MB</abbr>,
    <br>
    <strong>Casting Time:</strong> 1 standard action<br>
    <strong>Range:</strong> Personal<br>
    <strong>Target:</strong> You<br>
    <strong>Duration:</strong> 1 round/level<br>
</div>
'''

# Parse HTML using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Extract relevant information
spell_name = soup.find('h2').text.strip()
level_tag = soup.find('strong', string='Level:')
level = ', '.join(a.text.strip() for a in level_tag.find_next_siblings('a'))
components_tag = soup.find('strong', string='Components:')
components = ', '.join(abbr.text.strip() for abbr in components_tag.find_next_siblings('abbr'))
casting_time = soup.find('strong', string='Casting Time:').next_sibling.strip()
range_ = soup.find('strong', string='Range:').next_sibling.strip()
target = soup.find('strong', string='Target:').next_sibling.strip()
duration = soup.find('strong', string='Duration:').next_sibling.strip()

# Format the output
output = f"{spell_name}\nLevel: {level}\nComponents: {components}\nCasting Time: {casting_time}\nRange: {range_}\nTarget: {target}\nDuration: {duration}"

print(output)
