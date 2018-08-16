[![Build Status](https://travis-ci.org/Gidraf/Stackoverflow-lite.svg?branch=get_questions)](https://travis-ci.org/Gidraf/Stackoverflow-lite)
<<<<<<< HEAD
[![Coverage Status](https://coveralls.io/repos/github/Gidraf/Stackoverflow-lite/badge.svg?branch=development)](https://coveralls.io/github/Gidraf/Stackoverflow-lite?branch=development)

[![stable](http://badges.github.io/stability-badges/dist/stable.svg)](http://github.com/badges/stability-badges)

[![Maintainability](https://api.codeclimate.com/v1/badges/e01c4acdf982d57d2cfa/maintainability)](https://codeclimate.com/github/Gidraf/Stackoverflow-lite/maintainability)
=======
[![Coverage Status](https://coveralls.io/repos/github/Gidraf/Stackoverflow-lite/badge.svg?branch=master)](https://coveralls.io/github/Gidraf/Stackoverflow-lite?branch=development)
>>>>>>> b4ecf303fd940471809bdc7401d71e83e4b8230d

# Stackoverflow-lite
StackOverflow-lite is a platform where people can ask questions and provide answers

## Required Features
    1. Users can create an account and log in.
    2. Users can post questions.
    3. Users can delete the questions they post
    4. Users can post answers
    5. Users can view the answers
    6. Users can accept an answer out of all the answers to his/her queston as they preferred answer

## Installation

### To install the stable version:

```
git clone https://github.com/Gidraf/Stackoverflow-lite.git
pip install -r requirements.txt
python run.py (run app)
```
## Testing
```
$ pytest
```

## Api Endpoints
### Questions API endpoints
```
/api/v1/questions (get all questions)
/api/v1/add_question (post a question)
/api/v1/questions/1 (get specific question and add answer to that question)
/api/v1/update_question/<int:question_id> (update question)
/api/v1/delete_question/<int:question_id> (delete question)

```
