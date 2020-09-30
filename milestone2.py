import tweepy,os,random,flask,requests,json;from tweepy import OAuthHandler;from tweepy import Cursor;from os.path import join, dirname; from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), 'tweepy & spoonacular.env')
load_dotenv(dotenv_path)

API_KEY = os.environ['API_KEY']
API_secret_KEY = os.environ['API_secret_KEY']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']
spoonacular_key = os.environ['SPOONACULAR_KEY']

auth = OAuthHandler(API_KEY, API_secret_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


app = flask.Flask(__name__)
@app.route("/")  # we ll use the default page
def index():
    fList = ['pizza','cookies','tacos','steak','eggs','bread','jelly','rice','salmon','apple pie','ice cream','pork']
    food_item = random.choice(fList);
    #<---------------------------------------------->
    url = "https://api.spoonacular.com/recipes/complexSearch?query={}&apiKey={}".format(food_item,spoonacular_key)
    jsonBodyResp = requests.get(url).json()
    ID    = json.dumps(jsonBodyResp["results"][0]["id"], indent = 2)
    title = json.dumps(jsonBodyResp["results"][0]["title"], indent=2).replace('\"',"")
    image = json.dumps(jsonBodyResp["results"][0]["image"], indent=2).replace('\"',"")

    #<---------------------------------------------->
    url = "https://api.spoonacular.com/recipes/search?query={}&apiKey={}".format(food_item,spoonacular_key)
    jsonBodyResp = requests.get(url).json()
    srcur = json.dumps(jsonBodyResp["results"][0]["sourceUrl"], indent=2).replace('\"',"")

    #<---------------------------------------------->
    url = "https://api.spoonacular.com/recipes/{}/ingredientWidget.json?apiKey={}".format(ID, spoonacular_key)
    jsonBodyResp = requests.get(url).json()
    LenOF_i_List = len(jsonBodyResp["ingredients"])
    ingredientsList = []
    for i in range(LenOF_i_List):
        in_item = json.dumps(jsonBodyResp["ingredients"][i]['name'], indent = 2).replace('\"',"")
        ingredientsList.append(in_item)
    #<---------------------------------------------->
    searchObjec = api.search(food_item)
    tweet = searchObjec[0].text
    tweetCreationTime = searchObjec[0].created_at
    AutherName = searchObjec[0].author.screen_name

    # title="Oreo Cookies & Cream No-Bake Cheesecake"
    # image="https://spoonacular.com/recipeImages/658277-312x231.jpg"
    image2="https://media.vanityfair.com/photos/5ef25d9d184617200a49bac5/master/w_2560%2Cc_limit/M8DBATM_WB002.jpg"
    
    # srcur="https://www.pinkwhen.com/oreo-cookie-balls-thanksgiving-turkey/"
    # ingredientsList=['cream cheese', 'heavy cream', 'lemon juice', 'oreo cookies', 'salt', 'sugar', 'vanilla powder']
    # tweet="RT @DaniBordas: Hay que leerse bien las cookies, que lo mismo ahí es donde votamos al rey."
    # tweetCreationTime="2020-09-29 21:33:44"
    # AutherName="Viirginia_bt"
    
    return flask.render_template("home.html", tw = tweet,tc = tweetCreationTime,an = AutherName,ing = ingredientsList, sWB = srcur, img2 = image2, img = image, title =title)
app.run(port=int(os.getenv("port",8080)), host=os.getenv("IP","0.0.0.0"), debug=True)