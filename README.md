# Scandinavian Language Models

Central repository for model configs, slurm scripts, singularity container definition files, and documentation for the Scandinavian Language Models project.

## Getting started on Leonardo

For general documentation on how to use Leonardo, see the [Leonardo User Guide](https://wiki.u-gov.it/confluence/display/SCAIUS/UG2.0%3A+General+Information), and information about the [Leonardo cluster](https://wiki.u-gov.it/confluence/display/SCAIUS/UG3.2.1%3A+LEONARDO+Booster+UserGuide).

### Login

If you haven't configured smallstep to set up a certificate, first follow the instructions in the [smallstep documentation](https://wiki.u-gov.it/confluence/display/SCAIUS/Setup+client+step-cli%3A+Linux+and+Mac+users).

To login with 2FA, authenticate with smallstep using the e-mail you registered with:

```bash
step ssh login '<user-email>' --provisioner cineca-hpc
```

This will open up a browser where you login with your Cineca credentials. Once you activated the 2FA:

```bash
ssh <username>@login.leonardo.cineca.it
```

Specific login servers can be found in the [Leonardo User Guide](https://wiki.u-gov.it/confluence/display/SCAIUS/UG3.2%3A+LEONARDO+UserGuide).

### Storage and group directories

Each user has `50GB` of storage in their home directory. Our project also has `4TB` of additional group storage on Leonardo. The project storage is located at: `/leonardo_work/EUHPC_A02_045`. 

You should be able to find these directories via the environment variables `$HOME` and `$WORK`. 

It is recommended that everyone creates a directory for their work under `scandinavian-lm`. Containers you've built or used to train a specific model go under `containers`. Model logs or tensorboard output in `experiment_logs`. 

```
/leonardo_work/EUHPC_A02_045
│   ├── containers
│   ├── data
|   ├── experiment_logs
│   ├── models
│   ├── scandinavian-lm
│   │   ├── <your-username>
|   ├── tokenizers
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

Leonardo has a [guide](https://wiki.u-gov.it/confluence/display/SCAIUS/Datamover) on how to transfer data with `rsync`, `scp`, `sftp`, `wget` or `curl`. You can either 

1. Transfer data directly via login node `rsync -PravzHS /data_path_from/local_dir <user>@login.leonardo.cineca.it:/data_path_to/leonardo_dir`. Login nodes only allow processes to run for a limited time however, so this is not recommended for large transfers.
2. Transfer via Leonardo's dedicated data transfer nodes. `rsync -PravzHS /data_path_from/local_dir <user>@data.leonardo.cineca.it:/data_path_to/leonardo_dir`.

## SLURM

Check the status of nodes on Leonardo:

```bash
sinfo
```

Check the status of your jobs:

```bash
squeue --me
```

Start an interactive session with SLURM (change job priority and max duration by changing `--qos`, see [documentation](https://wiki.u-gov.it/confluence/display/SCAIUS/UG3.2.1%3A+LEONARDO+Booster+UserGuide)):

```bash
srun --partition=boost_usr_prod --nodes=1 --ntasks=1 --cpus-per-task=1 --mem=8GB --gres=gpu:1 --time=0-00:30:00 --qos=boost_qos_dbg --account=EUHPC_A02_045 --pty /bin/bash
```

Kill a job:

```bash
scancel <job_id>
```

Typically, multinode jobs are submitted via `sbatch`. This is a generalized way of submitting a job that automatically launches scripts on each node (technically each task on a node). We have a [start script template](https://github.com/kb-labb/scandinavian-lm-leonardo/blob/main/scripts/start_script.sh). Everything in this script is run only once, except for whatever follows the `srun` command. The container and script that `srun` execute will be run independently on *every* task/process. 

In most cases the start script will only need modifications of the container name and the training launch script that the container runs. It is the training launch script that is customized for each model. See [this training launch script as an example](https://github.com/kb-labb/scandinavian-lm-leonardo/blob/main/scripts/bert-base/start_training-nemo-bert-base-unigram-64k-pretok-small_data.sh).

Example of launching a job based on the [start script]((https://github.com/kb-labb/scandinavian-lm-leonardo/blob/main/scripts/start_script.sh)) ($1, $2, $3 in the script are positional arguments):

```bash
sbatch --job-name="bert" scripts/start_script.sh bert-base/start_training-bert-base-unigram-64k-pretok.sh faton
```

## Getting Git to work on Leonardo

On most clusters it is possible to forward your SSH agent (with credentials/keys) to the cluster using the `-A` flag with `ssh`. Leonardo does not appear to have `ssh-agent` activated upon login which causes issues with this method. 

As a work around you can either create a new SSH key pair on Leonardo and add the public key to your GitHub account, or you can transfer your existing public/private key pair to Leonardo (to the directory `~/.ssh/`). If you transfer keys, you need to set appropriate permissions on the public/private key files:

```bash
chmod 600 ~/.ssh/my_private_key
chmod 644 ~/.ssh/my_public_key.pub
```

Then activate `ssh-agent` (it may be good to add this to your `.bashrc` file): 

```bash
eval `ssh-agent`
```

And finally add your private key to the agent:

```bash
ssh-add ~/.ssh/my_private_key
```

Configure your git user name and email:

```bash
git config --global user.name "Your username"
git config --global user.email "Your email"
```

## Singularity

See the [README in the containers directory](https://github.com/kb-labb/scandinavian-lm-leonardo/tree/main/container) for instructions on how to install Singularity, build containers, and run containers on Leonardo. 

## Developing with python venv and modules

If you want to test and run things without containers, you can use python venv through the `module` system on Leonardo. See the documentation on how to [load Leonardo's AI module and create a python venv](https://wiki.u-gov.it/confluence/display/SCAIUS/Leonardo+-+Scientific+Python+user+environment+and+tools+for+AI%3A+the+CINECA+Artificial+Intelligence+project).

```bash
module load profile/deeplrn
module load cineca-ai/3.0.1 # There are other version, check with 'module av cineca-ai'
```

You are then able to use Python with Leonardo's pre-installed packages. To create your own virtual environment:

```bash
python -m venv <myvenv> --system-site-packages
```

Activate the venv:

```bash
source <myvenv>/bin/activate
pip list
```

You can then install packages with pip as usual. However, you may have to unload the `cineca-ai` module for the default python path to actually use the packages in your venv as opposed to the system site packages. To unload the module, use the following command:

```bash
module unload cineca-ai
```

If you still require CUDA, GCC or other system modules, you can load them separately.

```
module load cuda/11.8
module load gcc/11.3.0
module load cudnn/8.9.6.50-11.8--gcc--11.3.0
module load nccl/2.14.3-1--gcc--11.3.0-cuda-11.8
```

*NOTE*: Internet access is not available on compute nodes. If you want to `pip install` packages, you need to do so on a login node.