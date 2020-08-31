/* Tutorial following: https://zellwk.com/blog/crud-express-mongodb/
*  Local DB: 
        const url = 'mongodb://127.0.0.1:27017'
        const dbName = 'game-of-thrones'
        let db

        MongoClient.connect(url, { useNewUrlParser: true }, (err, client) => {
        if (err) return console.log(err)

        // Storing a reference to the database so you can use it later
        db = client.db(dbName)
        console.log(`Connected MongoDB: ${url}`)
        console.log(`Database: ${dbName}`)
        })
*
*  Left off in CRUD - UPDATE. Error wasn't able to make the database update.
*  DB Password: dynWmDH9ygMjpdh1
*  User name: alfre
*
*/

console.log('May Node be with you');

// Connects express
const express = require('express');
const bodyParser = require('body-parser');
const MongoClient = require('mongodb').MongoClient;
const app = express ();
const connectionString = "mongodb+srv://alfre:dynWmDH9ygMjpdh1@cluster0.saxrj.mongodb.net/test?retryWrites=true&w=majority";

app.use(bodyParser.urlencoded({extended: true}));
app.use(express.static('public'));
app.use(bodyParser.json());

MongoClient.connect(connectionString, {useUnifiedTopology: true})
    .then(client => {
        console.log('Connected to Database');
        const db = client.db('famous-quotes');
        const quotesCollection = db.collection('quotes');
        
        app.set('view engine', 'ejs');
        
        app.listen(3000, function(){
            console.log('Listening on 3000');
        })

        app.get('/', (req, res) => {
            // res.sendFile(__dirname + '/index.html');
            db.collection('quotes').find().toArray()
                .then(results => {
                    console.log(results)
                    res.render('index.ejs', {quotes: results})
                })
                .catch(error => console.error(error))
        })

        app.post('/quotes', (req, res) => {
            quotesCollection.insertOne(req.body)
                .then(result => {
                    console.log(result);
                    res.redirect('/');
                })
                .catch(error => console.log(error))
            console.log(req.body);
        })

        app.put('/quotes', (req, res) => {
            console.log(req.body)
          })
    })
    .catch(error => console.error(error))
