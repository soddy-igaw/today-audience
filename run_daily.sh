#!/bin/bash
cd /home/soddy/today-audience
export AWS_PROFILE=audmaker_soddy

# SSO 세션 확인
if ! aws sts get-caller-identity --profile audmaker_soddy > /dev/null 2>&1; then
    echo "$(date) SSO 세션 만료 — aws sso login --profile audmaker_soddy 필요" >> /home/soddy/today-audience/cron.log
    exit 1
fi

echo "$(date) 자동 발행 시작" >> /home/soddy/today-audience/cron.log
python3 daily_publish.py >> /home/soddy/today-audience/cron.log 2>&1

# git push
git add -A
git diff --staged --quiet || git commit -m "🎯 $(date +%Y-%m-%d) 오늘의 오디언스 자동 발행"
git push >> /home/soddy/today-audience/cron.log 2>&1
echo "$(date) 완료" >> /home/soddy/today-audience/cron.log
