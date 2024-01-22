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
    with open("./templates/post.jinja", "r") as f:
        postTemplate = Template(f.read())

    if not os.path.exists("./build"):
        os.makedirs("./build")
    with open("./build/index.html", "w+") as f:
        indexTemplate = Template(open("./templates/index.jinja", "r").read())
        f.write(indexTemplate.render(blogTitle=meta["title"], description=meta["description"]))

    for post in posts:
        if post.endswith('.md'):
            with open(f"./posts/{post}", 'r') as f:
                creationDate = datetime.fromtimestamp(os.path.getctime(f"./posts/{post}")).strftime("%m/%d/%Y")
                modDate = datetime.fromtimestamp(os.path.getmtime(f"./posts/{post}")).strftime("%m/%d/%Y")

                content = markdown.markdown(f.read())
                soup = BeautifulSoup(content, 'html.parser')

                title = soup.find('h1').text

                renderedPost = postTemplate.render(postTitle=title, blogTitle=meta["title"], description=meta["description"], postContent=content)
                
                path = "./build/" + post.split('.')[0]
                if not os.path.exists(path):
                    os.makedirs(path)
                with open(f"./{path}/index.html", "w+") as f:
                    f.write(renderedPost)

main()
