# ./scripts/gen_workflow.sh

TASK_ID=$1
PHASE=$2

cat > .cline/aceflow.workflow.json <<EOF
{
  "name": "ACEFLOW CLI Agent",
  "description": "Auto-generated workflow for $TASK_ID / $PHASE",
  "entry": "bash aceflow/scripts/cli_run.sh",
  "arguments": ["$TASK_ID", "$PHASE"],
  "pre_hooks": [
    "python aceflow/tools/state_lock.py --lock $TASK_ID",
    "python aceflow/tools/context_mount.py --task $TASK_ID",
    "python aceflow/tools/phase_validator.py --task $TASK_ID --phase $PHASE",
    "python aceflow/tools/flow_sentinel.py --phase $PHASE --task $TASK_ID"
  ],
  "post_hooks": [
    "python aceflow/tools/state_lock.py --unlock $TASK_ID"
  ]
}
EOF
