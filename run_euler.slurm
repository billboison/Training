#!/bin/bash
#SBATCH --job-name=euler_ode
#SBATCH --output=euler_%A_%a.out
#SBATCH --error=euler_%A_%a.err
#SBATCH --array=0-6
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=256M
#SBATCH --time=00:10:00

Z=$SLURM_ARRAY_TASK_ID

read DT NSTEPS <<< $(python3 -c "
import math
z = int('$Z')
dt = 10**(-z)
nsteps = math.ceil(9.0 / dt)
print(dt, nsteps)
")

RUNDIR="$HOME/training/data/run_z${Z}"
mkdir -p "$RUNDIR"

cat > "$RUNDIR/params.dat" <<EOF
dt     $DT
nsteps $NSTEPS
EOF

cd "$RUNDIR"
"$HOME/training/bin/euler"
