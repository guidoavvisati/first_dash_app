# First Dash App
Replicate the dash steps from [here](https://www.rkingdc.com/blog/2019/3/6/shiny-vs-dash-a-side-by-side-comparison) and 
test deployment to google

# Deployment to Heroku
1. Setup account on Heroku and download Heroku CLI utility
2. Navigate to this folder
3. Commit this folder to Git
4. 'heroku login' and type in your credentials
5. 'heroku create -n [YOUR-APP-NAME]' where YOUR-APP-NAME refers to the title of your Dash app
6. 'heroku git:remote -a [YOUR-APP-NAME]'.
7. 'git push heroku master' will deploy your app to Heroku
8. 'heroku ps:scale web=1' will create a Dyno and make your app live