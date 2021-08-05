
### Content model
class ContentDto:
    def __init__(self, owner_id, title, author, url, img_url, pub_date):
        self.owner_id = owner_id
        self.title = title
        self.author = author
        self.url = url
        self.img_url = img_url
        self.pub_date = pub_date

### Content model
class OwnerDto:
    def __init__(self, name, url):
        self.name = name
        self.url = url