var express = require('express');
const lunr = require('lunr');
var cors = require('cors')
var fs = require('fs');
var app = express();
var sqlite3 = require('sqlite3').verbose();
var db = new sqlite3.Database('.\\data\\search.db');


app.use(cors())
app.use(express.json())
app.use('/images', express.static('.\\data\\images'))
app.use('/', express.static('website/dist/gallary'))


app.post('/post', function (req, res) {
    post = ":" + req.body.post.split(":")[2]
    let sql = 'SELECT * FROM tags where file = ?';
    tags = []
    console.log("Getting post tags")
    db.all(sql, [post], (err, rows) => {
        if (err) {
            console.log("error")
            throw err;
        }
        rows.forEach((row) => {
            tags.push(row.tag)
        });

        console.log("Sent post tags")
        res.json({
            'tags': tags
        });

    });
});

app.post('/fileCount', function (req, res) {
    output = {
        count: 0
    }
    let sql = 'SELECT * FROM search';
    tags = []
    console.log("Getting post tags")
    db.all(sql, (err, rows) => {
        if (err) {
            console.log("error")
            throw err;
        }
        rows.forEach((row) => {
            output.count += 1
        });
        res.json(output);
    });
});

app.post('/tags', function (req, res) {
    // Search terms should be comma seperated
    filtered = []
    array = []

    terms = req.body.terms.split(", ")

    searchTerm = ""
    criteria = {
        and: [],
        or: [],
        not: []
    }

    for (var p = 0; p < terms.length; p++) {
        if (terms[p].startsWith("-")) {
            criteria.not.push(terms[p].substring(1))
        }
        else if (terms[p].startsWith("+")) {
            criteria.and.push(terms[p].substring(1))
        }
        else {
            criteria.or.push(terms[p])
        }
    }

    if (criteria.or.length) {
        searchTerm = criteria.or[0]
    }
    else if (criteria.and.length) {
        searchTerm = criteria.and[0]
    }
    else {
        res.json({
            'tags': [],
            'images': []
        });
        return
    }

    console.log(criteria)
    console.log('SELECT * FROM search where tag LIKE "%' + searchTerm + '%"')

    let sql = 'SELECT * FROM search where tag LIKE "%' + searchTerm + '%"';
    tags = []
    console.log("Getting post tags")
    db.all(sql, (err, rows) => {
        if (err) {
            console.log("error")
            throw err;
        }
        rows.forEach((row) => {
            skip = false
            for (var p = 0; p < criteria.not.length; p++) {
                if (row.tag.includes(criteria.not[p])) {
                    skip = true
                    break
                }
            }
            if (!skip) {
                for (var p = 0; p < criteria.or.length; p++) {
                    if (row.tag.includes(criteria.or[p])) {
                        array.push(row.file)
                        tag = row.tag.split(", ")
                        for (var p = 0; p < tag.length; p++) {
                            tags.push(tag[p])
                        }
                    }
                }
                andCounter = 0
                for (var p = 0; p < criteria.and.length; p++) {
                    if (row.tag.includes(criteria.and[p])) {
                        andCounter++
                    }
                }

                if (andCounter == criteria.and.length && criteria.and.length != 0 && !array.includes(row.file)) {
                    array.push(row.file)
                    tag = row.tag.split(", ")
                    for (var p = 0; p < tag.length; p++) {
                        tags.push(tag[p])
                    }
                }
            }
        });

        filtered = sortByFrequencyAndRemoveDuplicates(tags)

        res.json({
            'tags': filtered,
            'images': array
        });
    });
});

app.post('/posts', function (req, res) {
    // Search terms should be comma seperated
    filtered = []
    array = []

    terms = req.body.terms.split(", ")

    searchTerm = ""
    criteria = {
        and: [],
        or: [],
        not: []
    }

    for (var p = 0; p < terms.length; p++) {
        if (terms[p].startsWith("-")) {
            criteria.not.push(terms[p].substring(1))
        }
        else if (terms[p].startsWith("+")) {
            criteria.and.push(terms[p].substring(1))
        }
        else {
            criteria.or.push(terms[p])
        }
    }

    if (criteria.or.length) {
        searchTerm = criteria.or[0]
    }
    else if (criteria.and.length) {
        searchTerm = criteria.and[0]
    }
    else {
        res.json({
            'tags': [],
            'images': []
        });
        return
    }

    console.log(criteria)
    console.log('SELECT * FROM search where tag LIKE "%' + searchTerm + '%"')

    let sql = 'SELECT * FROM search where tag LIKE "%' + searchTerm + '%"';
    tags = []
    console.log("Getting post tags")
    db.all(sql, (err, rows) => {
        if (err) {
            console.log("error")
            throw err;
        }
        rows.forEach((row) => {
            skip = false
            for (var p = 0; p < criteria.not.length; p++) {
                if (row.tag.includes(criteria.not[p])) {
                    skip = true
                    break
                }
            }
            if (!skip) {
                for (var p = 0; p < criteria.or.length; p++) {
                    if (row.tag.includes(criteria.or[p])) {
                        array.push(row.file)
                        tag = row.tag.split(", ")
                        for (var p = 0; p < tag.length; p++) {
                            tags.push(tag[p])
                        }
                    }
                }
                andCounter = 0
                for (var p = 0; p < criteria.and.length; p++) {
                    if (row.tag.includes(criteria.and[p])) {
                        andCounter++
                    }
                }

                if (andCounter == criteria.and.length && criteria.and.length != 0 && !array.includes(row.file)) {
                    array.push(row.file)
                    tag = row.tag.split(", ")
                    for (var p = 0; p < tag.length; p++) {
                        tags.push(tag[p])
                    }
                }
            }
        });

        filtered = sortByFrequencyAndRemoveDuplicates(tags)

        res.json({
            'tags': filtered.splice(0, 15),
            'images': array
        });
    });
});

function sortByFrequencyAndRemoveDuplicates(array) {
    var frequency = {}, value;

    // compute frequencies of each value
    for (var i = 0; i < array.length; i++) {
        value = array[i];
        if (value in frequency) {
            frequency[value]++;
        }
        else {
            frequency[value] = 1;
        }
    }

    // make array from the frequency object to de-duplicate
    var uniques = [];
    for (value in frequency) {
        uniques.push(value);
    }

    // sort the uniques array in descending order by frequency
    function compareFrequency(a, b) {
        return frequency[b] - frequency[a];
    }

    return uniques.sort(compareFrequency);
}

app.get('*', function (req, res) {
    if (req.url.match('^\/images')) {
    } else {
        res.sendFile(__dirname + '/website/dist/gallary/index.html');
    }
});

app.listen(3007);
