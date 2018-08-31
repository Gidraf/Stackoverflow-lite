[![Build Status](https://travis-ci.org/Gidraf/Stackoverflow-lite.svg?branch=get_questions)](https://travis-ci.org/Gidraf/Stackoverflow-lite)
[![Test Coverage](https://api.codeclimate.com/v1/badges/e01c4acdf982d57d2cfa/test_coverage)](https://codeclimate.com/github/Gidraf/Stackoverflow-lite/test_coverage)
[![stable](http://badges.github.io/stability-badges/dist/stable.svg)](http://github.com/badges/stability-badges)
[![Maintainability](https://api.codeclimate.com/v1/badges/e01c4acdf982d57d2cfa/maintainability)](https://codeclimate.com/github/Gidraf/Stackoverflow-lite/maintainability)

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

## Api Endpoints(api/v1)
### Questions API endpoints


|Method | Endpoint     | Functionality       |
|:-----:|:------------:|---------------------|
|POST   | `/questions` | post a question     |
|GET    | `/questions` |  get questions      |     
|GET    | `/questions/ |get specific question|
|       |  question_id`|                     |
|PUT    | `questions/1`| edit question       |
|DELETE | `questions/1`| Delete question     |
|       |              |                     |
