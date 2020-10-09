# franceme.github.io
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![Jekyll Site Website](https://github.com/franceme/franceme.github.io/workflows/Jekyll%20Site%20Website/badge.svg)
![Resume Repo Build](https://github.com/franceme/Resume/workflows/Create%20and%20Release%20Latex%20File/badge.svg)
---

This is hosted [here](https://franceme.github.io).

---


# Resume

## What is this?

The static code generation of my website.
I picked this design specifically since it's a single file with little to no Javascript once it's updated.

## How is the website build?

### How does GitHub Actions run?

* Checking out the latest branch
    * checks out the latest code
* Retriving Ruby Setup
    * Downloads Ruby for the website generation
* Installing Bundle Packages
    * Downloads the website dependencies
* Installing Dependencies
    * Downloads the general dependencies
* Decode Secret
    * Decode the _config.yml secret that is hosted on GitHub Secrets
* Get Time
    * Determines the current timestamp
        * *NOTE*: There is a known-timezone issue in the library
* Find and Replace
    * sets the time in the index page
* Download the CV.pdf
    * Downloads the CV.pdf file from the latest Resume Repo Release
* Move the CV
    * Moves the CV.pdf file to the files folder
* Download the Resume.pdf
    * Downloads the Resume.pdf file from the latest Resume Repo Release
* Move the Resume
    * Moves the Resume.pdf file to the files folder
* Download the Website Archive
    * Downloads the Website.zip file from the latest Resume Repo Release
* Extract the Website Archive
    * Unzips the Website content
* Builds the Website
    * builds the website
* Get Excess Time
    * Gets the time used for creating a release timestamp
* Zip the Website
    * Compresses the website for the release
* Create a Release
    * Creates a release
* Upload Release Asset
    * Uploads the website zip file to the release
* Deploy
    * Deploys the fully built website so GitHub Pages can pick it up

## Source of the template

This template was originally created by [Sproogen](https://github.com/sproogen/) at [Github Repo](https://github.com/sproogen/modern-resume-theme).
The changes made are listed below.

## What makes it special?

This very custom website is tied to my Resume website.
Once the Resume is updated and uploaded this repo will build automatically and download the latest information.

### Template Changes

* Created an extra groups html in the includes, to created groups sections.
* Created a groups yaml file, to create groups.
* Added the groups into the default html file.
* Made a new footer html in the includes, to attribute [Sproogen](https://github.com/sproogen/) again.
* Made a new header html in the includes, to add a custom divider.
* Overwrote the google-analytics in the includes, to avoid any analytics.
* Created a skills yaml file/html file to create custom logic/rating for skills.
* Reorded the layout, experiences first.
* Added a resume link similar to the github link into the default page.
* Changed the a.html to always include https://.
* Increased the size of the github icon for projects.

## License

The theme is available as open source under the terms of the [GPL-3.0 License](https://www.gnu.org/licenses/gpl-3.0.en.html).
