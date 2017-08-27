"use strict";
const express = require('express');
const uuidV1 = require('uuid/v1');
const app = express();
const bodyParser = require('body-parser');
const path = require('path');
const fs = require('fs');
const PythonShell = require('python-shell');
const fileUpload = require('express-fileupload');
const PORT = 1338;

var passAsArgs = function (args) {
  return {
    mode: 'text',
    pythonPath: '/usr/bin/python3',
    scriptPath: process.cwd(),
    args: JSON.stringify(args)
  }
}
// app.use(express.static(path.join(__dirname, 'build')));
app.use(express.static(path.join(__dirname, 'output')));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
  extended: true
}))

app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  next();
});

app.use(fileUpload());

app.get('/test', function (req, res) {
  let response = "filename: "+ uuidV1();
  console.log('connection handled!');
  res.json({"hello": "world"})
})

var processImage = function () {
  PythonShell.run('/cspaceIO.py', passAsArgs(test), function (err, results) {
    if (err) throw err;
    // results is an array consisting of messages collected during execution
    console.log('results: %j', results);

    console.log(test.name);
  });
};

var saveFilePath = function (name) {
  return filePath()+'output/' + name;
}

var srcFilePath = function (name) {
  return filePath()+'input/' + name;
}

var fileNameGenerator = function () {
  return uuidV1()+".jpg";
}

var filePath = function () {
  return process.cwd()+'/';
}

const prepareArgs = (req, srcFileName, outputFileNames) => {
  let params = req.body;
  return {
    cspaceLabel: params.colorSpaceLabel,
    paths: {
      maskedPath: saveFilePath(outputFileNames.masked),
      srcPath: srcFilePath(srcFileName),
      maskPath: saveFilePath(outputFileNames.mask)
    },
    sliderPos: [
      //  || 0 for python json parsing
      parseInt(params.c1min),
      parseInt(params.c1max),
      parseInt(params.c2min) || 0,
      parseInt(params.c2max) || 0,
      parseInt(params.c3min) || 0,
      parseInt(params.c3max) || 0
    ]
  }
}


app.post('/upload', function (req, res) {
  if (req.files && req.body) {
    let srcFileName = fileNameGenerator();
    let maskedPath = fileNameGenerator();
    let maskPath = fileNameGenerator();
    let output = {mask: maskPath, masked: maskedPath}
    let apiArgs = prepareArgs(req, srcFileName, output)
    let uploadedImage = req.files.uploadedImage;
    console.log(passAsArgs(apiArgs));
    apiArgs.cspaceLabel = apiArgs.cspaceLabel || "BGR";
    uploadedImage.mv(apiArgs.paths.srcPath, function(err) {
      if (err) {
        console.log(err);
        return res.status(500).send(err);
      }
      PythonShell.run('./cspaceIO.py', passAsArgs(apiArgs), function (err, results) {
        try {
          if (err) throw err;
        }
        catch (e) {
          console.log('errored: ');
          console.error(e);
        }
        // results is an array consisting of messages collected during execution
        fs.unlinkSync(apiArgs.paths.srcPath);
        res.json(output);
      });
    });

  } else {
    res.send('sorry didnt find that file')
  }
})

app.listen(PORT, function () {
  console.log(`Example app listening on port ${PORT}!`)
});
