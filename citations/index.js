const express = require("express");
const Cite = require('citation-js');
require('@citation-js/plugin-csl')
const { convert } = require('html-to-text');

const app = express ();
app.use(express.json());


app.listen(3000, () => {
    console.log("Server Listening on PORT:", 3000);
  });


app.get('/citing', (request, response) => {
    let paper = new Cite(request.query.doi)

    let output = paper.format('bibliography', {
    format: 'html',
    template: request.query.style,
    lang: 'en-US'
    })

    response.send({
        bib: convert(output)
    })

});
    


