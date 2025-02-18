#!/bin/bash

# צבעים להדפסה
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "🔍 בודק את המערכת לפני commit..."

# הרצת בדיקת המערכת
python3 debug_tool.py
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ נכשל בבדיקת המערכת${NC}"
    exit 1
fi

# בדיקת קבצים לא רצויים
echo "🧹 מנקה קבצים זמניים..."
find . -type f -name "*.pyc" -delete
find . -type d -name "__pycache__" -exec rm -r {} +
find . -type d -name "node_modules" -prune -o -type f -name ".DS_Store" -delete

# בדיקת פורמט קוד
echo "📝 בודק פורמט קוד..."
if command -v black &> /dev/null; then
    black backend/
fi

# הכנת רשימת קבצים לcommit
echo -e "${YELLOW}📋 קבצים שישתתפו ב-commit:${NC}"
git status

# שאלה לפני commit
read -p "האם להמשיך עם commit? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    # קבלת הודעת commit
    echo -e "${YELLOW}הכנס הודעת commit:${NC}"
    read commit_message
    
    # ביצוע commit
    git add .
    git commit -m "$commit_message"
    
    echo -e "${GREEN}✅ Commit בוצע בהצלחה${NC}"
    
    # שאלה לגבי push
    read -p "האם לבצע push? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        git push
        echo -e "${GREEN}✅ Push בוצע בהצלחה${NC}"
    fi
else
    echo -e "${YELLOW}⏸️  Commit בוטל${NC}"
fi
