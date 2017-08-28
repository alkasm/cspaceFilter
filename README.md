# cspaceFilter
Backend API and front-end build for cspaceFilter

The cspaceFilter web application seeks to help users play around with multiple values for thresholding an image in different colorspaces, both to get comfortable working in different colorspaces and helping automate some trial and error for getting the correct values. It is a web version of the native Python and OpenCV module I built, which can be found [here](https://github.com/alkasm/cspaceFilterPython).

The project has three main components on GitHub:
1. The back-end API, containing Javascript, Docker, Python files, and so fourth.
2. The front-end UI, which is built to static pages.
3. The static web front, accessible at https://alkasm.github.io/cspaceFilter

Parts 1 and 3 are contained in this repo; the `master` branch contains the API, while the `gh-pages` branch contains the static generated pages from the front-end UI. The actual front-end UI repo lives on [Shaun Sweet's GitHub](https://github.com/shaun-sweet/image-processing-ui), a Javascript web-developer who is a friend and collaborator for this project.
