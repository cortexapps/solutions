# ServiceNow Sample Plugin

This is a simple example of how to leverage Cortex plugins to retrieve incidents from ServiceNow

The project was scaffolded using Cortex's [cookiecutter template](https://github.com/cortexapps/cookiecutter-cortex-plugin) and it was tested against a ServiceNow development instance with the sample data it contains.

![ServiceNow Plugin](img/snow-plugin.png)

## Notes

* At this time, the plugin only retrieves the first 10 incidents from the instance, it does not use the Cortex context to only get the incidents against this service.

* Set up the Cortex Proxy with the following headers:
    * `Accept`: `application/json`
    * `Content-Type`: `application/json`
    * `Authorization`: `Basic <64bit endocded username:password>`

*To encode your username and password, [this](https://www.debugbear.com/basic-auth-header-generator) tool is pretty handy.*

## SetUp

### Prerequisites

Developing and building this plugin requires either [yarn](https://classic.yarnpkg.com/lang/en/docs/install/) or [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm).

## Getting started

1. Run `yarn` or `npm install` to download all dependencies
2. Run `yarn build` or `npm run build` to compile the plugin code into `./dist/ui.html`
3. Upload `ui.html` into Cortex on a create or edit plugin page
4. Add or update the code and repeat steps 2-3 as necessary

### Notable scripts

The following commands come pre-configured in this repository. You can see all available commands in the `scripts` section of [package.json](./package.json). They can be run with npm via `npm run {script_name}` or with yarn via `yarn {script_name}`, depending on your package manager preference. For instance, the `build` command can be run with `npm run build` or `yarn build`.

* `build` - compiles the plugin. The compiled code root is `./src/index.tsx` (or as defined by [webpack.config.js](webpack.config.js)) and the output is generated into `dist/ui.html`.
* `test` - runs all tests defined in the repository using [jest](https://jestjs.io/)
* `lint` - runs lint and format checking on the repository using [prettier](https://prettier.io/) and [eslint](https://eslint.org/)
