# MongoDB
## Install
``` title="/etc/yum.repos.d/mongodb-org-7.0.repo"
[mongodb-org-7.0]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/amazon/2023/mongodb-org/7.0/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://pgp.mongodb.com/server-7.0.asc
```
``` bash
sudo yum install -y mongodb-mongosh-shared-openssl3
```
## Connect
Please note that you need to set the ENDPOINT_URL variable.
``` bash
mongosh --ssl --host $ENDPOINT_URL --sslCAFile global-bundle.pem --username mongo --password mongopass!
```
## Database
``` bash
use school
db.dropDatabase()
```
## Collection
``` bash
db.createCollection("students")

# maximum size 10MB, no more than 100 documents
db.createCollection("teachers", {capped: true, size: 10000000, max: 100})
```
## Insert
``` bash
db.students.insertOne({
    name: "Larry", 
    age: 32, 
    gpa: 2.8, 
    fullTime: false, dddddddddddd
    registerDate: new Date(), 
    graduationDate: null, 
    courses: ["Biology", "Chemistry", "Calculus"], 
    address: {street: "123 Fake St.", city: "Bikini Bottom", zip: 12345}
})

db.students.insertMany([
    {name: "Patrick", age: 38, gpa: 1.5}, 
    {name: "Sandy", age: 27, gpa: 4.0}, 
    {name: "Gary", age: 18, gpa: 2.5}
])
```
## Find
``` bash
db.students.find({gpa: 4.0}, {_id: false, name: true})  # (Query, Projection)
db.students.find({name: {$ne: "Spongebob"}})    # Not Equal

db.students.find({age: {$lt: 27}})  # less than
db.students.find({age: {$lte: 27}}) # less than or equal
db.students.find({age: {$gt: 27}})  # greater than
db.students.find({age: {$gte: 27}}) # greater than or equal

db.students.find({name: {$in: ["Spongebob", "Patrick", "Sandy"]}})  # in
db.students.find({name: {$nin: ["Spongebob", "Patrick", "Sandy"]}}) # not in

db.students.find({$and: [{fullTime: true}, {age: {$lt: 27}}]})  # True & True -> True
db.students.find({$or: [{fullTime: true}, {age: {$lte: 22}}]})  # True & False -> True
db.students.find({$nor: [{fullTime: true}, {age: {$lte: 22}}]}) # False & False -> True
db.students.find({age: {$not: {$gte: 30}}}) # not

db.students.find().sort({gpa: 1})  # 1 -> ASC, -1 -> DESC
db.students.find().limit(5)
```
## Update
``` bash
# (Filter, Update)
db.students.updateOne({_id: ObjectId('65f419c70457b0bd5d9ce3f2')}, {$set: {fullTime: true}})
db.students.updateMany({fullTime: {$exists: false}}, {$set: {fullTime: true}})
```
## Delete
``` bash
db.students.deleteOne({_id: ObjectId('65f423ea08740278768bf208')})
db.students.deleteMany({registerDate: {$exists: false}})
```
## Index
``` bash
db.students.createIndex({name: 1})
db.students.getIndexes()
db.students.dropIndex("name_1")
```