# Workshop 3 - MongoDB with Python

## Prerequisites

First of all, you need to install MongoDB and get it running. How to do that depends on your operating system. If you have any issues, please don't hesistate to reach out.

### Installing MongoDB - MacOS

[Official Instructions](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/)

It's easiest to install MongoDB Community Edition using [brew](https://brew.sh/).

### Installing MongoDB - Windows

It takes some extra work to get MongoDB running on Windows. If you have trouble using this official method, check out Docker below.

[Official Instructions](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/)

### Installing Using Docker

If you have trouble installing MongoDB Community Edition with the above instructions, I recommend you try using [Docker](https://docs.docker.com/get-docker/) + [Kitematic](https://kitematic.com/).

Docker allows you to create "containers" that can run instances of programs. You can download a MongoDB image and run/manage it through Docker. Kitematic is a user interface for Docker. This setup requires a few more steps, but if you're not comfortable using the Terminal, then this is the optimal situation.

Steps

1) Install Docker
2) Install Kitematic
3) Run Docker, run Kitematic
4) Install the MongoDB image using Kitematic
5) Run MongoDB by clicking 'start'

## Database Tab - PyCharm

The Database tab is near the right hand side corner. It's listed vertically, with the  icon, right under the 'search' icon.

![](https://i.imgur.com/thIG6HX.png)

We can use this interface to examine what data is in our database.

Once you have it installed, you can view your MongoDB databases by clicking the plus sign and selecting MongoDB as the data source.

![](https://imgur.com/pVy5pFT.png)

Once you've added MongoDB, right click on 'MongoDB' to select your databases. You should get an interface like this.

NOTE: ONLY DATABASES WITH SAVED ITEMS WILL SHOW. Just connecting will not create a database, you also need to save an item to the database.

![](https://imgur.com/vx91y8f.png)

Double-clicking on a collection will bring up the center panel, which displays all the saved items in that collection. 

## MongoEngine

In this application, we will be using [MongoEngine](https://docs.mongoengine.org/) to connect to MongoDB through Python. MongoEngine also provides us with a library to save and query data to the database.

## Connecting to DB

Connecting to our DB is easy. If you've followed the default configuration, the code below should be enough (main.py)
```
connect('workshop3')
```
All of our new items will be saved to the 'workshop3' database. If you aren't using the default ports, you can do the following to pass in a configuration
```
connect('project1', host='192.168.1.35', port=12345)
```

## Question v. QuestionDocument

You'll notice we've created a new class, QuestionDocument.

```
class QuestionDocument(Document):
    question_text = StringField(max_length=200, required=True)
    replies = ListField(field=StringField())
    num_replies = IntField()
```

The class takes a Document argument from MongoEngine, allowing us to use this class as a model for our Question document in the database. We can also use some items from MongoEngine to create some rules about our model properties.

However, we still want to keep our Question class because it has some logic attached to it. You can combine them, but I find this a bit cleaner.

So basically, we use QuestionDocument whenever we want to save and read to the database. We use the old Question class (and need to convert between the two) whenever we want to do some application logic.

## Creating, Saving Documents
```
question_doc = QuestionDocument(question_text=new_question.question_text,
                                replies=new_question.replies,
                                num_replies=new_question.get_num_replies())
question_doc.save()
```
If we've created a class that takes a Document as a parameter, it gains the .save() method. Invoking .save() will create a collection of the same name as the class and save that object to that collection.

For example, question_document.save() will find the QuestionDocument class, if no existing collection exists, create a collection called question_document (MongoEngine does its own formatting) according to the fields we've defined. 

NOTE: MongoDB creates an id field called _id when a new document is added. You can access with the 'pk' property on any class that is compatible

E.g. QuestionDocumentObject.pk

## Querying

You'll get a list of all the items in the question_document collection with 
```
questions = QuestionDocument.objects
```
To query this list, you can use objects in this way (find objects with more than 1 reply)
```
active_questions = QuestionDocument.objects(num_replies__gte=1)
```

More information on how to query using MongoEngine can be found [here.](https://docs.mongoengine.org/guide/querying.html#filtering-queries)

You can also add [custom methods with pre-written filters.](https://docs.mongoengine.org/guide/querying.html#default-document-queries)

## Updating

You can either use save again, as so
```
the_doc = QuestionDocument.objects(id=new_question.primary_key).first()
# objects returns a list, first() returns the first result

the_doc.replies = new_question.replies
the_doc.save()
```
Or invoke an update function in a query
```
QuestionDocument.objects(id=new_question.primary_key).update_one(replies=new_question.replies)
```