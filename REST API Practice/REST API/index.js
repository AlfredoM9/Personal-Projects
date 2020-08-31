'use strict'

const
    port = 8888,
    express = require('express'),
    app = express();

app.get('/hello/:name?', (req, res) =>
res
    .append('Access-Control-Allow-Origin', '*')
    .json(
    { message: `Hello ${req.params.name || 'world'}!` }
    )
);

app.use((req, res, next) => {
    res.append('Access-Control-Allow-Origin', '*');
    next();
  });

app.listen(
    port, () => console.log(`Server started on port ${port}`)
)