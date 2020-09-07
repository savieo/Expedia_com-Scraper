import requests
import csv
from json import loads
from redis import StrictRedis
redis = StrictRedis('172.16.253.235',db=13)

EMAIL_BACKEND = 'django_mailgun.MailgunBackend'
MAILGUN_ACCESS_KEY = 'key-7fd1d3446f980023ef36c4aab0609ebc'
MAILGUN_SERVER_NAME = 'in.scrapehero.com'


def send_mail_using_mailgun(send_from, send_to, subject, text, files, server="smtp.gmail.com", port=587, username='', password='', isTls=True):
	return requests.post(
		"https://api.mailgun.net/v3/in.scrapehero.com/messages",
		auth=("api", MAILGUN_ACCESS_KEY),
		data={"from": "data@scrapehero.com",
		      "to":["jasoneaton@bransontourismcenter.com"],
			  # "to":["savieo@scrapehero.com","satheesh@scrapehero.com","nagaraj.p@scrapehero.com"],
			  "bcc": ["savieo@scrapehero.com","satheesh@scrapehero.com","nagaraj.p@scrapehero.com"],
			  "subject": "Daily Data",
			  "text":text ,
			  "html": "<html>"+text+"</html>"})

def process(run):
	owncloud_links = {}
	owncloud_data = redis.lrange('2363_Data',0,-1)
	for i in owncloud_data:
		link = loads(i)
		site = list(link.keys())[0]
		oclink = list(link.values())[0]
		if site not in owncloud_links.keys():
			owncloud_links[site] = oclink

	redis.delete('2363_Data')
	text12 = "The links sent in this email and associated data are deleted within 2 weeks from the time this email is sent, please download the data to your own computers to save it."
	text = "Here is the data for today :" +'<br><br>'+"Expedia : "+owncloud_links['expedia']+'<br>'+"Radisson : "+owncloud_links['radisson']+'<br><br>'+text12+'<br>'+'<br>'+"Thanks"

	send_mail_using_mailgun('savieo@scrapehero.com',['savieoseb@gmail.com'],'test mail',text,[])

	url = 'https://chat.turbolab.in/hooks/iq4pkouqqpgf5qe4tpfdiwp6cr'
	text = "@savieo @nagaraj @satheesh mail has been sent to customer via mail. Check your mail for data."
	icon_url = ""
	spidername = "2363_Data"
	payload = '{"text":"' + text + '","username":"' + str(spidername) + '","icon_url":"' + icon_url + '"}'
	requests.post(url,data=payload)
