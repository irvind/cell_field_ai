# Cell Field AI

Cell Field AI is an example of a genetic algorithm implementation. The algorithm finds the best solution among the population by using a feedforward neural network.

## What is a cell field?

The cell field is a 3x3 integer matrix, each cell of which contains value between 0 and 10. The cell field becomes complete if each cell is greater or equal to 1. 

## How does it work?

The feedforward neural net is used to increment the value of the cell field cells by 1. The network has 9 inputs (values of the field cells) and 9 outputs indicating which cell should be incremented next. A simulation of the cell field continues until all cells have value greater than 0, or if value of single cell becomes greater or equal to 10.

## Dependencies

* Python >= 3.9
* Numpy == 1.24.3

## Getting started

TODO
