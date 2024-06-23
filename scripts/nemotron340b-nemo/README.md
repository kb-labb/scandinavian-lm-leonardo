## Nemotron-340B inference

This directory contains scripts for performing inference with Nemotron-340B on 4 nodes with 4 A100 65GB VRAM GPUs each.

### Usage

Spinning up a server for inference should be as simple as running the following command:

```bash
sbatch start_inference.sh
```
You may have to wait ~4 minutes before the server is ready to accept requests. You can check the status of the server by checking the logs in the `logs` directory. Wait for `0: server (0.0.0.0:1424) is up running` to appear in the logs.

> [!NOTE]
> Change the `SCRIPTS_DIR` variable in `start_inference.sh` to point to your local absolute path to the `scripts` directory found inside this directory.
> All commands in this guide assume that the directory of this `README` is the current working directory.

> [!WARNING]
> Create a `logs` directory in the current directory before running the sbatch script, or the script will silently fail.

### Making requests

Once the server is up and running, you can make requests by

1. SSH:ing into one of the nodes running the server. Check which nodes are running with `squeue --me`. Pick one of the nodes named `lrdnXXXX` (e.g. `lrdn0135`) and SSH into it with `ssh lrdn0135`. You will be prompted for a password, this password is the same as the one you set up to verify your 2FA when logging in to `sso.hpc.cineca.it` when running smallstep.
2. Once inside the node, start an interactive singularity shell with the following command: `singularity shell --nv --bind /leonardo_work/EUHPC_D07_027 /leonardo_work/EUHPC_D07_027/containers/nemotron_2401.sif`.
3. Inside the singularity shell you can perform inference either by `python scripts/call_server.py`, or by starting an interactive python shell with `python` and running the code in `call_server.py` manually.

Make sure to cancel/kill your SLURM job when you are done with inference `scancel <job_id>`.

### Modifying the inference call

Modify `call_server.py` to change how the responses are handled and how the requests are made. Current script just prints responses. 