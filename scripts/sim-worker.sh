## Setup and run ddsim instance; useful as task for pytaskfarmer or standalone
## Args: input_file output_prefix [nevents=-1 [skipevents=0]]
## Notes:
## - provided as template and, while it might fit many use-cases, it's meant to be customized
## - ultimately, a DDSimTaskList handler for pytaskfarmer should incorporate these functionalities and is preferred, when possible.

# Settings

IN_PATH="/global/cfs/cdirs/atlas/arastogi/WFA/slcio_out/Files_100K/WithPhotonEtaElePtFilters/"
OUT_PATH="/global/cfs/cdirs/atlas/spgriso/WFA/data/WarpX-out/ddsim/MuColl_v1/bib-only/"
#IN_PATH="/global/cfs/cdirs/atlas/spgriso/WFA/data/single-particles/"
#OUT_PATH="/global/cfs/cdirs/atlas/spgriso/WFA/data/single-particles/"


random_postfix=`echo $RANDOM | md5sum | head -c 6`
RUN_PATH="${SCRATCH}/wcd-simrun-${random_postfix}" #temporary unique running path
SIM_CONFIG="/global/cfs/cdirs/atlas/spgriso/WFA/WakefieldBeamStudiesWorkspace/configs/ddsim_steer_baseline.py"
GEO_CONFIG="/global/cfs/cdirs/atlas/spgriso/WFA/WakefieldBeamStudiesWorkspace/geometry/MuColl/MuColl_v1/MuColl_v1.xml"

TIME="Time %E (%P CPU)\nMem %Kk/%Mk (avg/max): %Xk(shared) + %Dk(data)\nI/O %I+%O; swaps: %W"

# Utility functions
tell () {
    now=`date +"%4Y.%m.%d-%H.%M.%S"`
    echo "${now} sim-worker: $1"
}

quit () {
    tell "$1"
    sleep 0.1
    exit $2
}

copyout() {
  IN=$1
  OUT=$2
  echo "Moving ${PWD}/${IN} -> ${OUT_PATH}/${OUT}"
  if [ -f $1 ]; then
  	if ! mv ${IN} ${OUT_PATH}/${OUT} ; then
	    tell "ERROR! Failed to transfer ${IN} -> ${OUT}"
 	fi
  else
    tell "ERROR! File ${IN} does not exist"
  fi	
}

# Determine input file and events
if [ -z "$1" ]; then
    quit "ERROR! Usage: $0 input_file output_prefix [nevents=-1 [skipevents=0]]" 1
fi
IN_FILE="${IN_PATH}/$1"

if [ -z "$2" ]; then
    quit "ERROR! Usage: $0 input_file output_prefix [nevents=-1 [skipevents=0]]" 1
fi
OUT_FILE_PREFIX=$2

N_EVENTS_PER_JOB=-1
N_SKIP_EVENTS=0
if ! [ -z "$3" ]; then
    N_EVENTS_PER_JOB=$3
    if ! [ -z "$4" ]; then
	N_SKIP_EVENTS=$4
    fi
    # update output file
    MAX_EVENT=$(( N_SKIP_EVENTS + N_EVENTS_PER_JOB - 1 ))
    OUT_FILE_PREFIX="${OUT_FILE_PREFIX}_${N_SKIP_EVENTS}-${MAX_EVENT}"
fi

tell "Input: ${IN_FILE} (start evt: ${N_SKIP_EVENTS}, n. evt: ${N_EVENTS_PER_JOB})."
tell "Output (prefix): ${OUT_FILE_PREFIX}"

# Preparing running folder
tell "Running ddsim in ${RUN_PATH}..."
mkdir -p ${RUN_PATH}
cd ${RUN_PATH}

# If output contains a folder, create it
OUT_HAS_FOLDER=`dirname ${OUT_FILE_PREFIX}`
if ! [ -z "$OUT_FILE_PREFIX" ]; then
    # Create output folder
    tell "Creating output sub-folder: ${OUT_HAS_FOLDER}"
    mkdir ${OUT_HAS_FOLDER}
fi

# Prepare to run - setup software only if needed
if [ -z "${WCD_VER}" ]; then
    echo "Setup WCD software"
    source /opt/setup_mucoll.sh
fi

# Run ddsim
#/usr/bin/time --format="${TIME}" --
export WCD_GEO=${GEO_CONFIG}
ddsim --steeringFile ${SIM_CONFIG} --inputFile ${IN_FILE} --outputFile ${OUT_FILE_PREFIX}.slcio  --numberOfEvents ${N_EVENTS_PER_JOB} --skipNEvents ${N_SKIP_EVENTS} >& ${OUT_FILE_PREFIX}.log 

tell "ddsim DONE."

# Copy output
tell "Copying output from current folder ($PWD) to ${OUT_PATH}"
ls -lh
tell "----------"

copyout ${OUT_FILE_PREFIX}.slcio ${OUT_FILE_PREFIX}.slcio
copyout ${OUT_FILE_PREFIX}.log ${OUT_FILE_PREFIX}.log

tell "All Done."
