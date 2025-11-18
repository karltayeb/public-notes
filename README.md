The website is built using Quartz, a static site builder made with Obsidian in mind. 
These notes are a subset of the notes from my private vault, those marked with the front-matter `share: true`. 
Here is the workflow for updating the website content and pushing to github.
```
uv run python get_public_notes.py
npx quartz sync --no-pull
```

The site is hosted using github pages.
```
```
