import {backendLookup} from '../lookup'

export function apiTweetCreate(newTweet, callback){
    backendLookup("GET", "/tweets/create", callback, {content:newTweet})
}


export function apiTweetList(callback) {
    backendLookup("GET", "/tweets/", callback)
}