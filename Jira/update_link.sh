SORCE_PATH=/d/work_platform/Github/Amt_work_platform/Jira/chart_link.txt
DEST_PATH=/d/work_platform/Github/Amt_work_platform/Jira/chart_link_open.sh

grep "^.*start" $SORCE_PATH | sed 's/^.*start/start/g' > $DEST_PATH

