cp nohup.out logs/nohup-"`date +"%Y-%m-%d"`".out
rm nohup.out
git pull origin master
pip3 install -r requirements.txt
cd Nano/
env BOT_TOKEN=$BOT_TOKEN DEVELOPER_KEY=$DEVELOPER_KEY  REDDIT_CLIENT_ID=$REDDIT_CLIENT_ID REDDIT_CLIENT_SECRET=$REDDIT_CLIENT_SECRET REDDIT_USER_AGENT='$REDDIT_USER_AGENT' nohup python3.6 -u main.py &
