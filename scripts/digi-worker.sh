## Setup and run k4run instance
## Args: input_file output_prefix [nevents=-1 [skipevents=0 [nBIB=10]]]
## Notes:
## - FIXME: k4run does not support skipEvents!!
## - randomizes BIB selection; select nBIB files
## - if a workspace folder is provided below, the environment is setup to include local packages
## - provided as template and, while it might fit many use-cases, it's meant to be customized
## - ultimately, a k4runTaskList handler for pytaskfarmer should incorporate these functionalities and is preferred, when possible.

# Settings

IN_PATH="/global/cfs/cdirs/atlas/spgriso/WFA/data/WarpX-out/digi/MuColl_v1/single-particles/single-nu/"
OUT_PATH="/global/cfs/cdirs/atlas/spgriso/WFA/data/WarpX-out/digi/MuColl_v1/bib-only/electron_positron_round/"
BIB_FILES="/global/cfs/cdirs/atlas/spgriso/WFA/data/WarpX-out/ddsim/MuColl_v1/bib-only/electron_positron_round/sim-out-merged.slcio"
NBIB_EVENTS=145 #electron_positron_round: 145, electron_positron_flat: 17, electron_electron_flat: 15, electron_electron_round: 0

CONFIG_PATH="/global/cfs/cdirs/atlas/spgriso/WFA/WakefieldBeamStudiesWorkspace/configs"
CONFIG_FILE="digi_steer.py" #relative to $CONFIG_PATH
GEO_CONFIG="/global/cfs/cdirs/atlas/spgriso/WFA/WakefieldBeamStudiesWorkspace/geometry/MuColl/MuColl_v1/MuColl_v1.xml"
WORKSPACE_PATH="/global/cfs/cdirs/atlas/spgriso/WFA/WakefieldBeamStudiesWorkspace/"
MYBUILD="build" #build folder (either relative to $WORKSPACE_PATH or absolute path

random_postfix=`echo $RANDOM | md5sum | head -c 6`
RUN_PATH="${SCRATCH}/muc-recrun-${random_postfix}" #temporary unique running path
TIME="Time %E (%P CPU)\nMem %Kk/%Mk (avg/max): %Xk(shared) + %Dk(data)\nI/O %I+%O; swaps: %W"


# Utility functions
tell () {
    now=`date +"%4Y.%m.%d-%H.%M.%S"`
    echo "${now} digi-worker: $1"
}

quit () {
    tell "$1"
    sleep 0.1
    exit $2
}

copyout() {
  IN=$1
  OUT=$2
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
    quit "ERROR! Usage: $0 input_file output_prefix [nevents=-1 [skipevents=0 [nBIB=10]]]" 1
fi
IN_FILE="${IN_PATH}/$1"

if [ -z "$2" ]; then
    quit "ERROR! Usage: $0 input_file output_prefix [nevents=-1 [skipevents=0 [nBIB=10]]]" 1
fi
OUT_FILE_PREFIX=$2

N_EVENTS_PER_JOB=-1
if ! [ -z "$3" ]; then
    N_EVENTS_PER_JOB=$3
    
    N_SKIP_EVENTS=0
    if ! [ -z "$4" ]; then
	N_SKIP_EVENTS=$4
    fi

    # update output file
    MAX_EVENT=$(( N_SKIP_EVENTS + N_EVENTS_PER_JOB - 1 ))
    OUT_FILE_PREFIX="${OUT_FILE_PREFIX}_${N_SKIP_EVENTS}-${MAX_EVENT}"
fi



tell "Input: ${IN_FILE} (start evt: ${N_SKIP_EVENTS}, n. evt: ${N_EVENTS_PER_JOB})."
tell "Output: ${OUT_FILE_PREFIX}.slcio/.log"

# Prepare and run Marlin
if ! [ -z "${WORKSPACE_PATH}" ]; then
    tell "Setting up workspace environment"
    cd ${WORKSPACE_PATH}    
    tell "Local packages:"
    for pkglib in `find ${MYBUILD}/packages -name '*.so' -type l -o -name '*.so' -type f`; do
	pkgname=$(basename ${pkglib})
	tell "- ${pkgname}"
    done
		  
    if ! [ -r "setup.sh" ]; then
	quit "Workspace provided (${WORKSPACE_PATH}), but no 'setup.sh' found."
    fi
    source setup.sh $MYBUILD
    echo "MARLIN_DLL=${MARLIN_DLL}"
    echo "PATH=${PATH}"    
fi

tell "Preparing to run"
mkdir -p ${RUN_PATH}
cd ${RUN_PATH}

cp -r ${CONFIG_PATH}/* . #copy the whole set of config files

# If output contains a folder, create it
OUT_HAS_FOLDER=`dirname ${OUT_FILE_PREFIX}`
if ! [ "$OUT_FILE_PREFIX" != "." ]; then
    # Create output folder
    tell "Creating output sub-folder: ${OUT_HAS_FOLDER}"
    mkdir ${OUT_HAS_FOLDER}
fi

tell "Running k4run..."
# Prepare to run - setup software only if needed
if [ -z "${WCD_VER}" ]; then
    echo "Setup WCD software"
    source /opt/setup_mucoll.sh
fi
#/usr/bin/time --format="${TIME}" --

NOBIB_OPTS="--OverlayFullPathToMuPlus \"\" --OverlayFullPathToMuMinus \"\" --OverlayFullNumberBackground 0"
OVERLAYIP_OPTS="--doOverlayIP --OverlayIPBackgroundFileNames ${BIB_FILES} --OverlayIPNumberBackground ${NBIB_EVENTS}"
export WCD_GEO=${GEO_CONFIG}
k4run --num-events ${N_EVENTS_PER_JOB} ${CONFIG_FILE} --writeAll --LcioEvent.Files ${IN_FILE} ${NOBIB_OPTS} ${OVERLAYIP_OPTS} &> ${OUT_FILE_PREFIX}.log
# --global.SkipNEvents=${N_SKIP_EVENTS}

tell "k4run DONE."

# Copy output
tell "Copying output from current folder ($PWD) to ${OUT_PATH}"
ls -lRh
tell "----------"

if [ -r output_digi_light.slcio ]; then
    copyout output_digi_light.slcio ${OUT_FILE_PREFIX}_light.slcio
fi
if [ -r output_digi.slcio ]; then
    copyout output_digi.slcio ${OUT_FILE_PREFIX}_full.slcio
fi
copyout ${OUT_FILE_PREFIX}.log ${OUT_FILE_PREFIX}.log

tell "All Done."
