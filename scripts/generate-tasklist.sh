#!/bin/bash
# Generate and print to screen the task list for a given input prefix ($1) and output prefix ($2).
# Arguments: $0 in_prefix out_prefix [n_events_per_job n_events_per_file n_events_input [worker_script]] > output-tasklist.txt
# Assumes two possible input file patterns:
# 1) input in files with format ${in_prefix}_XXXX-YYYY.slcio, indicating that the file contains events from #XXXX to event number #YYYY from previous processing steps;
# 2) if running on single input files, provide n_events_input == n_events_per_file, and input will be ${in_prefix} (add .slcio to the argument)
# Notes:
# - you can further split longer lists as in the example that follows:
#   split -l 50 -a 3 --numeric-suffixes=1 my-tasks.txt my-tasks-
#   that generates smaller lists of 50 tasks per file called my-tasks-XXX.

in_prefix=$1 #input prefix (e.g. out1 for out1_XXXX-YYYY.slcio inputs)
out_prefix=$2 #output prefix (output files: ${out_prefix}_XXXX-YYYY_WWWW-ZZZZ.slcio, where (XXXX+WWWW)-(XXXX+ZZZZ) is the range of events processed
n_events_per_job=${3:-5} #events per reco job
n_events_per_file=${4:-500} #events per file per input prefix
n_events_input=${5:-20000} #total events to process per input prefix
worker=${6:-"${PWD}/reco-worker.sh"} #name of worker/script for the task

n_files=$(( n_events_input / n_events_per_file ))
if [ $((n_events_input % n_events_per_file)) != 0 ]; then
    n_files=$((n_files+1))
fi
for i_file in `seq 0 $((n_files-1))`; do
    job_skip_events=0 #will increment as we go
    min_event=$(( i_file*n_events_per_file ))
    max_event=$(( min_event + n_events_per_file - 1 ))
    if [ ${max_event} -gt ${n_events_input} ]; then
	max_event=${n_events_input}
    fi
    # check if we're processing multiple input files, or just one
    if [ ${n_files} -eq 1 ]; then
	# single input file from previous step
	input_file="${in_prefix}"
	out_file="${out_prefix}"
    else
	# multiple input files
	input_file="${in_prefix}_${min_event}-${max_event}.slcio"
	out_file="${out_prefix}_${min_event}-${max_event}"
    fi
	
    # split each file into sub-jobs
    n_tasks=$(( n_events_per_file / n_events_per_job ))
    if [ $((n_events_per_file % n_events_per_job)) != 0 ]; then
	#add additional task for the remaining
	n_tasks=$(( n_tasks + 1 ))
    fi
    for i_task in `seq 0 $((n_tasks-1))`; do
	job_n_events=${n_events_per_job}
	job_max_event=$((job_skip_events + job_n_events - 1)) #start numbering from zero
	if [ ${job_skip_events} -ge ${max_event} ]; then
	    #enough jobs scheduled, break
	    break
	elif [ ${job_max_event} -ge $((max_event)) ]; then
	    #limit max events to what available
	    job_max_event=$((max_event))
	    job_n_events=$((job_max_event - job_skip_events + 1))
	fi
		 
	echo "${worker} ${input_file} ${out_file} ${job_n_events} ${job_skip_events}"

	job_skip_events=$((job_skip_events + job_n_events))
    done
done

