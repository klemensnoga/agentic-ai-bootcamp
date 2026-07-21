#!/usr/bin/env bash
#SBATCH --job-name=llama32
#SBATCH --account=tutorial
#SBATCH --partition=tutorial
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --gres=gpu:1
#SBATCH --time=1:00:00
#SBATCH --output=nim-%j.out
#SBATCH --error=nim-%j.err

set -Eeuo pipefail

export APPTAINER_CACHEDIR=$SCRATCHDIR/apptainer_cache
export APPTAINER_TMPDIR=$SCRATCHDIR/apptainer_cache

mkdir -p $APPTAINER_CACHEDIR $APPTAINER_TMPDIR

#IMAGE_DIR="PATH_TO_IMAGE_DIRECTORY"
# Apptainer image directory on Athena cluster
IMAGE_DIR="/net/pr2/projects/tutorial/2026-07-20-nvidia-agentic-ai/"

IMAGE="${IMAGE_DIR}/llama-3.2-3b-instruct.sif"
#CACHE_DIR="PATH_TO_CACHE_DIRECTORY"
# Cache directory on Athena cluster
CACHE_DIR="${SCRATCH}/nim/cache"
mkdir -p $CACHE_DIR

# check if the NIM_API_KEY environment variable is set
if [ -z "$NIM_API_KEY" ]; then
    echo "Error: NIM_API_KEY environment variable is not set. Please set it before running this script."
    exit 1
fi

# set unique unused ports for NIM
export ipnport=$(
python << END
import socket, random, sys

while True:
    ipnport = random.randint(8000, 9999)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(('localhost', ipnport))
        print(ipnport)
        break
    except:
        print(f'Port {ipnport} not available', file=sys.stderr)
END
)
echo "Using port $ipnport for NIM HTTP API"

export APPTAINERENV_NGC_API_KEY="$NIM_API_KEY"
export APPTAINERENV_NIM_CACHE_PATH="/opt/nim/.cache"
export APPTAINERENV_NIM_HTTP_API_PORT="$ipnport"
export APPTAINERENV_TMPDIR="/tmp"

exec apptainer run --nv --writable-tmpfs \
    --bind $CACHE_DIR:$APPTAINERENV_NIM_CACHE_PATH \
    --bind $SCRATCHDIR:$APPTAINERENV_TMPDIR \
    --bind /net:/net \
    ${IMAGE}
