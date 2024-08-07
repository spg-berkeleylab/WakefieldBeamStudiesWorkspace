# Template Workspace

Template for developing custom Marlin packages. Fork this repository and rename to create your own project.

## Repository Structure
- `exts/` External packages not included with the ILC framework.
- `packages/` All custom packages linked using git submodules.

## Setup Instructions

### Container
All commands are compatible and should be run inside the latest `gitlab-registry.cern.ch/muon-collider/muoncollider-docker/mucoll-sim:master-alma9` image (versions 2.8 and above).

#### Apptainer
```bash
apptainer shell --cleanenv gitlab-registry.cern.ch/muon-collider/muoncollider-docker/mucoll-sim:master-alma9
```

#### Shifter
```bash
shifter --image gitlab-registry.cern.ch/muon-collider/muoncollider-docker/mucoll-sim:master-alma9 /bin/bash
```

### Build Instructions
Run the following commands from inside your container. The same commands will also work with a local installation of the ILC and Key4Hep software, with the exception of the first line.
```bash
source /opt/setup_mucoll.sh # Setup software
cmake -S . -B build 
cmake --build build
```

### Setup Script
The included `setup.sh` script is useful for defining all paths for the binaries built by the workspace. At the current stage, it setups the following:
- software via `init_mucoll.sh`
- External binaries/libraries found in `exts`.
- Add all package libraries to `MARLIN_DLL`.
- Export `MYBUILD` variable with absolute path to the build directory.
- Export `MYWORKSPACE` variable with absolute path to the workspace directory.

Run the following at the start of every session. It has an optional argument to the build directory and is set to `build/` by default.
```bash
source setup.sh [build]
```
