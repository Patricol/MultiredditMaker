import praw

from time import sleep

COMBO_PREFIX = "combo"

def multireddit_is_combo(multireddit_name):
    return type(multireddit_name) is str and multireddit_name.startswith(COMBO_PREFIX) and multireddit_name[len(COMBO_PREFIX):].isdecimal()

def chunks(list_of_stuff, chunk_size):
    chunk_size = max(1, chunk_size)
    return list(list_of_stuff[i:i+chunk_size] for i in range(0, len(list_of_stuff), chunk_size))

def chunk_into_hundreds(list_of_stuff):
    return chunks(list_of_stuff, 100)

def getSubs(subreddit):
    return r.subreddit(subreddit).subscribers

def get_subscribed_subreddits():
    return [subreddit.display_name for subreddit in r.user.subreddits(limit=1000)]

def get_multireddit_names():
    return [multireddit.display_name for multireddit in r.user.multireddits()]

def sort_by_subs(subreddit_list):
    sub_name_tuples = []
    for subreddit in subreddit_list:
        sub_name_tuples.append(tuple([getSubs(subreddit), subreddit]))
    sorted_tuples = list(reversed(sorted(sub_name_tuples)))
    return [pair[1] for pair in sorted_tuples]

def setout(set_to_convert):
    return sorted(list(set_to_convert), key=lambda s: s.casefold())

def setdiff(list1, list2):
    return setout(set(list1) - set(list2))

def get_subs_in_combo_multireddit():
    subs_in_combo_multireddits = set()
    for multireddit in r.user.multireddits():
        if multireddit_is_combo(multireddit.display_name):
            for subreddit in multireddit.subreddits:
                subs_in_combo_multireddits.add(subreddit.display_name)
    return setout(subs_in_combo_multireddits)

def get_subs_in_non_combo_multireddit():
    subs_in_non_combo_multireddits = set()
    for multireddit in r.user.multireddits():
        if not multireddit_is_combo(multireddit.display_name):
            for subreddit in multireddit.subreddits:
                subs_in_non_combo_multireddits.add(subreddit.display_name)
    return setout(subs_in_non_combo_multireddits)

def get_subs_only_in_combo_multireddit():
    return setdiff(get_subs_in_combo_multireddit(), get_subs_in_non_combo_multireddit())

def delete_combo_multireddits():
    warn_lost_subs = setdiff(get_subs_only_in_combo_multireddit(), get_subscribed_subreddits())
    if warn_lost_subs:
        print("These subreddits are in existing combo multireddits, but are in no other multireddits and are not subscribed to.")
        print("They may be 'lost' through this process.")
        print(warn_lost_subs)

    existing_combo_multireddits = [multireddit for multireddit in r.user.multireddits() if multireddit_is_combo(multireddit.display_name)]
    for existing_combo_multireddit in existing_combo_multireddits:
        existing_combo_multireddit.delete()

def reset_combo_multireddits():
    print("Deleting any existing combo multireddits...")
    delete_combo_multireddits()
    print("Getting subscribed subreddits...")
    subscribed = get_subscribed_subreddits()
    print("Sorting by number of subscribers...")
    subscribed_sorted_by_subs = sort_by_subs(subscribed)
    print("Chunking into hundreds...")
    new_combo_multireddits = chunk_into_hundreds(subscribed_sorted_by_subs)
    print("Creating multireddits...")
    for i in range(len(new_combo_multireddits)):
        name = COMBO_PREFIX + "{}".format(i+1)
        print(" Creating {}...".format(name))
        r.multireddit.create(name, new_combo_multireddits[i])
    print("Done.")

def login_to_praw():
    import creds
    praw_r = praw.Reddit(client_id=creds.client_id,
                    client_secret=creds.client_secret,
                    user_agent=creds.user_agent,
                    password=creds.password,
                    username=creds.username)
    print("Logged in....")
    return praw_r


r = login_to_praw()
reset_combo_multireddits()