#!/bin/bash
# 매일 오전 10시 자동 실행 (crontab -e 에서 등록)
# 0 10 * * * /home/soddy/today-audience/daily_update.sh

cd /home/soddy/today-audience

# 1. 트렌드 수집
python3 trend_collector.py --all

# 2. git push (변경사항 있으면)
git add -A
git commit -m "$(date +%Y-%m-%d) 트렌드 리포트 자동 업데이트" 2>/dev/null
git push 2>/dev/null

echo "✅ $(date) 트렌드 수집 완료"
