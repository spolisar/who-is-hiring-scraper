import http.client
import json

# tools built to assist in scraping data from hackernews for building data files from whoishiring threads
# written for v0 of Hacker News api


class HNUser:
    def __init__(self, about, created, karma, submitted):
        self.about = about
        # creation date in unix time
        self.created = created
        self.karma = karma
        #submitted posts
        self.submitted = submitted
    
    def __iter__(self):
        yield from {
            "about": self.about,
            "created": self.created,
            "karma": self.karma,
            "submitted": self.submitted
        }.items()
    
    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)

    def to_json(self):
        return json.dumps(dict(self), ensure_ascii=False)
    
    @staticmethod
    def from_json(json_dct):
        return HNUser(json_dct['about'], json_dct['created'], json_dct['karma'], json_dct['submitted'])

#may want to add subtypes for different item models e.g. base, job, story, etc.
class HNItem:
    def __init__(self, by, descendants, itemId, kids, score, text, time, title, itemType):
        self.by = by
        #number of descendants
        self.descendants = descendants
        self.id = itemId
        #direct children
        self.kids = kids
        self.score = score
        self.text = text
        self.time = time
        self.title = title
        self.type = itemType
    
    def __iter__(self):
        yield from {
            "by": self.by,
            "descendants": self.descendants,
            "id": self.id,
            "kids": self.kids,
            "score": self.score,
            "text": self.text,
            "time": self.time,
            "title": self.title,
            "type": self.type
        }.items()
    
    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)
    
    def to_json(self):
        return json.dumps(dict(self), ensure_ascii=False)
    
    @staticmethod
    def from_json(json_dct):
        by = json_dct['by']
        descendants = json_dct['descendants']
        itemId = json_dct['id']
        kids = json_dct['kids']
        score = json_dct['score']
        text = json_dct['text']
        time = json_dct['time']
        title = json_dct['title']
        itemType = json_dct['type']

        return HNItem(by, descendants, itemId, kids, score, text, time, title, itemType)


def getUser(userId):
    conn = http.client.HTTPSConnection("hacker-news.firebaseio.com")

    payload = "{}"

    userRequest = "/v0/user/{userId}.json"
    conn.request("GET", userRequest.format(userId=userId), payload)

    res = conn.getresponse()
    # typeof data is 'bytes'
    data = res.read()

    jsonStr = data.decode('utf8')
    user = json.loads(jsonStr, object_hook=HNUser.from_json)

    return user

# made to be a parallel to https://hackernews.api-docs.io/v0/items/get-by-id    
def getItem(itemId):
    conn = http.client.HTTPSConnection("hacker-news.firebaseio.com")

    payload = "{}"

    itemRequest = "/v0/item/{itemId}.json"
    conn.request("GET", itemRequest.format(itemId=itemId), payload)

    res = conn.getresponse()
    data = res.read()
    jsonStr = data.decode('utf8')

    item = json.loads(jsonStr, object_hook=HNItem.from_json)

    return item



def main():
    userId = "whoishiring"
    user = getUser(userId)
    itemId = user.submitted[0]
    thread = getItem(itemId)
    print(thread)

    
    

if __name__ == "__main__":
    main()