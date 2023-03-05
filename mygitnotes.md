# I created a repo called freecertitty on github.com
# I had a private key ~/id_rsa so created a public key
# ssh-keygen -f id_rsa -y
# and added it to github 
rm -rf .git
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin git@github.com:bradymd/freecertiffy.git
git push -u origin main
git status
