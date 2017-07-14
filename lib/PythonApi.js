const PythonShell = require('python-shell');


default export class PythonApi {
  constructor() {
    this.options = {
      mode: 'text',
      pythonPath: '/usr/bin/python3',
      scriptPath: process.cwd() + "/api",
      args: JSON.stringify(args)
    };
  }
  PythonShell.run('/cspaceIO.py', passAsArgs(processingInput), function (err, results) {
    if (err) throw err;
    // results is an array consisting of messages collected during execution
    console.log('results: %j', results);
    fs.unlinkSync(processingInput.paths.srcPath);
    res.send(dstFileName);
  });

}
