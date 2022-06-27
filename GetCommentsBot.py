import mysql.connector
import requests
import re



channelId = []
userId = []
videoId = []
date ="empty"


videoName = []
videoDate = []

channelName = []
channelDate = []

deliverChannel = []


def getId(cusId):
    mydb = mysql.connector.connect(
        host="192.168.10.251",
        user="portal_master",
        password="vahh9Ugh2eiCh8",
        database="portal_master"
    )

    mycursor = mydb.cursor()

    mycursor.execute(
        "SELECT * FROM portal_master.YouTubeRules WHERE datastream_id="+str(cusId)+";")

    myresult = mycursor.fetchall()


    for x in range(len(myresult)):
        if "user" in myresult[x][3]:
            userId.append(myresult[x][3].split("/")[-1])
        if "watch" in myresult[x][3]:
            videoId.append(myresult[x][3].split("=")[-1])
        if "channel" in myresult[x][3]:
            channelId.append(myresult[x][3].split("/")[-1])

    channelInfoDeliver = getChannelInfo(channelId)
    videoInfoDeliver = getVideoInfo(videoId)


def getChannelInfo(channelIdRx):
    fileAppend = open("channelLatest.csv", "w")
    fileAppend.write('Channel Id , Channel Name , Video Name , Last Published Video')

    for x in range(len(channelIdRx)):

        apiUrl = "https://api.boardreader.com/v1/Video/Search?key=asdfg_bcc3aa752a1d295ece64453b4d&rt=xml&body=snippet&highlight=1&dn=youtube.com&video_comments=on&filter_username="+str(channelIdRx[x])+"&filter_date_from=0&sort_mode=time_desc&limit=10&offset=0&mode=full"

        response = requests.get(apiUrl)

        try:
            date = re.search('<Published>(.+?)</Published>', response.text).group(1)
            videoName = re.search('<VideoTitle>(.+?)</VideoTitle>',response.text).group(1)
            channelName = re.search(
                '<Name>(.+?)</Name>', response.text).group(1)
        
        except:
            date = "No Video"
        
        fileAppend.write(str("\n"+str(channelIdRx[x])+" , "+str(channelName)+" , "+str(videoName)+" , "+str(date)))

def getVideoInfo(videoId):
    fileAppend2 = open("videoLatest.csv", "w")
    fileAppend2.write('Video Id , Latest Comment , Published Date')
    for x in range(len(videoId)):
        apiUrl = "https://api.boardreader.com/v1/Video/Search?key=asdfg_bcc3aa752a1d295ece64453b4d&filter_thread=yt."+videoId[x]+"&rt=xml&body=both&video_comments=on&filter_inserted_from=0&limit=10&offset=0&mode=full&sort_mode=time_desc"
        response = requests.get(apiUrl)

        try:
            date = re.search('<Published>(.+?)</Published>',
                                response.text).group(1)
            comment = re.search('<VideoTitle>(.+?)</VideoTitle>',
                                response.text).group(1)

        except:
            date = "No Comments"
        
        fileAppend2.write("\n"+str(videoId[x])+" , "+str(comment)+" , "+str(date))

        print(videoId[x])



if __name__ == "__main__":
    getId(1712)


