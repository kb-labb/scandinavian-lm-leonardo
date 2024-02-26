## Singularity

### Installation

You ideally need to install Singularity on a system where you can build containers with root access (`sudo`). Follow [the instructions here](https://docs.sylabs.io/guides/3.0/user-guide/installation.html#install-on-linux) to install Singularity from source.

### Building containers

Run `singularity build` with a def file:

```bash
sudo singularity build pytorch_2307_nemo.sif pytorch_ngc_nemo.def
```

You can also build containers in sandbox mode, where the container is not packed into a single file, but is instead a directory of the entire container filesystem. This can be useful for debugging and development:

```bash
sudo singularity build --sandbox pytorch_2307_nemo pytorch_ngc_nemo.def
```

### Running containers

To run containers in interactive mode with GPU support, use the following command:

```bash
singularity shell --nv pytorch_2307_nemo.sif
```