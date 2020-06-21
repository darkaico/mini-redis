# Rest API

By starting mini redis server we will able to interact with REST API for our mini redis implementation.

## Set Key

Set a value for a certain key

**URL** : `/api/store/:key`

**URL Parameters** : `key=[str]` where `key` is the key in where we want to store a value

**Method** : `PUT`

**Data constraints**

```json
{
  "value": "can only be the characters from the set [a-zA-Z0-9-_]."
}
```

### Success Response

**Code** : `200 OK`

**Content examples**

```json
"OK"
```

## Get Key

Get the key value

**URL** : `/api/store/:key`

**URL Parameters** : `key=[str]` where `key` is the key for we want to retrieve data

**Method** : `GET`

### Success Response

**Code** : `200 OK`

### Success Response

**Code** : `200 OK`

**Content examples**

#### Key exists

```json
"<key content>"
```

#### Key does not exists

```json
"nil"
```

## Delete Key

Delete a key

**URL** : `/api/store/:key`

**URL Parameters** : `key=[str]` where `key` is the key we want to delete

**Method** : `DELETE`

### Success Response

**Code** : `200 OK`

**Content examples**

#### Key exists

```json
"OK"
```

#### Key does not exists

```json
"nil"
```

## INCR Key

Increments the number stored at key by one

**URL** : `/api/store/:key/incr`

**URL Parameters** : `key=[str]` where `key` is the key we want to delete

**Method** : `PUT`

### Success Response

**Code** : `200 OK`

### Request Error Response

**Code** : `400 OK`

**Content examples**

#### Key exists

```json
"OK"
```

#### Key does not exists

```json
"nil"
```

#### Key does not exists

```json
"nil"
```

## ZADD Key

Adds all the specified members with the specified scores to the sorted set stored at key

**URL** : `/api/store/:key/zadd`

**URL Parameters** : `key=[str]` where `key` is the key we want to delete

**Method** : `PUT`

**Data constraints**

```json
{
  "score": "string representation of a double precision floating point number",
  "member": "member to use"
}
```

### Success Response

**Code** : `200 OK`

### Request Error Response

**Code** : `400 OK`

**Content examples**

#### Key exists

```json
"OK"
```

#### Key does not exists

```json
"nil"
```

#### Key does not exists

```json
"nil"
```

## ZCARD Key

Returns the sorted set cardinality (number of elements) of the sorted set stored at key

**URL** : `/api/store/:key/zcard`

**URL Parameters** : `key=[str]` where `key` is the key for we want to retrieve data

**Method** : `GET`

### Success Response

**Code** : `200 OK`

### Success Response

**Code** : `200 OK`

**Content examples**

#### Key exists

```json
"integer"
```

#### Key does not exists

```json
"nil"
```

## ZRANK Key

Returns the rank of member in the sorted set stored at key

**URL** : `/api/store/:key/zrank`

**URL Parameters** : `key=[str]` where `key` is the key for we want to retrieve data

**Method** : `GET`

### Success Response

**Code** : `200 OK`

### Success Response

**Code** : `200 OK`

**Content examples**

#### Key exists

```json
"integer"
```

#### Key does not exists

```json
"nil"
```

## ZRANGE Key

Returns the specified range of elements in the sorted set stored at key

**URL** : `/api/store/:key/zrange`

**URL Parameters** : `key=[str]` where `key` is the key for we want to retrieve data

**QUERY Parameters** : `start=[int]` and `stop=[int]`

**Method** : `GET`

### Success Response

**Code** : `200 OK`

### Success Response

**Code** : `200 OK`

**Content examples**

#### Key exists

```json
["Wolverine", "Guepardo"]
```

#### Key does not exists

```json
"nil"
```

## DBSIZE Key

Return the number of keys in the currently-selected database.

**URL** : `/api/dbsize`

**Method** : `GET`

### Success Response

**Code** : `200 OK`

### Success Response

**Code** : `200 OK`

**Content examples**

```json
"integer"
```
