# Linear Regression 

## About

To be defined.

## Setup 

To be defined. 

## Usage

To be defined. 

### CLI

You can train and score a linear regression directly form the commandline. 

**Training** a linear regression:   

```commandline
$ python main.py train_linear_regression \
    --data-path data/weather.csv  \
    --target-column max_temp \
    --method linalg \
    --save-path model-example.json
```

Options: 

```text

```


**Scoring** a linear regression:  

```commandline
$ python main.py score_linear_regression \
    --model-path model-example.json
```

Options: 

```text

```


### Python

To be defined