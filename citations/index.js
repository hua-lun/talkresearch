const express = require("express");
const Cite = require('citation-js');
const { convert } = require('html-to-text');

const app = express ();
app.use(express.json());


app.listen(3000, () => {
    console.log("Server Listening on PORT:", 3000);
  });


app.get('/citing', async (request, response) => {
    let example = await Cite.async(request.query.doi)
   
    let output = example.format('bibliography', {
        format: 'html',
        template: 'apa',
        lang: 'en-US'
      })
    
    let results = convert(output)
    response.send({
        bib: results
    })
});


