// Schema
{
  cspaceLabels: {
    // input needs 1 of these
    BGR: "BGR",
    HSV: "HSV",
    HLS: "HLS",
    Lab: "Lab",
    Luv: "Luv",
    YCrCb: "YCrCb",
    XYZ: "XYZ",
    Grayscale: "Grayscale"
  },
  paths: {
    // needs both
    srcPath: "image/location/currently.png",
    outPath: "target/output/path.png"
  }
  sliderValues: [0,1,3,2,4,5]
}

// Example input
{
  cspaceLabel: "BGR",
  paths: {
    srcPath: "input/test.jpg",
    dstPath: "output/output.png"
  },
  sliderPos: [50,100,50,100,50,100]
}
// example of what will be passed in
'{"cspaceLabel":"BGR","paths":{"srcPath":"input/test.jpg","dstPath":"output/output.png"},"sliderPos":[50,100,50,100,50,100]}'
