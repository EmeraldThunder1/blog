# To be run as an action when the repository is pushed to
# Load all the posts and use them to fill in the templates

import os
from os.path import join, dirname
import yaml
from datetime import datetime
import markdown
from bs4 import BeautifulSoup
from jinja2 import Template

def main():
    with open("meta.yml", "r") as f:
        meta = yaml.load(f, Loader=yaml.FullLoader)
    
    posts = os.listdir("./posts")
    print(posts)

    with open(join(dirname(__file__), "../templates/post.jinja"), "r") as f:
        postTemplate = Template(f.read())
        print(f.read())

    for post in posts:
        if post.endswith('.md'):
            with open(f"./posts/{post}", 'r') as f:
                creationDate = datetime.fromtimestamp(os.path.getctime(f"./posts/{post}")).strftime("%m/%d/%Y")
                modDate = datetime.fromtimestamp(os.path.getmtime(f"./posts/{post}")).strftime("%m/%d/%Y")

                content = markdown.markdown(f.read())
                soup = BeautifulSoup(content, 'html.parser')

                title = soup.find('h1').text

                renderedPost = postTemplate.render(postTitle=title, blogTitle=meta["title"], description=meta["description"], postContent=content)
                
                if not os.path.exists(post.split('.')[0]):
                    os.makedirs(post.split(".")[0])
                with open(f"{post.split('.')[0]}/index.html", "w+") as f:
                    f.write(renderedPost)

main()