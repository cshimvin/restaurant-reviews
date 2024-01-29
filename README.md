# Milestone Project 3: Restaurant Reviews Site

![Website shown on various devices](static/images/documentation/responsive.jpg)

## Live Project

[View the live project](https://restaurant-reviews-ms3-8bb62e7f7033.herokuapp.com/)

## Table of Contents
1. [Project Goals](#project-goals)
- Business Goals
- User Goals
- Adminstrator Goals
2. [User Experience](#user-experience)
- User Stories
- Design and Structure
- Wireframes
3. [Features](#features)
- Must Have (current features)
- Could Have
- Won't Have (for now)
4. [Technologies Used](#technologies-used)
5. [Database Structure](#database-structure)
6. [Testing](#testing)
- User stories tests
- Functionality
- HTML Validation
- CSS Validation
- JS Validation
- Python Validation
- Accessibility and Performance
- Browser Compatibility
- Device Compatibility
7. [Bugs](#bugs)
8. [Deployment](#deployment)
9. [Credits](#credits)

## Project Goals

### Business Goals

As a business, I would like the website to:
- contain a comprehensive list of restaurants
- contain reviews so people can make an informed decision
- showcase various restaurants
- be able to book restaurants through the site in future

### User Goals

As a user, I would like the website to
- be easy to understand and navigate
- show me what restaurants are available
- show me reviews on restaurants so I can decide where to go to eat
- be easy to find a restaurant based on name, address or cuisine
- display easily on a number of devices

### Administrator Goals

As a website administrator I would like the website to:
- be easy to understand and navigate
- let me administer users on the site
- let me add or edit restaurants
- let me add or edit categories/cuisines

## User Experience

### User Stories

First time visitor goals:
- As a first time visitor, I would like to easily find out about restaurants.
- As a first time visitor, I would like to easily find out about reviews of restaurants.
- As a first time visitor, I would like to be able to add my review of a restaurant.

Returning visitor goals
- As a returning visitor, I would like to navigate the site and find featured restaurants.
- As a returning visitor, I would like to keep up to date with the latest reviews.
- As a returning visitor, I would like to add my reviews for restaurants I have visited.

Frequent visitor goals:
- As a frequent visitor, I would like to keep up to date with featured restaurants and any new restuarants and reviews.

### Design and Structure

The website consists of a number of pages which have a consistent structure and design. The background image was designed to convey the fact it is a restaurant site.

The main goal of the site is to show users restaurants available in Wales and real user reviews about them.

The website allows users to search for restaurants and reviews without logging in which should encourage users to regsiter an account and log in to leave their own reviews. This is why the log in and register links are consistently shown on the top navigation bar.

Once logged in, users can add their own reviews for restaurants.

#### Colour Palette

The brown and green colour represented earthy tones relating to Welsh heritage. These colours also allowed for a good contrast between text and background.

The colours I have chosen are:
- Navigation bar and footer: Brown `#A52A2A`
- Homepage title, view restaurants, add review and search buttons: Green `#008000`
- Main text: Black `#000000`
- Edit button (admin only): Blue `#0000FF`
- Delete button (admin only): Red `#FF0000`

![Colour Palette](/static/images/documentation/colour-palette.png)

#### Typography

I chose the following typography:
- [Kalam](https://fonts.google.com/specimen/Kalam) font for the main site title on the navigation bar
- [Montserrat](https://fonts.google.com/specimen/AR+One+Sans) for the rest of the site text

### Wireframes

Wireframes of the initial design can be found in the following wireframes:

- [Mobile wireframes](/static/images/documentation/restaurant-reviews-mobile-wireframes.pdf)
- [Desktop wireframes](/static/images/documentation/restaurant-reviews-desktop-wireframes.pdf)

## Features

### Must Have (current features)

### Could Have

### Won't Have (for now)

## Technologies Used

- [HTML5](https://en.wikipedia.org/wiki/HTML5) to create the website.
- [CSS3](https://en.wikipedia.org/wiki/CSS3) to style the website.
- [Bootstrap 4](https://getbootstrap.com/docs/4.1/getting-started/introduction/) was used for the layout of the site.
- [FontAwesome](https://fontawesome.com/) was used to create some of the icons on the site.
- [Google Fonts](https://fonts.google.com/) was used to display the typography of the site.
- [Git](https://git-scm.com/) was used for version control of the code.
- [GitHub](https://github.com/) was used as a repository for the code and GitHub pages was used to host the site.
- [Javascript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) and [JQuery 3.3.1](https://jquery.com/) to create the functionality of the site
- [Python](https://www.python.org/) was used as the back-end programming language.
- [Gitpod](https://gitpod.io/) and [CodeAnywhere](https://codeanywhere.com/) were used as a cloud-based IDEs for development.
- [Flask](https://flask.palletsprojects.com/en/3.0.x/) was used as the Python framework for the site togther with the [Jinja](https://jinja.palletsprojects.com/en/3.1.x/) template.
- [MongoDB](https://www.mongodb.com/) was used as the non-relational database management with Flask.
- [Heroku](https://www.heroku.com/) was used for hosting the deployed back-end site.
- [Balsamiq](https://balsamiq.com/) was used to create the project wireframes.

## Database Structure

I used MongoDB, a non-relational database architecture.

The database is named __restaurant_review__ which has 4 collections as follows:

### restaurant_types

This contains a record of the types of restaurants/cuisines that a restaurant would be categorised as

| Key  | Type       | Comment                 |
|------|------------|-------------------------|
| _id  | ObjectId() | Automatically generated |
| type | String     |                         |

### restaurants

This contains details of the restaurants.

| Key         | Type       | Comment                                |
|-------------|------------|----------------------------------------|
| _id         | ObjectId() | Automatically generated                |
| name        | String     |                                        |
| url         | String     |                                        |
| type        | String     | Taken from restaurant_types collection |
| address     | String     |                                        |
| town        | String     |                                        |
| county      | String     |                                        |
| postcode    | String     |                                        |
| description | String     |                                        |
| image_url   | String     |                                        |
| featured    | Boolean    |                                        |

### reviews

This contains the reviews of the restaurants. It uses resturant_id to refer to the _id in the restaurants table which acts as a foreign key.

| Key            | Type       | Comment                                     |
|----------------|------------|---------------------------------------------|
| _id            | ObjectId() | Automatically generated                     |
| title          | String     |                                             |
| review_date    | String     |                                             |
| user_id        | String     |                                             |
| food_rating    | Int32      |                                             |
| service_rating | Int32      |                                             |
| overall_rating | Int32      |                                             |
| restaurant_id  | String     | _id of restaurant in restaurants collection |
| review_content | String     |                                             |

### users

Collection of users including their username, hashed password and indication if they are an administrator or not.

| Key      | Type       | Comment                 |
|----------|------------|-------------------------|
| _id      | ObjectId() | Automatically generated |
| username | String     |                         |
| password | String     | sha56 hashed password   |
| is_admin | String     | yes or no               |

## Testing

### User stories tests

### Functionality

### HTML Validation

All pages were tested using the [W3C HTML validator](https://validator.w3.org/nu/) and no errors were found. The results are in the attached [PDF document](/static/images/documentation/html-validation.pdf).

### CSS Validation

The CSS stylesheet styles.css was checked using the [W3C CSS validator](https://validator.w3.org/) and no errors were found.

![CSS Validation results](/static/images/documentation/css-validation.png).

## JS Validation

[JSHint](https://jshint.com/) was used to validate the JavaScript for script.js using the configuration to assume ES6 and jQuery. The validator identified 2 statements without semicolons which were corrected and the script.js file then passed validation.

![JS Validation results](/static/images/documentation/js-validation.png)

## Python Validation

The app.py Python code was checked using the [CI Python Linter](https://pep8ci.herokuapp.com/). There were a number of lines that were too long so these were corrected. The check was rerun and was found to be PEP8 compliant with no errors.

![Python Validator results](/static/images/documentation/python-linter.png)

### Accessibility and Performance

Accessibility was checked to ensure that Aria labels and image alt text was added to all images and visual elements on the site.

Lighthouse reports were also created which passed accessibility except sequential headings as h5 was used in the card section as recommended by Bootstrap. Changing this to h2 would change the look of the website but this could be looked at in future iterations. There were also a few performance suggestions which could be implemented in future iterations:

- [Lighthouse report for index page](/static/images/documentation/lighthouse-report-index.pdf)
- [Lighthouse report for add category page](/static/images/documentation/lighthouse-report-add-category.pdf)
- [Lighthouse report for add restaurant page](/static/images/documentation/lighthouse-report-add-restaurant.pdf)
- [Lighthouse report for categories page](/static/images/documentation/lighthouse-report-categories.pdf)
- [Lighthouse report for edit restaurant page](/static/images/documentation/lighthouse-report-edit-restaurant.pdf)
- [Lighthouse report for login page](/static/images/documentation/lighthouse-report-login.pdf)
- [Lighthouse report for restaurant display page](/static/images/documentation/lighthouse-report-restaurant.pdf)
- [Lighthouse report for restaurants listing page](/static/images/documentation/lighthouse-report-restaurants.pdf)
- [Lighthouse report for user administration page](/static/images/documentation/lighthouse-report-user-admin.pdf)
- [Lighthouse report for write review page](/static/images/documentation/lighthouse-report-write-review.pdf)

### Browser Compatibility

### Device Compatibility

The responsiveness and layout of the site has been tested on a number of devices including tablets, desktops and mobile phones from iPhone 5 to 5K screens and the website displays correctly.

Chrome developer tools were used at various points during the development including when changes were made to the layout.

### Check links work

All links were tested manually and by using the [Broken Link Checker](https://chrome.google.com/webstore/detail/broken-link-checker/nibppfobembgfmejpjaaeocbogeonhch?utm_source=ext_sidebar&hl=en-US) extension on Google Chrome.

## Bugs

## Deployment

## Credits

- The colour palette was generated by https://www.color-hex.com/
