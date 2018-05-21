# capital-gains

Capital gains calculator.

## Installation

    pip install capital-gains

## Usage

```
usage: capital-gains [<options>] [--] <input file>

Capital gains calculator

optional arguments:
  -h, --help     show this help message and exit
  --cents        round to nearest cents, not dollars
  -v, --version  show program's version number and exit
```

## Input format

See [example/input.csv](example/input.csv).

Each entry has the following format:

    date,symbol,name,shares,price,fee

Buys have positive `shares`; sells have negative `shares`. `price` and `fee` are
always positive. `fee` and `name` are optional. A sell without a `name` will
sell all open lots FIFO; a sell with a `name` will only sell lots with the same
`name`. Thus `name` can be used to specify sell orders other than FIFO.

## Output format

Closed lots are tabulated in a format suitable for [form
8949](https://www.irs.gov/pub/irs-pdf/f8949.pdf), rounded to the nearest dollar
(use `--cents` to round to the nearest cent).

Open lots are also summarized.

## Examples

    capital-gains example/input.csv > example/output.txt

## License

[MIT License](LICENSE.txt)
