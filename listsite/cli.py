# List manager API
import httplib2
import json
import re
import functools

base_url = "http://localhost:5000"
http = httplib2.Http()
add_regex = re.compile("^.*?\\s\"(.+)\"\\s*$")


# Creates a new list through the /newlist endpoint, then prints its id
def new_list(listid, user_input):
    url = base_url + "/newlist"
    resp, content = http.request(url, 'POST')
    parsed = json.loads(content)
    listid = parsed['list_id']
    print("New list created with id " + listid)
    return listid


# Validates and sets the list
def set_list(curr, userinput):
    if len(userinput) != 2:
        print("Usage: set <new list id>")
        return curr
    elif len(userinput[1]) != 6:
        print("List id must be of size 6")
        return curr
    else:
        url = base_url + "/validatelist"
        body = json.dumps({"list_id": userinput[1]})
        resp, content = http.request(url, "POST", body,  headers={'content-type': 'application/json'})
        parsed = json.loads(content)
        if parsed["exists"]:
            print("List switched to " + userinput[1])
            return userinput[1]
        else:
            print("List doesn't exist")
            return curr


def curr_list(curr, userinput):
    print(curr)


def add_item(curr, userinput):
    if len(userinput) < 2:
        print("Usage: add \"<item to add to curr list>\"")
        return curr
    else:
        body = extract_item(curr, userinput)
        if body:
            url = base_url + "/additem"
            res, content = http.request(url, "POST", json.dumps(body), headers={'content-type': 'application/json'})
            print(body["item"] + " has been added to List " + curr)
            return curr
        else:
            print("Usage: add \"<item to add to curr list>\"")
            return curr


def get_items(curr, userinput):
    url = base_url + "/viewlist"
    body = {"list_id": curr}
    res, content = http.request(url, "POST", json.dumps(body), headers={'content-type': 'application/json'})
    items = json.loads(content)["list_items"]
    if len(items) == 0:
        print("List is empty")
    elif len(items) == 1:
        print(items[0]["item"])
    else:
        toprint = functools.reduce(lambda x, y: x["item"] + "\n" + y["item"], items)
        print(toprint)
    return curr


def remove_item(curr, userinput):
    if len(userinput) < 2:
        print("Usage: add \"<item to remove from curr list>\"")
        return curr
    else:
        body = extract_item(curr, userinput)
        if body:
            url = base_url + "/deleteitem"
            res, content = http.request(url, "POST", json.dumps(body), headers={'content-type': 'application/json'})
            print(body["item"] + " has been removed from List " + curr)
            return curr
        else:
            print("Usage: add \"<item to remove from curr list>\"")
            return curr


def clear_list(curr, userinput):
    url = base_url + "/clearlist"
    res, content = http.request(url, "GET", json.dumps({"list_id": curr}), headers={'content-type': 'application/json'})
    print("List " + curr + " has been cleared")
    return curr

# helper
def extract_item(curr, userinput):
    raw_input = functools.reduce(lambda x, y: x + " " + y, userinput)
    item_match = add_regex.match(raw_input)
    if item_match:
        item = item_match.group(1)
        return {
            "list_id": curr,
            "item": item,
        }
    else:
        return None


# Register new commands here. Commands are functions that take in two arguments: the current list ID
# and a whitespace separated list of user input. Commands must return the current list id
input_map = {
    "new": new_list,
    "curr": curr_list,
    "set": set_list,
    "add": add_item,
    "list": get_items,
    "remove": remove_item,
    "clear": clear_list
}

if __name__ == "__main__":
    print("Welcome to the CLI")
    curr_id = ""
    while True:
        user_input = input("").split(" ")
        if user_input[0] in input_map:
            curr_id = input_map[user_input[0]](curr_id, user_input)
        else:
            print("Command not recognized")


