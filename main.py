from bs4 import BeautifulSoup

# Your HTML content
html = '''
<div class="client-focus-tile" data-v-1ba95bc4="" data-v-d7c1f96d="">
    <div class="client-focus-icon age-focus" data-v-d7c1f96d=""></div> 
    <h3 class="heading-element heading-element-4 client-focus-group-title" data-v-d7c1f96d="" data-v-70c85fe3=""><!--[-->Age<!--]--></h3> 
    <!--[--><div class="client-focus-item" data-v-d7c1f96d="">
        <span class="client-focus-description" data-x="attribute-330" data-v-d7c1f96d="">Preteen <span class="force-no-highlight" data-v-d7c1f96d="">,&nbsp;</span></span>
    </div>
    <div class="client-focus-item" data-v-d7c1f96d="">
        <span class="client-focus-description" data-x="attribute-326" data-v-d7c1f96d="">Teen <span class="force-no-highlight" data-v-d7c1f96d="">,&nbsp;</span></span>
    </div>
    <div class="client-focus-item" data-v-d7c1f96d="">
        <span class="client-focus-description" data-x="attribute-327" data-v-d7c1f96d="">Adults <span class="force-no-highlight" data-v-d7c1f96d="">,&nbsp;</span></span>
    </div>
    <div class="client-focus-item" data-v-d7c1f96d="">
        <span class="client-focus-description" data-x="attribute-328" data-v-d7c1f96d="">Elders (65+) <!----></span>
    </div>
<!--]--></div>
'''

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Find all elements with the class "client-focus-item"
client_focus_items = soup.find_all('div', class_="client-focus-item")

# Extract the inner text
extracted_text = []
for item in client_focus_items:
    # Get the text content from the span with class "client-focus-description"
    description = item.find('span', class_='client-focus-description')
    if description:
        extracted_text.append(description.get_text(strip=True))  # Extract the text and strip extra whitespace

# Print the extracted values
print("Extracted Text:", extracted_text)
