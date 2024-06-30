import requests
from bs4 import BeautifulSoup
import time

def fetch_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    spells = []
    for spell in soup.select('td a[href^="/spells/draconomicon--92/"]'):
        spells.append({'name': spell.text.strip(), 'link': spell['href']})
    return spells

def fetch_spell(url):
    # Make a request to fetch the HTML content
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch {url}. Status code: {response.status_code}")
        return None
    
    # Parse HTML using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the content div or inaccurate div
    content_div = soup.find('div', id='content') or soup.find('div', id='inaccurate')
    
    if not content_div:
        print(f"Could not find content for {url}")
        return None
    
    # Extract relevant information using BeautifulSoup
    spell_name = content_div.find('h2').text.strip()
    
    level_tag = content_div.find('strong', string='Level:')
    level = ', '.join(a.text.strip() for a in level_tag.find_next_siblings('a')) if level_tag else ''
    
    components_tag = content_div.find('strong', string='Components:')
    components = ', '.join(abbr.text.strip() for abbr in components_tag.find_next_siblings('abbr')) if components_tag else ''
    
    casting_time_tag = content_div.find('strong', string='Casting Time:')
    casting_time = casting_time_tag.next_sibling.strip() if casting_time_tag and casting_time_tag.next_sibling else ''
    
    range_tag = content_div.find('strong', string='Range:')
    range_ = range_tag.next_sibling.strip() if range_tag and range_tag.next_sibling else ''
    
    target_tag = content_div.find('strong', string='Target:')
    target = target_tag.next_sibling.strip() if target_tag and target_tag.next_sibling else ''
    
    duration_tag = content_div.find('strong', string='Duration:')
    duration = duration_tag.next_sibling.strip() if duration_tag and duration_tag.next_sibling else ''
    
    # Format the output
    output = f"{spell_name}\n"
    output += f"Level: {level}\n"
    output += f"Components: {components}\n"
    output += f"Casting Time: {casting_time}\n"
    output += f"Range: {range_}\n"
    output += f"Target: {target}\n"
    output += f"Duration: {duration}\n"
    
    return output.strip()

base_url = 'https://dndtools.net'
spells_urls = [
    f'{base_url}/spells/draconomicon--92/',
    f'{base_url}/spells/draconomicon--92/?page=2',
    f'{base_url}/spells/draconomicon--92/?page=3'
]
all_spells = []

for spells_url in spells_urls:
    all_spells.extend(fetch_page(spells_url))
    time.sleep(1)  # To avoid hammering the server

# Fetch and write spell details to a file
with open('Dragonomicon.txt', 'w', encoding='utf-8') as file:
    for spell in all_spells:
        spell_url = f"{base_url}{spell['link']}"
        spell_details = fetch_spell(spell_url)
        if spell_details:
            file.write(spell_details + "\n\n")
        else:
            file.write(f"Failed to fetch details for {spell['name']}\n\n")
        time.sleep(1)  # To avoid hammering the server
