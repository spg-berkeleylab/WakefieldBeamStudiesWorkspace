# Beam-Beam interactions studies for Wakefield Collider Detector

## Repository Structure
- `exts/` External packages not included with the ILC framework.
- `packages/` All custom packages linked using git submodules.
- `configs/` common configurations files
- `geometry/` xml geometry files for ddsim
- `scripts/` utility scripts 

## Setup Instructions

See [wcd-docker](https://github.com/spg-berkeleylab/wcd-docker) for instructions to setup the container.

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

## Simulations
The file `configs/ddsim_steer_baseline.py` contains a baseline `ddsim` configuration.
Specify the geometry setting the `WCD_GEO` environment variable, e.g.

```bash
export WCD_GEO=/global/cfs/cdirs/atlas/spgriso/WFA/WakefieldBeamStudiesWorkspace/geometry/MuColl/MuColl_v1/MuColl_v1.xml
ddsim --steeringFile ${MYWORKSPACE}/configs/ddsim_steer_baseline.py --inputFile /global/cfs/cdirs/atlas/spgriso/WFA/data/WarpX-out/lcio/electron_electron_flat.slcio --outputFile /global/cfs/cdirs/atlas/spgriso/WFA/data/WarpX-out/ddsim/MuColl_v1/bib-only/sim-electron_electron_flat.slcio
```