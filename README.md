# Scandinavian Language Models

Central repository for model configs, slurm scripts, singularity container definition files, and documentation for the Scandinavian Language Models project.

## Getting started on Leonardo

For general documentation on how to use Leonardo, see the [Leonardo User Guide](https://wiki.u-gov.it/confluence/display/SCAIUS/UG2.0%3A+General+Information), and information about the [Leonardo cluster](https://wiki.u-gov.it/confluence/display/SCAIUS/UG3.2.1%3A+LEONARDO+Booster+UserGuide).

### Storage and group directories

Each user has `50GB` of storage in their home directory. Our project also has `4TB` of additional group storage on Leonardo. The project storage is located at: `/leonardo_work/EUHPC_D07_027`. 

You should be able to find these directories via the environment variables `$HOME` and `$WORK`. 

It is recommended that everyone creates a directory for their work under `scandinavian-lm`. 

```
/leonardo_work/EUHPC_D07_027
│   ├── containers
│   ├── data
│   ├── models
│   ├── scandinavian-lm
│   │   ├── <your-username>
```

In order for other users to be able to access your files, you should set `umask 007` in your `.bashrc` file. This gives everyone in the group read and write access to files you create.

### Usage quotas

To check the project's compute usage and quotas in a given month:

```bash
saldo -b
```

To check the your personal, and the project's storage usage:

```bash
cindata
```

### Transferring data

Leonardo has a [guide](https://wiki.u-gov.it/confluence/display/SCAIUS/Rsync) on how to transfer data with `rsync`. They recommend starting an interactive session with SLURM on the `lrd_all_serial` partition (cpu only):

```bash
srun --partition=lrd_all_serial --nodes=1 --ntasks=1 --cpus-per-task=1 --mem=8GB --time=0-01:00:00 --qos=normal --account=EUHPC_D07_027 --pty /bin/bash
```

Then you can use `rsync` to transfer data to Leonardo from your local machine:

```bash
rsync -PravzHS /data_path_from/dir username@login.leonardo.cineca.it:/data_path_to/dir
```

However, it does not appear to be necessary to start an interactive session. You can simply use the `rsync` command without the `srun` job. 

## SLURM

