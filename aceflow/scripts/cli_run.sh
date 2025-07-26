#!/bin/bash
TASK_ID=$1
PHASE=$2

python aceflow/tools/state_lock.py --lock $TASK_ID
python aceflow/tools/context_mount.py --task $TASK_ID
python aceflow/tools/phase_validator.py --task $TASK_ID --phase $PHASE
python aceflow/tools/flow_sentinel.py --phase $PHASE --task $TASK_ID
echo "🚀 执行 cline run --task $TASK_ID --phase $PHASE"
python aceflow/tools/state_lock.py --unlock $TASK_ID
