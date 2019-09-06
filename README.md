# cdss-rest-services-examples #

This repository contains examples to access data from HydroBase REST web services,
using various tools and technologies.
This is a new project that will enhance information that is presented on the 
[Technical Information & Help](https://dwr.state.co.us/rest/get/help#TechInfoHelp) page.
The goal of this project is to provide technical examples in a way that can be understood
by non-technical people and streamline implementing tools to consume the web services.

* [Examples](#examples)
* [Repository Contents](#repository-contents)
* [Development Environment](#development-environment)
* [License](#license)
* [Contributing](#contributing)
* [Maintainers](#maintainers)
* [Release Notes](#release-notes)

------------------

## Examples ##

This repository contains examples illustrating how to access HydroBase REST web services
using various tools and technologies.

| **Tool / Technology** | **Description** |
| --------------------- | --------------- |
| [ArcGIS](examples/arcgis/README.md) | ArcGIS Geographic Information System (GIS) software. |
| [curl](examples/curl/README.md)<br>![curl](README-resources/images/curl-thumbnail.png) | `curl` command line tool to retrieve data and save to local file. |
| [Excel](examples/excel/README.md) | Microsoft Excel workbook examples. |
| [Google Sheets](examples/googlesheets/README.md) | Google Sheets, online spreadsheets. |
| [JavaScript](examples/javascript/README.md) | JavaScript, used for web application development. |
| [Python](examples/python/README.md) | Python programming language, used to automate data processing. |
| [R](examples/r/README.md) | R programming language, used to automate data processing for statistical analysis. |
| [StateDMI](examples/statedmi/README.md)| StateDMI software (part of Colorado's Decision Support Systems), used to automate creation of StateCU and StateMod model files. |
| [TSTool](examples/tstool/README.md)<br>![TSTool](README-resources/images/tstool-thumbnail.png) | TSTool software (part of Colorado's Decision Support Systems), used to automate time series and other data processing. |

## Repository Contents ##

The repository contains the following folders and files.
Currently, README files are used to present information,
but the content may be converted to a GitHub page, Wiki, or some other form in the future.
`README.md` files provide information and can be viewed in the repository using a web browser.

```text
cdss-rest-services-examples/  Repository name and main folder.
  .github/                    Files specific to GitHub such as issue template.
  .gitattributes              Git configuration file.
  .gitignore                  Git configuration file.
  README.md                   This file.
  examples/                   Main examples folder
    arcgis/                   ArcGIS examples.
    curl/                     Curl/script examples.
    excel/                    Excel examples.
    googlesheets/             Google sheets examples.
    javascript/               JavaScript API and examples.
    python/                   Python examples.
    r/                        R examples.
    tstool/                   TSTool examples.
```

A recommended (but not required) folder structure to contain the repository files on the local computer is as follows.
This folder structure is consistent with other CDSS products, and provides consistency and flexibility.
Examples are constructed to work using relative paths or absolute paths that are dynamically determined
from the local files.

```
C:\Users\user\                         Windows user files.
  cdss-dev/                            CDSS development files.
    REST-Examples/                     This product.
      git-repos/                       Git repositories for the website.
        cdss-rest-services-examples/   The repository files, as shown above.
```

## Development Environment ##

The development environment for examples varies by technology used.
Additional information will be provided as the examples are implemented.

## License ##

The license for this documentation is the [Creative Commons CC-BY 4.0 license](LICENSE.md).
Examples that are implemented in software code are distributed using GPL v3 license.

## Contributing ##

See the [OpenCDSS Licensing](http://opencdss.state.co.us/opencdss/licensing/) documentation.

## Maintainers ##

This repository is maintained by the OpenCDSS team in coordination with
Colorado Water Conservation Board and Colorado Division of Water Resources staff.

## Release Notes ##

The following are major updates for the repository and examples.
See the GitHub issues for details.

* 2019-09-06 - Add initial TSTool and `curl` examples.
* 2019-08-12 - Initialize the repository.
