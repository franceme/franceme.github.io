# franceme.github.io
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![Jekyll Site Website](https://github.com/franceme/franceme.github.io/workflows/Jekyll%20Site%20Website/badge.svg)
![Resume Repo Build](https://github.com/franceme/Resume/workflows/Create%20and%20Release%20Latex%20File/badge.svg)
---

This is hosted [here](https://franceme.github.io).

---



## Source of the template

This template was originally created by [Sproogen](https://github.com/sproogen/) at [Github Repo](https://github.com/sproogen/modern-resume-theme).
The changes made are listed below.

## How is the website build?

### gitHub Action Events
* push
* workflow_dispatch
* repository_dispatch

### GitHub Action Steps
1. Checking out the latest branch
2. Retriving Ruby Setup
3. Installing Bundle Packages
4. Installing Dependencies
5. Decode Secret
6. Get Time
   * https://github.com/marketplace/actions/get-timestamp-action
7. Find and Replace
    * https://github.com/marketplace/actions/string-replace
8. Download the CV.pdf
9. Move the CV
10. Download the Resume.pdf
11. Move the Resume
12. Download the Website Archive
13. Extract the Website Archive
14. Builds the Website
    * https://github.com/marketplace/actions/get-timestamp-action
15. Get Excess Time
16. Zip the Website
17. Create a Release
18. Upload Release Asset
19. Deploy
    * https://github.com/marketplace/actions/github-pages-action

### Changes

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
