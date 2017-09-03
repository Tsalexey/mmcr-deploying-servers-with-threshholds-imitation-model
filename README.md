# mmcr deploying servers with threshholds imitation model
Imitation model for M/M/C/R system with 'c' core servers, 'k' servers to deploy and two threshholds

- C - total servers count
- c - core servers
- k - servers to be deployed\n
- R - queue size\n
- L - first threshhold\n
- H - second threshhold\n

## System description

 We have 'c' permanently servers working. If queue size is more then 'H' new servers start to turn on. If queue size is less then 'L' excessive servers turn off.

## Run
> python main.py output_filename lambda mu theta C c0 Q L H simulation_time is_debug
