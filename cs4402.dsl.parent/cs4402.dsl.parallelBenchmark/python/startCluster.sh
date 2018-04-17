#!/bin/bash
dask-ssh --nthreads 1 --nprocs 1 --scheduler $(hostname -s) --ssh-private-key /cs/home/lw96/.ssh/id_internal --hostfile $1
