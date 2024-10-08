# talkresearch
https://talkresearch.onrender.com

Devpost page: https://devpost.com/software/talkresearch 

## Video Demo
[![talkresearch video demo on YouTube](https://img.youtube.com/vi/MfSLZj6D1J0/0.jpg)](https://www.youtube.com/watch?v=MfSLZj6D1J0)

## Running this app locally

Clone project
```bash
git clone https://github.com/hua-lun/talkresearch.git 
```

### Part 1 (Running the Express app to use citations api)
1. Open shell terminal to `citations`
```bash
cd citations
```

2. Install modules
```bash
npm install 
```

3. Run Express app
```bash
node index.js 
```

4. Take note of localhost url
- By default, it hosts on port `3000` at `http://127.0.0.1:3000/citing?`
### Part 2 (Running the Flask app)
1. In a new shell, go to `talkresearch`'s root directory

2. Install Python Requirements
```bash
pip install -r requirements.txt
```

3. Create `.env` based on `.env.sample`
- MongoDB cluster
- Auth0 
- Flask secret key
- URL in `part 1`

4. Run Flask app
```bash
 flask run
```

5. Enter Flask app URL in browser and use

## Devpost Writeup
## Inspiration
Writing papers, preparing reports, they are very time consuming. 
There's so many things to look out for. Such as - getting the correct format, making sure citations and references are given. In addition, we have to keep track of all the resources and readings to refer back. 

## What it does
- write documents with clear formatting and helpful functionalities
- store all resources and references used in the paper into one document, helping users to organise their work better
- add references and citations from 3 different styles: Harvard, APA, Vancouver

## How we built it
 Flask Web App
- TinyMCE Editor. Made use of a plethora of open source and premium plugins to provide functionality to TalkResearch's editor. 
Highlighted plugins used and essential for writing papers and reports:
1. Page Break (Open Source)
2. Print (Open Source)
3. Horizontal Rule (Open Source)
4. Export (Premium)
5. Footnote (Premium) 
- MongoDB to save user's information and documents

REST API with Express and Node
- Citations, used Citations.js to collect citation output

## Challenges we ran into
- ways to store data and how to structure it
-  authentication routes and making sure the flow is correct

## Accomplishments that we're proud of
- Use MongoDB and successfully it get it to create, update and remove documents
- Authenticated with Auth0
- Create custom templates for TinyMCE

## What we learned
- Technologies: MongoDB, Auth0, TinyMCE
- Databases, differences between SQL and NoSQL
- Authentication setup

## What's next for TalkResearch
- Suggestion function to provide users with curated list of research papers based on their work

## Screenshots
![Home Page](https://d112y698adiu2z.cloudfront.net/photos/production/software_photos/002/686/262/datas/original.png)
![Creator Page](https://github.com/hua-lun/talkresearch/blob/main/static/create.png)
![Editor Page](https://github.com/hua-lun/talkresearch/blob/main/static/edit.png)
![Manage Page](https://github.com/hua-lun/talkresearch/blob/main/static/manage.png)
