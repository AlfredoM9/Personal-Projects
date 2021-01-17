import re

def main():
    followers_file = open('Followers.txt', 'r', encoding='utf-8')
    following_file = open('Following.txt', 'r', encoding='utf-8')

    followers = followers_file.readlines()
    following = following_file.readlines()

    followers_file.close()
    following_file.close()

    filter_followers = []
    filter_following = []
    for i in followers:
        if re.match("^[A-Za-z0-9_.]*$", i):
            filter_followers.append(i.strip())

    for i in following:
        if re.match("^[A-Za-z0-9_.]*$", i):
            filter_following.append(i.strip())

    person_not_following_me = []
    im_not_following_person = []

    for i in filter_following:
        if i not in filter_followers:
            person_not_following_me.append(i)

    for i in filter_followers:
        if i not in filter_following:
            im_not_following_person.append(i)

    with open('not_following_me.txt', 'w') as f:
        for i in person_not_following_me:
            f.write("%s\n" % i)

    with open('im_not_following.txt', 'w') as f:
        for i in im_not_following_person:
            f.write("%s\n" % i)

if __name__ == '__main__':
    main()