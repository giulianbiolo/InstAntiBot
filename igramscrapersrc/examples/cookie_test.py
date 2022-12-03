from context import Instagram # pylint: disable=no-name-in-module
from time import sleep

instagram = Instagram()
cookie="/home/fanibi/Downloads/cookies.txt"
instagram.set_cookies(cookie)


#Search for account
accounts = instagram.search_accounts_by_username('3.1415926535897932384626433832')
print(accounts[0])

#get media
account=accounts[0]
account=account.username
medias=instagram.get_medias(account,5)
media1=medias[0]

#like a picture:Does not work not logged in

# instagram.like(media1.identifier)
#unlike picture:Does not work not logged in
# instagram.unlike(media1.identifier)


#Try to get stories
stories = instagram.get_stories()
user_stories = stories[0]
print(user_stories.owner)
for story in user_stories.stories:
    print(story)

#Get media by tags
medias = instagram.get_medias_by_tag('instagood', count=20)

for media in medias:
    print(media)
    print('Account info:')
    account = media.owner
    print('Id', account.identifier)
    # print('Username', account.username)
    # print('Full Name', account.full_name)
    # print('Profile Pic Url', account.get_profile_picture_url_hd())
    print('--------------------------------------------------')

#get media from location

medias = instagram.get_medias_by_location_id('788945024', 10)
media = medias[0]
#same issues with grabbing data from search as feed example
#fix do a direct search with id from specific picture in feed
media= instagram.get_media_by_id(media.identifier)
account=media.owner
print('Id', account.identifier)
print('Username', account.username)
print('Full Name', account.full_name)


#get media from feed
feed = instagram.get_medias_from_feed('anwar')

picture = feed[7]
print(picture)
print('Account info:')
#account object from media doesn't not have desired info
# account = media.owner
# print('Id', account.identifier)
# print('Username', account.username)
# print('Full Name', account.full_name)
# # print('Profile Pic Url', account.get_profile_picture_url_hd())

#fix do a direct search with id from specific picture in feed
media= instagram.get_media_by_id(picture.identifier)
account=media.owner
print('Id', account.identifier)
print('Username', account.username)
print('Full Name', account.full_name)








#get tagged
print("tagged")
tagged_users = instagram.get_media_tagged_users_by_code('CFK2BdsDRPu')
print(tagged_users)



#get media code
media = instagram.get_media_by_id(picture.identifier)
code=media.short_code

#get Media likes
print("likes")
#not optimal to many calls
likes= instagram.get_media_likes_by_code(code,5)
# likes=likes['accounts']
for account in likes['accounts']:
    print(account.username)


#get comments
print("comments")
comments = instagram.get_media_comments_by_code(code, 10)
for comment in comments['comments']:
    print(comment.text)
    print(comment.owner)


#get media from link
print("get from link")
media = instagram.get_media_by_url('https://www.instagram.com/p/BHaRdodBouH')
print(media)
print(media.owner)


#get media via code
print("media from code")
media = instagram.get_medias_by_code('BHaRdodBouH')

print(media)
print(media.owner)



#get media via ID
media = instagram.get_media_by_id('1270593720437182847')
print("media from id")
print(media)
print('Account info:')
account = media.owner
print('Id', account.identifier)


#get location by id
print("get location by id")
location = instagram.get_location_by_id(788945024)
print(location)




#top media for tag
print("top for tag")
medias = instagram.get_current_top_medias_by_tag_name('youneverknow')
media = medias[0]

print(media)
print(media.owner)

#top for location
print("top for location")

medias = instagram.get_current_top_medias_by_location_id('788945024')

media = medias[0]
print(media)
print(media.owner)


#get media from account name
print("media from account name")
medias = instagram.get_medias("balleralert", 25)
media = medias[6]

print(media)
account = media.owner
print(account)
account2=instagram.get_account_by_id(account.identifier)
print(account2)

#get following
print("following")
sleep(2) # Delay to mimic user

username = 'balleralert'
following = []
account = instagram.get_account(username)
sleep(1)
following = instagram.get_following(account.identifier, 10, 10, delayed=True)
for following_user in following['accounts']:
    print(following_user)

#get folleers
print("followers")

sleep(2) # Delay to mimic user

username = 'balleralert'
followers = []
account = instagram.get_account(username)
sleep(1)
followers = instagram.get_followers(account.identifier, 10, 10, delayed=True)

for follower in followers['accounts']:
    print(follower)


#get account by username
print("account from username")
account = instagram.get_account('kevin')

# Available fields
print('Account info:')
print('Id', account.identifier)
print('Username', account.username)
print('Full name', account.full_name)
print('Biography', account.biography)
print('Profile pic url', account.get_profile_picture_url())
print('External Url', account.external_url)
print('Number of published posts', account.media_count)
print('Number of followers', account.followed_by_count)
print('Number of follows', account.follows_count)
print('Is private', account.is_private)
print('Is verified', account.is_verified)



#get account from id
print("account from id")
account = Instagram().get_account_by_id('3')

# Available fields
print(account)
print('Account info:')
print('Id', account.identifier)
print('Username', account.username)
print('Full name', account.full_name)
print('Biography', account.biography)
print('External Url', account.external_url)
print('Number of published posts', account.media_count)
print('Number of followers', account.followed_by_count)
print('Number of follows', account.follows_count)
print('Is private', account.is_private)
print('Is verified', account.is_verified)


#block unblock
print("block account and unblock")
instagram.block('adamw')
instagram.unblock('adamw')

#follow unfollow
print("follow and unfollow")
instagram.follow('adamw')
sleep(10)
instagram.unfollow('adamw')


#try add comment
#Does not work
# print("add comment")
# mediaId = '1874597980243548658'
# comment = instagram.add_comment(mediaId, 'nice!!')
# # replied to comment
# comment_b = instagram.add_comment(mediaId, 'cool man', comment)
#
# instagram.delete_comment(mediaId, comment)

