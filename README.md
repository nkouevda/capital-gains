# capital-gains

Capital gains calculator.

This transforms transaction histories into a format suitable for [IRS form
8949](https://www.irs.gov/pub/irs-pdf/f8949.pdf), taking care of wash sale
adjustments.

Note: The logic is ignorant of share type, and cannot account for e.g. bargain
elements for ESPP, ISO, and NSO. You must enter the appropriate cost basis
depending on your situation, e.g. the fair market value on exercise date for
ESPP disqualifying dispositions.

See also
[nkouevda/estimated-taxes](https://github.com/nkouevda/estimated-taxes).

## Installation

    pip install capital-gains

## Usage

```
usage: capital-gains [<options>] [--] <input file>

Capital gains calculator

optional arguments:
  -h, --help            show this help message and exit
  -d <n>, --decimal-places <n>
                        round $ to <n> decimal places; default: 0
  -s <n>, --shares-decimal-places <n>
                        round shares to <n> decimal places; default: 0
  -t, --totals          output totals
  -v, --verbose         verbose output
  -V, --version         show program's version number and exit
```

## Input Format

See [input/example.csv](input/example.csv).

Each entry has the following format:

    date,symbol,name,shares,price,fee

Buys have positive `shares`; sells have negative `shares`. `price` and `fee` are
always positive. `fee` and `name` are optional. A sell without a `name` will
sell all open lots FIFO; a sell with a `name` will only sell lots with the same
`name`. Thus `name` can be used to specify sell orders other than FIFO.

## Examples

    capital-gains -t input/example.csv > output/example.txt

## TODO

- STCG vs. LTCG

## License

[MIT License](LICENSE.txt)
