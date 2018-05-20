# -*- coding:utf-8 -*-
from pymongo import MongoClient
import pprint

# setting for mongoDB
client = MongoClient('localhost', 27017)
db = client.importnewDb
posts = db.importnewPosts
wechats = db.wechatPosts
recentPostsNP = db.recentPostsNP
oldHotPostsNP = db.oldHotPostsNP
oldLessHotPostsNP = db.oldLessHotPostsNP

pipeline_recent_posts_nonpublished = [
	{
		"$match": { 
			"date": {"$gte": 20180401}
		}

	},
	{
		"$lookup": {
			"from": "wechatPosts",
			"localField": "title",
			"foreignField": "title",
			"as": "matched_docs"
		}
	},
	{
		"$match": { 
			"matched_docs": { "$eq": [] }
		}
	}

]

pipeline_old_hot_posts_nonpublished = [
	{
		"$match": { 
			"date": {"$lt": 20180401, "$gte": 20170508},
			"view": {"$gte": 5000}
		}

	},
	{
		"$lookup": {
			"from": "wechatPosts",
			"localField": "title",
			"foreignField": "title",
			"as": "matched_docs"
		}
	},
	{
		"$match": { 
			"matched_docs": { "$eq": [] }
		}
	}
]

pipeline_old_less_hot_posts_nonpublished = [
	{
		"$match": { 
			"date": {"$lt": 20180401, "$gte": 20170508},
			"view": {"$lt": 5000}
		}

	},
	{
		"$lookup": {
			"from": "wechatPosts",
			"localField": "title",
			"foreignField": "title",
			"as": "matched_docs"
		}
	},
	{
		"$match": { 
			"matched_docs": { "$eq": [] }
		}
	}
]

# recent posts newer within 1 month
# and not ever published
recent_posts_nonpublished = posts.aggregate(pipeline_recent_posts_nonpublished)
#pprint.pprint(list(recent_posts_nonpublished))
recentPostsNP.remove()
recentPostsNP.insert_many(recent_posts_nonpublished)

# not recent posts older than 1 month but within 1 year
# view > 5000
# and not ever published
old_hot_posts_nonpublished = posts.aggregate(pipeline_old_hot_posts_nonpublished)
#pprint.pprint(list(old_hot_posts_nonpublished))
oldHotPostsNP.remove()
oldHotPostsNP.insert_many(old_hot_posts_nonpublished)

# not recent posts older than 1 month but within 1 year
# view < 5000 
# and not ever published
old_less_hot_posts_nonpublished = posts.aggregate(pipeline_old_less_hot_posts_nonpublished)
#pprint.pprint(list(old_less_hot_posts_nonpublished))
oldLessHotPostsNP.remove()
oldLessHotPostsNP.insert_many(old_less_hot_posts_nonpublished)
