import json
import sys
import os

# Get the json file path and markdown file path from the environment variable
json_file_path =  os.getenv('JSON_FILE_PATH')
markdown_file_path = os.getenv('MARKDOWN_FILE_PATH')

if not json_file_path:
    # If the file path is not set, print an error message and exit the program
    print("No file path provided. Please set the JSON_FILE_PATH environment variable. Exiting.")
    sys.exit()

if not markdown_file_path:
    # If the file path is not set, print an error message and exit the program
    print("No file path provided. Please set the MARKDOWN_FILE_PATH environment variable. Exiting.")
    sys.exit()

# Load data from json
with open(json_file_path, 'r') as file:
    json_data = json.load(file)

# Filter the JSON data to only include content with links to GitHub repos
json_data = {category: [article for article in articles_list if 'github.com' in article['link']] 
            for category, articles_list in json_data.items()}

# Remove categories with no articles, to avoid empty sections in the markdown file
json_data = {category: articles for category, articles in json_data.items() if articles}

# Open the markdown file and store the intro paragraph(s)
with open(markdown_file_path, 'r') as markdown_file:
    lines = markdown_file.readlines()
    intro = ""
    for line in lines:
        if line.strip().startswith('<details'):
            break
        intro += line

# Open the markdown file again for writing
with open(markdown_file_path, 'w') as markdown_file:
    # Write the intro paragraph(s) from the original markdown file
    markdown_file.write(intro)
    
    # Write the categories and tables in markdown from the JSON data
    for category, articles_list in json_data.items():
        markdown_file.write(f'<details><summary><b>{category}</b></summary>\n<br>\n\n')
        markdown_file.write('|Repo|Description|Publish Date|\n')
        markdown_file.write('|-|-|-|\n')
        # Write the articles under each category
        for article in articles_list:
            markdown_file.write(f"| [{article['title']}]({article['link']}) | {article['description']} | *{article['date']}* |\n")
        markdown_file.write('\n</details>')
